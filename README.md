# AWS Security Photo Scanner

## 📌 Project Overview
This project implements an automated, cloud-based security photo scanning pipeline. The primary task is to seamlessly analyze images—such as employee badge photos—for security auditing, specifically to detect human faces and determine the confidence level of those detections. 

By leveraging cloud infrastructure, we have created an end-to-end automated workflow that eliminates the need for manual image inspection. Whenever new image data is introduced to the system, it is automatically processed, analyzed, and the security metrics are recorded and stored for review.

## 🏗️ Architecture Design
The high-level flow of this project is fully automated and event-driven:

1. **Triggering the Event**: The process begins when a new photo is added to the repository's designated image directory and pushed to the main branch. This action acts as the catalyst for the entire pipeline.
2. **Cloud Storage Integration**: Once the pipeline is triggered, the system securely uploads the newly added image to a remote cloud storage bucket (AWS S3). This acts as a staging area for our analysis tools.
3. **Intelligent Image Analysis**: After the image is securely stored in the cloud, our machine learning analysis service (AWS Rekognition) is invoked. It scans the uploaded image specifically to detect human faces and calculates a confidence score for each detected face.
4. **Automated Auditing and Logging**: The results from the image analysis—such as the total number of faces detected and their respective confidence scores—are collected and appended to a centralized audit log file (`result.json`).
5. **Closing the Loop**: Finally, the system takes the updated audit log and automatically commits it back to the repository. This ensures that a persistent, version-controlled record of all security scans is maintained alongside the project data.

## 🧰 AWS Services Utilized
- **Amazon S3**: Acts as a secure, temporary staging storage area to hold the images before they are processed by the ML service.
- **Amazon Rekognition**: Utilized as the primary computer vision service to perform intelligent face detection and compute confidence scores.
- **Boto3 (AWS SDK for Python)**: Enables programmable interaction with both S3 and Rekognition from our analysis scripts.

## 🔐 Security Best Practices Implemented
- The entire process is automated, reducing the need for manual inspection of sensitive images or photos.
- We utilize environment variables for configuration (`BUCKET_NAME` and `AWS_REGION`), strictly avoiding hardcoded credentials.
- A centralized JSON audit log ensures transparency, immutability, and version control for all face detection analysis results.

## 📂 Repository Contents
- `analyze.py`: Python script used to upload photos to AWS S3 and perform face detection using AWS Rekognition.
- `README.md`: Comprehensive documentation detailing the architecture, components, and workflow of the project.
- `employee.jpg`: A sample image located in the root directory.
- `photos/`: A directory storing additional photo inputs and test images for the pipeline.

## 🚀 Verification & Testing
Whenever new photos are added to the repository, the automated pipeline kicks off. The images below represent inputs and test screenshots used in the verification process:

![Employee Photo](employee.jpg)
![Employee Scan 1](photos/employee.jpg)
![Scan Screenshot 1](photos/screenshot_1.jpg)
![Scan Screenshot 2](photos/screenshot_2.jpg)