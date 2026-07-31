"""
========================================================================
  CONTROLLERS.PY  —  FICHIER PRÉ-ÉCRIT — NE PAS MODIFIER
========================================================================
C'est ici que l'API "branche" vos fonctions de logic.py. Vous n'avez rien
à toucher. Si vos fonctions dans logic.py sont correctes, ces contrôleurs
renverront automatiquement les bons résultats pour les 8 modules
d'AgriCoop Connect.
========================================================================
"""
import json
import os
import logic

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "comaki.json")

# État en mémoire (pas de base de données pour ce projet pédagogique).
# Rechargé au démarrage de l'application ; les nouvelles livraisons/ventes/
# paiements ajoutés via les formulaires sont conservés tant que le serveur
# tourne.
_DONNEES = None


def _charger_donnees():
    global _DONNEES
    if _DONNEES is None:
        with open(DATA_PATH, encoding="utf-8") as f:
            _DONNEES = json.load(f)
    return _DONNEES


# ---------- Module 1 : Tableau de bord ---------------------------------
def dashboard_controller():
    d = _charger_donnees()
    indicateurs = logic.calculer_indicateurs_globaux(d["livraisons"], d["ventes"], d["paiements"])
    livraisons_par_jour = logic.calculer_livraisons_par_jour_semaine(d["livraisons"])
    return {
        "indicateurs": indicateurs,
        "livraisons_par_jour": livraisons_par_jour,
    }


# ---------- Module 2 : Membres ------------------------------------------
def membres_controller():
    d = _charger_donnees()
    resultat = []
    for m in d["membres"]:
        solde = logic.calculer_solde_membre(m["id"], d["livraisons"], d["paiements"])
        statut = "À jour" if solde <= 0 else "En retard"
        resultat.append({
            "id": m["id"],
            "nom": m["nom"],
            "village": m.get("village"),
            "contact": m.get("contact"),
            "solde": solde,
            "statut_cotisation": statut,
        })
    inactifs = logic.detecter_membres_inactifs(d["membres"], d["livraisons"])
    return {"membres": resultat, "membres_inactifs": inactifs}


def creer_membre_controller(donnees):
    d = _charger_donnees()
    anomalies = logic.valider_nouveau_membre(donnees)
    if anomalies:
        return {"succes": False, "anomalies": anomalies}

    nom_complet = f"{donnees['prenom'].strip()} {donnees['nom'].strip()}"
    doublon = logic.rechercher_membre_similaire(nom_complet, d["membres"])
    if doublon:
        return {
            "succes": False,
            "anomalies": [f"Un membre très similaire existe déjà : {doublon['nom']}."],
            "membre_existant": doublon,
        }

    nouvel_id = max((m["id"] for m in d["membres"]), default=0) + 1
    nouveau_membre = {
        "id": nouvel_id,
        "nom": nom_complet,
        "date_adhesion": donnees.get("date_adhesion", "2026-07-17"),
        "village": donnees["village"].strip(),
        "contact": donnees["contact"].strip(),
    }
    d["membres"].append(nouveau_membre)
    return {"succes": True, "membre": nouveau_membre}


def membre_detail_controller(membre_id):
    d = _charger_donnees()
    membre = next((m for m in d["membres"] if m["id"] == membre_id), None)
    if not membre:
        return None
    solde = logic.calculer_solde_membre(membre_id, d["livraisons"], d["paiements"])
    historique_livraisons = [l for l in d["livraisons"] if l["membre_id"] == membre_id]
    historique_paiements = logic.calculer_historique_paiements_membre(membre_id, d["paiements"])
    return {
        "membre": membre,
        "solde": solde,
        "historique_livraisons": historique_livraisons,
        "historique_paiements": historique_paiements,
    }


# ---------- Module 3 : Livraisons ---------------------------------------
def livraisons_controller():
    d = _charger_donnees()
    livraisons_triees = sorted(d["livraisons"], key=lambda l: l["date"], reverse=True)
    membres_par_id = {m["id"]: m["nom"] for m in d["membres"]}
    enrichies = []
    for l in livraisons_triees:
        copie = dict(l)
        copie["membre_nom"] = membres_par_id.get(l["membre_id"], "Inconnu")
        enrichies.append(copie)
    return enrichies


def enregistrer_livraison_controller(nouvelle_livraison):
    d = _charger_donnees()
    anomalies = logic.detecter_anomalie_livraison(nouvelle_livraison)
    if anomalies:
        return {"succes": False, "anomalies": anomalies}

    nouvel_id = max((l["id"] for l in d["livraisons"]), default=0) + 1
    livraison_complete = {
        "id": nouvel_id,
        "membre_id": nouvelle_livraison["membre_id"],
        "culture": nouvelle_livraison["culture"],
        "quantite": nouvelle_livraison["quantite"],
        "date": nouvelle_livraison.get("date", "2026-07-17"),
    }
    d["livraisons"].append(livraison_complete)

    solde = logic.calculer_solde_membre(nouvelle_livraison["membre_id"], d["livraisons"], d["paiements"])
    return {"succes": True, "livraison": livraison_complete, "solde": solde}


# ---------- Module 4 : Paiements -----------------------------------------
def paiements_controller():
    d = _charger_donnees()
    membres_par_id = {m["id"]: m["nom"] for m in d["membres"]}
    paiements_tries = sorted(d["paiements"], key=lambda p: p["date"], reverse=True)
    enrichis = []
    for p in paiements_tries:
        copie = dict(p)
        copie["membre_nom"] = membres_par_id.get(p["membre_id"], "Inconnu")
        enrichis.append(copie)
    total = sum(p["montant"] for p in d["paiements"])
    return {"paiements": enrichis, "total_paiements": total}


def enregistrer_paiement_controller(nouveau_paiement):
    d = _charger_donnees()
    membre_id = nouveau_paiement["membre_id"]
    solde_du = logic.calculer_solde_membre(membre_id, d["livraisons"], d["paiements"])

    anomalies = logic.verifier_paiement_valide(nouveau_paiement, solde_du)
    if anomalies:
        return {"succes": False, "anomalies": anomalies, "solde_du": solde_du}

    nouvel_id = max((p["id"] for p in d["paiements"]), default=0) + 1
    paiement_complet = {
        "id": nouvel_id,
        "membre_id": membre_id,
        "montant": nouveau_paiement["montant"],
        "date": nouveau_paiement.get("date", "2026-07-17"),
        "mode_paiement": nouveau_paiement.get("mode_paiement", "Espèces"),
    }
    d["paiements"].append(paiement_complet)

    membre = next((m for m in d["membres"] if m["id"] == membre_id), None)
    membre_nom = membre["nom"] if membre else "Inconnu"
    recu = logic.generer_recu(membre_nom, paiement_complet["montant"])
    nouveau_solde = logic.calculer_solde_membre(membre_id, d["livraisons"], d["paiements"])

    return {"succes": True, "paiement": paiement_complet, "recu": recu, "nouveau_solde": nouveau_solde}


# ---------- Module 5 : Ventes & Stock ------------------------------------
def ventes_stock_controller():
    d = _charger_donnees()
    stock = logic.calculer_stock_disponible(d["livraisons"], d["ventes"])
    acheteurs_par_id = {a["id"]: a["nom"] for a in d["acheteurs"]}
    ventes_enrichies = []
    for v in d["ventes"]:
        copie = dict(v)
        copie["acheteur_nom"] = acheteurs_par_id.get(v["acheteur_id"], "Inconnu")
        copie["marge"] = logic.calculer_marge_vente(v)
        ventes_enrichies.append(copie)
    return {"stock_disponible": stock, "ventes": ventes_enrichies, "acheteurs": d["acheteurs"]}


def enregistrer_vente_controller(nouvelle_vente):
    d = _charger_donnees()
    stock = logic.calculer_stock_disponible(d["livraisons"], d["ventes"])
    if not logic.verifier_stock_avant_vente(nouvelle_vente, stock):
        return {"succes": False, "erreur": "Stock insuffisant pour cette vente.",
                "stock_disponible": stock}

    nouvel_id = max((v["id"] for v in d["ventes"]), default=0) + 1
    vente_complete = {
        "id": nouvel_id,
        "acheteur_id": nouvelle_vente["acheteur_id"],
        "culture": nouvelle_vente["culture"],
        "quantite": nouvelle_vente["quantite"],
        "prix_kg": nouvelle_vente["prix_kg"],
        "date": nouvelle_vente.get("date", "2026-07-17"),
    }
    d["ventes"].append(vente_complete)
    nouveau_stock = logic.calculer_stock_disponible(d["livraisons"], d["ventes"])
    return {"succes": True, "vente": vente_complete, "stock_disponible": nouveau_stock}


# ---------- Module 6 : Statistiques & Rapport bailleur --------------------
def statistiques_controller():
    d = _charger_donnees()
    classement = logic.classer_membres_par_production(d["livraisons"])
    membres_par_id = {m["id"]: m["nom"] for m in d["membres"]}
    classement_avec_noms = []
    for c in classement:
        copie = dict(c)
        copie["nom"] = membres_par_id.get(c["membre_id"], "Inconnu")
        classement_avec_noms.append(copie)

    stats_globales = logic.calculer_statistiques_globales(d["livraisons"], d["ventes"])
    top_acheteur = logic.identifier_top_acheteur(d["ventes"], d["acheteurs"])

    return {
        "classement_membres": classement_avec_noms,
        "statistiques_par_culture": stats_globales,
        "top_acheteur": top_acheteur,
    }


def rapport_bailleur_controller():
    d = _charger_donnees()
    return logic.generer_indicateurs_rapport_bailleur(d["livraisons"], d["ventes"], d["paiements"])


# ---------- Module 7 : Authentification & Comptes (NOUVEAU) --------------
def login_controller(identifiants):
    d = _charger_donnees()
    utilisateur = logic.authentifier_utilisateur(
        identifiants.get("nom_utilisateur", ""),
        identifiants.get("mot_de_passe", ""),
        d["utilisateurs"],
    )
    if utilisateur is None:
        return {"succes": False, "erreur": "Identifiant ou mot de passe incorrect."}
    return {"succes": True, "utilisateur": utilisateur}


def utilisateurs_controller():
    d = _charger_donnees()
    # On ne renvoie jamais les mots de passe, même à l'écran de gestion des comptes.
    return [
        {
            "id": u["id"],
            "nom_utilisateur": u["nom_utilisateur"],
            "role": u["role"],
            "nom_complet": u["nom_complet"],
            "membre_id": u["membre_id"],
        }
        for u in d["utilisateurs"]
    ]


def creer_utilisateur_controller(donnees):
    d = _charger_donnees()
    nom_utilisateur = donnees.get("nom_utilisateur", "").strip()
    if not nom_utilisateur or not donnees.get("mot_de_passe") or not donnees.get("role"):
        return {"succes": False, "erreur": "Nom d'utilisateur, mot de passe et rôle sont obligatoires."}

    if any(u["nom_utilisateur"] == nom_utilisateur for u in d["utilisateurs"]):
        return {"succes": False, "erreur": "Ce nom d'utilisateur existe déjà."}

    if donnees["role"] not in logic.ACTIONS_PAR_ROLE:
        return {"succes": False, "erreur": f"Rôle inconnu : {donnees['role']}."}

    nouvel_id = max((u["id"] for u in d["utilisateurs"]), default=0) + 1
    nouvel_utilisateur = {
        "id": nouvel_id,
        "nom_utilisateur": nom_utilisateur,
        "mot_de_passe": donnees["mot_de_passe"],
        "role": donnees["role"],
        "nom_complet": donnees.get("nom_complet", nom_utilisateur),
        "membre_id": donnees.get("membre_id"),
    }
    d["utilisateurs"].append(nouvel_utilisateur)
    return {
        "succes": True,
        "utilisateur": {k: v for k, v in nouvel_utilisateur.items() if k != "mot_de_passe"},
    }


def villages_controller():
    d = _charger_donnees()
    return d["villages"]


def verifier_acces_controller(role, action):
    return {"autorise": logic.verifier_acces_role(role, action)}
