import os
import struct
import wave
import numpy as np
import whisper
from pvrecorder import PvRecorder
from pydub import AudioSegment


def rms(samples):
    return np.sqrt(np.mean(np.square(samples)))


def listen(config={}):
    recorder = PvRecorder(device_index=-1, frame_length=512, log_silence=False)
    audio = []
    threshold = 100
    frame_duration_ms = 50
    silent_frames = 0
    try:
        recorder.start()
        while True:
            frame = recorder.read()
            audio.extend(frame)
            audio_samples = np.array(frame, dtype=np.int16)
            audio_rms = rms(audio_samples)
            num_silent_frames = int(
                config["whisper"]["silence_duration"] * (1000 / frame_duration_ms)
            )
            if audio_rms < threshold:
                silent_frames += 1
            else:
                silent_frames = 0

            if silent_frames >= num_silent_frames:
                print("thinking ...")
                recorder.stop()
                with wave.open(config["recording"], "w") as f:
                    f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                    f.writeframes(struct.pack("h" * len(audio), *audio))
                break

    except KeyboardInterrupt:
        recorder.stop()
        with wave.open(config["recording"], "w") as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()


def voice_to_text(config={}):
    print("Cadbury: I am listening:")
    listen(config)
    # Load the audio file
    audio_file = AudioSegment.from_file(config["recording"])

    # Check if the entire audio file is silent
    if audio_file.dBFS <= -50:
        return "SILENT"

    # Load whisper model and make it dynamic
    model = whisper.load_model(config["whisper"]["model"])
    # load the audio file
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(config["recording"])
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    try:
        os.remove(config["recording"])
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")
    return result.text
