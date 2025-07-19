from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app  = FastAPI(
  title= "Proxy proof attendance system",
  description="Backend for attendance using QR + Bluetooth + Face Recognition",
  version="1.0.0"
)
origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials = True, allow_methods =["*"], allow_headers = ["*"])


