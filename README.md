# MLTD
MLTD (Machine Learning Threat Detection)

MLTD is a threat detection API used for detecting any cyber threats in log files. It uses machine learning to find any threats from user-provided log files. Users can upload their log files using a frontend web interface, the command line, or scripts. Then the threat detection API will use machine learning to analyze the log files to determine wether or not a threat exists.


## Setup

### Requirements
- Docker
- Docker Compose

Clone the repository, and run the API with docker compose.
```
git clone https://github.com/IU-Capstone-Project-2025/MLTD
docker compose up --build -d
```

