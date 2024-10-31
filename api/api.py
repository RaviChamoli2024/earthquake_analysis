import requests

# Replace these variables with your actual Prefect Cloud credentials
PREFECT_API_KEY = "pnu_ibVgpenMxf1TGaGzDv0engDR8jAQEN3l7ipG"  # Your Prefect Cloud API key
ACCOUNT_ID = "6f5eaacd-e259-45a3-a000-1a492db7bc46"  # Your Prefect Cloud Account ID
WORKSPACE_ID = "c2eedb3c-c6fb-488f-af7a-42e718fad8f0"  # Your Prefect Cloud Workspace ID

# Correct API URL to list artifacts
PREFECT_API_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}/artifacts/filter"

# Data to filter artifacts
data = {
    "sort": "CREATED_DESC",  # Sort by creation date in descending order
    "limit": 5,  # Limit the number of artifacts returned
    "artifacts": {
        "key": {
            "exists_": True  # Filter for artifacts that have a key
        }
    }
}

# Set up headers with Authorization
headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}

# Make the request to the Prefect API
response = requests.post(PREFECT_API_URL, headers=headers, json=data)

# Check the response status
if response.status_code != 200:
    print(f"Error: Received status code {response.status_code}")
    print(f"Response content: {response.text}")
else:
    # Parse the JSON response
    artifacts = response.json()
    print("Artifacts retrieved:")
    
    # Check if the response is a list
    if isinstance(artifacts, list):
        for artifact in artifacts:  # Directly iterate over the list
            print(artifact)
    else:
        print("Unexpected response format:", artifacts)
