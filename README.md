# AWS Security Photo Scanner

This project is an automated security photo scanning solution that leverages AWS S3, AWS Rekognition, and GitHub Actions to analyze photos pushed to the repository.

## Overview

Whenever a new photo (such as an employee badge photo) is added to the `photos/` directory and pushed to the repository, a GitHub Action is automatically triggered. This workflow performs the following steps:
1. **Upload**: Uploads the newly added photo to an Amazon S3 bucket.
2. **Analyze**: Uses Amazon Rekognition to scan the photo and detect faces, retrieving confidence scores and face counts.
3. **Record**: Appends the analysis results (including face count and confidence scores) to a `result.json` file.
4. **Commit**: Automatically commits and pushes the updated `result.json` back to the repository.

## Architecture & Technologies
- **Python (boto3)**: Used for the core analysis script (`analyze.py`) that interacts with AWS APIs.
- **AWS S3**: Storage service where the photos are temporarily or permanently stored.
- **AWS Rekognition**: Machine learning service used to detect faces within the uploaded images.
- **GitHub Actions**: Provides the CI/CD pipeline (`.github/workflows/python-app.yml`) that orchestrates the workflow upon a `push` event.

## Setup Instructions

To run this project in your own environment, you need an AWS account and a GitHub repository.

### 1. AWS Configuration
1. Create an **S3 Bucket** in your preferred AWS Region.
2. Create an **IAM User** with programmatic access (Access Key ID and Secret Access Key).
3. Attach policies to the IAM User granting permissions for:
   - `s3:PutObject` on your S3 bucket.
   - `rekognition:DetectFaces` to allow face detection.

### 2. GitHub Secrets
In your GitHub repository, navigate to **Settings > Secrets and variables > Actions** and add the following repository secrets:
- `AWS_ACCESS_KEY_ID`: Your IAM User's access key.
- `AWS_SECRET_ACCESS_KEY`: Your IAM User's secret key.
- `AWS_REGION`: The AWS region (e.g., `us-east-1`).
- `BUCKET_NAME`: The exact name of your created S3 bucket.

### 3. Repository Permissions
Ensure that your GitHub Actions have permission to write to the repository. 
Go to **Settings > Actions > General > Workflow permissions** and select **Read and write permissions**.

## Usage

1. Place a new image (supported formats: `.jpg`, `.jpeg`, `.png`) inside the `photos/` directory.
2. Commit and push the new image to the `main` branch.
   ```bash
   git add photos/your_image.jpg
   git commit -m "Add new photo for analysis"
   git push origin main
   ```
3. Navigate to the **Actions** tab in your GitHub repository to watch the workflow run.
4. Once completed, a new commit will automatically appear in your repository with the updated `result.json` file containing the analysis data.