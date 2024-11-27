from pydantic import BaseModel

class SteganographyInput(BaseModel):
   text: str
   image_path: str
   file_name: str

class EncodeResponse(BaseModel):
   imagePath: str

class DecodeResponse(BaseModel):
   decodedText: str