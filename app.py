import os
import sys
import pymongo
import pandas as pd

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi import FastAPI, File, UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict(request: Request,file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor= preprocesor, model= final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)

        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        NetworkSecurityException(e, sys)


if __name__ == "__main__" :
    app_run(app, host = "0.0.0.0", port = 3000)