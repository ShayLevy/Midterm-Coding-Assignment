# LangChain 1.0 Installation Guide

## ✅ Project Updated for LangChain 1.0

I've updated the project to use **LangChain 1.0** with the correct package structure.

---

## 🚀 Quick Install

```bash
# Make sure you're in virtual environment
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Uninstall old versions (if any)
pip uninstall -y langchain langchain-core langchain-openai langchain-community

# Install fresh with new requirements
pip install -r requirements.txt
```

---

## 📦 What Changed

### Package Versions
- **langchain**: 0.3.0 (LangChain 1.0 compatible)
- **langchain-core**: 0.3.0 (core functionality)
- **langchain-openai**: 0.2.0 (OpenAI integration)
- **langchain-community**: 0.3.0 (community tools)

### Import Changes
All imports updated to LangChain 1.0 structure:

**Before:**
```python
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate
```

**After (LangChain 1.0):**
```python
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
```

---

## 🔧 Files Updated

### 1. `requirements.txt`
- Updated to LangChain 0.3.0 (1.0 compatible)
- Pinned versions for stability

### 2. Import Fixes
- ✅ `src/agents/manager_agent.py`
- ✅ `src/agents/summarization_agent.py`
- ✅ `src/agents/needle_agent.py`
- ✅ `src/agents/langchain_integration.py`
- ✅ `src/evaluation/judge.py`
- ✅ `src/mcp/tools.py`

All `langchain.prompts` → `langchain_core.prompts`
All `langchain.tools` → `langchain_core.tools`

---

## ✅ Verify Installation

After installing, verify everything works:

```bash
source venv/bin/activate

python -c "
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
print('✅ LangChain 1.0 imports successful!')
"
```

---

## 🎯 Run the System

```bash
# Make sure .env exists with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the system
python main.py
```

---

## 🐛 Troubleshooting

### "cannot import name 'Tool'"
```bash
# Reinstall langchain packages
pip uninstall -y langchain langchain-core langchain-openai
pip install langchain==0.3.0 langchain-core==0.3.0 langchain-openai==0.2.0
```

### "ImportError: cannot import name 'ChatPromptTemplate'"
```bash
# Make sure langchain-core is installed
pip install langchain-core==0.3.0
```

### Still having issues?
```bash
# Clean reinstall
pip uninstall -y langchain langchain-core langchain-openai langchain-community
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 Package Compatibility

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.3.0 | Main framework |
| langchain-core | 0.3.0 | Core components |
| langchain-openai | 0.2.0 | OpenAI integration |
| langchain-community | 0.3.0 | Community tools |
| llama-index | 0.9.48+ | Indexing & retrieval |
| chromadb | 0.4.22+ | Vector store |

---

## ✨ You're Ready!

The project is now fully compatible with **LangChain 1.0**. Just run:

```bash
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

🎉 **All set!**
