from fastapi import FastAPI
from app.apiRouter import router

app = FastAPI()
app.include_router(router)
