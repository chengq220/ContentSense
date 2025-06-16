from fastapi import APIRouter
from app.models.KoalaAIDeberta import ModerationModel
from inference import inference
from transformers import AutoTokenizer
from app.models.CNN import CNN
from utils import load
import torch 
import os
import time

router = APIRouter()
model = ModerationModel()

SAVE_DIR = os.path.join(os.getcwd(), "training/weights")
tokenizer = AutoTokenizer.from_pretrained("KoalaAI/Text-Moderation")
model = CNN(vocab_size=tokenizer.vocab_size, n_classes=9)
_ = load(path = "models/CNN_weight.pth", model = model, optimizer=None)

@router.get("/")
async def home():
    return {"Message": "This is the start of an amazing project", "cudaisavailable":torch.cuda.is_available()}

@router.post("/pred")
async def predict(payload:dict) -> dict:
    sentences = payload["content"]
    threshold = int(0.05 * len(sentences))
    
    start = time.time()
    # output = model.pred_classes(sentences)
    output = inference(sentences, model, tokenizer)
    end = time.time()
    time_taken = end - start

    numViolation = len(sentences) - output.count("OK")
    level = "Not safe" if numViolation > threshold else "Safe"
    
    return {"level": level, "violation": numViolation, "output": output, "time": time_taken }