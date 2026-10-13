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
| `POST /summarize-audio` | audio | transcript + summary |
| `POST /caption/batch` | several images | list of captions |
| `GET /health` | - | status |

## Stack

FastAPI, Whisper for transcription, a small vision-language model for captions, pytest, GitHub Actions for CI.

Run tests: `pytest`

First request is slow while models load. A GPU helps but isn't required for small models.

MIT
