import requests

# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_ibVgpenMxf1TGaGzDv0engDR8jAQEN3l7ipG"  # Your Prefect Cloud API key
ACCOUNT_ID = "6f5eaacd-e259-45a3-a000-1a492db7bc46"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "c2eedb3c-c6fb-488f-af7a-42e718fad8f0"  # Your Prefect Cloud Workspace ID
DEPLOYMENT_ID = "99fef0d9-656e-47ca-93cc-a6af4aa92a14"  # Your Deployment ID

# Correct API URL to get deployment details
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/deployments/{DEPLOYMENT_ID}"

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request using GET
response = requests.get(PREFECT_API_URL, headers=headers)

# Check the response status
if response.status_code == 200:
    deployment_info = response.json()
    print("Deployment Information:")
    print(deployment_info)
else:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")