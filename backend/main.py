
from fastapi import FastAPI
from fastapi.requests import *
from fastapi.responses import *

app = FastAPI()

# NOTE: This function is temporary because it was created to satisfy the conditions for week one of the Capstone project.
# It shall either be changed or removed during project development.
@app.get("/", response_class=HTMLResponse)
def temporary_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Temporary API response page</title>
        </head>
        <body>
            <h1>IT WORKS?!??!?!</h1>
            <br>
            <p>If you are seeing this, then it means that the temporary app created for this week satisfies the conditions for week one. At least we hope it does... right?</p>
        </body>
    </html>
    """
