from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Steganography API", description="Encode and Decode Text in Images")

app.include_router(router)