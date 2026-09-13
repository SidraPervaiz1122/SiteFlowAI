# Troubleshooting

Below is a table of real issues encountered during deployment and setup, along with their fixes.

| Issue | Description | Fix |
| :--- | :--- | :--- |
| **Image pull auth failures** | Azure App Service failed to pull the Docker image from ACR due to authentication issues. | Ensure the App Service is configured with the correct ACR credentials or has Managed Identity access to pull from the registry. |
| **Missing GitHub secrets** | The GitHub Actions deployment workflow failed because required secrets were not found. | Verify that all secrets (`ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`, `AZURE_CREDENTIALS`, `AZURE_WEBAPP_NAME`, `AZURE_RESOURCE_GROUP`) are properly set in repository settings. |
| **Service principal setup** | Deployment failed during Azure login due to invalid service principal format. | Ensure `AZURE_CREDENTIALS` is a valid JSON object containing all required fields (clientId, clientSecret, subscriptionId, tenantId, etc.). |
| **SQLite-on-ephemeral-storage demo login bug** | On Azure App Service (which uses ephemeral storage by default for containers), the SQLite database was lost on container restart, causing login failures. | Implemented auto-seeding of the database on startup for ephemeral environments (commit `fdd4f20`) so demo accounts are always available. |
