from fastapi import FastAPI, UploadFile, File
import base64
import time

F_LAMBDA = 15.0725

def encode_bytes(data: bytes):
    signals = []
    for i, b in enumerate(data):
        signal = (b * F_LAMBDA + (i + 1)) % 1.0
        signals.append(float(f"{signal:.12f}"))
    return signals

app = FastAPI()

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
