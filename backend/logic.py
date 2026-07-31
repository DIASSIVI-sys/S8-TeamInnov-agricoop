"""
========================================================================
  LOGIC.PY  —  À COMPLÉTER PAR L'ÉQUIPE DATA SCIENCE
========================================================================
AgriCoop Connect — Coopérative COMAKI, Kintélé

Vous n'écrivez QUE des fonctions (ce que vous savez déjà faire : boucles,
conditions, dictionnaires). Vous ne touchez à AUCUN autre fichier.

Chaque fonction reçoit des données simples (listes, dictionnaires) et doit
RENVOYER un résultat. Pas de print, pas de input, pas de requête réseau,
pas de Flask, pas de base de données. Juste : des paramètres entrent, une
valeur sort.

Le fichier est découpé en 4 zones de responsabilité. Si vous êtes 2 Data
Scientists, une répartition équilibrée est : Personne 1 = Zone A + Zone C
(11 fonctions), Personne 2 = Zone B + Zone D (9 fonctions). Si vous êtes 3 :
Personne 1 = Zone A (6), Personne 2 = Zone B (7), Personne 3 = Zone C + D (7).

  - ZONE A : Tableau de bord & Statistiques    — 6 fonctions
  - ZONE B : Membres & Livraisons              — 7 fonctions
  - ZONE C : Ventes, Stock & Paiements         — 5 fonctions
  - ZONE D : Authentification (NOUVEAU)        — 2 fonctions

Référentiels déjà définis ci-dessous, réutilisez-les :
  PRIX_ACHAT_KG, PRIX_VENTE_KG : prix par culture (mêmes valeurs que le
  jeu de données standard).
  ACTIONS_PAR_ROLE : ce que chaque rôle a le droit de faire (module
  Authentification).

Quand vos fonctions sont correctes :
  1. les tests passent au vert   (python -m pytest -v, depuis backend/)
  2. l'API démarre et renvoie les bons résultats  (python app.py)

Remplacez chaque `pass` / `# TODO` par votre code.
========================================================================
"""

PRIX_ACHAT_KG = {
    "Manioc": 150,
    "Maïs": 200,
    "Arachide": 400,
}

PRIX_VENTE_KG = {
    "Manioc": 220,
    "Maïs": 280,
    "Arachide": 500,
}

# Ce que chaque rôle a le droit de faire (module Authentification).
# Un "rôle" correspond à un type d'utilisateur connecté ; une "action" est
# une opération précise de l'application. Si l'action demandée n'apparaît
# pas dans la liste du rôle, l'accès doit être refusé .
ACTIONS_PAR_ROLE = {
    "Secrétaire": ["gerer_comptes", "gerer_membres", "tableau_de_bord", "consulter_rapport_partenaire"],
    "Président": ["enregistrer_vente", "tableau_de_bord", "generer_rapport_partenaire"],
    "Trésorière": ["enregistrer_paiement", "tableau_de_bord"],
    "Responsable dépôt": ["enregistrer_livraison", "tableau_de_bord"],
    "Membre": ["consulter_fiche_membre"],
}


# ========================================================================
# ZONE A — Tableau de bord & Statistiques
# ========================================================================

def calculer_indicateurs_globaux(livraisons, ventes, paiements):
    """
    Calcule les principaux indicateurs globaux affichés sur le tableau
    de bord à partir des livraisons, ventes et paiements.

    Paramètres :
        livraisons : liste de dict, chacun contenant au minimum
            "membre_id", "culture" et "quantite"

        ventes : liste de dict, chacun contenant au minimum
            "quantite"

        paiements : liste de dict, chacun contenant au minimum
            "montant"

    Retourne :
        un dictionnaire contenant :
            - "stock_total" : quantité restante en stock
            - "montant_du_total" : montant restant à payer aux membres
            - "nb_membres_actifs" : nombre de membres ayant effectué
              au moins une livraison
            - "nb_livraisons_mois" : nombre total de livraisons

    Exemple :
        entrée -> 2 livraisons (100 kg et 50 kg), 1 vente (40 kg),
                  1 paiement (30 000)

        sortie -> {
            "stock_total": 110,
            "montant_du_total": 120000,
            "nb_membres_actifs": 2,
            "nb_livraisons_mois": 2
        }
    """
         # TODO : à compléter
    pass


def calculer_livraisons_par_jour_semaine(livraisons):
    """
    Regroupe le volume total livré (toutes cultures) par date, pour le
    graphique en barres du tableau de bord.

    Paramètre :
        livraisons : liste de dict, chacun avec "date" (str "AAAA-MM-JJ") et "quantite" (int)

    Retourne :
        un dictionnaire {date: quantite_totale_ce_jour}, une clé par date
        distincte présente dans la liste reçue.

    Exemple :
        entrée -> [{"date": "2026-07-08", "quantite": 40}, {"date": "2026-07-08", "quantite": 10}]
        sortie -> {"2026-07-08": 50}
    """
         # TODO : à compléter
    pass


def classer_membres_par_production(livraisons):
    """
    Trie les membres par volume total livré, du plus gros producteur au
    plus petit. Utilisée à la fois par le module Membres et le module
    Statistiques (classement).

    Paramètre :
        livraisons : liste de dict. Chaque dict a les clés :
            - "membre_id" (int)
            - "quantite"  (int, en kg)
            (les autres clés éventuelles, comme "culture" ou "date",
            n'ont pas besoin d'être utilisées ici)

    Retourne :
        une liste de dictionnaires {"membre_id": int, "volume_total": int},
        triée par volume_total DÉCROISSANT. Un membre apparaît une seule
        fois, avec la somme de TOUTES ses livraisons (peu importe la
        culture).

    Exemple :
        livraisons = [
            {"membre_id": 1, "quantite": 100},
            {"membre_id": 2, "quantite": 50},
            {"membre_id": 1, "quantite": 30},
            
        ]
        -> le membre 1 a livré 100 + 30 = 130 au total
        -> le membre 2 a livré 50 au total

        sortie -> [
            {"membre_id": 1, "volume_total": 130},
            {"membre_id": 2, "volume_total": 50},
        ]
    """
         # TODO : à compléter
    pass


def calculer_statistiques_globales(livraisons, ventes):
    """
    Calcule, pour chaque culture, le volume total livré et la valeur totale
    générée par les ventes de cette culture (module 5, rendement par culture).

    Paramètres :
        livraisons : liste de dict avec :
            - "culture"  (str)
            - "quantite" (int, en kg)
        ventes : liste de dict avec :
            - "culture"  (str)
            - "quantite" (int, en kg)
            - "prix_kg"  (int, en FCFA — le prix RÉELLEMENT négocié pour
              cette vente précise, pas le prix de référence PRIX_VENTE_KG)

    Retourne :
        un dictionnaire {culture: {"volume_total": int, "valeur_totale": int}}
        - volume_total  = somme des "quantite" des LIVRAISONS de cette culture
        - valeur_totale = somme de (quantite * prix_kg) des VENTES de cette culture
        Seules les cultures présentes dans livraisons ET/OU ventes doivent
        apparaître dans le résultat (pas besoin de générer les 3 cultures
        du référentiel si l'une d'elles n'a aucune donnée).

    Exemple :
        livraisons = [{"culture": "Manioc", "quantite": 100}]
        ventes     = [{"culture": "Manioc", "quantite": 50, "prix_kg": 220}]

        volume_total (Manioc)  = 100
        valeur_totale (Manioc) = 50 * 220 = 11000

        sortie -> {"Manioc": {"volume_total": 100, "valeur_totale": 11000}}
    """
         # TODO : à compléter
    pass


def generer_indicateurs_rapport_bailleur(livraisons, ventes, paiements):
    """
    Calcule les indicateurs utilisés dans le rapport bailleur (module 5),
    destiné à être transmis à un partenaire financier.

    RÈGLE DE CONFIDENTIALITÉ IMPORTANTE (issue du FRD) :
    cette fonction NE DOIT JAMAIS retourner de donnée nominative (aucun
    nom de membre, aucun membre_id dans le résultat). Seulement des
    chiffres agrégés.

    Paramètres :
        livraisons : liste de dict avec "membre_id" (int), "quantite" (int)
        ventes     : liste de dict avec "quantite" (int), "prix_kg" (int)
        paiements  : liste de dict avec "membre_id" (int), "montant" (int)

    Retourne un dictionnaire avec EXACTEMENT ces 4 clés :
        {
            "volume_total_periode": int,      # somme des "quantite" de livraisons
            "montant_ventes_periode": int,    # somme de (quantite * prix_kg) des ventes
            "taux_regularite_paiements": int, # pourcentage 0-100, voir calcul ci-dessous
            "nb_membres_actifs": int,         # nombre de membre_id DISTINCTS dans livraisons
        }

    Calcul de taux_regularite_paiements :
        (nombre de membres actifs ayant reçu AU MOINS un paiement
         / nombre de membres actifs total) * 100, arrondi à l'entier.
        Si nb_membres_actifs == 0, retournez 0 (pour éviter une division par zéro).

    Exemple :
        livraisons = [{"membre_id": 1, "quantite": 100}, {"membre_id": 2, "quantite": 50}]
        ventes     = [{"quantite": 80, "prix_kg": 220}]
        paiements  = [{"membre_id": 1, "montant": 5000}]

        volume_total_periode   = 100 + 50 = 150
        montant_ventes_periode = 80 * 220 = 17600
        nb_membres_actifs      = 2   (membre_id 1 et 2 ont livré)
        membres payés           = {1}   (seul le membre 1 a un paiement)
        taux_regularite_paiements = round(1 / 2 * 100) = 50

        sortie -> {"volume_total_periode": 150, "montant_ventes_periode": 17600,
                   "taux_regularite_paiements": 50, "nb_membres_actifs": 2}
    """
         # TODO : à compléter
    pass


def identifier_top_acheteur(ventes, acheteurs):
    """
    NOUVELLE FONCTION — identifie l'acheteur ayant acheté le plus grand
    volume total (toutes cultures confondues), pour mettre en avant le
    partenaire commercial le plus actif dans le module Statistiques.

    Paramètres :
        ventes    : liste de dict avec "acheteur_id" (int), "quantite" (int)
        acheteurs : liste de dict avec "id" (int), "nom" (str)

    Retourne :
        un dictionnaire {"acheteur_nom": str, "volume_total": int}
        représentant l'acheteur ayant le plus gros volume cumulé.
        Si la liste de ventes est vide, retourner
        {"acheteur_nom": None, "volume_total": 0}.

    Exemple :
        ventes    -> [{"acheteur_id": 1, "quantite": 150}, {"acheteur_id": 2, "quantite": 60}]
        acheteurs -> [{"id": 1, "nom": "Christiane Nkaya"}, {"id": 2, "nom": "Talangaï"}]
        sortie    -> {"acheteur_nom": "Christiane Nkaya", "volume_total": 150}
    """
         # TODO : à compléter
    pass


# ========================================================================
# ZONE B — Membres & Livraisons
# ========================================================================

def calculer_solde_membre(membre_id, livraisons, paiements):
    """
    Calcule ce qui est dû à un membre : valeur totale de ses livraisons
    (au prix d'achat de référence) moins ce qu'il a déjà reçu en paiement.
    C'est la fonction la plus utilisée du projet : elle sert au module
    Membres (statut à jour/en retard), au module Livraisons (solde affiché
    après saisie) et au module Paiements (vérifier qu'on ne verse pas trop).

    Paramètres :
        membre_id  : int — l'identifiant du membre dont on calcule le solde
        livraisons : liste de dict. Chaque dict a les clés :
            - "membre_id" (int)
            - "culture"   (str, une des clés de PRIX_ACHAT_KG)
            - "quantite"  (int, en kg)
          Ne comptez QUE les livraisons dont "membre_id" correspond au
          paramètre membre_id — ignorez celles des autres membres.
        paiements : liste de dict. Chaque dict a les clés :
            - "membre_id" (int)
            - "montant"   (int, en FCFA)
          Même logique : ne comptez que les paiements de ce membre.

    Retourne :
        solde (int, en FCFA) = valeur totale de SES livraisons
                                (quantite * PRIX_ACHAT_KG[culture], sommé)
                                moins somme de SES paiements déjà reçus.
        Peut être 0 si le membre n'a rien livré, ou négatif si (cas
        théorique) il a été payé plus que ce qu'il a livré.

    Exemple (correspond au cas déjà vérifié lors du kickoff du projet) :
        membre_id  = 1
        livraisons = [
            {"membre_id": 1, "culture": "Manioc", "quantite": 120},
            {"membre_id": 1, "culture": "Maïs",   "quantite": 50},
            {"membre_id": 2, "culture": "Manioc", "quantite": 999},  # ignorée : autre membre
        ]
        paiements = [{"membre_id": 1, "montant": 5000}]

        valeur des livraisons du membre 1 = 120*150 + 50*200 = 18000 + 10000 = 28000
        solde = 28000 - 5000 = 23000

        sortie -> 23000
    """
         # TODO : à compléter
    pass


def detecter_membres_inactifs(membres, livraisons, jours_seuil=90):
    """
    Identifie les membres n'ayant fait aucune livraison (version
    simplifiée : présence/absence dans la liste reçue, pas de calcul de
    date réelle — c'est une évolution possible hors périmètre Must).

    Paramètres :
        membres : liste de dict. Chaque dict a les clés :
            - "id"  (int)
            - "nom" (str)
        livraisons : liste de dict, chacun avec au moins "membre_id" (int)
        jours_seuil : non utilisé dans cette version simplifiée (paramètre
            gardé pour compatibilité avec une évolution future à date réelle)

    Retourne :
        une liste de dict {"membre_id": int, "nom": str} — un élément par
        membre dont l'"id" n'apparaît dans AUCUNE livraison de la liste reçue.

    Exemple :
        membres    = [{"id": 1, "nom": "Jean Mabiala"}, {"id": 2, "nom": "Sandra Malonga"}]
        livraisons = [{"membre_id": 1, "culture": "Manioc", "quantite": 50}]

        -> le membre id=1 a livré, donc il n'est PAS inactif
        -> le membre id=2 n'apparaît dans aucune livraison, donc il EST inactif

        sortie -> [{"membre_id": 2, "nom": "Sandra Malonga"}]
    """
         # TODO : à compléter
    pass


def detecter_anomalie_livraison(livraison):
    """
    Vérifie qu'une livraison respecte les règles métier de base avant
    d'être enregistrée (règle métier BA, FRD module Livraisons).

    Paramètre :
        livraison : dict avec les clés "membre_id", "culture", "quantite"
            (potentiellement invalides — c'est justement ce qu'on vérifie)

    Retourne :
        une liste de chaînes de caractères décrivant chaque anomalie
        détectée (liste VIDE si tout est correct — vérifiez bien qu'une
        livraison valide donne [] et pas None).

    Règles à vérifier (une livraison peut cumuler plusieurs anomalies) :
        - "quantite" doit être un nombre strictement positif
          sinon ajouter : "Quantité invalide : doit être strictement positive."
        - "culture" doit être une clé connue de PRIX_ACHAT_KG
          sinon ajouter : "Culture inconnue : {culture}."
        - "membre_id" ne doit pas être vide/None/0
          sinon ajouter : "Aucun membre rattaché à cette livraison."

    Exemple 1 (livraison invalide, deux anomalies à la fois) :
        livraison = {"membre_id": 2, "culture": "Café", "quantite": -10}
        sortie -> ["Quantité invalide : doit être strictement positive.",
                   "Culture inconnue : Café."]

    Exemple 2 (livraison valide) :
        livraison = {"membre_id": 1, "culture": "Manioc", "quantite": 100}
        sortie -> []
    """
    anomalies = []
         # TODO : à compléter
    pass


def generer_recu(membre_nom, montant):
    """
    Formate un texte de reçu simple pour un paiement effectué.

    Paramètres :
        membre_nom : str — le nom complet du membre, ex. "Jean Mabiala"
        montant    : int — le montant versé, en FCFA

    Retourne (une chaîne de caractères, EXACTEMENT ce format) :
        - si montant <= 0 : "Aucun montant à verser pour {membre_nom}."
        - sinon            : "Reçu - {membre_nom} : paiement de {montant} FCFA effectué."

    Exemples :
        generer_recu("Jean Mabiala", 5000)
          -> "Reçu - Jean Mabiala : paiement de 5000 FCFA effectué."
        generer_recu("Jean Mabiala", 0)
          -> "Aucun montant à verser pour Jean Mabiala."
    """
         # TODO : à compléter
    pass


def calculer_historique_paiements_membre(membre_id, paiements):
    """
    NOUVELLE FONCTION — extrait l'historique des paiements d'un membre
    précis, pour la nouvelle page Paiements (fiche membre).

    Paramètres :
        membre_id : int
        paiements : liste de dict avec "membre_id" (int), "montant" (int), "date" (str)

    Retourne :
        une liste de dict (uniquement les paiements de ce membre),
        triée par date DÉCROISSANTE (le plus récent en premier).

    Exemple :
        paiements -> [{"membre_id": 1, "montant": 5000, "date": "2026-07-05"},
                      {"membre_id": 2, "montant": 3000, "date": "2026-07-06"},
                      {"membre_id": 1, "montant": 15000, "date": "2026-07-14"}]
        membre_id -> 1
        sortie    -> [{"membre_id": 1, "montant": 15000, "date": "2026-07-14"},
                      {"membre_id": 1, "montant": 5000, "date": "2026-07-05"}]
    """
         # TODO : à compléter
    pass


def rechercher_membre_similaire(nom_complet, membres):
    """
    NOUVELLE FONCTION — recherche tolérante de doublon (RM-7 du FRD) :
    avant de créer un nouveau membre, on vérifie qu'un membre au nom
    quasi identique n'existe pas déjà, pour éviter les doublons créés par
    une simple différence de majuscules ou d'espaces.

    Paramètres :
        nom_complet : str — le nom complet saisi dans le formulaire,
            ex. "  jean MABIALA " (avec espaces ou casse irrégulière
            possibles, comme le ferait une vraie saisie utilisateur)
        membres : liste de dict, chacun avec au moins "nom" (str)

    Retourne :
        le dictionnaire du membre existant si son "nom", une fois
        normalisé (mis en minuscules, espaces de début/fin retirés,
        espaces multiples réduits à un seul espace), correspond
        EXACTEMENT au nom_complet donné (lui aussi normalisé de la même
        façon). Retourne None si aucune correspondance.

    Indication : pour "réduire les espaces multiples à un seul", vous
    pouvez utiliser " ".join(texte.split()) — .split() sans argument
    découpe déjà sur n'importe quelle suite d'espaces et ignore les
    espaces de bord.

    Exemple :
        membres = [{"id": 1, "nom": "Jean Mabiala"}, {"id": 2, "nom": "Alphonsine Nkounkou"}]

        rechercher_membre_similaire("  jean   MABIALA ", membres)
        -> {"id": 1, "nom": "Jean Mabiala"}   (même nom une fois normalisé)

        rechercher_membre_similaire("Marie Koumba", membres)
        -> None   (aucun membre existant ne porte ce nom)
    """
         # TODO : à compléter
    pass


def valider_nouveau_membre(donnees):
    """
     — vérifie que le formulaire de création d'un
    nouveau membre est complet avant de l'enregistrer.

    Paramètre :
        donnees : dict avec les clés "nom", "prenom", "village", "contact"
            (valeurs potentiellement vides ou manquantes — c'est
            justement ce qu'on vérifie)

    Retourne :
        une liste de chaînes de caractères décrivant chaque anomalie
        détectée (liste VIDE si tout est correct).

    Règles à vérifier (un formulaire peut cumuler plusieurs anomalies) :
        - "nom" ne doit pas être vide (après avoir retiré les espaces
          de début/fin) sinon ajouter : "Le nom est obligatoire."
        - "prenom" ne doit pas être vide sinon ajouter :
          "Le prénom est obligatoire."
        - "village" ne doit pas être vide sinon ajouter :
          "Le village est obligatoire."
        - "contact" ne doit pas être vide sinon ajouter :
          "Le contact est obligatoire."

    Exemple 1 (formulaire incomplet) :
        donnees = {"nom": "Koumba", "prenom": "", "village": "Séo", "contact": ""}
        sortie -> ["Le prénom est obligatoire.", "Le contact est obligatoire."]

    Exemple 2 (formulaire valide) :
        donnees = {"nom": "Koumba", "prenom": "Marie", "village": "Séo", "contact": "064111222"}
        sortie -> []
    """
         # TODO : à compléter
    pass


# ========================================================================
# ZONE C — Ventes, Stock & Paiements
# ========================================================================

def calculer_stock_disponible(livraisons, ventes):
    """
    Calcule la quantité disponible à la vente, par culture.

    Paramètres :
        livraisons : liste de dict avec "culture" (str) et "quantite" (int)
        ventes     : liste de dict avec "culture" (str) et "quantite" (int)

    Retourne :
        un dictionnaire {culture: quantite_disponible}, avec TOUTES les
        cultures du référentiel PRIX_ACHAT_KG présentes (même à 0 — donc
        toujours exactement 3 clés dans le résultat : "Manioc", "Maïs",
        "Arachide", même si l'une d'elles n'a aucune livraison).

    Règle : stock disponible = somme des livraisons de cette culture
            moins somme des ventes de cette culture.

    Exemple :
        livraisons = [{"culture": "Manioc", "quantite": 100}]
        ventes     = [{"culture": "Manioc", "quantite": 30}]

        Manioc : 100 - 30 = 70
        Maïs et Arachide : aucune livraison ni vente -> 0

        sortie -> {"Manioc": 70, "Maïs": 0, "Arachide": 0}
    """
         # TODO : à compléter
    pass


def verifier_stock_avant_vente(vente, stock_disponible):
    """
    Vérifie qu'une vente demandée ne dépasse pas le stock réellement
    disponible avant de l'accepter.

    Paramètres :
        vente : dict avec "culture" (str) et "quantite" (int) —
            la quantité qu'on cherche à vendre
        stock_disponible : dict {culture: quantite_disponible}
            (typiquement le résultat de calculer_stock_disponible, mais
            cette fonction reçoit directement le dict — pas besoin de le
            recalculer ici)

    Retourne :
        True  si vente["quantite"] <= stock_disponible.get(vente["culture"], 0)
        False sinon

    Exemples :
        verifier_stock_avant_vente({"culture": "Manioc", "quantite": 100},
                                    {"Manioc": 50})
          -> False (100 > 50, stock insuffisant)

        verifier_stock_avant_vente({"culture": "Manioc", "quantite": 50},
                                    {"Manioc": 50})
          -> True  (cas limite : égalité exacte, la vente est acceptée)
    """
         # TODO : à compléter
    pass


def calculer_marge_vente(vente):
    """
    Calcule la marge générée par une vente :
        marge = (prix_kg - prix_achat_reference) * quantite

    Paramètre :
        vente : dict avec les clés :
            - "culture"  (str, une des clés de PRIX_ACHAT_KG)
            - "quantite" (int, en kg)
            - "prix_kg"  (int, en FCFA — le prix RÉELLEMENT négocié pour
              cette vente, pas forcément égal à PRIX_VENTE_KG)

    Retourne :
        marge (int, en FCFA). Utilisez PRIX_ACHAT_KG[vente["culture"]]
        comme prix d'achat de référence. La marge peut être négative
        (vente à perte), c'est un résultat valide, ne le bloquez pas.

    Exemple :
        vente = {"culture": "Manioc", "quantite": 150, "prix_kg": 220}
        prix d'achat de référence du Manioc (PRIX_ACHAT_KG) = 150
        marge = (220 - 150) * 150 = 70 * 150 = 10500

        sortie -> 10500
    """
         # TODO : à compléter
    pass


def verifier_paiement_valide(paiement, solde_du):
    """
    NOUVELLE FONCTION — règle métier centrale du module Paiements : un
    paiement ne peut jamais dépasser le solde réellement dû à un membre
    (on ne peut pas "trop" payer quelqu'un).

    Paramètres :
        paiement : dict avec "montant" (int)
        solde_du : int (résultat de calculer_solde_membre pour ce membre)

    Retourne :
        une liste de chaînes de caractères décrivant chaque anomalie
        détectée (liste VIDE si le paiement est valide).

    Règles à vérifier :
        - "montant" doit être strictement positif
          sinon ajouter : "Le montant doit être strictement positif."
        - "montant" ne doit pas dépasser solde_du
          sinon ajouter : "Le montant dépasse le solde dû ({solde_du} FCFA)."

    Exemple :
        paiement={"montant": 50000}, solde_du=20000
        -> ["Le montant dépasse le solde dû (20000 FCFA)."]
    """
         # TODO : à compléter
    pass


def calculer_moyenne_prix_vente(ventes, culture):
    """
    NOUVELLE FONCTION — calcule le prix de vente moyen réellement obtenu
    pour une culture donnée, pour comparer avec le prix de référence
    (utile pour négocier avec les acheteurs).

    Paramètres :
        ventes  : liste de dict avec "culture" (str), "quantite" (int), "prix_kg" (int)
        culture : str — la culture pour laquelle on veut la moyenne

    Retourne :
        la moyenne pondérée par quantité des prix de vente pour cette
        culture (int, arrondi). Si aucune vente pour cette culture,
        retourner 0.

    Indication : moyenne pondérée = somme(quantite * prix_kg) / somme(quantite)
    pour les ventes de la culture demandée uniquement (ignorez les ventes
    des autres cultures).

    Exemple :
        ventes = [
            {"culture": "Manioc", "quantite": 100, "prix_kg": 200},
            {"culture": "Manioc", "quantite": 50,  "prix_kg": 230},
            {"culture": "Maïs",   "quantite": 60,  "prix_kg": 280},  # ignorée : autre culture
        ]
        culture = "Manioc"

        somme(quantite * prix_kg) = 100*200 + 50*230 = 20000 + 11500 = 31500
        somme(quantite)           = 100 + 50 = 150
        moyenne = round(31500 / 150) = round(210.0) = 210

        sortie -> 210
    """
         # TODO : à compléter
    pass


# ========================================================================
# ZONE D — Authentification (nouveau module)
# ========================================================================

def authentifier_utilisateur(nom_utilisateur, mot_de_passe, utilisateurs):
    """
    NOUVELLE FONCTION — vérifie les identifiants saisis sur l'écran de
    connexion et retourne le profil de l'utilisateur s'ils sont corrects
    (module Authentification, section 3.1 du FRD, scénario nominal
    étapes 1 et 4).

    Paramètres :
        nom_utilisateur : str — identifiant saisi
        mot_de_passe    : str — mot de passe saisi
        utilisateurs    : liste de dict, chacun avec les clés
            "nom_utilisateur" (str), "mot_de_passe" (str), "role" (str),
            "nom_complet" (str), "membre_id" (int ou None)

    Retourne :
        - si un utilisateur de la liste a EXACTEMENT ce nom_utilisateur
          ET ce mot_de_passe : un dictionnaire avec les clés
          "nom_utilisateur", "role", "nom_complet" et "membre_id"
          — SANS la clé "mot_de_passe" (on ne renvoie jamais un mot de
          passe, même correct, dans le résultat).
        - si aucun utilisateur ne correspond : None

    Exemple :
        utilisateurs = [
            {"nom_utilisateur": "smalonga", "mot_de_passe": "Secretaire2026",
             "role": "Secrétaire", "nom_complet": "Sandra Malonga", "membre_id": 4}
        ]

        authentifier_utilisateur("smalonga", "Secretaire2026", utilisateurs)
        -> {"nom_utilisateur": "smalonga", "role": "Secrétaire",
            "nom_complet": "Sandra Malonga", "membre_id": 4}

        authentifier_utilisateur("smalonga", "mauvais_mdp", utilisateurs)
        -> None
    """
         # TODO : à compléter
    pass


def verifier_acces_role(role, action):
    """
    NOUVELLE FONCTION — vérifie qu'un rôle a le droit d'effectuer une
    action donnée (règle métier RM-6 du FRD : accès refusé si hors du
    rôle). Utilise le dictionnaire ACTIONS_PAR_ROLE défini en haut de ce
    fichier — ne recopiez pas les permissions, lisez-les depuis cette
    constante.

    Paramètres :
        role   : str — un des rôles définis dans ACTIONS_PAR_ROLE
            (ex. "Trésorière"). Si ce rôle n'existe pas dans
            ACTIONS_PAR_ROLE, considérez qu'il n'a aucun droit.
        action : str — l'action demandée (ex. "enregistrer_paiement")

    Retourne :
        True  si action fait partie de la liste des actions autorisées
              pour ce role dans ACTIONS_PAR_ROLE
        False sinon (rôle inconnu, ou action non listée pour ce rôle)

    Exemple :
        verifier_acces_role("Trésorière", "enregistrer_paiement") -> True
        verifier_acces_role("Trésorière", "enregistrer_vente")    -> False
        verifier_acces_role("Livreur",    "tableau_de_bord")      -> False  (rôle inconnu)
    """
         # TODO : à compléter
    pass
