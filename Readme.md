# Tracking the Trends of Trackers

These is repositroy for the project of CSE-534. The project aims to analyse the trends of Trackers and compare the efficiencies of Trackers detections lists over the years.  

# Setup guide

Python version : 3.7
**Step 1** : Install required python libraries using following command
```
pip install -r requirements.txt
```
**Step 2** Install [chromedriver](https://chromedriver.chromium.org/downloads)
> *Note* : Version of Google Chrome and chromedriver should be the same. 

For Windows : Copy the `chromedriver.exe` file in to `C:/Windows` folder. 
For Linux : Make sure the path to chromdriver is in `/usr/lib/chromium-browser/chromedriver`

**Step 3** Install [Browsermob Proxy](https://bmp.lightbody.net/). *Note* : It is already added in the repo. 

**Step 4** Run `HAR-Capture.py` . The file takes input from `Wayback-data-top-2000.csv` which contains the URLs of Wayback Machine. 

> *Note* : As running selenium webdriver for multiple websites sometimes results in a memory leak, a Docker container can also be used to run this file. Dockerfile for the Docker build is added in the repo. Make sure you have installed `chromedriver` before running the Docker.  
To build Docker image : `docker build .`
To run Docker image : `docker run <image_id>`
 
## Structure



| Name               | Details                                                  
|----------------|-------------------------------|
|top-1m.csv|CSV file containing Alexa's top-1m websites             |            
|Wayback-crawler.py|Extract URLs from Wayback Machine API for given timstamp            |        
|Wayback-data.csv|Wayback Machine URLs for websites (2014-2021)|
|Website_Categorization.csv| Categorization of selected websites using [MacAfee trusted source](https://www.trustedsource.org/en/feedback/url)|
|HAR-Capture.py | Create HAR files from websites in `Wayback-data.csv`|
|Dockerfile| Docker Image file for running HAR-Capture inside Docker Container|
|Plots | Contains a few of the plots used in Presentation and report.|
|Trends | Yearwise Tracker lists output of trackers detected in the website|
|browsermob-proxy-2.1.4| Used for running Proxy Server|
