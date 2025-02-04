from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/define", methods=["POST"])
def define():
    
    data = request.get_json()
    word = data.get("word")
    sentence = data.get("sentence")
    lang="español"
    if word and sentence:
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",

            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Explain the meaning of the word '{word}' in '{sentence}' in {lang}, be concise, explain the root of the word and the particles (if any)"
                }
            ]
        )
        print(completion.choices[0].message.content)
        return jsonify({"definition": completion.choices[0].message.content}), 200
    else:
        return jsonify({"error": "Faltan parámetros: 'word' y 'sentence'"}), 400

if __name__ == "__main__":
    app.run()