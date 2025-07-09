import os
from fastapi import FastAPI, File, UploadFile, status
from fastapi.requests import *
from fastapi.responses import *
from fastapi.middleware.cors import CORSMiddleware

from ML.HDFS.hdfs_parser import parse_file as parse_hdfs
from ML.HDFS.hdfs_model import analyze as analyze_hdfs
from ML.BGL.bgl_parser import parse_file as parse_bgl
from ML.BGL.bgl_model import analyze as analyze_bgl
from ML.MAC.mac_parser import parse_file as parse_mac
from ML.MAC.mac_model import analyze as analyze_mac

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["*"])

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

    return Response(status_code=status.HTTP_200_OK)

@app.get("/health")
async def get_health():
    # Health check logic will be implemented later
    return JSONResponse({"status", "healthy"}, status_code=status.HTTP_200_OK)

@app.get("/version")
async def get_version():
    return JSONResponse({"version": "0.1"}, status_code=status.HTTP_200_OK)

@app.get("/analyze/{file}")
async def detect_threats(file: str, format: str):
    if not os.path.isfile(f"logs/{file}"):
        return Response(f"'{file}' not found", status_code=status.HTTP_404_NOT_FOUND)

    elif file is None:
        return Response(f"'{file}' is empty", status_code=status.HTTP_400_BAD_REQUEST)

    if format.upper() == "HDFS":
        parse_hdfs(file)
        result = analyze_hdfs(file.replace(".log", ".csv"),29)
        return JSONResponse({"probability": result}, status_code=status.HTTP_200_OK)

    elif format.upper() == "BGL":
        parse_bgl(file)
        result = analyze_bgl(file.replace(".log", ".csv"))
        return JSONResponse({"probability": result}, status_code=status.HTTP_200_OK)

    elif format.upper() == "MAC":
        parse_mac(file)
        result = analyze_mac(file.replace(".log", ".csv"))
        return JSONResponse({"probability": result}, status_code=status.HTTP_200_OK)

    return Response(f"\"{format}\" is not a supported log format", status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/results/{id}")
async def get_result(result_id: int):
    return Response("Result retrival is not yet implemented", status_code=status.HTTP_501_NOT_IMPLEMENTED)

@app.get("/batch-detect")
async def batch_detection():
    return Response("Batch processing is not yet implemented", status_code=status.HTTP_501_NOT_IMPLEMENTED)