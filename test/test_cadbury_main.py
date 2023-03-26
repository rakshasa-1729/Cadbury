import unittest
from unittest.mock import MagicMock, patch
from cadbury_main import ask_gpt4, synthesize_text

class TestCadbury(unittest.TestCase):
    def test_ask_gpt4(self):
        with patch("openai.ChatCompletion.create") as mock_create:
            mock_create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="Test response"))]
            )

            question = "What is the capital of France?"
            expected_response = "Test response"
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
