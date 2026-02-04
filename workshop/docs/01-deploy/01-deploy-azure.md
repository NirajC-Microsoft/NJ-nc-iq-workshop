# Deploy Infrastructure

## Clone the Repository

```bash
git clone https://github.com/nchandhi/nc-iq-workshop.git
cd nc-iq-workshop
```

## Login to Azure

```bash
azd auth login
```

This opens a browser for authentication.

## Deploy Resources

```bash
azd up
```

Follow the prompts to select your environment name, subscription, and location etc.

!!! warning "Wait for Completion"
    Deployment takes 5-7 minutes. Don't proceed until you see the success message.

## Verify Deployment

You should see:

```
SUCCESS: Your application was provisioned in Azure.
```

Verify in [Azure Portal](https://portal.azure.com/) that your resource group contains all resources:

- Azure AI Services (Foundry)
- Azure AI Search
- Storage Account
- Application Insights

## Environment Variables

After deployment, Azure endpoints are automatically saved to `.azure/<env>/.env` and loaded by the scripts.

!!! note "No Manual Configuration"
    You don't need to manually set Azure connection strings. The scripts read them from the azd environment automatically.

---

[← Overview](index.md) | [Configure Fabric items →](02-setup-fabric.md)
