from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = []


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.get('/models')
def get_models():
    return {}


@app.get('/models/{modelname}')
def get_model():
    return {}


@app.post('/models/{modelname}')
def post_model():
    return {}


@app.post('/models/{modelname}/localresult')
def post_localresult():
    return {}


@app.post('/models/{modelname}/globalresult')
def post_globalresult():
    return {}

