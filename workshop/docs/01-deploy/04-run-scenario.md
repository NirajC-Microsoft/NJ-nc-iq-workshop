# Build solution

## Run the Full Pipeline

One command builds everything using the pre-populated sample data:

```bash
python scripts/00_build_solution.py --from 02
```

This uses the `data/default` folder and runs all setup steps:

| Step | What Happens | Time |
|------|--------------|------|
| 02 | Setup Fabric workspace | ~30s |
| 03 | Load data into Fabric | ~1min |
| 04 | Generate NL2SQL prompt | ~5s |
| 05 | Create Fabric Data Agent | ~30s |
| 06 | Upload documents to AI Search | ~1min |
| 07a | Create Multi-Tool Agent | ~10s |

## Expected Output

```
============================================================
Building Solution
============================================================

[02/07] Setting up Fabric workspace...
  ✓ Lakehouse: iqworkshop_lakehouse
  ✓ Warehouse: iqworkshop_warehouse

[03/07] Loading data into Fabric...
  ✓ network_outages.csv → 25 rows
  ✓ trouble_tickets.csv → 50 rows

[04/07] Generating NL2SQL prompt...
  ✓ Schema prompt created

[05/07] Creating Fabric Data Agent...
  ✓ Agent: fabric-data-agent

[06/07] Uploading documents to AI Search...
  ✓ 3 documents → 24 chunks indexed

[07/07] Creating Multi-Tool Agent...
  ✓ Agent: multi-tool-agent

============================================================
Build complete! Run: python scripts/08a_test_multi_tool_agent.py
============================================================
```

## Test the Agent

```bash
python scripts/08a_test_multi_tool_agent.py
```

### Sample Conversation

```
============================================================
Multi-Tool Agent Testing
============================================================
Agent: multi-tool-agent
Tools: [ai_search, fabric_iq]

Type 'exit' to quit.
------------------------------------------------------------

You: How many outages occurred last month?

Agent: Based on the database, there were 12 network outages recorded 
       last month across all regions.

You: What are the policies for notifying customers of outages?

Agent: According to our Customer Service Policies document:
       
       - Customers must be notified within 15 minutes of confirmed outage
       - Use SMS, email, and app notifications for affected customers
       - Provide estimated restoration time when available
       - Send updates every 30 minutes during extended outages
       
       [Source: customer_service_policies.pdf, page 2]

You: Which outages exceeded the maximum duration defined in our policy?

Agent: Let me check the outage data against our policy thresholds...

       These outages exceeded the 4-hour maximum duration policy:
       
       | Outage ID | Region | Duration | Policy Max | Status |
       |-----------|--------|----------|------------|--------|
       | OUT-1042 | Northeast | 6.5 hrs | 4 hrs | Exceeded |
       | OUT-1089 | West | 5.2 hrs | 4 hrs | Exceeded |
       
       Recommend reviewing root cause and escalation procedures.

You: exit
```

## Checkpoint

!!! success "Solution Deployed!"
    You now have a working solution with:
    
    - [x] **Fabric IQ** answering data questions
    - [x] **Foundry IQ** retrieving document knowledge
    - [x] **Multi-Tool Agent** combining both sources
    
    ---

[← Configure dev environment](03-configure.md) | [Customize for your use case →](../02-customize/index.md)
