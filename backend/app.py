"""
========================================================================
  APP.PY  —  FICHIER PRÉ-ÉCRIT — NE PAS MODIFIER
========================================================================
Démarre l'API AgriCoop Connect. Lancez :   python app.py
Puis testez dans le navigateur :
   http://localhost:5000/api/dashboard
   http://localhost:5000/api/membres
   http://localhost:5000/api/livraisons
   http://localhost:5000/api/paiements
   http://localhost:5000/api/ventes-stock
   http://localhost:5000/api/statistiques
   http://localhost:5000/api/rapport-bailleur
   http://localhost:5000/api/utilisateurs
   http://localhost:5000/api/villages
   (POST) http://localhost:5000/api/login
========================================================================
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import controllers

app = Flask(__name__)
CORS(app)  # autorise le frontend à appeler cette API

# Empêche le débogueur interactif Werkzeug (page HTML brute) de répondre
# aux erreurs : tant que certaines fonctions de logic.py sont encore à
# `pass`, plusieurs routes lèvent une exception Python (ex. comparer
# `None <= 0`). Sans ce réglage, le navigateur reçoit une page HTML de
# débogage à la place du JSON attendu, ce qui casse le fetch() côté
# frontend de façon peu lisible pour vous. Avec ce réglage, l'erreur
# s'affiche proprement dans le terminal (traceback complet, comme avant)
# ET le navigateur reçoit un message JSON clair.
app.config["PROPAGATE_EXCEPTIONS"] = False


@app.errorhandler(Exception)
def gerer_erreur(erreur):
    import traceback
    traceback.print_exc()  # trace complète toujours visible dans le terminal
    return jsonify({
        "erreur": "Cette route a échoué car une fonction de logic.py n'est "
                   "pas encore implémentée (ou contient une erreur). "
                   "Regardez le terminal où tourne 'python app.py' pour le "
                   "détail exact (traceback Python).",
        "detail_technique": str(erreur),
    }), 500


@app.route("/")
def home():
    return {"message": "API AgriCoop Connect — Coopérative COMAKI. Voir /api/dashboard, /api/membres, "
                        "/api/livraisons, /api/paiements, /api/ventes-stock, /api/statistiques"}


# ---------- Module 1 : Tableau de bord -----------------------------------
@app.route("/api/dashboard")
def dashboard():
    return jsonify(controllers.dashboard_controller())


# ---------- Module 2 : Membres --------------------------------------------
@app.route("/api/membres", methods=["GET", "POST"])
def membres():
    if request.method == "POST":
        payload = request.get_json(force=True)
        resultat = controllers.creer_membre_controller(payload)
        code = 201 if resultat.get("succes") else 400
        return jsonify(resultat), code
    return jsonify(controllers.membres_controller())


@app.route("/api/membres/<int:membre_id>")
def membre_detail(membre_id):
    resultat = controllers.membre_detail_controller(membre_id)
    if resultat is None:
        return jsonify({"erreur": "Membre introuvable"}), 404
    return jsonify(resultat)


@app.route("/api/villages")
def villages():
    return jsonify(controllers.villages_controller())


# ---------- Module 3 : Livraisons -----------------------------------------
@app.route("/api/livraisons", methods=["GET", "POST"])
def livraisons():
    if request.method == "POST":
        payload = request.get_json(force=True)
        resultat = controllers.enregistrer_livraison_controller(payload)
        code = 201 if resultat.get("succes") else 400
        return jsonify(resultat), code
    return jsonify(controllers.livraisons_controller())


# ---------- Module 4 : Paiements ------------------------------------------
@app.route("/api/paiements", methods=["GET", "POST"])
def paiements():
    if request.method == "POST":
        payload = request.get_json(force=True)
        resultat = controllers.enregistrer_paiement_controller(payload)
        code = 201 if resultat.get("succes") else 400
        return jsonify(resultat), code
    return jsonify(controllers.paiements_controller())


# ---------- Module 5 : Ventes & Stock --------------------------------------
@app.route("/api/ventes-stock", methods=["GET", "POST"])
def ventes_stock():
    if request.method == "POST":
        payload = request.get_json(force=True)
        resultat = controllers.enregistrer_vente_controller(payload)
        code = 201 if resultat.get("succes") else 400
        return jsonify(resultat), code
    return jsonify(controllers.ventes_stock_controller())


# ---------- Module 6 : Statistiques & Rapport bailleur ----------------------
@app.route("/api/statistiques")
def statistiques():
    return jsonify(controllers.statistiques_controller())


@app.route("/api/rapport-bailleur")
def rapport_bailleur():
    return jsonify(controllers.rapport_bailleur_controller())


# ---------- Module 7 : Authentification & Comptes (NOUVEAU) ----------------
@app.route("/api/login", methods=["POST"])
def login():
    payload = request.get_json(force=True)
    resultat = controllers.login_controller(payload)
    code = 200 if resultat.get("succes") else 401
    return jsonify(resultat), code


@app.route("/api/utilisateurs", methods=["GET", "POST"])
def utilisateurs():
    if request.method == "POST":
        payload = request.get_json(force=True)
        resultat = controllers.creer_utilisateur_controller(payload)
        code = 201 if resultat.get("succes") else 400
        return jsonify(resultat), code
    return jsonify(controllers.utilisateurs_controller())


@app.route("/api/verifier-acces", methods=["POST"])
def verifier_acces():
    payload = request.get_json(force=True)
    return jsonify(controllers.verifier_acces_controller(payload.get("role"), payload.get("action")))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
