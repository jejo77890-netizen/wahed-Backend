from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import time

F_LAMBDA = 15.0725

app = FastAPI()

# ===== CORS =====
origins = [
    "https://YOUR_FRONTEND_GITHUB_PAGES_URL",  # ضع هنا رابط GitHub Pages
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Encode Function =====
def encode_bytes(data: bytes):
    signals = []
    for i, b in enumerate(data):
        signal = (b * F_LAMBDA + (i + 1)) % 1.0
        signals.append(float(f"{signal:.12f}"))
    return signals

# ===== Decode Function Placeholder =====
def decode_bytes(signals):
    return b""  # تركناها فارغة حاليا

# ===== API Endpoint =====
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()
    contents = await file.read()
    signals = encode_bytes(contents)
    recovered_bytes = decode_bytes(signals)
    encoded_file = base64.b64encode(recovered_bytes).decode('utf-8')
    
    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "signals_count": len(signals),
        "processing_time": f"{time.time() - start_time:.4f}s",
        "recovered_file": encoded_file
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
