from flask import Flask, jsonify, request

app = Flask(__name__)

eleves = [
    {"nom": "Alice", "points": 50},
    {"nom": "Mme Grella", "points": 70}
]

@app.route('/eleves', methods=['GET'])
def get_eleves():
    return jsonify(eleves)

@app.route('/ajouter_points', methods=['POST'])
def ajouter_points():
    data = request.json
    for eleve in eleves:
        if eleve["nom"] == data["nom"]:
            eleve["points"] += data["points"]
    return jsonify({"message": "Points ajoutés avec succès"}), 200

if __name__ == '__main__':
    app.run(debug=True)
