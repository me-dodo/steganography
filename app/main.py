from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(title="Steganography API", description="Encode and Decode Text in Images")

app.include_router(router)
# Mount the uploaded_images folder as static
app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")
