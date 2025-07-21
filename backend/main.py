import os
import traceback

from fastapi import FastAPI, UploadFile, status
from fastapi.requests import *
from fastapi.responses import *
from fastapi.middleware.cors import CORSMiddleware

from ML.HDFS.hdfs_parser import parse_file as parse_hdfs
from ML.HDFS.hdfs_model import analyze as analyze_hdfs
from ML.BGL.bgl_parser import parse_file as parse_bgl
from ML.BGL.bgl_model import analyze as analyze_bgl
from ML.MAC.mac_parser import parse_file as parse_mac
from ML.MAC.mac_model import analyze as analyze_mac
from ML.SSH.ssh_parser import parse_file as parse_ssh
from ML.SSH.ssh_model import analyze as analyze_ssh

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

@app.get("/")
async def load_frontend():
    return RedirectResponse(url="http://localhost:3000/")

@app.post("/upload")
async def upload_log(file: UploadFile):
    if not os.path.isdir("logs"):
        os.mkdir("./logs")
    if not file.filename.endswith((".txt",".log",".csv")):
        return Response("Invalid log file format", status_code=status.HTTP_400_BAD_REQUEST)

    if file.size <= 0:
        return Response("File is empty", status_code=status.HTTP_400_BAD_REQUEST)

    with open(f"logs/{file.filename}", "wb") as f:
        f.writelines(file.file.readlines())

    return Response(f"Successfully uploaded \"{file.filename}\"", status_code=status.HTTP_200_OK)

@app.get("/version")
async def get_version():
    return JSONResponse({"version": "1.0"}, status_code=status.HTTP_200_OK)

@app.get("/analyze/{file}")
async def detect_threats(file: str, format: str):
    if not os.path.isfile(f"logs/{file}"):
        return Response(f"'{file}' not found", status_code=status.HTTP_404_NOT_FOUND)

    elif file is None:
        return Response(f"'{file}' is empty", status_code=status.HTTP_400_BAD_REQUEST)

    match (format.upper()):
        case "BGL":
            parse_bgl(file)
            result = analyze_bgl(file.replace(".log", ".csv"))
            return JSONResponse(result, status_code=status.HTTP_200_OK)

        case "HDFS":
            parse_hdfs(file)
            result = analyze_hdfs(file.replace(".log", ".csv"), 29)
            return JSONResponse(result, status_code=status.HTTP_200_OK)

        case "MAC":
            parse_mac(file)
            result = analyze_mac(file.replace(".log", ".csv"))
            return JSONResponse(result, status_code=status.HTTP_200_OK)

        case "SSH":
            parse_ssh(file)
            result = analyze_ssh(file.replace(".log", ".csv"))
            return JSONResponse(result, status_code=status.HTTP_200_OK)

        case _:
            return Response(f"\"{format}\" is not a supported log format", status_code=status.HTTP_400_BAD_REQUEST)
