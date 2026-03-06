# Voice Agent Arena

A Python-based benchmarking and evaluation system for AI text-to-speech (TTS) models. Creates a controlled A/B testing environment where different voice agents compete across predefined business scenarios to assess performance, clarity, and suitability.

## What It Does

Users paste or type text, select a scenario (customer service, banking, etc.), and the system generates audio from two different TTS models simultaneously. The outputs are randomly assigned to "Agent A" and "Agent B" so the user can listen and compare without knowing which model is which. This removes bias from evaluation.

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | Python + FastAPI |
| Frontend | Static HTML / CSS / JavaScript |
| TTS Engine 1 | Google Cloud Text-to-Speech API |
| TTS Engine 2 | Coqui TTS (locally hosted) |
| Audio Storage | Local file system (`generated_audio/`) |
| Server | Uvicorn |

## How to Run Locally

### Prerequisites

- Python 3.8+
- Google Cloud service account credentials (for Google TTS)
- Coqui TTS installed locally

### Setup

```bash
# Clone the repo
git clone https://github.com/tiffanyelangwa/voice-agent-arena-backend
cd voice-agent-arena-backend/Backend

# Install dependencies
pip install -r requirements.txt

# Add your Google Cloud credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account.json"

# Run the server
uvicorn main:app --reload
```

Open your browser at [http://localhost:8000](http://localhost:8000)

## API

### POST /generate

Accepts text input and returns audio file paths for both agents.

**Request:**
```json
{
  "text": "Hello, how can I help you today?"
}
```

**Response:**
```json
{
  "agent_a": "/audio/23f8a92a-voiceA.wav",
  "agent_b": "/audio/84d12bc3-voiceB.wav",
  "mapping": { "agent_a": "google", "agent_b": "coqui" }
}
```

The `mapping` field is revealed after the user votes, not before, to keep evaluation unbiased.

## Project Structure

```
Backend/
  main.py              # FastAPI app, routes, CORS config
  tts_google.py        # Google Cloud TTS integration
  tts_coqui.py         # Coqui local model integration
  models.py            # Pydantic request/response schemas
  generated_audio/     # UUID-named audio output files
index.html             # Frontend UI
```

## Evaluation Scenarios

- Customer Service
- Banking
- Support
- Custom user-defined scenarios

## Key Engineering Decisions

- **Randomized A/B assignment** at runtime so users cannot guess which model they are evaluating
- **UUID filenames** (`uuid.uuid4()`) for collision-safe audio storage
- **Modular TTS abstraction** so new models can be added without changing endpoint logic
- **FastAPI StaticFiles** for serving audio directly over HTTP
