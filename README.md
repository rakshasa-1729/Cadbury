# Cadbury - Voice Assistant using OpenAI GPT-3.5 Turbo and Google Text-to-Speech

This repository contains a Python script that demonstrates a simple voice assistant using OpenAI's GPT-3.5 Turbo model for generating textual responses to spoken questions and Google Text-to-Speech API for converting the responses to speech.

## Prerequisites

- Python 3.6 or later
- OpenAI API key
- Google Cloud Text-to-Speech API credentials
- GNU Make

## Installation

1. Clone the repository:

``` 
git clone <https://github.com/rakshasa-1729/Cadbury.git>
cd Cadbury 
```

2. Create a virtual environment and activate it:

``` make env ```


## Configuration

1. Obtain an OpenAI API key by signing up for an OpenAI account at https://beta.openai.com/signup/. Navigate to the API Keys page at https://beta.openai.com/account/api-keys and copy your API key.

2. Obtain Google Cloud Text-to-Speech API credentials by signing up for a Google Cloud account at https://cloud.google.com/free/. Create a new project or select an existing one, enable the Text-to-Speech API by following the instructions at https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#before-you-begin, and create a service account key by following the instructions at https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#set_up_a_service_account. Download the JSON key file.

3. Set up environment variables:

```
export OPENAI_API_KEY=<your-api-key>
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-your-json-key-file>
```

## Usage

Run the script with:

```
python cadbury_main.py
```


The script will prompt you to speak for a specified number of seconds, transcribe your speech to text using OpenAI's Whisper ASR API, and ask GPT-3.5 Turbo the transcribed question. It will then use Google Text-to-Speech API to convert the model's textual response to speech and play the generated audio response.

## Makefile

The Makefile provided in this repository automates common tasks for setting up and testing the project:

- `make env`: Set up the virtual environment and install the required Python packages.
- `make fmt`: Check that the code is autoformatted with Black.
- `make lint`: Run Flake8 to check for linting issues.
- `make unittest`: Run unit tests with Pytest and report coverage.
- `make test`: Run all tests, including formatting, linting, and unit testing.
- `make clean`: Remove the virtual environment.

## Contributing

Please feel free to submit issues or pull requests if you have any improvements or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
