from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/alexa", methods=["POST"])
def alexa():
    data = request.get_json()

    print("REQUEST COMPLETO ALEXA:", data)

    # 🔥 obtener pregunta robusto
    pregunta = "hola"
    try:
        if data.get("request", {}).get("type") == "IntentRequest":
            intent = data["request"].get("intent", {})
            slots = intent.get("slots", {})

            if "question" in slots and "value" in slots["question"]:
                pregunta = slots["question"]["value"]

    except Exception as e:
        print("ERROR PARSEANDO INPUT:", e)

    print("PREGUNTA:", pregunta)

    # 🔥 llamada a OpenAI
    try:
        respuesta = client.responses.create(
            model="gpt-4.1-mini",
            input=pregunta
        )

        print("RESPUESTA OPENAI RAW:", respuesta)

        # 🔥 parsing + marca clara
        texto = "SOY CHATGPT: " + respuesta.output[0].content[0].text

        if not texto:
            texto = "no pude generar respuesta"

    except Exception as e:
        print("ERROR OPENAI:", e)
        texto = "Hubo un problema al consultar la inteligencia artificial"

    # 🔥 respuesta Alexa
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto
            },
            "shouldEndSession": False
        }
    })

@app.route("/ping")
def ping():
    return "alive"

@app.route("/")
def home():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)