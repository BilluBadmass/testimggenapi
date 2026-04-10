from flask import Flask, request, Response
import requests
import uuid
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "MagicStudio Raw Proxy API 🚀"


@app.route('/generate-art', methods=['GET', 'POST'])
def generate_art():
    # Get prompt
    if request.method == 'GET':
        prompt = request.args.get('prompt', 'cat running in water')
    else:
        if request.is_json:
            prompt = request.json.get('prompt', 'cat running in water')
        else:
            prompt = request.form.get('prompt', 'cat running in water')

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    # Dynamic values (like curl)
    anonymous_user_id = str(uuid.uuid4())
    request_timestamp = str(time.time())

    boundary = "----WebKitFormBoundary50KgHY9XGtva90hY"

    # EXACT RAW BODY (matches curl)
    body = (
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"prompt\"\r\n\r\n"
        f"{prompt}\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"output_format\"\r\n\r\n"
        f"bytes\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"user_profile_id\"\r\n\r\n"
        f"null\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"anonymous_user_id\"\r\n\r\n"
        f"{anonymous_user_id}\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"request_timestamp\"\r\n\r\n"
        f"{request_timestamp}\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"user_is_subscribed\"\r\n\r\n"
        f"false\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY\r\n"
        f"Content-Disposition: form-data; name=\"client_id\"\r\n\r\n"
        f"pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o\r\n"
        f"------WebKitFormBoundary50KgHY9XGtva90hY--\r\n"
    )

    # EXACT HEADERS (from curl)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": f"multipart/form-data; boundary={boundary}",
        "origin": "https://magicstudio.com",
        "priority": "u=1, i",
        "referer": "https://magicstudio.com/ai-art-generator/",
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    }

    try:
        res = requests.post(
            url,
            data=body.encode("utf-8"),
            headers=headers,
            stream=True,
            timeout=30
        )

        content_type = res.headers.get("content-type", "image/png")

        # ✅ RETURN RAW IMAGE (UNCHANGED)
        return Response(
            res.iter_content(chunk_size=8192),
            content_type=content_type,
            status=res.status_code
        )

    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=500)


# Required for Vercel
def handler(environ, start_response):
    return app(environ, start_response)
