FROM python:3.13
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "fastapi", "run", "main.py", "--host", "0.0.0.0" ]
EXPOSE 8080


