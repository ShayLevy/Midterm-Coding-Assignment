# System Architecture Diagram

## Overview

This document describes the system architecture for the Insurance Claim Timeline Retrieval System. Since this is a text-based submission, the architecture is described in detail below. You can use this description to create a visual diagram using tools like draw.io, Figma, or similar.

## Architecture Diagram Components

### Layer 1: User Interface
```
┌─────────────────────────────────────────────────────────────┐
│                        USER QUERY                            │
│  "What was the exact deductible amount?"                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
```

### Layer 2: Manager Agent (Router)
```
┌─────────────────────────────────────────────────────────────┐
│            LANGCHAIN: Manager (Router) Agent                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │  Query Classification Engine                            │ │
│ │  • Analyze query type                                   │ │
│ │  • Determine: SUMMARY | NEEDLE | HYBRID | MCP          │ │
│ │  • Select appropriate tools                             │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  Tools Available:                                             │
│  [SummaryRetriever] [NeedleRetriever] [SectionRetriever]     │
│  [GetMetadata] [CalculateDays] [EstimatePayout]...           │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
```

### Layer 3: Specialist Agents
```
┌────────────────────────────┐      ┌────────────────────────────┐
│  LANGCHAIN:                 │      │  LANGCHAIN:                 │
│  Summarization Agent        │      │  Needle Agent               │
│                             │      │                             │
│  Handles:                   │      │  Handles:                   │
│  • Timeline queries         │      │  • Exact dates/amounts      │
│  • "What happened"          │      │  • Names of people          │
│  • Overviews               │      │  • Specific facts           │
│  • High-level summaries     │      │  • Precise details          │
│                             │      │                             │
│  Strategy:                  │      │  Strategy:                  │
│  • Query summary index      │      │  • Start with small chunks  │
│  • Use pre-computed data    │      │  • Auto-merge if needed     │
│  • Fast O(1) access         │      │  • High precision           │
└────────────────────────────┘      └────────────────────────────┘
              ↓                                    ↓
```

### Layer 4: Index Layer
```
┌────────────────────────────┐      ┌────────────────────────────┐
│  LLAMAINDEX:                │      │  LLAMAINDEX:                │
│  Summary Index              │      │  Hierarchical Index         │
│                             │      │                             │
│  Strategy: MapReduce        │      │  Strategy: Auto-Merging     │
│                             │      │                             │
│  Content:                   │      │  Content:                   │
│  • Document summaries       │      │  • Large chunks (2048 tok)  │
│  • Section summaries        │      │  • Medium chunks (512 tok)  │
│  • Timeline data            │      │  • Small chunks (128 tok)   │
│  • Key entity lists         │      │  • Parent-child links       │
│                             │      │                             │
│  Metadata:                  │      │  Metadata:                  │
│  • doc_type                 │      │  • chunk_level              │
│  • timestamp                │      │  • parent_id                │
│  • section_title            │      │  • section_title            │
│  • entities                 │      │  • doc_type                 │
└────────────────────────────┘      └────────────────────────────┘
              ↓                                    ↓
```

### Layer 5: Vector Store (ChromaDB)
```
┌──────────────────────────────────────────────────────────────┐
│                  CHROMADB VECTOR STORE                        │
│                     (Persistent Storage)                      │
│                                                               │
│  ┌────────────────────────┐      ┌────────────────────────┐  │
│  │ Collection:             │      │ Collection:            │  │
│  │ insurance_summaries     │      │ insurance_hierarchical │  │
│  │                         │      │                        │  │
│  │ Vector Dimension: 1536  │      │ Vector Dimension: 1536 │  │
│  │ (OpenAI embeddings)     │      │ (OpenAI embeddings)    │  │
│  │                         │      │                        │  │
│  │ Distance: Cosine        │      │ Distance: Cosine       │  │
│  │                         │      │                        │  │
│  │ Documents: ~10          │      │ Chunks: ~500           │  │
│  └────────────────────────┘      └────────────────────────┘  │
│                                                               │
│  Features:                                                     │
│  ✓ Metadata filtering      ✓ Persistence to disk             │
│  ✓ Semantic search         ✓ Fast retrieval (<100ms)          │
└──────────────────────────────────────────────────────────────┘
                              ↓
```

### Layer 6: MCP Tools Layer
```
┌──────────────────────────────────────────────────────────────┐
│        LANGCHAIN: MCP TOOLS (Tool-Augmented LLM)              │
│                                                               │
│  ┌──────────────────┐  ┌───────────────────┐                 │
│  │ GetDocumentMetadata│  │ CalculateDaysBetween │             │
│  │ Input: claim_id    │  │ Input: date1,date2  │             │
│  │ Output: metadata   │  │ Output: days, weeks │             │
│  └──────────────────┘  └───────────────────┘                 │
│                                                               │
│  ┌──────────────────┐  ┌───────────────────┐                 │
│  │EstimateCoveragePayout││ValidateClaimStatus│               │
│  │ Input: damage,deduct││ Input: filed_date  │               │
│  │ Output: payout amt  ││ Output: status_ok   │              │
│  └──────────────────┘  └───────────────────┘                 │
│                                                               │
│  ┌──────────────────┐                                         │
│  │ GetTimelineSummary│                                        │
│  │ Input: claim_id    │                                        │
│  │ Output: timeline   │                                        │
│  └──────────────────┘                                         │
│                                                               │
│  Purpose: Extend LLM capabilities beyond retrieval            │
│  • Computations (dates, costs)                                │
│  • Metadata access (database lookups)                         │
│  • Validations (rule-based checks)                            │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Example 1: Summary Query

```
User: "What is this insurance claim about?"
  ↓
Manager Agent analyzes: Keywords ["what", "about"] → SUMMARY type
  ↓
Routes to: SummaryRetriever tool
  ↓
Summarization Agent queries Summary Index
  ↓
Summary Index returns pre-computed summary from ChromaDB
  ↓
Response: "This claim involves a multi-vehicle collision..."
```

### Example 2: Needle Query

```
User: "What was the exact collision deductible?"
  ↓
Manager Agent analyzes: Keywords ["exact", "deductible"] → NEEDLE type
  ↓
Routes to: NeedleRetriever tool
  ↓
Needle Agent queries Hierarchical Index (small chunks)
  ↓
ChromaDB filters: chunk_level="small", section="POLICY INFORMATION"
  ↓
Returns 3 most relevant small chunks
  ↓
LLM extracts: "$750"
  ↓
Response: "The collision deductible was exactly $750."
```

### Example 3: MCP Tool Query

```
User: "How many days between incident and filing?"
  ↓
Manager Agent analyzes: Keywords ["how many days"] → MCP type
  ↓
Routes to: CalculateDaysBetween tool
  ↓
Manager extracts dates from context:
  - Incident: January 12, 2024
  - Filed: January 15, 2024
  ↓
MCP Tool calculates: 3 days, 3 business days
  ↓
Response: "3 days passed between the incident and filing."
```

## Color Coding (for visual diagram)

If creating a visual diagram, use these colors:

- **User Layer**: Light blue (#E3F2FD)
- **Manager Agent**: Orange (#FFE0B2)
- **Specialist Agents**: Green (#C8E6C9)
- **Indexes**: Purple (#E1BEE7)
- **ChromaDB**: Dark blue (#BBDEFB)
- **MCP Tools**: Yellow (#FFF9C4)

## Arrows and Connections

- Solid arrows (→): Main data flow
- Dashed arrows (⇢): Optional/fallback paths
- Bidirectional arrows (↔): Two-way communication

## Key Design Principles Illustrated

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Dual Index Strategy**: Different indexes for different query types
3. **Hierarchical Retrieval**: Multi-granularity chunks with auto-merging
4. **Tool Augmentation**: MCP extends capabilities beyond retrieval
5. **Intelligent Routing**: Manager decides optimal path
6. **Graceful Fallback**: Section retrieval uses 3-tier fallback (exact match → partial match → regular search) to handle ChromaDB filter limitations

## Technical Stack Layers

```
┌─────────────────────────────────────────┐
│  Application: main.py                   │
├─────────────────────────────────────────┤
│  Orchestration: LangChain Agents        │
├─────────────────────────────────────────┤
│  Indexing/Retrieval: LlamaIndex         │
├─────────────────────────────────────────┤
│  Vector Store: ChromaDB                 │
├─────────────────────────────────────────┤
│  Embeddings: OpenAI API                 │
├─────────────────────────────────────────┤
│  LLM: GPT-4                             │
└─────────────────────────────────────────┘
```

## Directory Mapping to Architecture

```
Project Directory                  Architecture Component
─────────────────────────────────────────────────────────
src/agents/manager_agent.py        → Manager Agent Layer
src/agents/summarization_agent.py  → Summarization Agent
src/agents/needle_agent.py         → Needle Agent
src/indexing/build_indexes.py      → Index Layer
src/vector_store/setup.py          → ChromaDB Layer
src/mcp/tools.py                   → MCP Tools Layer
src/retrieval/                     → Retrieval Logic
```

---

**Note**: Use this description to create a professional diagram using your preferred diagramming tool. Export as PNG/JPEG and place in this diagrams/ folder.

Recommended tools:
- draw.io (free, web-based)
- Figma (free for basic use)
- Lucidchart (free tier available)
- Microsoft PowerPoint/Visio
