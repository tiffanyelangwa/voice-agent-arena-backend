# Backend/main.py
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import texttospeech
from TTS.api import TTS  # Local TTS engine
import uuid
from pathlib import Path
from random import shuffle, choice

# --- App setup ---
app = FastAPI()

BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# --- Models ---
class PromptRequest(BaseModel):
    text: str

# --- Google TTS client ---
google_client = texttospeech.TextToSpeechClient()

# Google voices to randomly pick from
GOOGLE_VOICES = [
    {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL},
    {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE},
    {"language_code": "en-US", "ssml_gender": texttospeech.SsmlVoiceGender.MALE},
]

def generate_with_google(text: str) -> str:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = choice(GOOGLE_VOICES)
    voice = texttospeech.VoiceSelectionParams(**voice_params)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = google_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    filename = f"{uuid.uuid4().hex}.mp3"
    output_path = AUDIO_DIR / filename
    with open(output_path, "wb") as out:
        out.write(response.audio_content)

    return filename

# --- Coqui TTS setup ---
COQUI_MODELS = [
    "tts_models/en/ljspeech/tacotron2-DDC",
    "tts_models/en/vctk/vits"
]

# Pre-initialize TTS engines
coqui_engines = [TTS(model_name=m) for m in COQUI_MODELS]

def generate_with_local(text: str) -> str:
    engine = choice(coqui_engines)
    filename = f"{uuid.uuid4().hex}.mp3"
    output_path = AUDIO_DIR / filename
    engine.tts_to_file(text=text, file_path=output_path)
    return filename

# --- Agent registry for randomization ---
AGENTS = {
    "google": generate_with_google,
    "coqui": generate_with_local
}

# --- Routes ---
@app.get("/")
def health_check():
    return {"status": "backend is running"}

@app.post("/generate")
def generate_audio(prompt: PromptRequest):
    # Randomize A/B assignment
    agent_items = list(AGENTS.items())
    shuffle(agent_items)
    (agent_a_name, agent_a_fn), (agent_b_name, agent_b_fn) = agent_items

    file_a = agent_a_fn(prompt.text)
    file_b = agent_b_fn(prompt.text)

    return {
        "voice_a": {"audio_url": f"/audio/{file_a}"},
        "voice_b": {"audio_url": f"/audio/{file_b}"}
    }
