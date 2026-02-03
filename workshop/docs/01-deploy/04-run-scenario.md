# Run Default Scenario

## Run the Full Pipeline

One command builds everything:

```bash
python scripts/00_build_solution.py
```

This runs all steps automatically:

| Step | What Happens | Time |
|------|--------------|------|
| 01 | Load sample data | ~10s |
| 02 | Setup Fabric workspace | ~30s |
| 03 | Load data into Fabric | ~1min |
| 04 | Generate NL2SQL prompt | ~5s |
| 05 | Create Fabric Data Agent | ~30s |
| 06 | Upload documents to AI Search | ~1min |
| 07a | Create Multi-Tool Agent | ~10s |

## Expected Output

```
============================================================
Building Solution: Default
============================================================

[01/07] Loading sample data...
  ✓ Generating scenario data

[02/07] Setting up Fabric workspace...
  ✓ Lakehouse: iqworkshop_lakehouse
  ✓ Warehouse: iqworkshop_warehouse

[03/07] Loading data into Fabric...
  ✓ products.csv → 16 rows
  ✓ orders.csv → 40 rows

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

You: How many products do we have?

Agent: Based on the database, we currently have 16 products in our catalog
       across 4 categories: Electronics, Apparel, Home & Kitchen, and Sports.

You: What's our return policy?

Agent: According to our Return Policy document:
       
       - Items can be returned within 30 days of purchase
       - Products must be in original packaging and unused condition
       - Electronics have a 15-day return window
       - Final sale items cannot be returned
       
       [Source: return_policy.pdf, page 1]

You: Which electronics products have low stock that might need reordering?

Agent: Let me check the inventory data against reorder points...

       These electronics products are at or below their reorder point:
       
       | Product | Stock | Reorder Point | Status |
       |---------|-------|---------------|--------|
       | Wireless Headphones | 45 | 50 | Reorder needed |
       | Smartwatch Pro | 22 | 30 | Reorder needed |
       
       Recommend placing purchase orders for these items.

You: exit
```

## Checkpoint

!!! success "Solution Deployed!"
    You now have a working solution with:
    
    - [x] **Fabric IQ** answering data questions (product counts, orders, inventory)
    - [x] **Foundry IQ** retrieving document knowledge (policies, guides)
    - [x] **Multi-Tool Agent** combining both sources
    
    ---

[← Configure environment](03-configure.md) | [Customize for your use case →](../02-customize/index.md)
