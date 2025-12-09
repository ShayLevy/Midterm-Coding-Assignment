# How to Process the Insurance Claim PDF

## 🎯 Quick Start (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 3. Run the system (PDF processes automatically!)
python main.py
```

**That's it!** The PDF is automatically detected, processed, and indexed.

---

## 📖 Detailed Processing Guide

### Step 1: Verify PDF Exists

```bash
# Check that the PDF is in the data folder
ls -lh data/insurance_claim_CLM2024001.pdf
```

**Expected output:**
```
-rw-r--r--  1 user  staff  29K Dec  8 18:13 insurance_claim_CLM2024001.pdf
```

---

### Step 2: Install Required Libraries

The system needs these libraries for PDF processing:

```bash
# Install from requirements.txt (recommended)
pip install -r requirements.txt

# Or install PDF libraries individually
pip install pypdf>=3.17.0      # For reading PDFs
pip install reportlab>=4.0.0   # For generating PDFs (optional)
pip install llama-index>=0.9.48  # For indexing
pip install langchain>=0.1.0     # For agents
pip install chromadb>=0.4.22     # For vector store
pip install openai>=1.0.0        # For LLM
```

---

### Step 3: Set Environment Variables

Create a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit and add your OpenAI API key
# .env should contain:
OPENAI_API_KEY=sk-your-actual-key-here
```

---

### Step 4: Run Main System

```bash
python main.py
```

### What Happens During First Run:

```
[1/8] Initializing Vector Store Manager...
      ✅ ChromaDB initialized at ./chroma_db

[2/8] Loading insurance claim documents...
      📄 Loading document: insurance_claim_CLM2024001.pdf
      📄 Extracting text from PDF: insurance_claim_CLM2024001.pdf
      ✅ Extracted 15 pages from PDF
      ✅ Parsed 7 sections from insurance_claim_CLM2024001.pdf
      ✅ Loaded 7 document sections

[3/8] Creating hierarchical chunks...
      🔨 Chunking 7 documents...
      === Chunk Distribution ===
        Large chunks: 15
        Medium chunks: 45
        Small chunks: 180
      ✅ Created 240 hierarchical chunks

[4/8] Building indexes...
      📊 Building Summary Index with MapReduce...
      ✅ Summary Index built with 7 documents

      📊 Building Hierarchical Index...
      ✅ Hierarchical Index built with 240 chunks

[5/8] Creating retrievers...
      ✅ HierarchicalRetriever initialized with 240 nodes

[6/8] Initializing MCP tools...
      ✅ Loaded 5 MCP tools

[7/8] Setting up LangChain integration...
      ✅ Created 8 tools for agents

[8/8] Initializing agents...
      ✅ ManagerAgent initialized
      ✅ SummarizationAgent initialized
      ✅ NeedleAgent initialized

System ready! 🚀
```

---

## 🔬 How PDF Processing Works

### Behind the Scenes Code Flow:

```python
# 1. Document Loader detects file type
file_path = Path("data/insurance_claim_CLM2024001.pdf")

if file_path.suffix.lower() == '.pdf':
    # 2. PDF text extraction
    content = _load_pdf(file_path)

    # _load_pdf() uses pypdf:
    from pypdf import PdfReader
    reader = PdfReader(str(file_path))

    # 3. Extract text from each page
    for page in reader.pages:
        page_text = page.extract_text()
        content.append(page_text)

    # 4. Parse sections from text
    sections = _parse_sections(content)

    # 5. Create Document objects
    for section in sections:
        doc = Document(
            text=section['content'],
            metadata={
                'section_title': section['title'],
                'doc_type': section['type'],
                ...
            }
        )
```

### Section Parsing:

The PDF text is parsed to identify sections:

```python
# Looks for section headers in the PDF text
SECTION 1: POLICY INFORMATION      → policy_information
SECTION 2: INCIDENT TIMELINE       → timeline
SECTION 3: WITNESS STATEMENTS      → witness_statements
SECTION 4: MEDICAL DOCUMENTATION   → medical_documentation
SECTION 5: VEHICLE DAMAGE          → damage_assessment
SECTION 6: FINANCIAL SUMMARY       → financial_summary
SECTION 7: CASE NOTES             → closure_documentation
```

---

## 🧪 Test PDF Processing Manually

If you want to test just the PDF loading (without running full system):

```python
# test_pdf_loading.py
from src.indexing.document_loader import InsuranceClaimLoader

# Initialize loader
loader = InsuranceClaimLoader(data_dir="./data")

# Load the PDF
documents = loader.load_document("./data/insurance_claim_CLM2024001.pdf")

# Print results
print(f"✅ Loaded {len(documents)} sections from PDF")
print(f"📊 Total words: {sum(d.metadata['word_count'] for d in documents):,}")

# Show first section
first_doc = documents[0]
print(f"\n📄 First Section:")
print(f"   Title: {first_doc.metadata['section_title']}")
print(f"   Type: {first_doc.metadata['doc_type']}")
print(f"   Words: {first_doc.metadata['word_count']}")
print(f"   Preview: {first_doc.text[:200]}...")
```

Run it:
```bash
python test_pdf_loading.py
```

**Expected output:**
```
✅ Loaded 7 sections from PDF
📊 Total words: 8,500

📄 First Section:
   Title: POLICY INFORMATION
   Type: policy_information
   Words: 450
   Preview: The policyholder, Sarah Mitchell, maintains a comprehensive auto insurance policy...
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'pypdf'"

**Solution:**
```bash
pip install pypdf
# or
pip install -r requirements.txt
```

### Issue 2: "PDF not found"

**Solution:**
```bash
# Check the file exists
ls data/insurance_claim_CLM2024001.pdf

# If missing, regenerate it
python generate_pdf.py
```

### Issue 3: "PDF text extraction returns gibberish"

**Solution:**
The PDF was generated with reportlab and should extract cleanly. If you see issues:

```python
# Test extraction manually
from pypdf import PdfReader
reader = PdfReader("data/insurance_claim_CLM2024001.pdf")
print(reader.pages[0].extract_text()[:500])
```

Should show clean text starting with:
```
COMPREHENSIVE INSURANCE CLAIM REPORT
Claim ID: CLM-2024-001
Document Type: Multi-Vehicle Collision Claim...
```

### Issue 4: "System loads .txt instead of .pdf"

The system loads **both** .txt and .pdf files. To use only PDF:

```bash
# Remove or rename the .txt file
mv data/insurance_claim_CLM2024001.txt data/insurance_claim_CLM2024001.txt.backup
```

Or modify the loader:
```python
# In main.py, explicitly load only PDF
loader = InsuranceClaimLoader(data_dir="./data")
documents = loader.load_document("./data/insurance_claim_CLM2024001.pdf")
```

---

## 🎯 Verify Processing Worked

After running `python main.py`, you should see:

### 1. ChromaDB Directory Created
```bash
ls -la chroma_db/
# Should show:
# chroma.sqlite3
# (other ChromaDB files)
```

### 2. Collections Populated
```python
from src.vector_store.setup import VectorStoreManager

vsm = VectorStoreManager()
stats = vsm.get_collection_stats()
print(stats)

# Expected output:
# {
#   'summary': {'count': 7, 'name': 'insurance_summaries'},
#   'hierarchical': {'count': 240, 'name': 'insurance_hierarchical'}
# }
```

### 3. Query Works
```bash
# In the interactive prompt that appears after running main.py:
🔍 Your query: What was the exact collision deductible?

# Should return:
📊 RESPONSE:
The collision deductible was exactly $750.
```

---

## 📊 Processing Time

**First Run (builds indexes):**
- PDF text extraction: ~2 seconds
- Section parsing: ~1 second
- Hierarchical chunking: ~5 seconds
- Summary index build: ~30-60 seconds (depends on OpenAI API)
- Hierarchical index build: ~20-40 seconds
- **Total: 2-3 minutes**

**Subsequent Runs (loads from ChromaDB):**
- Loading indexes: ~2 seconds
- **Total: instant**

---

## 🔄 Rebuild Indexes

If you want to rebuild indexes from scratch:

### Method 1: Delete ChromaDB folder
```bash
rm -rf chroma_db/
python main.py  # Will rebuild
```

### Method 2: Use rebuild flag
```python
# In main.py
system = InsuranceClaimSystem(
    data_dir="./data",
    chroma_dir="./chroma_db",
    rebuild_indexes=True  # ← Set to True
)
```

---

## 📝 Processing Summary

| Step | What Happens | Time |
|------|--------------|------|
| 1. Load PDF | pypdf extracts text from 15 pages | 2s |
| 2. Parse sections | Regex identifies 7 sections | 1s |
| 3. Create chunks | 3 levels: 240 total chunks | 5s |
| 4. Build summary index | MapReduce summarization | 30-60s |
| 5. Build hierarchical index | Vector embeddings | 20-40s |
| 6. Store in ChromaDB | Persist to disk | 5s |
| **Total** | **First run** | **~2-3 min** |

---

## ✅ Success Checklist

After processing, verify:

- [ ] PDF file exists in `data/` folder
- [ ] `chroma_db/` directory created
- [ ] System shows "System ready!" message
- [ ] Interactive prompt appears
- [ ] Query "What is this claim about?" returns summary
- [ ] Query "What was the deductible?" returns $750
- [ ] No error messages in console

---

## 🎓 Advanced: Inspect PDF Processing

### View extracted text:
```python
from pypdf import PdfReader

reader = PdfReader("data/insurance_claim_CLM2024001.pdf")
print(f"Pages: {len(reader.pages)}")

# View page 1
print(reader.pages[0].extract_text())
```

### View parsed sections:
```python
from src.indexing.document_loader import InsuranceClaimLoader

loader = InsuranceClaimLoader(data_dir="./data")
docs = loader.load_all_documents()

for doc in docs:
    print(f"Section: {doc.metadata['section_title']}")
    print(f"Type: {doc.metadata['doc_type']}")
    print(f"Words: {doc.metadata['word_count']}")
    print("---")
```

### View chunks:
```python
from src.indexing.chunking import HierarchicalChunker

chunker = HierarchicalChunker()
nodes = chunker.chunk_documents(docs)

print(f"Total chunks: {len(nodes)}")

# View small chunks
small_chunks = [n for n in nodes if n.metadata['chunk_level'] == 'small']
print(f"Small chunks: {len(small_chunks)}")
```

---

## 🚀 You're Ready!

The PDF processing is **fully automatic**. Just run:

```bash
python main.py
```

And the system handles everything! 🎉
