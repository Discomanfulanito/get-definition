from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import ast

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/define", methods=["POST"])
def define():
    
    data = request.get_json()
    word = data.get("word")
    sentence = data.get("sentence")
    lang= "english"
    if word and sentence:
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",

            messages = [
                {"role": "system", "content": 'Salida en JSON: { "c": "<código BCP 47 completo> (p.ej. ko-KR)", "d": "<explicación en MD>" }.'},
                {"role": "user", "content": f"'{sentence}'. Explica '{word}' en {lang}. Si coreano, explica partículas."}
            ]
        )
        print(completion.choices[0].message.content)
        result_str = completion.choices[0].message.content
        result_json = ast.literal_eval(result_str)
        return jsonify(result_json), 200
    else:
        return jsonify({"error": "Faltan parámetros: 'word' y 'sentence'"}), 400

if __name__ == "__main__":
    app.run()