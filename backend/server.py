import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eleves.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback_secret_key")  # Secure in production!

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define database models
class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Route: Home (for testing)
@app.route("/")
def home():
    return jsonify({"message": "Server is running!"})

# Route: Get all students (Admin only)
@app.route('/eleves', methods=['GET'])
@jwt_required()
def get_eleves():
    eleves = Eleve.query.all()
    return jsonify([{"nom": e.nom, "points": e.points} for e in eleves])

# Route: Add or remove points (Admin only)
@app.route('/ajouter_points', methods=['POST'])
@jwt_required()
def ajouter_points():
    data = request.json
    eleve = Eleve.query.filter_by(nom=data.get("nom")).first()

    if not eleve:
        return jsonify({"message": "Élève non trouvé"}), 404

    try:
        points_ajoutes = int(data.get("points", 0))

        # Allow negative points for removal
        eleve.points += points_ajoutes
        db.session.commit()

        return jsonify({
            "message": "Points mis à jour avec succès",
            "total_points": eleve.points
        }), 200

    except ValueError:
        return jsonify({"message": "Valeur de points invalide"}), 400

# Route: Admin login (returns JWT token)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    admin = Admin.query.filter_by(username=data.get("username")).first()

    if admin and bcrypt.check_password_hash(admin.password_hash, data.get("password")):
        token = create_access_token(identity=admin.username)
        return jsonify({"access_token": token}), 200

    return jsonify({"message": "Identifiants incorrects"}), 401

# Route: Register an admin (One-time setup)
@app.route('/register_admin', methods=['POST'])
def register_admin():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    if Admin.query.filter_by(username=data.get("username")).first():
        return jsonify({"message": "Admin déjà existant"}), 400

    new_admin = Admin(username=data.get("username"), password_hash=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin créé avec succès"}), 201

# Get the correct port from Render environment (default to 5000)
PORT = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
