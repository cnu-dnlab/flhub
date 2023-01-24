from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = []


@app.get('/')
def root():
    return {'message': 'Hello World'}

