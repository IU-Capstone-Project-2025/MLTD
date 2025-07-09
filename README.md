# MLTD
MLTD (Machine Learning Threat Detection)

MLTD is a threat detection API used for detecting any cyber threats in log files. It uses machine learning to find any threats from user-provided log files. Users can upload their log files using a frontend web interface, the command line, or scripts. Then the threat detection API will use machine learning to analyze the log files to determine wether or not a threat exists.

## Setup

### Requirements
To run MLTD with Docker:
- Docker
- Docker Compose

To run MLTD natively:
- Nodejs 24
- Python 3.13

Clone the repository:
```
git clone https://github.com/IU-Capstone-Project-2025/MLTD
cd MLTD
```

#### Run MLTD (in development mode) with Docker Compose:
```
docker compose up -d
```

#### Run MLTD natively:

##### Frontend:
Install dependencies:
```
cd frontend
npm install .
```

Run development build:
```
npm run dev
```

Run production build:
```
npm run build
npm start
```

##### Backend:
Install dependencies:
```
cd backend
pip install -r ./requirements.txt
```

Run development build:
```
fastapi dev ./main.py
```

Run production build:
```
fastapu run ./main.py
```

## How to use the API
The API will listen on localhost with port 8000, you can open a brower and visit "http://localhost:8000/". It will load a page that allows you to upload and analyze files for any threats. First you select a .csv, .log, or .txt file on your machine, then you click on the "Upload" button to upload it to the backend API. Once the file is uploaded to the API, you click on the "Analyze" button to analyze the file you uploaded. Finally after the API finishes analyzing the file, it will send back the results and display it on the web interface.

|  Endpoint  |  HTTP Method  |  Purpose  |
|------------|---------------|-----------|
|  /health |  GET  |  Gives status of the API in JSON format.  |
|  /version  |  GET  |  Returns the version of the API in JSON format.  |
|  /upload  |  POST  | Uploads given log files to the server for examination.  |
|  /analyze/{file}?format={log format}  |  GET  | Examines a log file for any potential threats. {log format} is the format of the log file (HDFS, BGL, MAC, etc.)  |
|  /results/{id}  | GET  | Returns the results of log analyzation.  |
|  /batch-detect  | GET  | Starts examining multiple logs by batches.  |
