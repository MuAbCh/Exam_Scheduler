import json
import boto3

# Initialize AWS Bedrock client
bedrock = boto3.client('bedrock', region_name='us-west-2')

# List available models
def list_models():
    try:
        response = bedrock.list_foundation_models()
        models = response['models']
        print("Available Foundation Models:")
        for model in models:
            print(f"Model ID: {model['modelId']}, Provider: {model['providerName']}")
    except Exception as e:
        print(f"Error listing models: {e}")

# Example usage
list_models()

def optimize_schedule():
    # Load mock data
    with open("database/mock_data.json", "r") as f:
        data = json.load(f)

    # Dummy optimization logic
    schedule = [
        {"course": "ECE300", "room": "Room A", "time": "9:00 AM"},
        {"course": "ECE400", "room": "Room B", "time": "11:00 AM"}
    ]

    return schedule
