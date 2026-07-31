/* =====================================================================
   FUNCTIONS.JS  —  À COMPLÉTER PAR L'ÉQUIPE FULL STACK
   =====================================================================
   AgriCoop Connect — Coopérative COMAKI, Kintélé

   Vous êtes 6 devs Full Stack. Chacun possède une ou deux pages
   principales (voir README.md) et complète 2 ou 3 fonctions ci-dessous.
   Ce fichier reste un travail SECONDAIRE : l'essentiel de votre note
   porte sur vos pages (structure, responsive, box model, Flexbox/Grid).

   Règle d'or : une fonction reçoit des paramètres et RENVOIE (return)
   un résultat. Pas de document.querySelector ici, pas de fetch.
   Le DOM et le réseau sont déjà gérés dans main.js (n'y touchez pas).

   Notions mobilisées (déjà vues en S7-S8) : variables, types, conditions,
   boucles, objets, tableaux et leurs méthodes (.filter, .sort, .includes,
   Object.values, Object.entries...).

   Vérifiez votre travail : ouvrez functions.test.html dans le navigateur.
   ===================================================================== */


/* [Dev FS1 — Connexion — niveau S7 : conditions simples]
   Vérifie qu'un formulaire de connexion est valide avant de l'envoyer au
   serveur (module Authentification, nouveau).
   Paramètre : donnees, un objet avec les clés :
     nom_utilisateur (chaîne), mot_de_passe (chaîne)
   Règles :
     - nom_utilisateur ne doit pas être vide (après avoir retiré les
       espaces de début/fin)
     - mot_de_passe ne doit pas être vide
   Retourne : true si tout est valide, false sinon.
   Astuce   : "  ".trim() donne une chaîne vide "". */
function validerFormulaireLogin(donnees) {
  // TODO : à compléter
}


/* [Dev FS1 — Tableau de bord — niveau S7 : boucle + condition]
   Compte le nombre de jours (parmi les entrées reçues) où le volume
   livré dépasse un seuil donné — utile pour repérer les pics d'activité.
   Paramètres : livraisonsParJour (objet {date: quantite}), seuil (nombre)
   Retourne   : un nombre entier.
   Exemple    : compterJoursActifs({"2026-07-08": 135, "2026-07-09": 60}, 100) -> 1
   Astuce     : Object.values(livraisonsParJour) donne un tableau des quantités. */
function compterJoursActifs(livraisonsParJour, seuil) {
  // TODO : à compléter
}


/* [Dev FS2 — Membres — niveau S8 : tableau .filter]
   Garde uniquement les membres ayant un statut de cotisation donné.
   Paramètres : membres (tableau d'objets), statut (chaîne, ex. "En retard")
   Chaque membre a une propriété .statut_cotisation
   Retourne   : un nouveau tableau ne contenant que les membres dont
                .statut_cotisation est égal au statut demandé. */
function filtrerMembresParStatut(membres, statut) {
  // TODO : à compléter
}


/* [Dev FS2 — Membres — niveau S8 : tableau .filter + méthode de chaîne]
   Garde uniquement les membres dont le nom contient le texte recherché
   (recherche insensible à la casse), pour la barre de recherche.
   Paramètres : membres (tableau d'objets, chacun avec .nom), texte (chaîne)
   Retourne   : un nouveau tableau filtré. Si texte est vide, retourne
                tous les membres tels quels.
   Astuce     : "Jean Mabiala".toLowerCase().includes("jean") -> true */
function rechercherMembreParNom(membres, texte) {
  // TODO : à compléter
}


/* [Dev FS2 — Membres — niveau S7 : conditions simples — NOUVEAU]
   Vérifie qu'un formulaire de création de nouveau membre est valide
   avant de l'envoyer au serveur (module Membres, section 4.1 du FRD).
   Paramètre : donnees, un objet avec les clés :
     nom (chaîne), prenom (chaîne), village (chaîne), contact (chaîne)
   Règles : chacun des 4 champs doit être non vide après .trim()
   Retourne : un objet {valide: true/false, erreurs: [liste de messages]}
   Exemple  : validerFormulaireNouveauMembre({nom:"Koumba", prenom:"",
              village:"Séo", contact:""})
              -> {valide: false, erreurs: ["Le prénom est obligatoire.",
                                            "Le contact est obligatoire."]} */
function validerFormulaireNouveauMembre(donnees) {
  // TODO : à compléter
}


/* [Dev FS3 — Livraisons — niveau S7 : conditions imbriquées]
   Vérifie qu'un formulaire d'enregistrement de livraison est valide.
   Paramètre : donnees, un objet avec les clés :
     membre_id (chaîne ou nombre), culture (chaîne), quantite (chaîne)
   Règles :
     - membre_id ne doit pas être vide
     - culture ne doit pas être vide
     - quantite doit être un nombre strictement supérieur à 0
   Retourne : true si tout est valide, false sinon.
   Astuce   : Number("abc") vaut NaN ; Number("40") vaut 40. */
function validerFormulaireLivraison(donnees) {
  // TODO : à compléter
}


/* [Dev FS3 — Livraisons — niveau S8 : tableau .sort]
   Trie une liste de livraisons par date, de la plus récente à la plus
   ancienne (utilisé par un bouton "trier" sur la page Livraisons).
   Paramètre : livraisons (tableau d'objets), chacun avec .date ("AAAA-MM-JJ")
   Retourne  : le tableau trié par .date décroissante.
   Astuce    : au format "AAAA-MM-JJ", comparer les chaînes fonctionne
               directement (ordre alphabétique = ordre chronologique). */
function trierLivraisonsParDate(livraisons) {
  // TODO : à compléter
}


/* [Dev FS4 — Paiements — niveau S7 : conditions imbriquées]
   Vérifie qu'un formulaire d'enregistrement de paiement est valide
   (règles simples côté formulaire — la vraie règle métier "ne dépasse
   pas le solde dû" est vérifiée côté serveur par Data Science).
   Paramètre : donnees, un objet avec les clés :
     membre_id (chaîne ou nombre), montant (chaîne), mode_paiement (chaîne)
   Règles :
     - membre_id ne doit pas être vide
     - montant doit être un nombre strictement supérieur à 0
     - mode_paiement doit être "Espèces" ou "Mobile Money"
   Retourne : true si tout est valide, false sinon. */
function validerFormulairePaiement(donnees) {
  // TODO : à compléter
}


/* [Dev FS4 — Paiements — niveau S7/S8 : boucle + accumulateur]
   Calcule le montant total d'une liste de paiements, pour l'indicateur
   affiché en haut de la page Paiements.
   Paramètre : paiements (tableau d'objets), chacun avec .montant (nombre)
   Retourne  : un nombre (la somme de tous les montants).
   Exemple   : calculerTotalPaiements([{montant:5000},{montant:3000}]) -> 8000 */
function calculerTotalPaiements(paiements) {
  // TODO : à compléter
}


/* [Dev FS5 — Ventes & Stock — niveau S7/S8 : condition sur un nombre]
   Retourne un texte de badge selon la quantité disponible d'une culture.
   Paramètre : quantiteDisponible (nombre, en kg)
   Règles :
     - 0 kg               -> "Épuisé"
     - 1 à 49 kg           -> "Stock faible"
     - 50 kg ou plus       -> "Disponible"
   Retourne : une chaîne de caractères. */
function getBadgeStock(quantiteDisponible) {
  // TODO : à compléter
}


/* [Dev FS5 — fonction transverse — niveau S8 : propriétés d'objet + formatage]
   Met en forme un montant en FCFA, utilisée sur presque toutes les pages
   (tableau de bord, membres, livraisons, paiements).
   Paramètre : montant (nombre)
   Retourne  : une chaîne de caractères, le nombre suivi de " FCFA".
   Exemple   : formaterMontant(23000) -> "23000 FCFA" */
function formaterMontant(montant) {
  // TODO : à compléter
}


/* [Dev FS6 — Statistiques — niveau S8 : tableau .sort]
   Trie le classement des membres par volume total, du plus gros
   producteur au plus petit (ordre décroissant).
   Paramètre : classement (tableau d'objets), chaque élément a .volume_total (nombre)
   Retourne  : le tableau trié par .volume_total décroissant. */
function trierClassementParVolume(classement) {
  // TODO : à compléter
}


/* [Dev FS6 — fonction transverse — niveau S8 : propriétés d'objet + formatage]
   Met en forme une date au format "AAAA-MM-JJ" en "JJ/MM/AAAA", utilisée
   sur plusieurs pages (livraisons, paiements, ventes).
   Paramètre : dateStr (chaîne, ex. "2026-07-12")
   Retourne  : une chaîne au format "12/07/2026".
   Astuce    : dateStr.split("-") donne ["2026", "07", "12"]. */
function formaterDate(dateStr) {
  // TODO : à compléter
}


/* NE PAS MODIFIER — rend vos fonctions accessibles à main.js et aux tests */
if (typeof module !== "undefined") {
  module.exports = {
    validerFormulaireLogin,
    compterJoursActifs,
    formaterDate,
    filtrerMembresParStatut,
    rechercherMembreParNom,
    validerFormulaireNouveauMembre,
    validerFormulaireLivraison,
    trierLivraisonsParDate,
    validerFormulairePaiement,
    calculerTotalPaiements,
    getBadgeStock,
    trierClassementParVolume,
    formaterMontant,
  };
}
