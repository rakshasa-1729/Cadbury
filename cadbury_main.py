import os
import openai
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
import io
import numpy as np
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

# Set up OpenAI API key and other necessary configurations
openai.api_key = os.getenv("OPENAI_API_KEY")


def play_audio_response(audio_data):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    play(audio_segment)


def voice_to_text(filename="audio.wav", seconds=10):
    RATE = 16000
    CHANNELS = 1
    FORMAT = np.int16

    print(f"Recording for {seconds} seconds...")

    recorded_audio = sd.rec(
        int(seconds * RATE), samplerate=RATE, channels=CHANNELS, dtype=FORMAT
    )
    sd.wait()  # Wait until the recording is finished

    print("Recording finished")

    wav_write(filename, RATE, recorded_audio)
    with open(file=filename, mode="rb") as audiofile:
        response = openai.Audio.transcribe("whisper-1", file=audiofile, stream=True)
        text = response["text"]
    return text


def ask_gpt4(question):
    messages = [{"role": "user", "content": question}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )
    answer = response.choices[0]["message"]["content"].strip()
    print(answer)
    return answer


def synthesize_text(
    text, language_code="en-GB", voice_name="en-GB-Wavenet-B", output_format="mp3"
):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content


def main():
    # Convert voice input to text
    text_input = voice_to_text()

    # Get GPT-4's response
    gpt4_response = ask_gpt4(text_input)

    # Convert GPT-4's response to speech using the specified voice parameters
    audio_response = synthesize_text(gpt4_response)

    # Play the generated audio response or save it as a file
    play_audio_response(
        audio_response
    )  # Replace this with the actual function to play the audio


if __name__ == "__main__":
    main()
