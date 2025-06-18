# MLTD
MLTD (Machine Learning Threat Detection)

MLTD is a threat detection API used for detecting any cyber threats in log files. It uses machine learning to find any threats from user-provided log files. Users can upload their log files using a frontend web interface, the command line, or scripts. Then the threat detection API will use machine learning to analyze the log files to determine wether or not a threat exists.

## Setup

### Requirements
- Docker
- Docker Compose

Clone the repository:
```
git clone https://github.com/IU-Capstone-Project-2025/MLTD
```

Now you can run the API with:
```
cd MTLD
docker compose up -d
```


## How to use the API
The API will listen on localhost with port 8000, you can open a brower and visit "http://localhost:8000/".

|  Endpoint  |  HTTP Method  |  Purpose  |
|------------|---------------|-----------|
|  /health |  GET  |  Gives status of the API in JSON format.  |
|  /version  |  GET  |  Returns the version of the API in JSON format.  |
|  /upload  |  POST  | Uploads given log files to the server for examination.  |
|  /detect/{file}  |  GET  | Examines a log file for any potential threats.  |
|  /results/{id}  | GET  | Returns the results of log analyzation.  |
|  /batch-detect  | GET  | Starts examining multiple logs by batches.  |
