# Build & Test (Customer PoC)

## Test Your Custom Agent

After generation completes, test the agent:

```bash
python scripts/08_test_foundry_agent.py
```

## Use the Generated Sample Questions

Each scenario generates ready-to-use sample questions in the data folder:

```bash
# View sample questions for your scenario
cat data/default/config/sample_questions.txt
```

The file contains three categories of questions:

| Category | Source | Example |
|----------|--------|---------|
| **Structured data questions** | Fabric IQ (data) | "How many outages occurred last month?" |
| **Unstructured data questions** | Foundry IQ (docs) | "What are the policies for notifying customers?" |
| **Combined questions** | Both sources | "Which outages exceeded our policy thresholds?" |

!!! tip "Use these questions first"
    The generated questions are tailored to your scenario's data and documents. Start with these before improvising.

## Testing Tips

### Start with structured data questions

Show the power of natural language over structured data:

```
"How many [entities] do we have?"
"What's the total [metric] for [time period]?"
"Show me the top 5 [entities] by [metric]"
```

### Then unstructured data questions

Demonstrate intelligent document retrieval:

```
"What's our policy on [topic]?"
"How do we handle [process]?"
"What are the requirements for [action]?"
```

### Finish with combined questions

This is the "wow" moment: questions that need both sources:

```
"Based on our [policy], which [entities] need attention?"
"Are we meeting our [documented SLA] according to the data?"
"Which [items] don't comply with our [policy/guidelines]?"
```

## Prepare your test script

Before customer meetings, prepare 5-7 questions:

| # | Question Type | Example |
|---|---------------|---------|
| 1 | Structured data | "How many outages occurred last month?" |
| 2 | Structured data | "What is the average resolution time for tickets?" |
| 3 | Structured data | "Which outage caused the most customer impact?" |
| 4 | Unstructured data | "What are the policies for notifying customers of outages?" |
| 5 | Unstructured data | "What steps must be taken to escalate an outage?" |
| 6 | **Combined** | "Which outages exceeded the maximum duration defined in our policy?" |
| 7 | **Combined** | "What percentage of tickets were resolved within our SLA?" |

!!! tip "Let customers ask questions"
    After your prepared questions, let customers ask their own questions. This shows the solution handles real scenarios, not just scripted ones.

## Checkpoint

!!! success "Ready for Customer PoC"
    Your custom PoC should:
    
    - [x] Answer structured data questions accurately
    - [x] Retrieve relevant unstructured document content
    - [x] Combine sources for complex questions
    - [x] Use industry-appropriate terminology
    
    **Next:** Review [Deep dive](../03-understand/index.md) to prepare for technical questions

## Quick Reference: Regenerate for Another Customer

```bash
# Edit .env with new customer's industry and use case, then:
python scripts/00_build_solution.py --ai --clean

# Or inline:
python scripts/00_build_solution.py --ai --clean \
  --industry "New Industry" \
  --usecase "New use case description"
```

---

[← Generate & Build](02-generate.md) | [Deep dive →](../03-understand/index.md)
