from flask import Flask, request, jsonify, Response
import requests
import uuid
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "MagicStudio Flask API running on Vercel 🚀"


@app.route('/generate-art', methods=['GET', 'POST'])
def generate_art():
    # Get prompt from GET or POST
    if request.method == 'GET':
        prompt = request.args.get('prompt', 'cat running')
    else:
        if request.is_json:
            prompt = request.json.get('prompt', 'cat running')
        else:
            prompt = request.form.get('prompt', 'cat running')

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    # Dynamic values (like browser request)
    anonymous_user_id = str(uuid.uuid4())
    request_timestamp = str(time.time())

    # Multipart form-data (NO manual boundary needed)
    files = {
        'prompt': (None, prompt),
        'output_format': (None, 'bytes'),
        'user_profile_id': (None, 'null'),
        'anonymous_user_id': (None, anonymous_user_id),
        'request_timestamp': (None, request_timestamp),
        'user_is_subscribed': (None, 'false'),
        'client_id': (None, 'pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o'),
    }

    # Headers (cleaned but equivalent)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://magicstudio.com",
        "referer": "https://magicstudio.com/ai-art-generator/"
    }

    try:
        response = requests.post(url, files=files, headers=headers, timeout=30)

        content_type = response.headers.get("content-type", "")

        # If image returned
        if content_type.startswith("image"):
            return Response(response.content, content_type=content_type)

        # If JSON/text
        try:
            return jsonify(response.json())
        except:
            return Response(response.text, content_type="text/plain")

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Request failed",
            "details": str(e)
        }), 500


# Required for Vercel serverless
def handler(environ, start_response):
    return app(environ, start_response)
