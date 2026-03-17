from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/alexa", methods=["POST"])
def alexa():
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Cote está lista 🔥"
            },
            "shouldEndSession": True
        }
    })

@app.route("/ping")
def ping():
    return "alive"