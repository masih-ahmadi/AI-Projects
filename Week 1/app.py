from flask import Flask, request, jsonify, send_from_directory
from flasgger import Swagger, swag_from
from prometheus_client import start_http_server, Counter, Histogram
from models import classify_text, compare_models
from utils import deescalate_text, identify_target
from prometheus_client import generate_latest, Gauge
import psutil
import os

app = Flask(__name__)

# Initialize Swagger
swagger = Swagger(app)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
INFERENCE_TIME = Histogram('inference_time', 'Time taken for inference')

# Health check endpoint
@app.route('/health', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'API is healthy',
            'examples': {
                'application/json': {
                    'status': 'healthy'
                }
            }
        }
    }
})
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

memory_usage_metric = Gauge('flask_memory_usage_bytes', 'Flask Memory Usage (bytes)')

@app.route('/metrics')
def metrics():
    memory_usage = psutil.Process(os.getpid()).memory_info().rss
    memory_usage_metric.set(memory_usage)
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    

# Text classification endpoint
@app.route('/check-text', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'example': 'This is a toxic message'
                    },
                    'model': {
                        'type': 'string',
                        'enum': ['bert', 'llm'],
                        'example': 'bert'
                    }
                },
                'required': ['text']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Classification results',
            'examples': {
                'application/json': {
                    'original_text': 'This is a toxic message',
                    'flagged': True,
                    'probability': [[0.2, 0.8]],
                    'target': 'unknown',
                    'deescalated_text': 'This is a non-toxic message'
                }
            }
        },
        400: {
            'description': 'Invalid input',
            'examples': {
                'application/json': {
                    'error': 'No text provided'
                }
            }
        }
    }
})
def check_text():
    data = request.get_json()
    text = data.get('text')

    model_type = data.get('model', 'llm')  # Choose 'bert' or 'llm'
    print(model_type)

    if not text:
        return jsonify({'error': 'No text provided'}), 400
    if (model_type=='llm'):
        classification = classify_text(text, model_type)
        target = identify_target(text) if classification['flagged'] else None
        deescalated_text = classification['deesc']
        types = classification['types']

        return jsonify({
            'original_text': text,
            'flagged': classification['flagged'],
            'probability': classification['probability'],
            'target': target,
            'types': types,
            'deescalated_text': deescalated_text
        }), 200
    else:
        classification = classify_text(text, model_type)
        return jsonify({
            'original_text': text,
            'flagged': classification['flagged'],
            'probability': classification['probability']
        }), 200
# Model comparison endpoint
@app.route('/compare', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'example': 'This is a toxic message'
                    }
                },
                'required': ['text']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Model comparison results',
            'examples': {
                'application/json': {
                    'bert': {
                        'flagged': True,
                        'probability': [[0.2, 0.8]]
                    },
                    'llm': {
                        'flagged': True,
                        'probability': 0.7
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input',
            'examples': {
                'application/json': {
                    'error': 'No text provided'
                }
            }
        }
    }
})
def compare():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    comparison = compare_models(text)
    return jsonify(comparison), 200

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000)
