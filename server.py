
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json

# Add netlify/functions to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'netlify', 'functions'))

from extract_memory import handler as extract_memory_handler
from generate_response import handler as generate_response_handler
from compare_personalities import handler as compare_personalities_handler
from personalities import handler as personalities_handler

app = Flask(__name__)
CORS(app)

# Mock Netlify event structure
def create_event(method='GET', body=None, path=''):
    return {
        'httpMethod': method,
        'path': path,
        'body': json.dumps(body) if body else '{}',
        'headers': {}
    }

@app.route('/.netlify/functions/personalities', methods=['GET', 'OPTIONS'])
def personalities():
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        }
    event = create_event('GET')
    result = personalities_handler(event, None)
    response_data = json.loads(result['body'])
    return jsonify(response_data), result['statusCode'], {
        'Access-Control-Allow-Origin': '*'
    }

@app.route('/.netlify/functions/extract_memory', methods=['POST', 'OPTIONS'])
def extract_memory():
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        }
    try:
        event = create_event('POST', request.json)
        result = extract_memory_handler(event, None)
        response_data = json.loads(result['body'])
        return jsonify(response_data), result['statusCode'], {
            'Access-Control-Allow-Origin': '*'
        }
    except Exception as e:
        print(f"Error in extract_memory: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500, {
            'Access-Control-Allow-Origin': '*'
        }

@app.route('/.netlify/functions/generate_response', methods=['POST', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        }
    try:
        event = create_event('POST', request.json)
        result = generate_response_handler(event, None)
        response_data = json.loads(result['body'])
        return jsonify(response_data), result['statusCode'], {
            'Access-Control-Allow-Origin': '*'
        }
    except Exception as e:
        print(f"Error in generate_response: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500, {
            'Access-Control-Allow-Origin': '*'
        }

@app.route('/.netlify/functions/compare_personalities', methods=['POST', 'OPTIONS'])
def compare_personalities():
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        }
    try:
        event = create_event('POST', request.json)
        result = compare_personalities_handler(event, None)
        response_data = json.loads(result['body'])
        return jsonify(response_data), result['statusCode'], {
            'Access-Control-Allow-Origin': '*'
        }
    except Exception as e:
        print(f"Error in compare_personalities: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500, {
            'Access-Control-Allow-Origin': '*'
        }

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("WARNING: GROQ_API_KEY not found in environment variables!")
        print("Please create a .env file with: GROQ_API_KEY=your_key_here")
    
    port = int(os.environ.get('PORT', 8888))
    print(f"Backend server starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

