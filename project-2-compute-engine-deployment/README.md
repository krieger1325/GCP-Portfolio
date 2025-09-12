# Project 2: Compute Engine Deployment

## Steps to Complete Setup (All Done in GCP Console):

-Create VM in Compute Engine  
Compute Engine -> VM Instances -> Create Instance  
(Name: web-server, Region: us-central1, Machine Type: E2-Micro,  
Image: Ubuntu, Firewall: Allow HTTP, HTTPS Traffic, External IP Address: Static) -> Create  

-SSH into VM  

-Install web server  
sudo apt update  
sudo apt install -y nginx  
(Place index.html into /var/www/html, add basic text to test)  
(Test with curl localhost)  


## Architecture

```mermaid
flowchart LR
    A[User Browser] -->|HTTP Request| B[Firewall Rule: TCP:80]
    B --> C[Compute Engine VM]
    C --> D[Nginx Web Server]
    D --> E[/var/www/html/index.html]
