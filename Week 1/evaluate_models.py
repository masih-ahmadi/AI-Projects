import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import requests
import pandas as pd

# Load your dataset (adjust the file path as necessary)
data = pd.read_csv('data/youtoxic_english_1000.csv',error_bad_lines=False)
texts = data['Text'].tolist()       
labels = data['IsToxic'].tolist()   

# BERT Model Evaluation
def evaluate_bert_model(texts, labels):
    tokenizer = AutoTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")  
    model = AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain")

    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=1).numpy()

    accuracy = accuracy_score(labels, predictions)
    # Update the averaging method to 'macro', 'micro', or 'weighted'
    precision = precision_score(labels, predictions, average='macro')
    recall = recall_score(labels, predictions, average='macro')
    f1 = f1_score(labels, predictions, average='macro')

    print(f"BERT Model - Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1:.2f}")
    return accuracy, precision, recall, f1

# LLM Model Evaluation via FastChat API
def evaluate_llm_model(texts, labels):
    def get_llm_prediction(text):
        url = "https://llm-api.aieng.fim.uni-passau.de/v1/chat/completions"
        headers = {
            "Authorization": "Bearer group5_s1b4b",  # Replace with actual API key
            "Content-Type": "application/json"
        }
        data = {
            "model": "Mixtral-8x7B-Instruct-v0.1",   # Replace with actual model ID/name
            "messages": [{"role": "user", "content": f"is the text is toxic if yes replay yes it is toxic: {text}"}]
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        # Process the response to determine if it is toxic (1) or non-toxic (0)
        return 1 if "toxic" in result['choices'][0]['message']['content'].lower() else 0

    predictions = [get_llm_prediction(text) for text in texts]

    accuracy = accuracy_score(labels, predictions)
    # Update the averaging method to 'macro', 'micro', or 'weighted'
    precision = precision_score(labels, predictions, average='macro')
    recall = recall_score(labels, predictions, average='macro')
    f1 = f1_score(labels, predictions, average='macro')

    print(f"LLM Model - Accuracy: {accuracy:.2f}, Precision: {precision:.2f}, Recall: {recall:.2f}, F1-Score: {f1:.2f}")
    return accuracy, precision, recall, f1

# Evaluate both models
print("Evaluating BERT Model...")
bert_metrics = evaluate_bert_model(texts, labels)

print("\nEvaluating LLM Model...")
llm_metrics = evaluate_llm_model(texts, labels)

# Optionally, save the results to a file
with open('evaluation_results.txt', 'w') as f:
    f.write("BERT Model Metrics:\n")
    f.write(f"Accuracy: {bert_metrics[0]:.2f}\nPrecision: {bert_metrics[1]:.2f}\nRecall: {bert_metrics[2]:.2f}\nF1-Score: {bert_metrics[3]:.2f}\n")
    f.write("\nLLM Model Metrics:\n")
    f.write(f"Accuracy: {llm_metrics[0]:.2f}\nPrecision: {llm_metrics[1]:.2f}\nRecall: {llm_metrics[2]:.2f}\nF1-Score: {llm_metrics[3]:.2f}\n")