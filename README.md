# Glorified Scribe

Glorified Scribe is a Python-based application that uses AI to automatically transcribe speech and generate intelligent meeting notes. It combines real-time speech recognition using OpenAI's Whisper models with natural language processing via the OpenAI API (using the gpt-3.5-turbo model) to provide comprehensive meeting documentation.

## Getting Started

To use this tool, you'll need to have Python installed on your system, along with some system dependencies. The application uses several Python libraries including OpenAI's Whisper for speech recognition and the OpenAI API for intelligent text processing.

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (required for AI-powered features)
- Microphone (for live transcription)
- FFmpeg (required for audio processing)
- PortAudio (required for PyAudio on macOS)

### System Dependencies Installation

#### macOS
Install required system dependencies using Homebrew:
```bash
# Install FFmpeg for audio processing
brew install ffmpeg

# Install PortAudio for PyAudio support
brew install portaudio
```

#### Linux
```bash
# Install FFmpeg and PortAudio using your package manager
# For Ubuntu/Debian:
sudo apt-get install ffmpeg portaudio19-dev

# For Fedora/CentOS:
sudo dnf install ffmpeg portaudio-devel
```

#### Windows
Download and install:
- FFmpeg: https://ffmpeg.org/download.html
- PortAudio: http://www.portaudio.com/download.html

### Installation

1. Clone or download this repository
2. Install the required Python packages:
```bash
pip install -r requirements.txt --upgrade
```

3. Set up your environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API key and configuration
# Or set the environment variable directly:
export OPENAI_API_KEY="your-api-key-here"
```

**Important:** An OpenAI API key is required for AI-powered meeting notes generation. You can obtain an API key <a href="https://openai.com/blog/openai-api">here</a>.

### Environment Configuration

The application uses a `.env` file for configuration. Copy `.env.example` to `.env` and configure:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
GENERATIVE_MODEL=gpt-3.5-turbo

# API Settings
MAX_NUMBER_OF_RETRIES=3
OPENAI_MODEL_TOKEN_LIMIT=950

# Processing Settings
CLEANING_TOKEN_LIMIT=950
SUMMERIZATION_TOKEN_LIMIT=950
SUMMERIZATION_INPUT_MIN=150
SUMMERIZATION_RESPONSE_MAX=1500
SUMMERIZATION_RESPONSE_MIN=100
```

## Usage

The `takenotes.py` script can be run in two modes: live transcription or file processing.

### Live Transcription Mode (Default)

For real-time speech transcription during meetings:

```bash
python takenotes.py
```

### File Processing Mode

To process existing transcript files with AI-powered cleaning and summarization:

```bash
python takenotes.py --file myfile.txt
```

### Command Line Options

- `--model`: Whisper model to use. Choices: "tiny", "base", "small", "medium", "large". Default: "medium"
- `--file`: Path to a transcript file to process (bypasses live transcription)
- `--teams`: Optimize processing for Microsoft Teams transcript format
- `--non_english`: Use non-English Whisper models
- `--energy_threshold`: Microphone sensitivity level (default: 1000)
- `--record_timeout`: Real-time recording sensitivity in seconds (default: 2.0)
- `--phrase_timeout`: Silence duration before new transcription line (default: 3.0)
- `--default_microphone`: (Linux only) Specify microphone device name

### Example Usage

```bash
# Live transcription with large model and higher sensitivity
python takenotes.py --model large --energy_threshold 500

# Process a Microsoft Teams transcript
python takenotes.py --file teams_meeting.txt --teams

# Process a non-English transcript
python takenotes.py --file meeting_es.txt --non_english
```

## Features

### Live Transcription
- Real-time speech-to-text using OpenAI's Whisper models
- Automatic phrase detection and segmentation
- Configurable sensitivity and timing parameters
- Support for multiple Whisper model sizes (tiny to large)

### AI-Powered Processing
When processing files (or transcripts with sufficient content), the application generates:

1. **Cleaned Transcript**: Removes artifacts, formats names properly, and converts to formal meeting notes style
2. **Intelligent Summary**: Includes:
   - Up to 10 key meeting highlights (bulleted)
   - Action items with assigned responsibilities
   - Attendee introductions with full names and titles
   - Humorous "Meeting Score" (1-100) evaluating meeting effectiveness

### Microsoft Teams Support
Special handling for Teams transcripts with:
- Name format normalization ("Last, First (org)" → "First Last")
- Duplicate name removal
- Attendee list generation

### Output Files
The application generates timestamped files:
- `transcript-{timestamp}-{uuid}.txt`: Raw transcription
- `cleaned-{timestamp}-{uuid}.txt`: AI-cleaned transcript
- `summary-{timestamp}-{uuid}.txt`: Comprehensive meeting summary

## Technical Details

### Architecture
- **Speech Recognition**: OpenAI Whisper models with GPU acceleration support (including Apple Silicon MPS)
- **Natural Language Processing**: OpenAI GPT-3.5-turbo for intelligent text processing via liteLLM
- **Audio Processing**: SpeechRecognition library with configurable microphone settings
- **Configuration Management**: Environment-based configuration using python-dotenv
- **Modular Prompts**: Externalized prompt templates in `prompts/` directory

### Supported Platforms
- macOS (including Apple Silicon)
- Linux (with microphone device selection)
- Windows

### Project Structure
```
glorified_scribe/
├── takenotes.py              # Main application script
├── module_nlp.py             # NLP processing module
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── prompts/                 # LLM prompt templates
│   ├── cleaning_prompt_default.txt
│   ├── cleaning_prompt_teams.txt
│   ├── summerization_prompt_default.txt
│   ├── summerization_prompt_teams.txt
│   ├── classifier_command.txt
│   ├── cleaning_command.txt
│   └── summerization_command.txt
└── README.md                # This file
```

### Architecture Changes

The application has been recently updated with the following improvements:

1. **Modular Prompts**: All LLM prompts are now stored in separate files in the `prompts/` directory for easier customization
2. **Environment Configuration**: Uses `.env` file for all configuration variables
3. **Unified LLM Interface**: Now uses `litellm` for better LLM provider flexibility
4. **Improved Error Handling**: Better retry logic and error management

### Dependencies

#### Python Packages
- `openai`: OpenAI API integration
- `openai-whisper`: Speech recognition models
- `litellm`: Unified LLM API interface
- `python-dotenv`: Environment variable management
- `torch`: Deep learning framework
- `transformers`: NLP model support
- `SpeechRecognition`: Audio input handling
- `sounddevice`: Audio device management
- `pyaudio`: Audio recording support
- `numpy`, `scipy`, `pydub`: Audio processing

#### System Dependencies
- **FFmpeg**: Required for audio processing by Whisper
- **PortAudio**: Required for PyAudio audio recording
- **Python 3.7+**: Base Python runtime

### Architecture Changes

The application has been recently updated with the following improvements:

1. **Modular Prompts**: All LLM prompts are now stored in separate files in the `prompts/` directory for easier customization
2. **Environment Configuration**: Uses `.env` file for all configuration variables
3. **Unified LLM Interface**: Now uses `litellm` for better LLM provider flexibility
4. **Improved Error Handling**: Better retry logic and error management

## License
Please see the <a href="LICENSE">LICENSE</a> file for details on how you can use and distribute this software.