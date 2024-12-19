from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(title="Steganography API", description="Encode and Decode Text in Images")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
# Mount the uploaded_images folder as static
app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")
