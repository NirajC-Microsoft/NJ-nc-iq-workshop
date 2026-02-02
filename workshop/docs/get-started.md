# Get Started

## Prerequisites

- Azure subscription with Contributor access
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- Microsoft Fabric workspace (for Fabric IQ features)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nchandhi/nc-iq-workshop)
[![Open in Dev Containers](https://img.shields.io/badge/Dev%20Containers-Open-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nchandhi/nc-iq-workshop)
[![Open in VS Code (Web)](https://img.shields.io/badge/VS%20Code-Open%20in%20Web-blue?logo=visualstudiocode)](https://vscode.dev/github/nchandhi/nc-iq-workshop)

## What You'll Demonstrate

| Component | Technology | Customer Value |
|-----------|------------|----------------|
| AI Agent | Azure AI Foundry | Single interface for all enterprise knowledge |
| Knowledge Base | Foundry IQ | Intelligent search over policies & documents |
| Business Ontology | Fabric IQ | Natural language queries over business data |
| Sample Data | AI-Generated | Realistic demo tailored to customer's industry |

## Your PoC Journey

### Module 01: Deploy Solution (Do Once)

Deploy infrastructure and run with pre-built **Retail / E-Commerce** data:

- Deploy Azure resources (AI Services, AI Search, Storage)
- Configure your environment
- See the agent working with sample Retail data
- Takes ~15 minutes

### Module 02: Customize for Your Customer (Repeat)

Generate custom data for **each customer engagement**:

| Customer Industry | Use Case Example | Demo Questions |
|-------------------|------------------|----------------|
| Retail | Product catalog + return policies | "What's our return policy for electronics over $500?" |
| Manufacturing | Equipment data + maintenance docs | "Which machines are overdue for maintenance per our schedule?" |
| Healthcare | Patient records + compliance docs | "Do we have capacity for emergency appointments today?" |
| Finance | Account data + lending policies | "Which loan applications meet our approval criteria?" |
| Insurance | Claims data + policy documents | "What's the status of claims filed this week vs our SLA?" |
| **Customer X** | **Their data + Their docs** | **Their burning questions** |

!!! tip "Pre-Meeting Prep"
    Run Module 03 the day before your customer meeting. Enter their industry and a brief use case description. The AI generates realistic sample data, documents, and test questions tailored to their world.

### Module 03: Understand the Technology

Prepare for technical questions in customer conversations:

- **Foundry IQ** — How agentic retrieval plans, iterates, and reflects
- **Fabric IQ** — How ontology translates business questions to SQL
- **Multi-Tool Agent** — How the agent decides which source to query

[Start Lab →](01-deploy/index.md)
