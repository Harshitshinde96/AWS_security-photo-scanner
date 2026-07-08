import boto3
import json
import os
import sys

# 1. Fetch Variables and Arguments
BUCKET_NAME = os.environ.get('BUCKET_NAME')
REGION = os.environ.get('AWS_REGION')

# Read the file path passed from GitHub Actions
if len(sys.argv) < 2:
    print("Error: No image path provided.")
    sys.exit(1)
    
photo_path = sys.argv[1]
photo_filename = os.path.basename(photo_path) # Extracts just 'image.jpg' from 'photos/image.jpg'

if not BUCKET_NAME or not REGION:
    print("Error: Missing AWS environment variables.")
    sys.exit(1)

# 2. Initialize AWS Clients
s3_client = boto3.client('s3', region_name=REGION)
rekognition_client = boto3.client('rekognition', region_name=REGION)

try:
    # 3. Upload & Analyze
    print(f"Uploading {photo_filename} to S3...")
    s3_client.upload_file(photo_path, BUCKET_NAME, photo_filename)

    print(f"Analyzing {photo_filename} for faces...")
    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': photo_filename}},
        Attributes=['DEFAULT']
    )

    # 4. Structure the New Result
    faces = response.get('FaceDetails', [])
    new_result = {
        "photo": photo_filename,
        "total_faces": len(faces),
        "face_data": [
            {"face_id": idx + 1, "confidence_score": round(face['Confidence'], 2)} 
            for idx, face in enumerate(faces)
        ]
    }
    
    print(f"Detected {len(faces)} faces.")

    # 5. Load, Append, and Save JSON
    json_file = 'result.json'
    all_results = []
    
    # Check if the file already exists and load its contents
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            try:
                all_results = json.load(f)
                # Ensure it's a list (in case the old file was a single dictionary)
                if not isinstance(all_results, list):
                    all_results = [all_results]
            except json.JSONDecodeError:
                all_results = [] # Reset if the file is corrupted or empty

    # Append the newly scanned image data
    all_results.append(new_result)

    # Overwrite the file with the newly updated list
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=4)
        
    print(f"Results for {photo_filename} successfully appended to {json_file}")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
