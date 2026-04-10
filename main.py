from flask import Flask, request, Response
import requests
import uuid
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Raw Image Proxy API 🚀"


@app.route('/generate-art', methods=['GET', 'POST'])
def generate_art():
    # Get prompt
    if request.method == 'GET':
        prompt = request.args.get('prompt', 'cat running')
    else:
        if request.is_json:
            prompt = request.json.get('prompt', 'cat running')
        else:
            prompt = request.form.get('prompt', 'cat running')

    url = "https://ai-api.magicstudio.com/api/ai-art-generator"

    # Dynamic values
    anonymous_user_id = str(uuid.uuid4())
    request_timestamp = str(time.time())

    boundary = "----WebKitFormBoundaryuGJAbBlkgtreHwWA"

    # Exact raw multipart body
    body = f"""------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="prompt"\r
\r
{prompt}\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="output_format"\r
\r
bytes\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="user_profile_id"\r
\r
null\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="anonymous_user_id"\r
\r
{anonymous_user_id}\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="request_timestamp"\r
\r
{request_timestamp}\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="user_is_subscribed"\r
\r
false\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA\r
Content-Disposition: form-data; name="client_id"\r
\r
pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o\r
------WebKitFormBoundaryuGJAbBlkgtreHwWA--\r
"""

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": f"multipart/form-data; boundary={boundary}",
        "origin": "https://magicstudio.com",
        "referer": "https://magicstudio.com/ai-art-generator/"
    }

    try:
        res = requests.post(
            url,
            data=body.encode("utf-8"),
            headers=headers,
            stream=True,   # IMPORTANT for raw streaming
            timeout=30
        )

        content_type = res.headers.get("content-type", "image/png")

        # 🔥 RETURN RAW IMAGE DIRECTLY
        return Response(
            res.iter_content(chunk_size=8192),
            content_type=content_type,
            status=res.status_code
        )

    except requests.exceptions.RequestException as e:
        return Response(f"Error: {str(e)}", status=500)


# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)
