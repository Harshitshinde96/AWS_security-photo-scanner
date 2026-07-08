import boto3
import json
import os
import sys

# 1. Fetch Secrets from Environment Variables
BUCKET_NAME = os.environ.get('BUCKET_NAME')
REGION = os.environ.get('AWS_REGION')
PHOTO_NAME = 'employee.jpg'

if not BUCKET_NAME or not REGION:
    print("Error: Missing AWS environment variables.")
    sys.exit(1)

# 2. Initialize AWS Clients
s3_client = boto3.client('s3', region_name=REGION)
rekognition_client = boto3.client('rekognition', region_name=REGION)

try:
    # 3. Upload the photo to S3
    print(f"Uploading {PHOTO_NAME} to S3 bucket: {BUCKET_NAME}...")
    s3_client.upload_file(PHOTO_NAME, BUCKET_NAME, PHOTO_NAME)
    print("Upload successful!")

    # 4. Analyze the photo with Rekognition
    print(f"Analyzing {PHOTO_NAME} for faces...")
    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': PHOTO_NAME}},
        Attributes=['DEFAULT']
    )

    # 5. Process the Results
    faces = response.get('FaceDetails', [])
    num_faces = len(faces)

    print("\n--- SECURITY SCAN COMPLETE ---")
    print(f"Number of faces detected: {num_faces}")

    results_data = {
        "photo": PHOTO_NAME,
        "total_faces": num_faces,
        "face_data": []
    }

    # Extract confidence scores
    for idx, face in enumerate(faces):
        confidence = face['Confidence']
        print(f"Face {idx + 1} Confidence: {confidence:.2f}%")
        results_data["face_data"].append({
            "face_id": idx + 1,
            "confidence_score": round(confidence, 2)
        })

    # 6. Save to JSON file
    with open('result.json', 'w') as f:
        json.dump(results_data, f, indent=4)
        
    print("\nResults successfully saved to result.json")

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
