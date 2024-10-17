import hvac

def read_secret_from_vault(vault_addr, vault_token, secret_path):
    """Reads a secret from HashiCorp Vault."""

    client = hvac.Client(url=vault_addr, token=vault_token)

    try:
        read_response = client.secrets.kv.v2.read_secret_version(path=secret_path)
        secret_data = read_response['data']['data']
        return secret_data
    except Exception as e:
        print(f"Error reading secret: {e}")
        return None

if __name__ == "__main__":
    vault_address = "http://your-vault-address:8200"  # Replace with your Vault address
    vault_token = "your-vault-token"  # Replace with your Vault token
    secret_path = "path/to/your/secret"  # Replace with the path to your secret

    secret = read_secret_from_vault(vault_address, vault_token, secret_path)

    if secret:
        print(f"Secret data: {secret}")
