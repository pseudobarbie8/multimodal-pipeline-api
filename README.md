# multimodal-pipeline-api

FastAPI service for image captioning and audio summarization.

```bash
docker build -t mm-api .
docker run -p 8000:8000 mm-api

curl -F "file=@cat.jpg" localhost:8000/caption
curl -F "file=@meeting.mp3" localhost:8000/summarize-audio
```

Without Docker:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

| Route | Input | Output |
|---|---|---|
| `POST /caption` | image | caption text |
| `POST /caption/batch` | several images | list of captions |
| `POST /summarize-audio` | audio | transcript + summary |
| `GET /health` | - | status |

## Stack

FastAPI, BLIP for captions, Whisper (tiny) for transcription, DistilBART for summaries, all through Hugging Face `transformers`. pytest and GitHub Actions for CI.

Tests: `pytest` (they cover routing only; models are not downloaded)

Models download on the first request to each endpoint, so that request is slow. Audio decoding needs `ffmpeg` (included in the Docker image).

MIT
