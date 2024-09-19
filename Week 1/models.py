import requests
from transformers import AutoTokenizer,AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification, GPT2Tokenizer, GPT2LMHeadModel
import torch
import json
# Load models and tokenizers
bert_tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
bert_model = AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")
REQUEST = "Provide me an answer as a json in the following format {\"toxic\": %true or false%, \"probability\":%probability%, \"type\": %type of undesirable language%, \"deescalated\": %deescalated text%} My request is to determine wheter the following text contains undesirable language, what is probability that this is a undesirable language, and what types are applicable to this undesirable language. The answer whether provided text contains undesirable language comes to the \"toxic\" key in json. Evaluate how probable that this text contains undesirable language, put this probabilty to the \"probability\" key in json. Classify the type of undesirable language and put the answers a list for the \"type\" key. Then deescalate the provided text by removing undesirable language and put the answer to the \"deescalated\" key. Example1: Text: \"Fuck you\" Resulting json: {\"toxic\":\"true\", \"probability\": 1, \"types\":[\"hate\",\"sexual\", \"harassment\"], \"deescalated\":\"I don't like you\"} ; Now provide me this json for the following text:"
# Usin gpt2 LLM 

#  API URL and API Key
API_URL = 'https://llm-api.aieng.fim.uni-passau.de/v1/chat/completions'
API_KEY = 'group5_s1b4b'

# Text classification 
def classify_text(text, model_type='llm'):
    if model_type == 'bert':
        # Use local BERT model
        inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = bert_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        flagged = torch.argmax(probs, dim=-1).item() == 1  # Assuming class 1 is 'toxic'
        return {'flagged': flagged,'probability': probs.tolist()}

    
    elif model_type == 'llm':
        # Use API
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'Mixtral-8x7B-Instruct-v0.1',      
            'messages': [
                {'role': 'user', 'content': f"{REQUEST}]: {text}"},
                
            ]
        }
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip().lower()
            d = json.loads(content)
            flagged = d['toxic']
            probability = d['probability']
            types = str(d['types'])
            deescalated = d['deescalated']
            return {'deesc': deescalated,'flagged': flagged, 'types': types,'probability': probability}
        else:
            return {'error': 'Error contacting API', 'status_code': response.status_code}

def compare_models(text):
    bert_result = classify_text(text, model_type='bert')
    llm_result = classify_text(text, model_type='llm')
    
    return {
        'bert': bert_result,
        'llm': llm_result
    }