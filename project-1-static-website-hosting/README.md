# Week 2 Project: Static Website Hosting with Google Cloud Load Balancer

## Overview
-This project demonstrates how to host a static website on Google Cloud Storage
and serve it securely over HTTPS using a Google Cloud HTTPS Load Balancer with
a custom domain.  

## Architecture

```mermaid
flowchart LR
    A[User Browser] -->|HTTPS Request| B[Google Cloud Load Balancer]
    B -->|URL Map| C[Backend Bucket]
    C -->|Static Files| D[Google Cloud Storage]
    subgraph DNS
        E[Domain matthewkrieger.site]
    end
    E --> B 
