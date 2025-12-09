# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
```

### Step 3: Run the System

```bash
# First run (builds indexes - takes 2-3 minutes)
python main.py
```

**What happens on first run:**
1. Loads insurance claim document from `data/` (15-page PDF)
2. Extracts text and parses into sections
3. Creates hierarchical chunks (small, medium, large)
4. Builds Summary Index using MapReduce
5. Builds Hierarchical Index for precise retrieval
6. Stores everything in ChromaDB (`chroma_db/` folder created automatically)
7. Launches interactive query interface

### Step 4: Try Example Queries

```
🔍 Your query: What is this insurance claim about?
🔍 Your query: What was the exact deductible amount?
🔍 Your query: Who was the claims adjuster?
🔍 Your query: How many days between incident and filing?
```

Type `quit` to exit.

### Step 5: Run Evaluation

```bash
python run_evaluation.py
```

This will:
- Run all 8 test queries
- Evaluate using LLM-as-a-judge
- Generate results in `evaluation_results/`
- Show aggregate scores

Expected output:
```
OVERALL AVERAGE: 4.25 / 5.00
Performance Grade: B (Very Good)
```

---

## 📁 What Gets Created

After running, you'll have:

```
Midterm-Coding-Assignment/
├── chroma_db/              # Vector store (auto-created)
│   ├── chroma.sqlite3
│   └── ...
├── evaluation_results/     # Eval outputs (auto-created)
│   └── evaluation_results_20241215_123456.json
└── .env                   # Your API key (you create this)
```

---

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"

**Solution**: Make sure you created `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### "ModuleNotFoundError: No module named 'llama_index'"

**Solution**: Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### ChromaDB Error

**Solution**: Delete `chroma_db/` folder and rebuild:
```bash
rm -rf chroma_db/
python main.py  # Will rebuild
```

### Out of Memory

**Solution**: Reduce chunk sizes in `src/indexing/chunking.py`:
```python
chunk_sizes=[1024, 256, 64]  # Smaller chunks
```

---

## 🎯 Next Steps

1. **Explore the code**: Start with `main.py` to understand the flow
2. **Read README.md**: Comprehensive documentation
3. **Check architecture**: See `diagrams/ARCHITECTURE.md`
4. **Modify test queries**: Edit `src/evaluation/test_queries.py`
5. **Add your own documents**: Place in `data/` folder

---

## 💡 Tips

- **First run is slow** (builds indexes). Subsequent runs are instant.
- **Use `rebuild_indexes=False`** in `main.py` after first run
- **Check `evaluation_results/`** for detailed eval JSON
- **Logs show routing decisions** - see which agents/tools were used

---

## 📞 Help

Check these resources:
- **README.md**: Full documentation
- **diagrams/ARCHITECTURE.md**: System design
- **Code comments**: Detailed inline explanations

---

**You're all set! 🎉**
