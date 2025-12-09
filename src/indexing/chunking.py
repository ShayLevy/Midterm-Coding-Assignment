"""
Hierarchical Chunking Strategy
Creates multi-granularity chunks (small, medium, large) for Auto-Merging Retriever
"""

from llama_index.core.node_parser import HierarchicalNodeParser, SentenceSplitter
from llama_index.core import Document
from llama_index.core.schema import TextNode
from typing import List, Dict, Optional
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HierarchicalChunker:
    """
    Creates hierarchical chunks at multiple granularity levels:
    - Small chunks (128 tokens): High-precision factual retrieval
    - Medium chunks (512 tokens): Balanced context and precision
    - Large chunks (2048 tokens): Broader narrative context

    Chunk overlap strategy: 20-30% to prevent information loss at boundaries
    """

    def __init__(
        self,
        chunk_sizes: List[int] = None,
        chunk_overlap_ratio: float = 0.2
    ):
        """
        Initialize hierarchical chunker

        Args:
            chunk_sizes: List of chunk sizes [large, medium, small] in tokens
            chunk_overlap_ratio: Ratio of overlap between chunks (0.2 = 20%)
        """
        # Default chunk sizes: large, medium, small
        self.chunk_sizes = chunk_sizes or [2048, 512, 128]
        self.chunk_overlap_ratio = chunk_overlap_ratio

        logger.info(f"Initializing HierarchicalChunker with sizes: {self.chunk_sizes}")
        logger.info(f"Overlap ratio: {chunk_overlap_ratio * 100}%")

        # Calculate overlaps for each level
        self.chunk_overlaps = [
            int(size * chunk_overlap_ratio) for size in self.chunk_sizes
        ]

        # HierarchicalNodeParser uses a single overlap for all levels,
        # so we must use an overlap smaller than the smallest chunk size
        smallest_chunk = min(self.chunk_sizes)
        max_overlap = int(smallest_chunk * chunk_overlap_ratio)

        # Create the hierarchical node parser
        self.parser = HierarchicalNodeParser.from_defaults(
            chunk_sizes=self.chunk_sizes,
            chunk_overlap=max_overlap  # Use overlap based on smallest chunk
        )

    def chunk_documents(self, documents: List[Document]) -> List[TextNode]:
        """
        Chunk documents into hierarchical nodes

        Args:
            documents: List of LlamaIndex Document objects

        Returns:
            List of TextNode objects with parent-child relationships
        """
        logger.info(f"Chunking {len(documents)} documents...")

        # Extract and store page boundaries before chunking (they're too large for small chunks)
        # Map doc_id -> page_boundaries
        self._page_boundaries_map = {}
        for doc in documents:
            page_boundaries = doc.metadata.pop('page_boundaries', [])
            doc.metadata.pop('total_pages', None)  # Also remove this
            self._page_boundaries_map[doc.id_] = page_boundaries

        # Get nodes from documents using hierarchical parser
        nodes = self.parser.get_nodes_from_documents(documents, show_progress=True)

        # Enhance metadata for each node (including page numbers)
        nodes = self._enhance_node_metadata(nodes)

        logger.info(f"Created {len(nodes)} hierarchical chunks")

        # Log chunk distribution
        self._log_chunk_distribution(nodes)

        return nodes

    def _get_pages_for_range(
        self,
        start_char: int,
        end_char: int,
        page_boundaries: List[Dict]
    ) -> List[int]:
        """
        Determine which page(s) a character range spans

        Args:
            start_char: Start character index of the chunk
            end_char: End character index of the chunk
            page_boundaries: List of page boundary dicts with page_num, start_char, end_char

        Returns:
            List of page numbers that the range spans
        """
        pages = []
        for boundary in page_boundaries:
            page_start = boundary['start_char']
            page_end = boundary['end_char']
            page_num = boundary['page_num']

            # Check if chunk overlaps with this page
            # Overlap exists if chunk_start < page_end AND chunk_end > page_start
            if start_char < page_end and end_char > page_start:
                pages.append(page_num)

        return pages if pages else [1]  # Default to page 1 if no match

    def _enhance_node_metadata(self, nodes: List[TextNode]) -> List[TextNode]:
        """
        Enhance node metadata with chunk level, page numbers, and additional info

        Args:
            nodes: List of nodes to enhance

        Returns:
            Enhanced nodes with rich metadata
        """
        for node in nodes:
            # Determine chunk level based on text length
            text_length = len(node.text)
            token_estimate = text_length // 4  # Rough token estimate

            if token_estimate > 1500:
                level = "large"
                level_num = 0
            elif token_estimate > 400:
                level = "medium"
                level_num = 1
            else:
                level = "small"
                level_num = 2

            # Get page boundaries from stored map (keyed by source doc ref)
            # Try to find the source document ID from node relationships
            source_doc_id = None
            if hasattr(node, 'source_node') and node.source_node:
                source_doc_id = node.source_node.node_id
            elif node.metadata.get('claim_id'):
                # Construct doc ID from claim_id and section
                claim_id = node.metadata.get('claim_id', '')
                section = node.metadata.get('section_number', 1)
                source_doc_id = f"{claim_id}_{section}"

            page_boundaries = self._page_boundaries_map.get(source_doc_id, [])

            # Determine page numbers for this chunk using character positions
            start_char = getattr(node, 'start_char_idx', None)
            end_char = getattr(node, 'end_char_idx', None)

            if start_char is not None and end_char is not None and page_boundaries:
                page_numbers = self._get_pages_for_range(start_char, end_char, page_boundaries)
            else:
                # Fallback: try to estimate from text position in source
                page_numbers = [1]

            # Add hierarchical metadata
            # Note: ChromaDB only accepts str, int, float, None for metadata
            # So we convert lists to strings and bools to ints
            parent_node = getattr(node, 'parent_node', None)
            child_nodes = getattr(node, 'child_nodes', None)
            node.metadata.update({
                'chunk_level': level,
                'chunk_level_num': level_num,
                'chunk_size': token_estimate,
                'parent_id': parent_node.node_id if parent_node else '',
                'has_children': 1 if (child_nodes and len(child_nodes) > 0) else 0,
                'page_numbers': ','.join(map(str, page_numbers)),  # Convert list to string
                'start_page': min(page_numbers),
                'end_page': max(page_numbers)
            })

        return nodes

    def _log_chunk_distribution(self, nodes: List[TextNode]):
        """Log statistics about chunk distribution"""
        distribution = {'small': 0, 'medium': 0, 'large': 0}
        total_chars = 0
        pages_covered = set()

        for node in nodes:
            level = node.metadata.get('chunk_level', 'unknown')
            if level in distribution:
                distribution[level] += 1
            total_chars += len(node.text)

            # Track pages covered (page_numbers is now a comma-separated string)
            page_nums_str = node.metadata.get('page_numbers', '')
            if page_nums_str:
                pages_covered.update(int(p) for p in page_nums_str.split(',') if p)

        logger.info("=== Chunk Distribution ===")
        logger.info(f"  Large chunks: {distribution['large']}")
        logger.info(f"  Medium chunks: {distribution['medium']}")
        logger.info(f"  Small chunks: {distribution['small']}")
        logger.info(f"  Total characters: {total_chars:,}")
        logger.info(f"  Avg chars per chunk: {total_chars // len(nodes) if nodes else 0}")
        logger.info(f"  Pages covered: {sorted(pages_covered) if pages_covered else 'N/A'}")


class CustomChunker:
    """
    Alternative custom chunking implementation with fine-grained control
    Useful when you need specific chunking behavior beyond HierarchicalNodeParser
    """

    def __init__(self):
        """Initialize custom chunkers for each granularity level"""
        # Large chunks - for broad context
        self.large_splitter = SentenceSplitter(
            chunk_size=2048,
            chunk_overlap=410  # ~20% overlap
        )

        # Medium chunks - balanced
        self.medium_splitter = SentenceSplitter(
            chunk_size=512,
            chunk_overlap=102  # ~20% overlap
        )

        # Small chunks - precision
        self.small_splitter = SentenceSplitter(
            chunk_size=128,
            chunk_overlap=26  # ~20% overlap
        )

    def create_multi_granularity_chunks(
        self,
        documents: List[Document]
    ) -> Dict[str, List[TextNode]]:
        """
        Create chunks at all three granularity levels independently

        Args:
            documents: Source documents

        Returns:
            Dictionary with keys 'large', 'medium', 'small' containing respective chunks
        """
        logger.info("Creating multi-granularity chunks...")

        chunks = {
            'large': [],
            'medium': [],
            'small': []
        }

        # Create large chunks
        logger.info("Creating large chunks...")
        large_nodes = self.large_splitter.get_nodes_from_documents(documents)
        for node in large_nodes:
            node.metadata['chunk_level'] = 'large'
            node.metadata['chunk_level_num'] = 0
        chunks['large'] = large_nodes

        # Create medium chunks
        logger.info("Creating medium chunks...")
        medium_nodes = self.medium_splitter.get_nodes_from_documents(documents)
        for node in medium_nodes:
            node.metadata['chunk_level'] = 'medium'
            node.metadata['chunk_level_num'] = 1
        chunks['medium'] = medium_nodes

        # Create small chunks
        logger.info("Creating small chunks...")
        small_nodes = self.small_splitter.get_nodes_from_documents(documents)
        for node in small_nodes:
            node.metadata['chunk_level'] = 'small'
            node.metadata['chunk_level_num'] = 2
        chunks['small'] = small_nodes

        logger.info(f"Created {len(large_nodes)} large, {len(medium_nodes)} medium, {len(small_nodes)} small chunks")

        return chunks


if __name__ == "__main__":
    from document_loader import InsuranceClaimLoader

    print("\n=== Hierarchical Chunking Test ===\n")

    # Load documents
    loader = InsuranceClaimLoader(data_dir="../../data")
    documents = loader.load_all_documents()

    print(f"Loaded {len(documents)} document sections\n")

    # Test hierarchical chunker
    chunker = HierarchicalChunker()
    nodes = chunker.chunk_documents(documents[:2])  # Test with first 2 sections

    print(f"\nCreated {len(nodes)} hierarchical chunks")

    # Show sample chunks at each level
    print("\n=== Sample Chunks ===")
    for level in ['large', 'medium', 'small']:
        level_nodes = [n for n in nodes if n.metadata.get('chunk_level') == level]
        if level_nodes:
            sample = level_nodes[0]
            print(f"\n{level.upper()} Chunk:")
            print(f"  Length: {len(sample.text)} chars")
            print(f"  Metadata: {sample.metadata}")
            print(f"  Preview: {sample.text[:150]}...")
