from flask import Flask, jsonify
import json

app = Flask(__name__)

def charger_donnees():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/eleves', methods=['GET'])
def get_eleves():
    return jsonify(charger_donnees())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
