# Cleanup

Delete your Azure resources when you're done to manage costs.

## Delete Azure Resources

```bash
azd down
```

Confirm when prompted:

```
? Total resources to delete: 8, are you sure? (y/N) y
```

## Verify Deletion

1. Go to [Azure Portal](https://portal.azure.com/)
2. Check **Resource groups**
3. Confirm your lab resource group is deleted

!!! warning "Important"
    Always run cleanup to avoid ongoing charges!

## Clean Up Fabric (Optional)

If you created Fabric artifacts and want to remove them:

1. Go to [Microsoft Fabric](https://app.fabric.microsoft.com/)
2. Open your workspace
3. Delete the Lakehouse and Warehouse created for this workshop

## Clean Up Local Files (Optional)

Remove generated data folders:

=== "Windows PowerShell"

    ```powershell
    Remove-Item -Recurse -Force data\*_*
    ```

=== "macOS/Linux"

    ```bash
    rm -rf data/*_*/
    ```

---

## 🎉 You're Ready to Build Customer PoCs!

You now have everything you need to accelerate customer engagements.

### What You Can Now Do

- ✅ **Deploy in minutes**: Infrastructure as Code makes setup repeatable
- ✅ **Generate any scenario**: AI creates realistic data for any industry
- ✅ **Demo document intelligence**: Foundry IQ with agentic retrieval
- ✅ **Demo data intelligence**: Fabric IQ with natural language queries
- ✅ **Show combined power**: Multi-tool agent answers complex questions

### Quick Reference: Building a Customer PoC

```bash
# Before each customer meeting, generate their scenario:
python scripts/00_build_solution.py --ai --clean \
  --industry "Customer's Industry" \
  --usecase "Brief description of their use case"
```

**Example for a retail customer:**
```bash
python scripts/00_build_solution.py --ai --clean \
  --industry "Retail" \
  --usecase "Fashion e-commerce with seasonal inventory, customer orders, and return processing"
```

### Talking Points for Customer Conversations

| Customer Question | Your Answer |
|-------------------|-------------|
| "How long to implement?" | Solution accelerator gets you to PoC in hours, production in weeks |
| "Does it work with our data?" | Connects to any documents and Fabric/SQL data sources |
| "How accurate is it?" | Agentic retrieval plans and validates answers, cites sources |
| "Is it secure?" | Enterprise security with Entra ID, runs in your Azure tenant |

### Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Responsible AI Practices](https://www.microsoft.com/ai/responsible-ai)

---

**Go build amazing customer demos! 🚀**
