# Customize for your use case

This is where it gets exciting. Generate a complete working PoC tailored to your industry and use case in minutes.

## What gets generated

When you run the AI generator for your scenario:

| Component | Generated Content |
|-----------|-------------------|
| **Documents** | Policies, procedures, FAQs specific to your industry |
| **Data** | Realistic CSV files with industry-appropriate entities |
| **Ontology** | Business rules and relationships for NL→SQL |
| **Sample Questions** | Demo questions to showcase the solution |

## Example Transformations

=== "Retail"

    **Input:** "Fashion e-commerce with seasonal inventory and returns"
    
    **Output:**
    - `products.csv` — SKUs, categories, seasonal collections
    - `orders.csv` — Customer orders with status
    - `return_policy.pdf` — Return and exchange guidelines
    - `shipping_guide.pdf` — Delivery options and timelines
    
    **Demo Questions:**
    - "What's our return policy for sale items?"
    - "Which products from the spring collection have low stock?"

=== "Manufacturing"

    **Input:** "Automotive parts with quality control and suppliers"
    
    **Output:**
    - `equipment.csv` — Machines, maintenance schedules
    - `suppliers.csv` — Vendor relationships, lead times
    - `quality_standards.pdf` — QC procedures
    - `maintenance_guide.pdf` — Equipment maintenance protocols
    
    **Demo Questions:**
    - "Which machines are overdue for maintenance?"
    - "What's our QC process for critical components?"

=== "Healthcare"

    **Input:** "Multi-location clinic with patient scheduling"
    
    **Output:**
    - `patients.csv` — Patient records, appointments
    - `providers.csv` — Doctor availability, specialties
    - `scheduling_policy.pdf` — Appointment guidelines
    - `insurance_guide.pdf` — Coverage verification
    
    **Demo Questions:**
    - "Which providers have availability this week?"
    - "What's our policy for same-day appointments?"

=== "Finance"

    **Input:** "Regional bank with loans and compliance"
    
    **Output:**
    - `accounts.csv` — Customer accounts, balances
    - `loans.csv` — Loan applications, status
    - `lending_policy.pdf` — Approval criteria
    - `compliance_guide.pdf` — Regulatory requirements
    
    **Demo Questions:**
    - "Which loan applications meet our approval criteria?"
    - "What are our compliance requirements for large transactions?"

!!! tip "The more specific, the better"
    The AI uses your description to generate appropriate entity names, realistic data relationships, industry-specific documents, and relevant sample questions.

---

[← Build solution](../01-deploy/04-run-scenario.md) | [Generate & Build →](02-generate.md)
