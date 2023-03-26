import os
import openai
import io
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

from utils.config_utils import load_config
from utils.whisper_utils import voice_to_text

# Set up OpenAI API key and other necessary configurations
openai.api_key = os.getenv("OPENAI_API_KEY")
# Load config from file
config = load_config("./config/config.yaml")


def play_audio_response(audio_data):
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    play(audio_segment)


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
    print("cadbury: " + answer)
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
    while 1:
        # Convert voice input to text
        text_input = voice_to_text(config)
        if "SILENT" == text_input:
            continue
        if "thank you" in text_input.lower():
            break
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
