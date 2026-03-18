from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/alexa", methods=["POST"])
def alexa():
    data = request.get_json()

    print("\n================ NUEVA REQUEST ================\n")

    # 🔥 LOG 1: TODO lo que manda Alexa
    print("RAW ALEXA JSON:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # 🔥 intento sacar pregunta desde slot
    pregunta = None

    try:
        pregunta = data["request"]["intent"]["slots"]["question"]["value"]
        print("\nSLOT QUESTION DETECTADO:", pregunta)
    except Exception as e:
        print("\nNO HAY SLOT QUESTION:", e)

    # 🔥 fallback PRO (esto es clave)
    if not pregunta:
        pregunta = data["request"].get("inputTranscript")

        if pregunta:
            print("\nUSANDO inputTranscript:", pregunta)

    # 🔥 fallback final
    if not pregunta:
        pregunta = "hola"
        print("\nFALLBACK A 'hola'")

    print("\nPREGUNTA FINAL QUE SE ENVÍA A OPENAI:", pregunta)

    # 🔥 llamada a OpenAI
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=pregunta
        )

        texto = response.output[0].content[0].text

        print("\nRESPUESTA OPENAI:")
        print(texto)

    except Exception as e:
        print("\nERROR OPENAI:", e)
        texto = "Hubo un problema al consultar la inteligencia artificial"

    print("\n================ FIN REQUEST ================\n")

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
    print("PING OK")
    return "alive"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)