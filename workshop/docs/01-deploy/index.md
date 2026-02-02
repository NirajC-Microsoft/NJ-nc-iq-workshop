# Deploy Solution

Deploy the solution and see it working with the default Retail scenario.

## What You'll Do

| Step | Action | Time |
|------|--------|------|
| 1 | Deploy Azure infrastructure | ~7 min |
| 2 | Configure your environment | ~3 min |
| 3 | Run the solution with Retail demo data | ~5 min |

## What Gets Deployed

| Resource | Purpose |
|----------|---------|
| Azure AI Services | Hosts GPT-4o and embedding models |
| Azure AI Search | Vector database for document retrieval |
| Storage Account | Stores documents and agent artifacts |
| Application Insights | Traces agent calls for debugging |

## Default Retail Scenario

The solution runs immediately with an **E-Commerce** demo:

| Component | Contents | Purpose |
|-----------|----------|---------|
| **Structured Data** | `products.csv`, `orders.csv` | Fabric IQ queries |
| **Documents** | Return policy, shipping guide, FAQ | Foundry IQ retrieval |
| **Configuration** | Ontology, schema, sample questions | Agent setup |

### Sample Data

**Products (16 items across 4 categories):**

- Electronics: Wireless Headphones, 4K Smart TV, Bluetooth Speaker, Smartwatch
- Apparel: Organic T-Shirt, Running Shoes, Hiking Jacket, Denim Jeans
- Home & Kitchen: Cookware Set, Robot Vacuum, Air Purifier, Espresso Machine
- Sports: Yoga Mat, Dumbbell Set, Mountain Bike, Tennis Racket

**Orders (40 transactions):**

- Across regions: North America, Europe, Asia Pacific, Latin America
- Channels: Website, Mobile App, Marketplace, Social Commerce

## Sample Questions

Once running, you'll be able to ask:

**Data Questions (Fabric IQ):**
> "How many products do we have in stock?"
> "What are the top selling products by revenue?"
> "Show me orders from North America this month"

**Document Questions (Foundry IQ):**
> "What's our return policy for electronics?"
> "How long does standard shipping take?"
> "Do we offer gift wrapping?"

**Combined Questions (Both):**
> "Which low-stock products have the highest order volume — should we expedite reorders?"
> "Based on our shipping policy, which pending orders qualify for free shipping?"

!!! success "One-Time Setup"
    Deploy once, then use **Module 02** to customize for each customer engagement.
