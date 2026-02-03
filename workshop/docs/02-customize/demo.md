# Build & Test (Customer PoC)

## Test Your Custom Agent

After generation completes, test the agent:

```bash
python scripts/08a_test_multi_tool_agent.py
```

## Demo Tips

### Start with Data Questions

Show the power of natural language over structured data:

```
"How many [entities] do we have?"
"What's the total [metric] for [time period]?"
"Show me the top 5 [entities] by [metric]"
```

### Then Document Questions

Demonstrate intelligent document retrieval:

```
"What's our policy on [topic]?"
"How do we handle [process]?"
"What are the requirements for [action]?"
```

### Finish with Combined Questions

This is the "wow" moment — questions that need both sources:

```
"Based on our [policy], which [entities] need attention?"
"Are we meeting our [documented SLA] according to the data?"
"Which [items] don't comply with our [policy/guidelines]?"
```

## Prepare Your Demo Script

Before customer meetings, prepare 5-7 questions:

| # | Question Type | Example |
|---|---------------|---------|
| 1 | Simple data | "How many customers do we have?" |
| 2 | Aggregation | "What's our total revenue this quarter?" |
| 3 | Filtering | "Show me orders over $1000" |
| 4 | Policy lookup | "What's our return policy?" |
| 5 | Process guide | "How do we handle escalations?" |
| 6 | **Combined** | "Which high-value orders might need expedited shipping per our SLA?" |
| 7 | **Combined** | "Are there any exceptions to our policy in the current data?" |

!!! tip "Let Customers Ask Questions"
    After your prepared demo, let customers ask their own questions. This shows the solution handles real scenarios, not just scripted ones.

## Checkpoint

!!! success "Ready for Customer Demo"
    Your custom PoC should:
    
    - [x] Answer data questions accurately
    - [x] Retrieve relevant document content
    - [x] Combine sources for complex questions
    - [x] Use industry-appropriate terminology
    
    **Next:** Review [Step 3: How it works](../03-understand/index.md) to prepare for technical questions

## Quick Reference: Regenerate for Another Customer

```bash
# Edit .env with new customer's industry and use case, then:
python scripts/00_build_solution.py --ai --clean

# Or inline:
python scripts/00_build_solution.py --ai --clean \
  --industry "New Industry" \
  --usecase "New use case description"
```
