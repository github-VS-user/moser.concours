from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eleves.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modèle Eleve
class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)

# Modèle Admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Création des tables
with app.app_context():
    db.create_all()

# Route pour récupérer la liste des élèves
@app.route('/eleves', methods=['GET'])
def get_eleves():
    eleves = Eleve.query.all()
    return jsonify([{"nom": e.nom, "points": e.points} for e in eleves])

# Route pour ajouter des points
@app.route('/ajouter_points', methods=['POST'])
@jwt_required()
def ajouter_points():
    data = request.json
    eleve = Eleve.query.filter_by(nom=data["nom"]).first()
    
    if eleve:
        try:
            points_ajoutes = int(data["points"])
            if points_ajoutes < 0:
                return jsonify({"message": "Les points ne peuvent pas être négatifs"}), 400
            
            eleve.points += points_ajoutes
            db.session.commit()
            return jsonify({"message": "Points ajoutés avec succès"}), 200
        except ValueError:
            return jsonify({"message": "Valeur de points invalide"}), 400
    return jsonify({"message": "Élève non trouvé"}), 404

# Route pour l’authentification admin
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    admin = Admin.query.filter_by(username=data["username"]).first()
    
    if admin and bcrypt.check_password_hash(admin.password_hash, data["password"]):
        token = create_access_token(identity=admin.username)
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Identifiants incorrects"}), 401

if __name__ == '__main__':
    app.run(debug=True)
