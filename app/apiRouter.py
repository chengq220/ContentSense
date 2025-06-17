from fastapi import APIRouter
from app.models.KoalaAIDeberta import ModerationModel
from app.inference import inference
from transformers import AutoTokenizer
from app.models.CNN import CNN
from app.utils import load
from app.config import MODEL
import torch
import time

router = APIRouter()

if(MODEL == "KoalaAI"):
    model = ModerationModel()
elif(MODEL == "CNN"):
    tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")
    model = CNN(vocab_size=tokenizer.vocab_size, n_classes=9)
    _ = load(path = "app/models/CNN_weight.pth", model = model, optimizer=None)
else:
    raise Exception("Model not recognized")

@router.get("/")
async def home():
    return {"Message": "This is the start of an amazing project", "cudaisavailable":torch.cuda.is_available()}

@router.post("/pred")
async def predict(payload:dict) -> dict:
    sentences = payload["content"]
    threshold = int(0.05 * len(sentences))
    
    start = time.time()
    if(MODEL == "KoalaAI"):
        output = model.pred_classes(sentences)
    elif(MODEL == "CNN"):
        output = inference(sentences, model, tokenizer)
    else:
        raise Exception("Model not recognized")
    end = time.time()
    time_taken = end - start

    numViolation = len(sentences) - output.count("OK")
    level = "Not safe" if numViolation > threshold else "Safe"

    return {"level": level, "violation": numViolation, "output": output, "time": time_taken }