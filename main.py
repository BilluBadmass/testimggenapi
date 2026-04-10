from flask import Flask, request, jsonify
import requests
import uuid
import time

app = Flask(__name__)

@app.route('/generate-art', methods=['GET', 'POST'])
def generate_art():
    # Handle GET / POST
    if request.method == 'GET':
        prompt = request.args.get('prompt', 'cat running in water')
    else:
        if request.is_json:
            prompt = request.json.get('prompt', 'cat running in water')
        else:
            prompt = request.form.get('prompt', 'cat running in water')

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    anonymous_user_id = str(uuid.uuid4())
    request_timestamp = str(time.time())

    files = {
        'prompt': (None, prompt),
        'output_format': (None, 'bytes'),
        'user_profile_id': (None, 'null'),
        'anonymous_user_id': (None, anonymous_user_id),
        'request_timestamp': (None, request_timestamp),
        'user_is_subscribed': (None, 'false'),
        'client_id': (None, 'pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o'),
    }

    headers = {
        "accept": "application/json, text/plain, */*",
    }

    response = requests.post(url, files=files, headers=headers)

    content_type = response.headers.get("content-type", "")

    if content_type.startswith("image"):
        return response.content, 200, {'Content-Type': content_type}

    try:
        return jsonify(response.json())
    except:
        return response.text


# Root route (optional)
@app.route('/')
def home():
    return "Flask API is running on Vercel 🚀"


# Required for Vercel
def handler(environ, start_response):
    return app(environ, start_response)
