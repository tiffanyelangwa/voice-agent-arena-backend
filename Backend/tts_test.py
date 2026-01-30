from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

# 1️⃣ What to say
synthesis_input = texttospeech.SynthesisInput(
    text="Hello Tiffany. Your backend is officially alive."
)

# 2️⃣ Which voice
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Wavenet-D"
)

# 3️⃣ Audio format
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Generate speech
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save to file
with open("test.mp3", "wb") as out:
    out.write(response.audio_content)

print("🎧 Audio file saved as test.mp3")
