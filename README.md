# Glorified Scribe

Glorified Scribe is a Python-based application that uses AI to automatically transcribe speech and generate intelligent meeting notes. It combines real-time speech recognition using OpenAI's Whisper models with natural language processing via the OpenAI API (using the gpt-3.5-turbo model) to provide comprehensive meeting documentation.

## Getting Started

To use this tool, you'll need to have Python installed on your system. The application uses several Python libraries including OpenAI's Whisper for speech recognition and the OpenAI API for intelligent text processing.

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (required for AI-powered features)
- Microphone (for live transcription)

### Installation

1. Clone or download this repository
2. Install the required packages:
```bash
pip install -r requirements.txt --upgrade
```

3. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Important:** An OpenAI API key is required for AI-powered meeting notes generation. You can obtain an API key <a href="https://openai.com/blog/openai-api">here</a>.

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
- **Natural Language Processing**: OpenAI GPT-3.5-turbo for intelligent text processing
- **Audio Processing**: SpeechRecognition library with configurable microphone settings

### Supported Platforms
- macOS (including Apple Silicon)
- Linux (with microphone device selection)
- Windows

### Dependencies
- `openai`: OpenAI API integration
- `whisper`: Speech recognition models
- `torch`: Deep learning framework
- `transformers`: NLP model support
- `SpeechRecognition`: Audio input handling
- `sounddevice`: Audio device management
- `numpy`, `scipy`, `pydub`: Audio processing

## License
Please see the <a href="LICENSE">LICENSE</a> file for details on how you can use and distribute this software.