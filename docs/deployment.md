# Deployment Guide

This project is configured with a GitHub Actions workflow that automates the deployment of the application to an Azure App Service using a Docker container hosted on Azure Container Registry (ACR).

## Prerequisites
- An Azure Container Registry (ACR).
- An Azure App Service (Web App for Containers) configured to pull the Docker image from your ACR.
- A Service Principal with permissions to access the ACR and restart the Web App.

## Required GitHub Secrets

To ensure the GitHub Actions workflow functions correctly, you must configure the following secrets in your GitHub repository:

- `ACR_LOGIN_SERVER`: The login server for your Azure Container Registry (e.g., `siteflow.azurecr.io`).
- `ACR_USERNAME`: The username for accessing the ACR.
- `ACR_PASSWORD`: The password for accessing the ACR.
- `AZURE_CREDENTIALS`: A JSON string representing your Azure Service Principal credentials. It should look like this:
  ```json
  {
    "clientId": "<GUID>",
    "clientSecret": "<GUID>",
    "subscriptionId": "<GUID>",
    "tenantId": "<GUID>",
    "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
    "resourceManagerEndpointUrl": "https://management.azure.com/",
    "activeDirectoryGraphResourceId": "https://graph.windows.net/",
    "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
    "galleryEndpointUrl": "https://gallery.azure.com/",
    "managementEndpointUrl": "https://management.core.windows.net/"
  }
  ```
- `AZURE_WEBAPP_NAME`: The name of your Azure App Service (e.g., `siteflow`).
- `AZURE_RESOURCE_GROUP`: The name of the resource group containing your App Service (e.g., `siteflow-rg`).

## Workflow Steps

The automated deployment workflow (`.github/workflows/deploy.yml`) performs the following steps on every push to the `main` branch:

1. **Checkout code**: Retrieves the latest code from the repository.
2. **Login to Azure Container Registry**: Authenticates with ACR using the provided secrets (`ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`).
3. **Build and push Docker image**: Builds the multi-stage Docker image and tags it with both `latest` and the current Git commit SHA. Pushes both tags to the ACR.
4. **Login to Azure**: Authenticates with Azure using the `AZURE_CREDENTIALS` service principal.
5. **Restart Azure Web App**: Uses the Azure CLI to restart the specified App Service (`AZURE_WEBAPP_NAME`) in the specified resource group (`AZURE_RESOURCE_GROUP`), which prompts it to pull the latest image.
6. **Health Check**: Waits 60 seconds and performs a `curl` request to the deployed application's URL. If the endpoint does not return an HTTP 200 status code, the deployment job fails.
