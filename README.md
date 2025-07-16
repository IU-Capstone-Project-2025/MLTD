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

Download the BGL Model:
The model was too big to be stored on GitHub, so you will need to download the model [here](https://drive.google.com/file/d/1miVZN5arMReuDLH0e9Pjmd7SIeJEXdaM/view?usp=sharing). After it has finished downloading, extract the ZIP archive and move/copy the "saved_model" folder to "MLTD/backend/ML/BGL".

#### Run MLTD in production mode with Docker Compose:
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
The backend API will listen on port 8000 while the frontend web interface listens on port 3000.

|  Endpoint  |  HTTP Method  |  Purpose  |
|------------|---------------|-----------|
|  /version  |  GET  |  Returns the version of the API in JSON format.  |
|  /upload  |  POST  | Uploads given log files to the server for examination.  |
|  /analyze/{file}?format={log format}  |  GET  | Examines a log file for any potential threats. {log format} is the format of the log file (HDFS, BGL, MAC, etc.)  |

### Interacting with the API using the web interface
Open any web browser that you use (ex. Google Chrome, Microsoft Edge, Mozilla Firefox, etc.) and enter "http://localhost:3000/" if you are running MLTD localy on your machine. If you are running MLTD on a different machine then enter "http://[Hostname/IP Address]:3000/". Next you click on the box that saya "No file selected." and select a .txt, .log, or .csv file that contains system or network activity. Once you have selected a file, you click on "Upload" and the file will be uploaded to tbe backend API. Then you click on "Log format" to select the type of logging format that is contained in the file (BGL, HDFS, MAC, SSH). Finally after you have selected the appropriate log format, you can click on "Analyze" and wait for the results. After file analyzation has finished, you should see results containing the numbers of lines contained in the analyzed file, the number of anomalies found, and the probability that threats are present.

### Interacting with the API using a terminal/command line interface
Open any terminal (ex. Windows Terminal, PowerShell, Command Prompt, etc.) and do the following:
```
curl -X POST -F "file=@path/to/log/file" http://[Backend API IP Address]:8000/upload
curl http://[Backend API IP Address]:8000/analyze/[File name you uploaded]?format=[format of the log]
```
