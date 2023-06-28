# Glorified Scribe

Glorified Scribe is a very simple Python-based application that uses AI to automatically transcribe speech and generate meeting notes. It uses a combination of speech recognition and natural language processing via the OpenAI API (using the gpt-3.5-turbo model) to achieve this.

## Getting Started

To use this tool, you'll need to have Python installed on your system. The script also uses several Python libraries, so make sure to install all dependencies using the following:

To install the required packages, you can use pip:
```bash
pip install -r requirements.txt --upgrade
```
**Please Note!** - An OpenAI API key is required to run this script if you wish to generate meeting notes! You can obtain an API key <a href="https://openai.com/blog/openai-api">here</a>.

## How to Run the `takenotes.py` Script
The takenotes.py script can be run from the command line with various options. Here is the basic usage:

This script has several options that you can specify when you run it:

- `--model`: Specifies the model to use. Choices are "tiny", "base", "small", "medium", "large". Default is "medium".
- `--file`: Specifies a file to process using the AI, without live transcription. By default, it is an empty string, meaning no file is processed.
- `--non_english`: If this flag is included, the non-English model is used.
- `--energy_threshold`: Sets the energy level for the microphone to detect. Default is 1000.
- `--record_timeout`: Sets how real-time the recording is in seconds. Default is 2 seconds.
- `--phrase_timeout`: Sets how much empty space between recordings before it is considered a new line in the transcription. Default is 3 seconds.
- `--default_microphone`: (Linux only) Specifies the default microphone name for SpeechRecognition. Default is 'pulse'.

An example of running the script with options would be:

```
python takenotes.py --model large --file myfile.txt --non_english --energy_threshold 2000
```
This would run the script using the "large" model, process the "myfile.txt" file, use the non-English model, and set the energy threshold for the microphone to 2000.

## Transcription and Summary Generation
The script automatically generates a transcription of the speech it hears and saves it as a text file. The script does not automaticlly process the transcript. If you run the script using the `--file` parameter then the selected file is processed by the AI to clean and summarize the content, and then saved as separate "cleaned" and "summary" text files.

## License
Please see the <a href="LICENSE">LICENSE</a> file for details on how you can use and distribute this software.