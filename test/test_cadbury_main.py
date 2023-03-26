import unittest
from unittest.mock import MagicMock, patch

from attr import dataclass
from cadbury_main import ask_gpt4, synthesize_text


@dataclass
class Response:
    choices: dict


class TestCadbury(unittest.TestCase):
    def test_ask_gpt4(self):
        with patch("openai.ChatCompletion.create") as mock_create:
            response = Response(
                choices=[
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Paris",
                        },
                        "finish_reason": "stop",
                    }
                ]
            )
            mock_create.return_value = response

            question = "What is the capital of France?"
            expected_response = "Paris"
            actual_response = ask_gpt4(question)

            self.assertEqual(actual_response, expected_response)

    def test_synthesize_text(self):
        with patch(
            "google.cloud.texttospeech.TextToSpeechClient.synthesize_speech"
        ) as mock_synthesize_speech:
            mock_synthesize_speech.return_value = MagicMock(
                audio_content=b"Test audio content"
            )

            text = "Hello, world!"
            expected_audio_content = b"Test audio content"
            actual_audio_content = synthesize_text(text)

            self.assertEqual(actual_audio_content, expected_audio_content)


if __name__ == "__main__":
    unittest.main()
