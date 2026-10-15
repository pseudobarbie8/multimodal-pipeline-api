import os
import tempfile
from functools import lru_cache
from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from PIL import Image

app = FastAPI(title="multimodal-pipeline-api")


# Models load on first use so the app starts fast and /health works without them.
@lru_cache
def captioner():
    from transformers import pipeline
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


@lru_cache
def transcriber():
    from transformers import pipeline
    return pipeline("automatic-speech-recognition", model="openai/whisper-tiny")


@lru_cache
def summarizer():
    from transformers import pipeline
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


async def _caption(file: UploadFile) -> str:
    img = Image.open(BytesIO(await file.read())).convert("RGB")
    return captioner()(img)[0]["generated_text"]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/caption")
async def caption(file: UploadFile = File(...)):
    return {"caption": await _caption(file)}


@app.post("/caption/batch")
async def caption_batch(files: list[UploadFile] = File(...)):
    return {"captions": [{"filename": f.filename, "caption": await _caption(f)} for f in files]}


@app.post("/summarize-audio")
async def summarize_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        text = transcriber()(tmp.name, chunk_length_s=30)["text"].strip()
    if len(text.split()) < 40:  # too short to summarize
        return {"transcript": text, "summary": text}
    summary = summarizer()(text, max_length=120, min_length=20, truncation=True)[0]["summary_text"]
    return {"transcript": text, "summary": summary}
