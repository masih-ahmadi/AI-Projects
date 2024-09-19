import pickle
import os
import requests
from django.shortcuts import render
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from .forms import ModuleQueryForm
from .models import Module
import json
# Load vectorized data once when the server starts
VECTOR_PATH = os.path.join(settings.BASE_DIR, 'module_vectors.pkl')
with open(VECTOR_PATH, 'rb') as f:
    X, vectorizer, modules = pickle.load(f)

def query_modules(query):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, X).flatten()
    best_idx = similarities.argmax()
    best_match = modules[best_idx]
    return best_match, similarities[best_idx]



def generate_response(module, similarity, user_query):
   
    
     # Call the LLM API
    api_url = "https://llm-api.aieng.fim.uni-passau.de/v1/chat/completions"
    api_key = "group5_s1b4b"
    headers = {
            "Authorization": f'Bearer {api_key}',
            "Content-Type": "application/json"
        }
    data = {
            "model": "Mixtral-8x7B-Instruct-v0.1",
            "messages": [{"role": "user", "content": f"here is the stored data from vectore file that returned as best much for user query your responsibility is to answer the user query based on this data here is the data: {module} and here is the query: {user_query}"}]
    }
   
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Sorry, I couldn't retrieve a detailed response at this moment."

def module_query_view(request):
    if request.method == 'POST':
        form = ModuleQueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            module, similarity = query_modules(query)
            
            # Generate a detailed response using the custom LLM API
            detailed_response = generate_response(module, similarity, query)
            
            context = {
                'form': form,
                'module': module,
                'similarity': similarity,
                'detailed_response': detailed_response,
            }
            return render(request, 'modules/query.html', context)
    else:
        form = ModuleQueryForm()
    
    return render(request, 'modules/query.html', {'form': form})
