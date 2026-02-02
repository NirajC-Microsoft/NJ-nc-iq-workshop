# Fabric IQ: Data Intelligence

## What is Fabric IQ?

Fabric IQ is a semantic intelligence platform that connects AI agents to business data. It goes beyond simple database queries by understanding the meaning of your data through an **Ontology**.

## What is an Ontology?

An ontology is a semantic model that helps AI understand your business:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Entities** | Business objects | Products, Orders, Customers |
| **Relationships** | How entities connect | Order → contains → Products |
| **Rules** | Business logic | "Low Stock = stockLevel < reorderPoint" |
| **Actions** | Queryable operations | GetTopProducts, GetRevenueByRegion |

## How NL→SQL Works

```
User: "What products are selling well in Europe?"

┌─────────────────────────────────────────────────────────────┐
│  Step 1: UNDERSTAND                                         │
│  Agent interprets intent using ontology:                    │
│  • "products" → Products entity                             │
│  • "selling well" → high quantity in Orders                 │
│  • "Europe" → region filter                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: TRANSLATE                                          │
│  Generate SQL from semantic understanding:                  │
│                                                             │
│  SELECT p.productName, SUM(o.quantity) as totalSold         │
│  FROM products p                                            │
│  JOIN orders o ON p.productId = o.productId                 │
│  WHERE o.region = 'Europe'                                  │
│  GROUP BY p.productName                                     │
│  ORDER BY totalSold DESC                                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: EXECUTE & EXPLAIN                                  │
│  Run against Fabric, format response:                       │
│                                                             │
│  "Here are the top selling products in Europe:              │
│   1. Wireless Headphones - 234 units                        │
│   2. Smart TV 55" - 189 units                               │
│   3. Running Shoes - 156 units"                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Ontology Matters

### Without Ontology: Brittle Keyword Matching

```
User: "Show me our best customers"
System: ??? (what makes a customer "best"?)
```

### With Ontology: Business Understanding

```yaml
# Ontology defines:
rules:
  - name: "Premium Customer"
    definition: "totalSpend > 10000 AND orderCount > 5"
  - name: "Best Customer"
    definition: "Premium Customer with healthScore > 80"
```

```
User: "Show me our best customers"
Agent: Uses "Best Customer" rule → Correct SQL → Meaningful results
```

## The Power of Combined Intelligence

| Question Type | Source | Example |
|---------------|--------|---------|
| **Policy/Process** | Foundry IQ (Documents) | "What's our return policy?" |
| **Metrics/Numbers** | Fabric IQ (Data) | "What's our return rate?" |
| **Combined** | Both | "Are we meeting our return SLA?" |

### Combined Example

```
User: "Are we meeting our shipping SLA?"

Agent thinking:
1. First, I need the SLA targets (documents)
   → Search Foundry IQ → "Standard: 5 days, Express: 2 days"

2. Then, I need actual performance (data)
   → Query Fabric IQ → "Avg standard: 4.2 days, Express: 1.8 days"

3. Compare and respond:
   "Yes, we're meeting both SLAs. Standard shipping averages 
   4.2 days (target: 5 days) and Express averages 1.8 days 
   (target: 2 days)."
```

## Customer Talking Points

| Question | Response |
|----------|----------|
| "Why not just let users write SQL?" | "Most users can't write SQL. And even those who can may not know the schema. Natural language lets anyone query data." |
| "How do you handle ambiguous terms?" | "The ontology defines business terms. 'Best customer', 'low stock', 'overdue order' all have precise definitions your business controls." |
| "What about performance?" | "Queries run against Fabric's optimized engine. The NL→SQL translation happens once, then it's standard SQL execution." |

## Technical Details

### Fabric Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Microsoft Fabric                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Lakehouse   │ →  │  Warehouse   │ →  │  Semantic    │  │
│  │  (Raw Data)  │    │  (SQL Tables)│    │  Model       │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                ↓            │
│                                          ┌──────────┐       │
│                                          │ Fabric IQ│       │
│                                          │ Ontology │       │
│                                          └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Ontology Configuration

```json
{
  "entities": [
    {
      "name": "Products",
      "table": "products",
      "key": "productId",
      "attributes": ["productName", "category", "unitPrice", "stockLevel"]
    }
  ],
  "relationships": [
    {
      "name": "contains_product",
      "from": "Orders",
      "to": "Products",
      "type": "many-to-one"
    }
  ],
  "businessRules": [
    {
      "name": "LowStock",
      "entity": "Products",
      "condition": "stockLevel < reorderPoint"
    }
  ]
}
```
