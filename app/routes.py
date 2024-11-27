import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
from .utils import encode_text_into_image, decode_text_from_image
from .models import *
from .responses import response
from .constants import *
import io

UPLOAD_FOLDER = "uploaded_images"
router = APIRouter()

@router.post("/encode")
async def encode_text_in_image_route(
    text: str = Form(...),
    image_file: UploadFile = File(...)
):
   try:
      # Ensure the upload folder exists
      os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
      # Save the uploaded image file to UPLOAD_FOLDER
      image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
      with open(image_path, "wb") as f:
         f.write(await image_file.read())

      # Encode text into the image
      encoded_image = encode_text_into_image(image_path, text)
        
      # Save the encoded image as PNG
      encoded_image_path = os.path.join(UPLOAD_FOLDER, f"encoded_{image_file.filename}")
      encoded_image.save(encoded_image_path, format='PNG', optimize=True)

      data_result = EncodeResponse(imagePath=encoded_image_path)
      result = response(200, SUCCESS_CODE, "Successfuly Encode Image", data_result)
      return result
   except Exception as e:
      result = response(500, FAILES_CODE, "Failed Encode Image", str(e))
      return result


@router.post("/decode")
async def decode_text_from_image_route(image_file: UploadFile = File(...)):
   try:
      # Read the uploaded image file
      image = Image.open(io.BytesIO(await image_file.read()))

      # Decode text from the image
      decoded_text = decode_text_from_image(image)
        
      data_result = DecodeResponse(decodedText=decoded_text)
      result = response(200, SUCCESS_CODE, "Successfuly Decode Image", data_result)
      return result
   except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_file/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        result = response(200, SUCCESS_CODE, "Successfuly Get File", file_path)
        return result
    return response(404, FAILES_CODE, "File Not Found", "")


@router.get("/download/{filename}")
async def download_file(filename: str):
    # Construct the file path
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise response(404, FAILES_CODE, "File Not Found", "")
    
    # Return the file as a response for download
    return FileResponse(
        path=file_path,
        media_type='application/octet-stream',  # Generic file type for download
        filename=filename  # Suggested filename for download
    )

