# module for the Huggingface Transformers model setup
from transformers import pipeline
import torch
import re
import os
import platform
import json
import unicodedata
from dotenv import load_dotenv
from litellm import completion

class nlp(object):

    # OpenAI API Settings
    isOpenAI_API = False                            # controls if the OpenAI API is used vs. local Huggingface models
    generative_model = os.getenv("GENERATIVE_MODEL", "gpt-3.5-turbo")
    max_number_of_retries = int(os.getenv("MAX_NUMBER_OF_RETRIES", "3"))
    openai_model_token_limit = int(os.getenv("OPENAI_MODEL_TOKEN_LIMIT", "950"))

    # OpenAI classification settings
    classifier_command_text = "" 
    cleaning_command_text = ""

    summerization_command_text = ""

    # Common cleaning settings
    cleaning_token_limit = int(os.getenv("CLEANING_TOKEN_LIMIT", str(openai_model_token_limit)))         # smaller chunks work better

    # Common Summerization settings
    summerization_token_limit = int(os.getenv("SUMMERIZATION_TOKEN_LIMIT", str(openai_model_token_limit)))    # this is the max size text chunk you can pass to the model
    summerization_input_min = int(os.getenv("SUMMERIZATION_INPUT_MIN", "150"))                           # minimum number of words for a summary
    summerization_response_max = int(os.getenv("SUMMERIZATION_RESPONSE_MAX", "1500"))                       # limit to under this number of words
    summerization_response_min = int(os.getenv("SUMMERIZATION_RESPONSE_MIN", "100"))                        # minimum number of words for the summary

    # GPU settings
    is_gpu_available = False                        # controls if GPU is available
    device = torch.device("cpu")                    # default device to use (cpu or cuda)
    
    # local classification settings
    classification_pipeline = "zero-shot-classification"
    classification_model = "sileod/deberta-v3-base-tasksource-nli"
    classifier = None

    # local Summerization settings
    summerization_pipeline = "summarization"
    summerization_model = "facebook/bart-large-cnn"
    summerizer = None

    def __init__(self, openAI=False):
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Load prompts from files
        self.load_prompts()
        
        # Let's handle some GPU initalization
        if(self.is_macos_arm64()):
            self.device = torch.device("mps")
            self.is_gpu_available = True
            print("MPS GPU ENABLED")


        # setup API key
        if(openAI == True):
            self.isOpenAI_API = True
        else:
            # set the classifier to be a zero-shot model and use the default pipeline
            self.classifier = pipeline(self.classification_pipeline, model=self.classification_model, device=self.device)

            # setup summarization model
            self.summerizer = pipeline(self.summerization_pipeline, model=self.summerization_model, device=self.device)
    
    def load_prompts(self):
        """Load all prompts from the prompts folder"""
        prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
        
        # Load classifier command
        with open(os.path.join(prompts_dir, 'classifier_command.txt'), 'r') as f:
            self.classifier_command_text = f.read().strip()
        
        # Load cleaning command
        with open(os.path.join(prompts_dir, 'cleaning_command.txt'), 'r') as f:
            self.cleaning_command_text = f.read().strip()
        
        # Load summerization command
        with open(os.path.join(prompts_dir, 'summerization_command.txt'), 'r') as f:
            self.summerization_command_text = f.read().strip()
    
    def get_prompt(self, prompt_name):
        """Get a specific prompt by name"""
        prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
        prompt_file = os.path.join(prompts_dir, f'{prompt_name}.txt')
        
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r') as f:
                return f.read().strip()
        return None

    def setup(self):
        # used during container configuration and setup
        
        # setup the classifier to be a zero-shot model and use the default pipeline (model download)
        self.classifier = pipeline( self.classification_pipeline, model=self.classification_model)
        # setup summarization model (model download)
        self.summerizer = pipeline(self.summerization_pipeline, model=self.summerization_model)

    def is_macos_arm64(self):
        system = platform.system()
        processor = platform.processor()

        return system == "Darwin" and processor == "arm"

    def submit_openai_request(self, messages, is_json=False):
        # wrapper to handle errors and retries for the OpenAI API using liteLLM
        attempts = 0
        success = False
        response = None  # Initializing with a default value
        while not success and attempts <= self.max_number_of_retries:
            attempts += 1
            try:
                print("Submitting API Request (Attempt #" + str(attempts) + ")")
                response = completion(model=self.generative_model, messages=messages)['choices'][0]['message']['content']
                success = True
            except Exception as e:
                print("OPENAI CONNECTION ERROR:", str(e))
                # Handle the error appropriately
        
        # attempt to JSON decode it
        if is_json:
            try:
                response = json.loads(response)
            except:
                print("JSON DECODE ERROR: ",response)
        
        print("OpenAI Response:", response)
        return response
    
    def num_words(self, text):
        # Remove leading and trailing whitespaces
        text = str(text).strip()
        
        # Split the text into words based on whitespaces
        words = text.split()
        
        # Return the count of words
        return len(words)
    
    def get_chunks(self, chunk_size, text, command_text):
        # Create an empty list to store the text chunks
        chunks = []

        # Split the text into sentences based on periods followed by a space or carriage returns
        sentences = re.split(r'\. |\n', text)

        # Iterate over the sentences
        current_chunk = ''
        for sentence in sentences:
            # Check if adding the current sentence exceeds the chunk size
            if self.num_words(current_chunk) + self.num_words(sentence) + self.num_words(command_text) > chunk_size:
                # If adding the current sentence exceeds the chunk size,
                # append the current chunk to the list of chunks and start a new chunk
                chunks.append(current_chunk)
                current_chunk = sentence
            else:
                # If adding the current sentence doesn't exceed the chunk size,
                # add it to the current chunk
                if current_chunk:
                    current_chunk += '. ' + sentence if current_chunk[-1] != '\n' else sentence
                else:
                    current_chunk = sentence

        # Append the last chunk to the list of chunks
        if current_chunk:
            chunks.append(current_chunk)

        # Return the list of text chunks
        return chunks

    def preprocess_text(self, text):
        # Normalize Unicode characters
        text = unicodedata.normalize("NFKD", text)

        # Remove non-ASCII characters
        text = text.encode("ascii", "ignore").decode("utf-8")

        # Remove special characters and symbols
        text = re.sub(r"[^\w\s]", "", text)

        # Remove multiple spaces and replace with a single space
        text = re.sub(r"\s+", " ", text)

        # Remove leading and trailing spaces
        text = text.strip()

        return text

    def remove_extra_spaces(self, text):
        return ' '.join(text.split())

    def fix_rogue_spaces(self, text):
        return text.replace(" .", ".")
    
    def contains_multiple_spaces(self, s):
        return bool(re.search(r' {3,}', s))
    
    def sort_classifications(self, output_from_model):
        # sort the dictionary by value
        print(output_from_model)
        
        return dict(sorted(output_from_model.items(), key=lambda item: -item[1]))

    def get_top_label(self, output_from_model):
        # accept the output from the NLP model and format it for the end user

        # print out to console for debugging
        # print(output_from_model['labels'], output_from_model['scores'])

        return output_from_model['labels'][0]

    def classification(self, sequence_to_classify, filter_labels):
        sequence_to_classify = self.preprocess_text(sequence_to_classify)
        if(self.isOpenAI_API == True):
            # submit the request to the OpenAI API
            return self.openai_classification(sequence_to_classify, filter_labels)
        else:
            # Classify the text using multiple sets of labels. 
            return self.classifier(sequence_to_classify, filter_labels)

    def summerization(self, text):
        # summerize the text using either a local model or the OpenAI API
        text = self.preprocess_text(text)
        if(self.isOpenAI_API == True):
            # submit the request to the OpenAI API
            summerization_results = self.openai_simple_summerization(text)
        else:
            if(len(text) >= self.summerization_token_limit):
                summerization_results = self.summerizer(text[0:self.summerization_token_limit])[0]['summary_text'] 
            else:
                summerization_results = self.summerizer(text)[0]['summary_text']

        return self.fix_rogue_spaces(summerization_results)

    def openai_cleaning(self, sequence_to_clean):
        # simple process to clean up text that has been scrapped from web pages and/or PDF files.
        results = ""
        # if text is larger than the max input, split it into chunks and submit each chunk individually
        if(self.num_words(sequence_to_clean) > self.cleaning_token_limit):
            chunks = self.get_chunks(self.openai_model_token_limit, sequence_to_clean, self.cleaning_command_text)
        else:
            chunks = [sequence_to_clean]
        
        setup_command = {
            'role': 'system',
            'content': f'{self.cleaning_command_text}'
        }
        for chunk in chunks:
            request = {
                'role': 'user',
                'content': f'Process the following text:{chunk}'
            }        
            response = self.submit_openai_request([setup_command, request])
            response += ' '
            results += response
        
        return results
    
    def openai_classification(self, sequence_to_classify, filter_labels):

        # Classify the text using multiple sets of labels. 
        setup_command = {
            'role': 'system',
            'content': f'{self.classifier_command_text}'
        }
        request = {
            'role': 'user',
            'content': f'Classify the following text into these categories ({filter_labels}) {sequence_to_classify}, sorting by score.'

        }
        return self.submit_openai_request([setup_command, request])

    def openai_simple_summerization(self, text):
        # Now let's summerize the text using liteLLM

        text = self.fix_rogue_spaces(text)

        if(len(text) >= self.summerization_token_limit): 
            request =   {
                'role': 'system', 
                'content': f'Summarize the following text in under {self.summerization_response_max} words and no less than {self.summerization_response_min} words: {text[0:self.summerization_token_limit - 1]}'
                }
        else:
            request = {
                'role': 'system', 
                'content': f'Summarize the following text in under {self.summerization_response_max} words and no less than {self.summerization_response_min} words: {text}'
                }

        results = completion(model=self.generative_model, messages=[request])
        summary_results = results['choices'][0]['message']['content']

        return summary_results
    
    def openai_summerization(self, text):
        # Now let's summerize the text

        text = self.fix_rogue_spaces(text)

        setup_command = {
            'role': 'system', 
            'content': f'{self.summerization_command_text}'
            }
        
        request = {
            'role': 'user', 
            'content': f'Summarize the following text : {text}'
            }

        return self.submit_openai_request([setup_command, request])