"""
========================================================================
  TESTS AUTOMATIQUES — ÉQUIPE DATA SCIENCE
========================================================================
AgriCoop Connect — Coopérative COMAKI, Kintélé

Lancez depuis le dossier backend :   python -m pytest -v

VERT  = votre fonction est correcte.
ROUGE = lisez le message, corrigez logic.py, relancez.

Vous n'avez pas besoin de comprendre ce fichier. Il vérifie juste que vos
fonctions renvoient les bons résultats.
========================================================================
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import logic


# ========================================================================
# ZONE A
# ========================================================================

def test_indicateurs_globaux_nb_livraisons():
    livraisons = [
        {"membre_id": 1, "culture": "Manioc", "quantite": 100},
        {"membre_id": 2, "culture": "Maïs", "quantite": 50},
    ]
    resultat = logic.calculer_indicateurs_globaux(livraisons, [], [])
    assert resultat["nb_livraisons_mois"] == 2
    assert resultat["nb_membres_actifs"] == 2


def test_indicateurs_globaux_stock_total_sans_dependre_dune_autre_fonction():
    """
    Ce test vérifie stock_total directement, sans passer par
    calculer_stock_disponible : calculer_indicateurs_globaux doit être
    autonome et ne dépendre d'aucune autre fonction de ce fichier.
    """
    livraisons = [
        {"membre_id": 1, "culture": "Manioc", "quantite": 100},
        {"membre_id": 2, "culture": "Maïs", "quantite": 50},
    ]
    ventes = [{"culture": "Manioc", "quantite": 30}]
    resultat = logic.calculer_indicateurs_globaux(livraisons, ventes, [])
    # (100 + 50) - 30 = 120
    assert resultat["stock_total"] == 120


def test_indicateurs_globaux_montant_du():
    livraisons = [{"membre_id": 1, "culture": "Manioc", "quantite": 100}]  # 100*150 = 15000
    paiements = [{"membre_id": 1, "montant": 5000}]
    resultat = logic.calculer_indicateurs_globaux(livraisons, [], paiements)
    assert resultat["montant_du_total"] == 10000


def test_livraisons_par_jour_semaine_regroupe():
    livraisons = [
        {"date": "2026-07-08", "quantite": 40},
        {"date": "2026-07-08", "quantite": 10},
        {"date": "2026-07-09", "quantite": 5},
    ]
    resultat = logic.calculer_livraisons_par_jour_semaine(livraisons)
    assert resultat["2026-07-08"] == 50
    assert resultat["2026-07-09"] == 5


def test_classer_membres_par_production():
    livraisons = [
        {"membre_id": 1, "quantite": 100},
        {"membre_id": 2, "quantite": 50},
        {"membre_id": 1, "quantite": 30},
    ]
    resultat = logic.classer_membres_par_production(livraisons)
    assert resultat[0]["membre_id"] == 1
    assert resultat[0]["volume_total"] == 130
    assert resultat[1]["membre_id"] == 2


def test_statistiques_globales():
    livraisons = [{"culture": "Manioc", "quantite": 100}]
    ventes = [{"culture": "Manioc", "quantite": 50, "prix_kg": 220}]
    resultat = logic.calculer_statistiques_globales(livraisons, ventes)
    assert resultat["Manioc"]["volume_total"] == 100
    assert resultat["Manioc"]["valeur_totale"] == 11000


def test_rapport_bailleur_pas_de_nom():
    livraisons = [{"membre_id": 1, "quantite": 100}]
    ventes = [{"quantite": 50, "prix_kg": 220}]
    paiements = [{"membre_id": 1, "montant": 5000}]
    resultat = logic.generer_indicateurs_rapport_bailleur(livraisons, ventes, paiements)
    assert "Jean" not in str(resultat) and "Mabiala" not in str(resultat)
    assert resultat["volume_total_periode"] == 100
    assert resultat["taux_regularite_paiements"] == 100


def test_rapport_bailleur_aucun_membre_actif():
    resultat = logic.generer_indicateurs_rapport_bailleur([], [], [])
    assert resultat["taux_regularite_paiements"] == 0
    assert resultat["nb_membres_actifs"] == 0


def test_top_acheteur():
    ventes = [
        {"acheteur_id": 1, "quantite": 150},
        {"acheteur_id": 2, "quantite": 60},
        {"acheteur_id": 1, "quantite": 40},
    ]
    acheteurs = [{"id": 1, "nom": "Christiane Nkaya"}, {"id": 2, "nom": "Talangaï"}]
    resultat = logic.identifier_top_acheteur(ventes, acheteurs)
    assert resultat["acheteur_nom"] == "Christiane Nkaya"
    assert resultat["volume_total"] == 190


def test_top_acheteur_liste_vide():
    resultat = logic.identifier_top_acheteur([], [])
    assert resultat["acheteur_nom"] is None
    assert resultat["volume_total"] == 0


# ========================================================================
# ZONE B
# ========================================================================

def test_solde_membre_jeu_de_donnees_standard():
    livraisons = [
        {"membre_id": 1, "culture": "Manioc", "quantite": 120},
        {"membre_id": 1, "culture": "Maïs", "quantite": 50},
        {"membre_id": 1, "culture": "Manioc", "quantite": 110},
    ]
    paiements = [{"membre_id": 1, "montant": 5000}]
    solde = logic.calculer_solde_membre(1, livraisons, paiements)
    # (120+110)*150 + 50*200 - 5000 = 34500 + 10000 - 5000 = 39500
    assert solde == 39500


def test_solde_membre_sans_livraison():
    assert logic.calculer_solde_membre(99, [], []) == 0


def test_membres_inactifs():
    membres = [{"id": 1, "nom": "A"}, {"id": 2, "nom": "B"}]
    livraisons = [{"membre_id": 1, "culture": "Manioc", "quantite": 10}]
    resultat = logic.detecter_membres_inactifs(membres, livraisons)
    assert len(resultat) == 1
    assert resultat[0]["membre_id"] == 2


def test_anomalie_livraison_invalide():
    livraison = {"membre_id": 2, "culture": "Café", "quantite": -10}
    anomalies = logic.detecter_anomalie_livraison(livraison)
    assert len(anomalies) == 2


def test_anomalie_livraison_valide():
    livraison = {"membre_id": 1, "culture": "Manioc", "quantite": 100}
    assert logic.detecter_anomalie_livraison(livraison) == []


def test_generer_recu_montant_positif():
    texte = logic.generer_recu("Jean Mabiala", 5000)
    assert "Jean Mabiala" in texte
    assert "5000" in texte


def test_generer_recu_montant_nul():
    texte = logic.generer_recu("Jean Mabiala", 0)
    assert "Aucun montant" in texte


def test_historique_paiements_membre_tri_decroissant():
    paiements = [
        {"membre_id": 1, "montant": 5000, "date": "2026-07-05"},
        {"membre_id": 2, "montant": 3000, "date": "2026-07-06"},
        {"membre_id": 1, "montant": 15000, "date": "2026-07-14"},
    ]
    resultat = logic.calculer_historique_paiements_membre(1, paiements)
    assert len(resultat) == 2
    assert resultat[0]["montant"] == 15000
    assert resultat[1]["montant"] == 5000


def test_historique_paiements_membre_aucun():
    assert logic.calculer_historique_paiements_membre(99, []) == []


def test_rechercher_membre_similaire_trouve_malgre_casse_et_espaces():
    membres = [{"id": 1, "nom": "Jean Mabiala"}, {"id": 2, "nom": "Alphonsine Nkounkou"}]
    resultat = logic.rechercher_membre_similaire("  jean   MABIALA ", membres)
    assert resultat is not None
    assert resultat["id"] == 1


def test_rechercher_membre_similaire_aucun_doublon():
    membres = [{"id": 1, "nom": "Jean Mabiala"}]
    assert logic.rechercher_membre_similaire("Marie Koumba", membres) is None


def test_valider_nouveau_membre_champs_manquants():
    donnees = {"nom": "Koumba", "prenom": "", "village": "Séo", "contact": ""}
    anomalies = logic.valider_nouveau_membre(donnees)
    assert len(anomalies) == 2
    assert any("prénom" in a for a in anomalies)
    assert any("contact" in a for a in anomalies)


def test_valider_nouveau_membre_complet():
    donnees = {"nom": "Koumba", "prenom": "Marie", "village": "Séo", "contact": "064111222"}
    assert logic.valider_nouveau_membre(donnees) == []


# ========================================================================
# ZONE C
# ========================================================================

def test_stock_disponible_toutes_cultures_presentes():
    livraisons = [{"culture": "Manioc", "quantite": 100}]
    ventes = [{"culture": "Manioc", "quantite": 30}]
    resultat = logic.calculer_stock_disponible(livraisons, ventes)
    assert resultat["Manioc"] == 70
    assert resultat["Maïs"] == 0
    assert resultat["Arachide"] == 0


def test_verifier_stock_avant_vente_insuffisant():
    stock = {"Manioc": 50}
    vente = {"culture": "Manioc", "quantite": 100}
    assert logic.verifier_stock_avant_vente(vente, stock) is False


def test_verifier_stock_avant_vente_cas_limite_exact():
    stock = {"Manioc": 50}
    vente = {"culture": "Manioc", "quantite": 50}
    assert logic.verifier_stock_avant_vente(vente, stock) is True


def test_calculer_marge_vente_positive():
    vente = {"culture": "Manioc", "quantite": 150, "prix_kg": 220}
    assert logic.calculer_marge_vente(vente) == 10500


def test_calculer_marge_vente_negative():
    vente = {"culture": "Manioc", "quantite": 100, "prix_kg": 100}
    assert logic.calculer_marge_vente(vente) == -5000


def test_verifier_paiement_valide_montant_excessif():
    paiement = {"montant": 50000}
    anomalies = logic.verifier_paiement_valide(paiement, 20000)
    assert len(anomalies) == 1
    assert "dépasse" in anomalies[0]


def test_verifier_paiement_valide_montant_negatif():
    paiement = {"montant": -100}
    anomalies = logic.verifier_paiement_valide(paiement, 20000)
    assert len(anomalies) == 1


def test_verifier_paiement_valide_montant_correct():
    paiement = {"montant": 15000}
    assert logic.verifier_paiement_valide(paiement, 20000) == []


def test_calculer_moyenne_prix_vente():
    ventes = [
        {"culture": "Manioc", "quantite": 100, "prix_kg": 200},
        {"culture": "Manioc", "quantite": 50, "prix_kg": 230},
        {"culture": "Maïs", "quantite": 60, "prix_kg": 280},
    ]
    # (100*200 + 50*230) / 150 = (20000 + 11500) / 150 = 210
    assert logic.calculer_moyenne_prix_vente(ventes, "Manioc") == 210


def test_calculer_moyenne_prix_vente_culture_absente():
    assert logic.calculer_moyenne_prix_vente([], "Arachide") == 0


# ========================================================================
# ZONE D
# ========================================================================

def test_authentifier_utilisateur_identifiants_corrects():
    utilisateurs = [
        {"nom_utilisateur": "smalonga", "mot_de_passe": "Secretaire2026",
         "role": "Secrétaire", "nom_complet": "Sandra Malonga", "membre_id": 4}
    ]
    resultat = logic.authentifier_utilisateur("smalonga", "Secretaire2026", utilisateurs)
    assert resultat is not None
    assert resultat["role"] == "Secrétaire"
    assert "mot_de_passe" not in resultat


def test_authentifier_utilisateur_mot_de_passe_incorrect():
    utilisateurs = [
        {"nom_utilisateur": "smalonga", "mot_de_passe": "Secretaire2026",
         "role": "Secrétaire", "nom_complet": "Sandra Malonga", "membre_id": 4}
    ]
    assert logic.authentifier_utilisateur("smalonga", "mauvais_mdp", utilisateurs) is None


def test_authentifier_utilisateur_inconnu():
    assert logic.authentifier_utilisateur("inconnu", "peu_importe", []) is None


def test_verifier_acces_role_autorise():
    assert logic.verifier_acces_role("Trésorière", "enregistrer_paiement") is True


def test_verifier_acces_role_refuse():
    assert logic.verifier_acces_role("Trésorière", "enregistrer_vente") is False


def test_verifier_acces_role_role_inconnu():
    assert logic.verifier_acces_role("Livreur", "tableau_de_bord") is False
