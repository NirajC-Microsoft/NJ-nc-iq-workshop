# Customize for your use case

This is where it gets exciting. Generate a complete working PoC tailored to your industry and use case in minutes.

## What you provide

Simply provide two inputs:

| Input | Description | Example |
|-------|-------------|---------|
| **Industry** | The business domain or vertical | Insurance, Retail, Manufacturing, Finance |
| **Use Case** | What the solution should help with | "Claims processing and policy management" |

!!! tip "Be descriptive"
    The more detail you provide in your use case, the better the generated content will match your scenario. For example:
    
    - ✓ "Property insurance with claims processing, policy management, and coverage verification"
    - ✗ "Insurance stuff"

## What gets generated

| Component | Generated Content |
|-----------|-------------------|
| **Documents** | Policies, procedures, FAQs specific to your industry |
| **Data** | Realistic CSV files with industry-appropriate entities |
| **Ontology** | Business rules and relationships for NL→SQL |
| **Sample Questions** | Questions to test the solution |

## Example Transformations

=== "Retail"

    **Input:** "Fashion e-commerce with seasonal inventory and returns"
    
    **Output:**
    - `products.csv` — SKUs, categories, seasonal collections
    - `orders.csv` — Customer orders with status
    - `return_policy.pdf` — Return and exchange guidelines
    - `shipping_guide.pdf` — Delivery options and timelines
    
    **Sample Questions:**
    - "What's our return policy for sale items?"
    - "Which products from the spring collection have low stock?"

=== "Manufacturing"

    **Input:** "Automotive parts with quality control and suppliers"
    
    **Output:**
    - `equipment.csv` — Machines, maintenance schedules
    - `suppliers.csv` — Vendor relationships, lead times
    - `quality_standards.pdf` — QC procedures
    - `maintenance_guide.pdf` — Equipment maintenance protocols
    
    **Sample Questions:**
    - "Which machines are overdue for maintenance?"
    - "What's our QC process for critical components?"

=== "Insurance"

    **Input:** "Property insurance with claims and policy management"
    
    **Output:**
    - `policies.csv` — Policy details, coverage, premiums
    - `claims.csv` — Claim status, amounts, dates
    - `claims_process.pdf` — How to file claims
    - `coverage_guide.pdf` — Policy coverage explanations
    
    **Sample Questions:**
    - "Which claims are approaching our SLA deadline?"
    - "What does our standard policy cover?"

=== "Finance"

    **Input:** "Regional bank with loans and compliance"
    
    **Output:**
    - `accounts.csv` — Customer accounts, balances
    - `loans.csv` — Loan applications, status
    - `lending_policy.pdf` — Approval criteria
    - `compliance_guide.pdf` — Regulatory requirements
    
    **Sample Questions:**
    - "Which loan applications meet our approval criteria?"
    - "What are our compliance requirements for large transactions?"

!!! tip "The more specific, the better"
    The AI uses your description to generate appropriate entity names, realistic data relationships, industry-specific documents, and relevant sample questions.

---

[← Build solution](../01-deploy/04-run-scenario.md) | [Generate & Build →](02-generate.md)
