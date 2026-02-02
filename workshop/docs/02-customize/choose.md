# Choose Industry & Use Case

## Gathering Customer Context

Before generating a PoC, gather these details from your customer conversation:

| Question | What to Capture |
|----------|-----------------|
| "What industry are you in?" | Retail, Manufacturing, Healthcare, Finance, etc. |
| "What's the business process?" | The workflow they want to improve |
| "What questions do users ask?" | The natural language queries they need answered |
| "Where does the info live?" | Documents (policies) vs. databases (metrics) |

## Defining Your Scenario

### Industry

Keep it simple and specific:

| ✅ Good | ❌ Too Vague |
|---------|-------------|
| Retail | Business |
| Healthcare | Services |
| Manufacturing | Industry |
| Insurance | Finance stuff |

### Use Case

Describe the specific business context:

| ✅ Good | ❌ Too Vague |
|---------|-------------|
| "Fashion e-commerce with seasonal collections and loyalty program" | "Online store" |
| "Hospital patient scheduling and insurance verification" | "Healthcare" |
| "Auto parts manufacturing with quality control and supplier management" | "Factory" |
| "Commercial property insurance claims processing" | "Insurance company" |

!!! tip "The More Specific, The Better"
    The AI uses your description to generate:
    
    - Appropriate entity names (e.g., "Claims" vs "Orders")
    - Realistic data relationships
    - Industry-specific document topics
    - Relevant sample questions

## Common Customer Scenarios

Here are proven scenarios that resonate with customers:

### Retail & E-commerce

```env
INDUSTRY=Retail
USECASE=Online electronics store with product catalog, customer orders, return processing, and warranty claims
```

### Manufacturing & Supply Chain

```env
INDUSTRY=Manufacturing
USECASE=Automotive parts production with equipment maintenance, quality inspections, and supplier relationships
```

### Healthcare & Life Sciences

```env
INDUSTRY=Healthcare
USECASE=Multi-location clinic with patient scheduling, provider availability, and insurance verification
```

### Financial Services

```env
INDUSTRY=Finance
USECASE=Regional bank with checking accounts, loan origination, and regulatory compliance
```

### Insurance

```env
INDUSTRY=Insurance
USECASE=Property and casualty insurance with claims processing, policy management, and fraud detection
```

### Professional Services

```env
INDUSTRY=Professional Services
USECASE=Consulting firm with project staffing, client engagements, and resource utilization
```

## Configure Your Scenario

Edit `.env` in the project root:

```env
# --- Customer PoC Configuration ---
INDUSTRY=Your Customer's Industry
USECASE=Detailed description of their business context
DATA_SIZE=small
```

### Data Size Options

| Size | Records | Best For |
|------|---------|----------|
| `small` | ~50 total | Quick demos, meetings |
| `medium` | ~250 total | Deeper exploration |
| `large` | ~1000 total | Extended workshops |

!!! tip "Start Small"
    Use `small` for customer demos. It's faster to generate and easier to walk through.

## Next Step

Once configured, proceed to [Generate Custom Data](generate.md) to build your PoC.
