# What you'll build

In this workshop, we'll deploy an AI solution using Fabric IQ and Foundry IQ, then customize it for your use case.

## Solution components

Powered by **Microsoft Fabric** and **Microsoft Foundry**:

| Component | What it does |
|-----------|--------------|
| **Fabric IQ** | Translates natural language into SQL queries via ontology |
| **Foundry IQ** | Searches documents using agentic retrieval (plan, iterate, reflect) |
| **Multi-Tool Agent** | Routes questions to the right source automatically |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Multi-Tool Agent                         │
│                   (Azure AI Foundry)                         │
├─────────────────────────────────────────────────────────────┤
│                          ↓                                   │
│    ┌─────────────────┐       ┌─────────────────┐           │
│    │   Fabric IQ     │       │   Foundry IQ    │           │
│    │   (SQL Tool)    │       │  (Search Tool)  │           │
│    └────────┬────────┘       └────────┬────────┘           │
│             ↓                         ↓                     │
│    ┌─────────────────┐       ┌─────────────────┐           │
│    │ Microsoft Fabric│       │  Azure AI Search │           │
│    │   (Data)        │       │   (Documents)    │           │
│    └─────────────────┘       └─────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Sample question flow

**User asks**: "Which outages exceeded our SLA threshold?"

1. **Agent receives question** → Determines it needs both data and documents
2. **Fabric IQ** → Queries outage data from Fabric warehouse
3. **Foundry IQ** → Retrieves SLA thresholds from policy documents
4. **Agent combines** → Returns answer with citations from both sources

---

[← Overview](index.md) | [Get Started →](../00-get-started/index.md)
