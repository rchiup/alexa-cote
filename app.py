from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializar cliente OpenAI con variable de entorno
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/alexa", methods=["POST"])
def alexa():
    data = request.get_json()

    try:
        pregunta = data["request"]["intent"]["slots"]["question"]["value"]
    except:
        pregunta = "hola"

    try:
        respuesta = client.responses.create(
            model="gpt-4.1-mini",
            input=pregunta
        )

        texto = respuesta.output[0].content[0].text

    except Exception as e:
        print("ERROR:", e)
        texto = "Hubo un problema al consultar la inteligencia artificial"

    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto
            },
            "shouldEndSession": True
        }
    })

@app.route("/ping")
def ping():
    return "alive"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)