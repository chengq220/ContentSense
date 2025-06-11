from fastapi import FastAPI

app = FastAPI()

@router.get("/")
async def hpg():
    return {"Message": "This is the start of an amazing project"}