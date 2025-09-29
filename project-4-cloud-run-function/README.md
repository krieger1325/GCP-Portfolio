# Project 4: Cloud Run Function for Event Processing

## Overview

Use case: Customer uploads color image, system converts to grayscale  

-Demonstrates serverless skills  
-Shows ability to integrate GCP services (Cloud Run Functions, Cloud Storage, Pub/Sub)  
-Event-driven architecture  

---

## Step-by-step Implementation

-Step 1: Set up GCS buckets  
-(Input, Output, Quarantine buckets)  
-Step 2: Create Pub/Sub topic  
-Step 3: Create Service Account  
-(Cloud Functions Invoker, Storage Object Admin, Pub/Sub Publisher)  
-Step 4: Create Cloud Run Function  
-(Trigger: Cloud Storage - Event Type: storage.objects.create)  
-(Set Environment Variables)  
-Step 5: Add Code (See main.py and requirements.txt in this folder for code)  
-Step 6: Deploy  
-Step 7: Test

