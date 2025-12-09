"""
Document Loader for Insurance Claim Documents
Parses claim documents and extracts structured sections with metadata
"""

from llama_index.core import Document
from pathlib import Path
import re
from typing import List, Dict, Any
from datetime import datetime
import logging
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsuranceClaimLoader:
    """
    Loads and parses insurance claim documents into structured LlamaIndex Documents
    with rich metadata for hierarchical indexing and retrieval
    """

    def __init__(self, data_dir: str = "./data"):
        """
        Initialize document loader

        Args:
            data_dir: Directory containing claim documents
        """
        self.data_dir = Path(data_dir)
        self.documents: List[Document] = []

    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document and parse into sections
        Supports both PDF and text files

        Args:
            file_path: Path to document file (.pdf or .txt)

        Returns:
            List of LlamaIndex Document objects with metadata
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        logger.info(f"Loading document: {file_path.name}")

        # Load content based on file type
        page_boundaries = []
        if file_path.suffix.lower() == '.pdf':
            content, page_boundaries = self._load_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # For text files, treat as single page
            page_boundaries = [{'page_num': 1, 'start_char': 0, 'end_char': len(content)}]

        # Extract claim ID from filename or content
        claim_id = self._extract_claim_id(content, file_path.name)

        # Parse document into sections
        sections = self._parse_sections(content)

        logger.info(f"Parsed {len(sections)} sections from {file_path.name}")

        # Create Document objects with metadata
        documents = []
        for section in sections:
            doc = Document(
                text=section['content'],
                metadata={
                    'claim_id': claim_id,
                    'file_name': file_path.name,
                    'section_number': section['section_number'],
                    'section_title': section['section_title'],
                    'doc_type': section['doc_type'],
                    'timestamp': section.get('timestamp', ''),
                    'word_count': len(section['content'].split()),
                    'char_count': len(section['content']),
                    'page_boundaries': page_boundaries,  # Store for chunk page mapping
                    'total_pages': len(page_boundaries)
                },
                id_=f"{claim_id}_{section['section_number']}"
            )
            documents.append(doc)

        self.documents.extend(documents)
        return documents

    def _load_pdf(self, file_path: Path) -> tuple:
        """
        Load and extract text from PDF file with page boundary tracking

        Args:
            file_path: Path to PDF file

        Returns:
            Tuple of (extracted text content, page_boundaries list)
            page_boundaries is a list of (start_char_idx, end_char_idx, page_num)
        """
        logger.info(f"Extracting text from PDF: {file_path.name}")

        try:
            reader = PdfReader(str(file_path))
            content = []
            page_boundaries = []
            current_pos = 0

            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    # Add a page separator (newlines only, no markers that pollute the text)
                    if current_pos > 0:
                        separator = "\n\n"
                        content.append(separator)
                        current_pos += len(separator)

                    start_pos = current_pos
                    content.append(page_text)
                    current_pos += len(page_text)
                    end_pos = current_pos

                    # Track page boundary
                    page_boundaries.append({
                        'page_num': page_num,
                        'start_char': start_pos,
                        'end_char': end_pos
                    })

            full_text = "".join(content)
            logger.info(f"Extracted {len(reader.pages)} pages from PDF")
            logger.info(f"Tracked {len(page_boundaries)} page boundaries")
            return full_text, page_boundaries

        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            raise

    def _extract_claim_id(self, content: str, filename: str) -> str:
        """Extract claim ID from content or filename"""
        # Try to find claim ID in content
        match = re.search(r'Claim ID:\s*(CLM-\d{4}-\d{3})', content)
        if match:
            return match.group(1)

        # Fall back to filename
        match = re.search(r'(CLM\d{7})', filename)
        if match:
            return match.group(1)

        return "CLM-UNKNOWN"

    def _parse_sections(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse document into sections based on headers

        Args:
            content: Full document text

        Returns:
            List of section dictionaries with metadata
        """
        sections = []

        # Split by section headers (=== SECTION N: TITLE ===)
        section_pattern = r'={70,}\s*SECTION\s+(\d+):\s+([A-Z\s]+)\s*={70,}'
        matches = list(re.finditer(section_pattern, content))

        if not matches:
            # If no formal sections, treat entire document as one section
            logger.warning("No section headers found, treating as single document")
            sections.append({
                'section_number': 1,
                'section_title': 'Complete Document',
                'doc_type': 'insurance_claim',
                'content': content.strip(),
                'timestamp': self._extract_dates(content)[0] if self._extract_dates(content) else ''
            })
            return sections

        for i, match in enumerate(matches):
            section_num = int(match.group(1))
            section_title = match.group(2).strip()

            # Extract content between this section and the next
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            section_content = content[start_pos:end_pos].strip()

            # Determine document type from section title
            doc_type = self._classify_section(section_title)

            # Extract dates from section
            dates = self._extract_dates(section_content)
            timestamp = dates[0] if dates else ''

            sections.append({
                'section_number': section_num,
                'section_title': section_title,
                'doc_type': doc_type,
                'content': section_content,
                'timestamp': timestamp
            })

        return sections

    def _classify_section(self, section_title: str) -> str:
        """Classify section type based on title"""
        title_lower = section_title.lower()

        if 'policy' in title_lower:
            return 'policy_information'
        elif 'timeline' in title_lower or 'incident' in title_lower:
            return 'timeline'
        elif 'witness' in title_lower:
            return 'witness_statements'
        elif 'police' in title_lower:
            return 'police_report'
        elif 'medical' in title_lower:
            return 'medical_documentation'
        elif 'damage' in title_lower or 'vehicle' in title_lower:
            return 'damage_assessment'
        elif 'rental' in title_lower:
            return 'rental_documentation'
        elif 'financial' in title_lower:
            return 'financial_summary'
        elif 'closure' in title_lower:
            return 'closure_documentation'
        else:
            return 'general'

    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text for timestamp metadata"""
        # Match various date formats
        date_patterns = [
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b',
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]

        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)

        return dates[:1]  # Return first date found

    def load_all_documents(self) -> List[Document]:
        """
        Load all document files from data directory
        Supports both .txt and .pdf files

        Returns:
            List of all documents
        """
        all_documents = []

        # Load both .txt and .pdf files
        for pattern in ["*.txt", "*.pdf"]:
            for file_path in self.data_dir.glob(pattern):
                try:
                    docs = self.load_document(str(file_path))
                    all_documents.extend(docs)
                    logger.info(f"Loaded {len(docs)} sections from {file_path.name}")
                except Exception as e:
                    logger.error(f"Error loading {file_path.name}: {e}")

        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents

    def get_document_summary(self) -> Dict[str, Any]:
        """Get summary statistics of loaded documents"""
        if not self.documents:
            return {"message": "No documents loaded"}

        sections_by_type = {}
        total_words = 0

        for doc in self.documents:
            doc_type = doc.metadata.get('doc_type', 'unknown')
            sections_by_type[doc_type] = sections_by_type.get(doc_type, 0) + 1
            total_words += doc.metadata.get('word_count', 0)

        return {
            'total_sections': len(self.documents),
            'sections_by_type': sections_by_type,
            'total_words': total_words,
            'avg_words_per_section': total_words / len(self.documents) if self.documents else 0
        }


if __name__ == "__main__":
    # Test the document loader
    loader = InsuranceClaimLoader(data_dir="./data")

    print("\n=== Insurance Claim Document Loader Test ===\n")

    # Load all documents
    documents = loader.load_all_documents()

    print(f"Loaded {len(documents)} document sections\n")

    # Print summary
    summary = loader.get_document_summary()
    print("=== Document Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Show first document
    if documents:
        print("\n=== First Document Sample ===")
        first_doc = documents[0]
        print(f"Section: {first_doc.metadata['section_title']}")
        print(f"Type: {first_doc.metadata['doc_type']}")
        print(f"Word Count: {first_doc.metadata['word_count']}")
        print(f"Content Preview: {first_doc.text[:200]}...")
