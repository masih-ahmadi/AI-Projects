import requests
import json

#  API URL and API Key
API_BASE_URL = 'https://llm-api.aieng.fim.uni-passau.de/v1'
API_URL_ENDPOINT = '/chat/completions'
API_TOKEN = 'group5_s1b4b'
ROLE = 'system'
MODEL = 'Mixtral-8x7B-Instruct-v0.1'


def parse_result(response):
    
    try:
        dict_response = json.loads(response)
    except ValueError as err:
        return 'NOT VALID API RESPONSE'
    print(response)
    if not 'text' in dict_response:
        return 'NOT VALID API RESPONSE'
    else:
        return dict_response['text']
    


def get_story_prompt(name, friend, topic, **kwargs):

    setting = 'fantasy/magic'
    age = '8-12'
    length = 500

    if 'setting' in kwargs:
        setting = kwargs['setting']
    if 'age' in kwargs:
        age = kwargs['age']
    if 'length' in kwargs:
        length = kwargs['length']

    prompt = f'''[Story Prompt]
        Main Character: A child named {name}, and their friend named {friend}.
        Theme/Topic: The story should focus on {topic}.
        Setting: The story takes place in {setting}.
    [Story Requirements]
        Age Group: Suitable for children aged {str(age)}.
        Themes: Include themes of friendship, problem-solving, and imagination.
        Structure: The story should have a clear bintroduction, adventures and resolution structure, while being single complete text.
        Tone: Completely avoid using violent or undesirable language and aim at having a good moral message.
        Length: {str(length)} words (+- 100 words)
    [Character Development]
        Character Traits: Define traits for {name} and {friend} to make them relatable (e.g., brave, curious, kind).
        
        ''' + '''Your response should be provided as one json string in the following format: {\'text\':%text of the story%, \'message\':%moral or message of the story%}'''
    
    return prompt


def run_prompt(prompt):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': MODEL,      
        'messages': [
            {'role': ROLE, 'content': prompt},
            
        ]
    }

    response = requests.post(API_BASE_URL+API_URL_ENDPOINT, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip(), 0
    else:
        return response.text, response.status_code
