# Get Started

## Prerequisites

- Azure subscription with Contributor access
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- Microsoft Fabric workspace (for Fabric IQ features)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nchandhi/nc-iq-workshop)
[![Open in Dev Containers](https://img.shields.io/badge/Dev%20Containers-Open-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nchandhi/nc-iq-workshop)
[![Open in VS Code (Web)](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/github/nchandhi/nc-iq-workshop)

## Your PoC journey

### Step 1: Deploy solution (do once)

Deploy infrastructure and run with pre-built **Retail / E-Commerce** data:

- Deploy **Microsoft Foundry** and Azure resources (AI Services, AI Search, Storage)
- Configure **Microsoft Fabric** connection
- Configure your environment
- See the agent working with sample Retail data
- Takes ~15 minutes

### Step 2: Customize for your use case (repeat)

Generate custom data for **each use case**:

| Customer Industry | Use Case Example | Demo Questions |
|-------------------|------------------|----------------|
| Retail | Product catalog + return policies | "What's our return policy for electronics over $500?" |
| Manufacturing | Equipment data + maintenance docs | "Which machines are overdue for maintenance per our schedule?" |
| Healthcare | Patient records + compliance docs | "Do we have capacity for emergency appointments today?" |
| Finance | Account data + lending policies | "Which loan applications meet our approval criteria?" |
| Insurance | Claims data + policy documents | "What's the status of claims filed this week vs our SLA?" |
| **Customer X** | **Their data + Their docs** | **Their burning questions** |

!!! tip "Pre-PoC prep"
    Run Step 2 before your PoC. Enter the industry and a brief use case description. The AI generates realistic sample data, documents, and test questions tailored to your scenario.

### Step 3: How it works

Prepare for technical questions in customer conversations:

- **Foundry IQ**: How agentic retrieval plans, iterates, and reflects
- **Fabric IQ**: How ontology translates business questions to SQL
- **Multi-Tool Agent**: How the agent decides which source to query

[Start Lab →](01-deploy/index.md)
