# AWS Security Photo Scanner

## Project Overview

This project implements an automated, cloud-based security photo scanning pipeline. The primary task is to seamlessly analyze images—such as employee badge photos—for security auditing, specifically to detect human faces and determine the confidence level of those detections. 

By leveraging cloud infrastructure, we have created an end-to-end automated workflow that eliminates the need for manual image inspection. Whenever new image data is introduced to the system, it is automatically processed, analyzed, and the security metrics are recorded and stored for review.

## The Conceptual Flow

The high-level flow of this project is fully automated and event-driven:

1. **Triggering the Event**: The process begins when a new photo is added to the repository's designated image directory and pushed to the main branch. This action acts as the catalyst for the entire pipeline.
   
2. **Cloud Storage Integration**: Once the pipeline is triggered, the system securely uploads the newly added image to a remote cloud storage bucket (AWS S3). This acts as a staging area for our analysis tools.

3. **Intelligent Image Analysis**: After the image is securely stored in the cloud, our machine learning analysis service (AWS Rekognition) is invoked. It scans the uploaded image specifically to detect human faces and calculates a confidence score for each detected face.

4. **Automated Auditing and Logging**: The results from the image analysis—such as the total number of faces detected and their respective confidence scores—are collected and appended to a centralized audit log file.

5. **Closing the Loop**: Finally, the system takes the updated audit log and automatically commits it back to the repository. This ensures that a persistent, version-controlled record of all security scans is maintained alongside the project data.

## What We Have Achieved

In this project, we have successfully bridged version control systems with robust cloud services to build a completely autonomous security scanning application. We've eliminated manual intervention in the auditing of photos and established a reliable CI/CD workflow that handles data storage, machine learning analysis, and automated record-keeping in one smooth operation.