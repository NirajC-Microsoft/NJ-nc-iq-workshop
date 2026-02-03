# Foundry IQ: Document Intelligence

## What is Foundry IQ?

Foundry IQ is Azure AI Foundry's unified knowledge layer that enables agents to access enterprise documents through intelligent retrieval.

## Key Capabilities

| Capability | Description |
|------------|-------------|
| **Knowledge Bases** | Automatic indexing and vectorization of documents |
| **Agentic Retrieval** | AI-driven search with planning, iteration, and reflection |
| **Enterprise Security** | Built-in Entra ID authentication and Purview integration |
| **Multi-format Support** | PDFs, Word, PowerPoint, and unstructured text |

## How Agentic Retrieval Works

Unlike simple vector search (find similar text), agentic retrieval uses AI to:

```
User: "What's our policy on returning electronics purchased on sale?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: PLAN                                               │
│  Agent decomposes into sub-queries:                         │
│  • "electronics return policy"                              │
│  • "sale items return conditions"                           │
│  • "exceptions for discounted products"                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: ITERATE                                            │
│  For each sub-query:                                        │
│  • Search knowledge base                                    │
│  • Evaluate relevance of results                            │
│  • Refine search if needed                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: REFLECT                                            │
│  Before responding:                                         │
│  • Do I have enough information?                            │
│  • Are sources consistent?                                  │
│  • Can I cite specific documents?                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Response with Citations                                    │
│  "According to our Return Policy (page 3), electronics can  │
│  be returned within 15 days. However, the Sale Items        │
│  Addendum (page 1) notes that clearance items are final     │
│  sale and cannot be returned..."                            │
└─────────────────────────────────────────────────────────────┘
```

## Why This Matters for Customers

### Problem: Simple RAG Fails on Complex Questions

Basic retrieval-augmented generation (RAG) does one search and uses whatever comes back. This fails when:

- Questions have multiple parts
- Information spans multiple documents
- The obvious search terms don't match the document language

### Solution: Agentic Retrieval Reasons About the Search

The agent acts like a knowledgeable employee who:

1. Understands what's really being asked
2. Knows to check multiple sources
3. Reconciles conflicting information
4. Admits when it can't find an answer

## Customer Talking Points

| Question | Response |
|----------|----------|
| "Why not just use search?" | "Search finds documents. Agentic retrieval finds answers — and knows when to look in multiple places." |
| "What about hallucination?" | "Every response cites specific documents. Users can click through to verify. The agent says 'I don't know' rather than guess." |
| "Can it handle our complex policies?" | "The Plan-Iterate-Reflect approach handles multi-part policies. Let me show you with this example..." |

## Technical Details

### Document Processing Pipeline

```
PDFs/Word/PPT → Text Extraction → Chunking → Embedding → Vector Index
```

- **Chunking**: Preserves sentence boundaries, typically 500-1000 tokens
- **Embedding**: Azure OpenAI text-embedding-3-large (3072 dimensions)
- **Index**: Azure AI Search with hybrid (keyword + vector) retrieval

### Search Configuration

```python
# Hybrid search combines:
# 1. Vector similarity (semantic meaning)
# 2. Keyword matching (exact terms)
# 3. Semantic ranking (re-ranking for relevance)

query_type = "vectorSemanticHybrid"
```

---

[← Step 3 Overview](index.md) | [Fabric IQ: Data →](02-fabric-iq.md)
