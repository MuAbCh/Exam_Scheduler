import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json

def test_bedrock_connection():
    try:
        # Initialize Bedrock runtime client (not bedrock client)
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

        # Send request to Claude 3.5 Sonnet model
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": "Can you help me optimize a scheduling system for university exams if I were to provide you the course information and course enrollment information such that there are no conflicts or at least minimum conflicts?"
                    }
                ]
            })
        )

        # Process and print the response
        response_body = json.loads(response['body'].read())
        print(f"Response: {response_body}")
        
    except NoCredentialsError:
        print("Credentials not found.")
    except PartialCredentialsError:
        print("Incomplete credentials.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Test the connection
test_bedrock_connection()
