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


@app.get('/models/{modelname}/localresults')
def get_localresults():
    return {}


@app.get('/models/{modelname}/globalresults')
def get_globalresults():
    return {}


@app.get('/models/{modelname}/globalresult')
def get_globalresult()
    return {}

