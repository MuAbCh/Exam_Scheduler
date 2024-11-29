import boto3
import json
import os
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
                        "content": f"Given the following course schedule and student enrollment data, your task is to optimize the exam schedule to avoid any conflicts and minimize student stress. Check for any exam time conflicts for students enrolled in multiple courses. If a student is taking two courses that have exams at the same time, adjust one of the exam times to avoid conflict. After resolving conflicts, assign appropriate rooms to each exam based on the available room capacities, ensuring that no room exceeds its capacity. Optimize the overall student workload by spreading exams out across days. Try to avoid scheduling multiple exams for a student on the same day, if possible, to minimize stress. Return a revised schedule with adjusted exam times and room assignments, while ensuring that no student faces overlapping exams. Make sure to only return the optimized schedule. Do not return any explanation or other wording. Only return the optimized schedule. Here is the course data: {json.dumps(mock_data)}"
                    }
                ]
            })
        )

        # Process and parse the model response
        response_body = json.loads(response['body'].read())
        schedule = json.loads(response_body['content'][0]['text'])

        # Save the schedule to a new_data.json file
        with open('database/new_data.json', 'w') as outfile:
            json.dump(schedule, outfile, indent=4)

        print("Optimized schedule saved successfully!")
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
    schedule = optimize_schedule(mock_data)  # Changed get_schedule_from_model to optimize_schedule
    if schedule:
        print("Schedule successfully generated!")

def loadexistingexams():
    # Construct absolute path to mock_data.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mock_data_path = os.path.join(current_dir, "database", "mock_data.json")

    try:
        with open(mock_data_path, "r") as f:
            data = json.load(f)
        print(f"Loaded mock data from {mock_data_path}")  # Debug log
    except FileNotFoundError:
        print(f"mock_data.json not found at {mock_data_path}")  # Debug log
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")  # Debug log
        return []

    existing_exams = []
    for course in data.get("courses", []):
        exam = course.get("exam", {})
        if exam.get("date") and exam.get("time") and exam.get("length"):
            try:
                # Improved parsing to handle different formats
                length_parts = exam["length"].split()
                if len(length_parts) != 2:
                    print(f"Invalid length format for course {course['name']}: {exam['length']}")  # Debug log
                    continue
                length_value, length_unit = length_parts
                if length_unit.lower().startswith("hour"):
                    exam_length = int(float(length_value) * 60)  # Convert hours to minutes
                elif length_unit.lower().startswith("minute"):
                    exam_length = int(length_value)
                else:
                    print(f"Unknown length unit for course {course['name']}: {length_unit}")  # Debug log
                    continue
            except (ValueError, IndexError) as e:
                print(f"Error parsing exam length for course {course['name']}: {e}")  # Debug log
                continue
            existing_exams.append({
                "course": course["name"],
                "room": exam.get("room", ""),  # Assuming room info is added in the future
                "date": exam["date"],
                "time": exam["time"],
                "exam_length": exam_length
            })

    print(f"Loaded Exams: {existing_exams}")  # Debug log
    return existing_exams