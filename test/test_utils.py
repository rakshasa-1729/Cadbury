import unittest
from unittest.mock import mock_open, patch
from utils.config_utils import load_config


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        sample_yaml = """settings:
  api_key: "your_api_key"
  language_code: "en-GB"
  voice_name: "en-GB-Wavenet-B"
"""
        expected_config = {
            "settings": {
                "api_key": "your_api_key",
                "language_code": "en-GB",
                "voice_name": "en-GB-Wavenet-B",
            }
        }

        with patch("builtins.open", mock_open(read_data=sample_yaml)):
            actual_config = load_config("config.yaml")

        self.assertEqual(actual_config, expected_config)

# great
if __name__ == "__main__":
    unittest.main()
