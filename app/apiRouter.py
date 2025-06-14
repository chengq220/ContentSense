from fastapi import APIRouter
from app.models.KoalaAIDeberta import ModerationModel
import torch 

router = APIRouter()
model = ModerationModel()

@router.get("/")
async def home():
    return {"Message": "This is the start of an amazing project", "cudaisavailable":torch.cuda.is_available()}

@router.post("/pred")
async def predict(payload:dict) -> dict:
    sentences = payload["content"]
    output = model.pred_classes(sentences)
    level = "Not safe"
    numViolation = len(sentences)
    return {"level": level, "violation": numViolation, "output": output }

@router.post("/query")
async def asdfa(payload):
    return {"hi": "hi"}