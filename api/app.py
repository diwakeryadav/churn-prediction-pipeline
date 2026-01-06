from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

# Creating FastAPI app
app = FastAPI(title=' Analytics API - Minimal ')

# Applying CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.getenv('CHURN_MODEL_PATH', 'models/artifacts/churn_model.pkl')

class PredictPayload(BaseModel):
    features: list

model = None

def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/predict/churn')
def predict_churn(p: PredictPayload):
    m = load_model()
    if m is None:
        raise HTTPException(status_code=500, detail='Model not loaded')
    feats = p.features
    if not isinstance(feats, list):
        raise HTTPException(status_code=400, detail='features must be a list')
    pred = m.predict_proba([feats])[0, 1]
    return {'churn_score': float(pred)}

