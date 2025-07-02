#!/bin/bash


echo "[1/4] Checking if './frontend' exists."
if [! -d "./frontend" ]
then
    echo "Directory 'frontend' does not exist."
    exit 1
fi

cd ./frontend

# Install dependencies
echo "[2/4] Installing dependencies."
npm install .
if [[ $? != 0 ]]
then
    echo "Failed to install dependencies."
    exit 1
fi

# Check for any errors
echo "[3/4] Checking for errors in the frontend code."
npm run lint
if [[ $? != 0 ]]
then
    echo "Errors found in frontend."
    exit 1
fi

# Runs development build
echo "[4/4] Running development build."
npm run dev &
sleep 10

if [[ $(pgrep npm) == 0 ]]
then
    echo "Development build failed."
    exit 1
fi
