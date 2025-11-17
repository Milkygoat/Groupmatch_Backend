from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"messege": "backend fastapi is running"}