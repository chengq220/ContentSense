from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {"Message": "This is the start of an amazing project"}

@router.get("/pred")
async def predict():
    return {"Message": "you are querying something from the backend"}