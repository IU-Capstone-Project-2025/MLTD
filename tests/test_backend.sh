#!/bin/bash

# Checkes for any missing directories
echo "[1/] Checking if backend directories exist."
if [! -d "./backend" ]
then
    echo "Backend directory does not exist."
    exit 1

elif [! -d "./backend/ML" ]
then
    echo "ML directory does not exist."
    exit 1
fi

cd ./backend

# Installs dependencies
echo "[2/] Installing dependencies."
python -m pip install --upgrade pip && python -m pip install -r ./requirements.txt
if [[ $? != 0 ]]
then
    echo "Failed to install dependencies."
    exit 1
fi

# Run development build
echo "Running development build."
fastapi dev ./main.py &
sleep 10

if [[ $(pgrep python | wc -l) == 0 ]]
then
    echo "Failed to run development build."
    exit 1
fi

