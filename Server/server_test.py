from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

urls = ['https://mail.google.com/',
        'https://www.youtube.com/',
        'https://web.facebook.com/',
        "https://www.youtube.com/feed/you",
        'https://www.messenger.com/']

@app.route("/check-url", methods=["POST"])
def check_url():
    data = request.get_json()
    url_inp = data.get("url", "")
    if url_inp in urls:
        is_malicious = True
    else: is_malicious = False

    print(f"URL: {url_inp} - Malicious: {is_malicious}")

    return jsonify({
        "url": url_inp,
        "isMalicious": is_malicious,
    })

if __name__ == "__main__":
    app.run(host = '0.0.0.0' , port = 5000)