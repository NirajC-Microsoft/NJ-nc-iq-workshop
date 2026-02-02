# Build faster with Solution Accelerators – Foundry IQ + Fabric IQ (Workshop)

Build AI agents that combine **unstructured document knowledge** with **structured enterprise data** using knowledge bases, ontology, and natural language queries.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR-ORG/fabric-ontology-lab?quickstart=1)

## The Opportunity

Organizations have valuable knowledge spread across documents (PDFs, policies, manuals) and structured systems (databases, data warehouses). By connecting these sources through AI, users can get unified answers from a single conversational interface.

## The Solution

This lab enables an intelligent agent that:

- **Creates knowledge bases** from documents with agentic retrieval (plan, iterate, reflect)
- **Defines business ontology** to understand entities, relationships, and rules
- **Queries data** using natural language over both documents and structured data
- **Combines both** to answer complex business questions

---

## Get Started

### Prerequisites

- Azure subscription with Contributor access
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Python 3.10+](https://www.python.org/downloads/)
- Microsoft Fabric workspace (for Fabric IQ features)

### What You'll Build

| Component | Technology | Description |
|-----------|------------|-------------|
| AI Agent | Azure AI Foundry | Orchestrates tools and generates responses |
| Knowledge Base | Foundry IQ | Agentic retrieval over documents |
| Business Ontology | Fabric IQ | Entities, relationships, and NL→SQL |
| Sample Data | AI-Generated | Custom data for any industry/use case |

### Open the Lab

[![Open in GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://codespaces.new/YOUR-ORG/fabric-ontology-lab?quickstart=1)
[![Open in VS Code](https://img.shields.io/badge/VS%20Code-Dev%20Containers-blue?logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/YOUR-ORG/fabric-ontology-lab)

---

## Lab Modules

### 01 Setup

#### Deploy Infrastructure

```bash
# Login to Azure
azd auth login

# Deploy all resources (AI Services, AI Search, Storage)
azd up
```

This deploys:
- Azure AI Services (Foundry) with GPT-4o-mini and text-embedding-3-large
- Azure AI Search (Basic tier with semantic search)
- Azure Storage Account
- Application Insights

All Azure endpoints are automatically saved to `.azure/<env>/.env` and loaded by the scripts.

#### Python Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Install dependencies (choose one)
pip install uv && uv pip install -r requirements.txt  # Fast (recommended)
pip install -r requirements.txt                        # Standard
```

#### Configure Environment

After `azd up`, Azure service endpoints are automatically available from the azd environment. 

Edit `.env` in the project root for **project-specific settings only**:

```env
# --- Microsoft Fabric (required) ---
FABRIC_WORKSPACE_ID=your-workspace-id
SOLUTION_NAME=myproject

# --- AI Data Generation ---
INDUSTRY=Logistics
USECASE=Fleet management with delivery tracking
DATA_SIZE=small
```

**Sample Industry-UseCase Combinations:**

| Industry | Use Case |
|----------|----------|
| Logistics | Fleet management with delivery tracking |
| Healthcare | Patient records and appointment scheduling |
| Retail | Inventory management with sales analytics |
| Finance | Transaction monitoring and fraud detection |
| Manufacturing | Production line tracking with quality control |
| Education | Student enrollment and course management |
| Hospitality | Hotel reservations and guest services |
| Real Estate | Property listings and lease management |
| Insurance | Claims processing and policy management |
| Telecommunications | Customer service and network monitoring |

> **Note**: Azure endpoints (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_SEARCH_ENDPOINT`, etc.) are read automatically from the azd environment. No need to copy them manually!

---

### 02 Run the Pipeline

Run the complete pipeline with a single command:

```bash
python scripts/00_build_solution.py --ai
```

This automatically:
1. **Generates sample data** - AI creates tables, PDFs, and questions for your industry
2. **Sets up Fabric** - Creates lakehouse and semantic ontology
3. **Loads data** - Uploads CSVs and creates Delta tables
4. **Generates prompts** - Creates optimized NL2SQL schema prompt
5. **Indexes documents** - Uploads PDFs to Azure AI Search
6. **Creates agent** - Builds multi-tool AI agent with SQL + Search

**Pipeline Options:**
- `--ai` - Use AI-generated data (recommended)
- `--from 03` - Start from a specific step
- `--only 06` - Run only one step
- `--skip 05` - Skip a specific step

---

### 03 Test the Agent

Run interactive tests combining both Foundry IQ and Fabric IQ:

```bash
python scripts/08a_test_multi_tool_agent.py
```

Try these question types:

| Type | Example | Data Source |
|------|---------|-------------|
| SQL | "How many orders last month?" | Fabric (structured) |
| Document | "What is our return policy?" | Search (unstructured) |
| Combined | "Which drivers violate the hours policy?" | Both |

---

### 04 Cleanup

Delete Azure resources when done:

```bash
azd down
```

---

## Project Structure

```
fabric-ontology-lab/
├── .devcontainer/          # GitHub Codespaces config
├── .env.example            # Configuration template
├── azure.yaml              # azd configuration
├── infra/                  # Bicep infrastructure
│   ├── main.bicep
│   └── modules/
│       └── foundry.bicep
├── scripts/
│   ├── 00_run_pipeline.py      # Full pipeline orchestrator
│   ├── 01a_generate_sample_data.py  # AI data generation
│   ├── 02_setup_fabric.py      # Fabric lakehouse & ontology
│   ├── 03_load_fabric_data.py  # Load data to Fabric
│   ├── 04_generate_prompt.py   # NL2SQL prompt generation
│   ├── 06_upload_to_search.py  # Document indexing
│   ├── 07a_create_foundry_agent.py  # Multi-tool agent
│   └── 08a_test_multi_tool_agent.py # Interactive testing
└── data/                   # Generated sample data
```

---

## Estimated Costs

| Resource | SKU | Est. Monthly Cost |
|----------|-----|-------------------|
| Azure AI Services | S0 | ~$0 (pay per token) |
| Azure AI Search | Basic | ~$70 |
| Storage Account | Standard LRS | ~$1 |
| Application Insights | Pay-per-use | ~$2 |

**Total**: ~$75/month + token usage

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "FABRIC_WORKSPACE_ID not set" | Get ID from Fabric portal URL |
| "Role assignment failed" | Wait 2 min after `azd up`, retry |
| "Model deployment not found" | Check MODEL_DEPLOYMENT in `.env` |

---

## License

MIT
