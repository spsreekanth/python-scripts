import hvac
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_vault_secret(vault_address, secret_path, service_account_file):
    """
    Reads a secret from Vault using GCP service account authentication.

    Args:
        vault_address (str): The address of the Vault server.
        secret_path (str): The path to the secret in Vault.
        service_account_file (str): The path to the service account JSON file.

    Returns:
        dict: The secret data retrieved from Vault.
    """

    # Create credentials using the service account file
    creds = Credentials.from_service_account_file(service_account_file)

    # Refresh the credentials if necessary
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

    # Create a Vault client and authenticate using the service account token
    client = hvac.Client(url=vault_address)
    client.auth.gcp(creds)

    # Read the secret from Vault
    secret = client.secrets.kv.v2.read_secret(path=secret_path)

    return secret["data"]["data"]

# Dictionary to store Vault URLs per environment
vault_urls = {
    "dev": "https://your-vault-dev-address.cloud.example.com",
    "qa": "https://your-vault-qa-address.cloud.example.com",
    "uat": "https://your-vault-uat-address.cloud.example.com",
    "prod": "https://your-vault-prod-address.cloud.example.com"
}

# Example usage
secret_path = "secret/my-secret"
service_account_file = "path/to/your/service-account.json"

# Get secret for each environment
for environment, vault_url in vault_urls.items():
    secret_data = get_vault_secret(vault_url, secret_path, service_account_file)
    print(f"Environment: {environment}")
    print(f"Secret Data: {secret_data}")
