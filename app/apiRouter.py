from fastapi import APIRouter
import torch 

router = APIRouter()

@router.get("/")
async def home():
    return {"Message": "This is the start of an amazing project", "cudaisavailable":torch.cuda.is_available()}

@router.get("/pred")
async def predict():
    return {"Message": "you are querying something from the backend"}