import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def optimize_schedule(mock_data):
    try:
        # Initialize Bedrock runtime client
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
                        "content": f"Given the following course schedule and student enrollment data, your task is to optimize the exam schedule to avoid any conflicts and minimize student stress. Check for any exam time conflicts for students enrolled in multiple courses. If a student is taking two courses that have exams at the same time, adjust one of the exam times to avoid conflict. After resolving conflicts, assign appropriate rooms to each exam based on the available room capacities, ensuring that no room exceeds its capacity. Optimize the overall student workload by spreading exams out across days. Try to avoid scheduling multiple exams for a student on the same day, if possible, to minimize stress. Return a revised schedule with adjusted exam times and room assignments, while ensuring that no student faces overlapping exams. Make sure to only return the optimized schedule. Do not return any explantion or other wording. Only return the optimized schedule. Here is the course data: {json.dumps(mock_data)}"
                    }
                ]
            })
        )

        # Process and parse the model response
        response_body = json.loads(response['body'].read())
        schedule = json.loads(response_body['content'][0]['text'])

        print(schedule)
        return schedule
        
    except NoCredentialsError:
        print("Credentials not found.")
    except PartialCredentialsError:
        print("Incomplete credentials.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Load mock data from mock_data.json
    with open('database/mock_data.json', 'r') as file:
        mock_data = json.load(file)

    # Get the schedule from the model
    schedule = get_schedule_from_model(mock_data)
    if schedule:
        print("Schedule successfully generated!")
