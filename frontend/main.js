/* =====================================================================
   MAIN.JS  —  FICHIER PRÉ-ÉCRIT — NE PAS MODIFIER
   =====================================================================
   AgriCoop Connect — Coopérative COMAKI, Kintélé

   Ce fichier détecte sur quelle page il s'exécute et branche vos
   fonctions (functions.js) au bon endroit : appel de l'API Flask,
   lecture des formulaires, écriture dans le DOM. Vous n'avez rien à
   écrire ici.
   ===================================================================== */

const API_URL = "http://localhost:5000/api";

/* ---------- SESSION (utilisée sur toutes les pages) -------------------- */
const CLE_SESSION = "agricoop_utilisateur";

function obtenirUtilisateurConnecte() {
  const brut = localStorage.getItem(CLE_SESSION);
  return brut ? JSON.parse(brut) : null;
}

function enregistrerUtilisateurConnecte(utilisateur) {
  localStorage.setItem(CLE_SESSION, JSON.stringify(utilisateur));
}

function deconnecterUtilisateur() {
  localStorage.removeItem(CLE_SESSION);
  window.location.href = "../login/login.html";
}

function initBarreSession() {
  const utilisateur = obtenirUtilisateurConnecte();
  const cible = document.getElementById("utilisateur-connecte");
  if (cible) {
    cible.textContent = utilisateur
      ? `Connecté(e) : ${utilisateur.nom_complet} (${utilisateur.role})`
      : "Non connecté(e)";
  }
  const btnDeconnexion = document.getElementById("btn-deconnexion");
  if (btnDeconnexion) {
    btnDeconnexion.addEventListener("click", deconnecterUtilisateur);
  }
}

/* ---------- CONNEXION (login.html) -------------------------------------- */
function initLogin() {
  const form = document.getElementById("form-login");
  if (!form) return;

  form.addEventListener("submit", async (evt) => {
    evt.preventDefault();
    const donnees = {
      nom_utilisateur: document.getElementById("l-nom-utilisateur").value,
      mot_de_passe: document.getElementById("l-mot-de-passe").value,
    };
    const messageErreur = document.getElementById("message-erreur-login");

    if (!validerFormulaireLogin(donnees)) {
      messageErreur.textContent = "Merci de remplir les deux champs.";
      messageErreur.hidden = false;
      return;
    }
    messageErreur.hidden = true;

    try {
      const reponse = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(donnees),
      });
      const resultat = await reponse.json();

      if (resultat.succes) {
        enregistrerUtilisateurConnecte(resultat.utilisateur);
        window.location.href = "../dashboard/dashboard.html";
      } else {
        messageErreur.textContent = resultat.erreur || "Connexion refusée.";
        messageErreur.hidden = false;
      }
    } catch (e) {
      messageErreur.textContent = "Impossible de contacter le serveur.";
      messageErreur.hidden = false;
      console.error(e);
    }
  });
}

/* ---------- TABLEAU DE BORD (index.html) ------------------------------ */
async function initDashboard() {
  const cible = document.getElementById("dashboard-cartes");
  if (!cible) return;

  let data;
  try {
    const reponse = await fetch(`${API_URL}/dashboard`);
    data = await reponse.json();
    if (!reponse.ok) {
      // L'API a répondu mais avec une erreur (ex. fonction logic.py pas
      // encore implémentée). Le message vient directement du serveur.
      cible.innerHTML = data.erreur || "Le serveur a renvoyé une erreur.";
      return;
    }
  } catch (e) {
    // Ici, l'API est réellement injoignable (backend pas démarré, etc.)
    cible.innerHTML = "Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).";
    console.error(e);
    return;
  }

  // Chaque section est indépendante : si l'une échoue (fonction JS pas
  // encore codée), les autres s'affichent quand même normalement.
  try {
    const ind = data.indicateurs;
    document.getElementById("carte-stock").textContent = ind.stock_total + " kg";
    document.getElementById("carte-montant-du").textContent = formaterMontant(ind.montant_du_total);
    document.getElementById("carte-membres").textContent = ind.nb_membres_actifs;
    document.getElementById("carte-livraisons").textContent = ind.nb_livraisons_mois;
  } catch (e) {
    cible.innerHTML = "Cartes indicateurs : vérifiez formaterMontant() dans functions.js.";
    console.error(e);
  }

  try {
    const joursActifs = document.getElementById("jours-actifs");
    if (joursActifs) {
      joursActifs.textContent = compterJoursActifs(data.livraisons_par_jour, 80) + " jour(s) à forte activité (> 80 kg)";
    }
  } catch (e) {
    console.error("Section jours-actifs :", e);
  }

  try {
    const graphique = document.getElementById("graphique-semaine");
    if (graphique) {
      graphique.innerHTML = Object.entries(data.livraisons_par_jour)
        .map(([date, qte]) => `<div class="barre" style="height:${qte}px" title="${formaterDate(date)} : ${qte} kg"></div>`)
        .join("");
    }
  } catch (e) {
    console.error("Section graphique-semaine :", e);
  }
}

/* ---------- MEMBRES (membres.html) ------------------------------------ */
let _membresCache = [];

async function initMembres() {
  const conteneur = document.getElementById("liste-membres");
  if (!conteneur) return;
  try {
    const reponse = await fetch(`${API_URL}/membres`);
    const data = await reponse.json();
    if (!reponse.ok) {
      conteneur.innerHTML = data.erreur || "Le serveur a renvoyé une erreur.";
      return;
    }
    _membresCache = data.membres;
    appliquerFiltresMembres();
  } catch (e) {
    conteneur.innerHTML = "Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).";
    console.error(e);
  }
}

function appliquerFiltresMembres() {
  let membres = _membresCache;

  const filtre = document.getElementById("filtre-statut");
  if (filtre && filtre.value) {
    membres = filtrerMembresParStatut(membres, filtre.value);
  }

  const recherche = document.getElementById("champ-recherche-membre");
  if (recherche && recherche.value) {
    membres = rechercherMembreParNom(membres, recherche.value);
  }

  afficherMembres(membres);
}

function afficherMembres(membres) {
  const conteneur = document.getElementById("liste-membres");
  if (!membres || membres.length === 0) {
    conteneur.innerHTML = "Aucun membre trouvé.";
    return;
  }
  conteneur.innerHTML = membres
    .map((m) => {
      const classeStatut = m.statut_cotisation === "À jour" ? "ok" : "alerte";
      return `
      <article class="membre-ligne">
        <strong>${m.nom}</strong>
        <span class="village">${m.village || ""}</span>
        <span class="contact">${m.contact || ""}</span>
        <span class="badge ${classeStatut}">${m.statut_cotisation}</span>
        <span>${formaterMontant(m.solde)}</span>
      </article>`;
    })
    .join("");
}

function initFiltresMembres() {
  const filtre = document.getElementById("filtre-statut");
  const recherche = document.getElementById("champ-recherche-membre");
  if (filtre) filtre.addEventListener("change", appliquerFiltresMembres);
  if (recherche) recherche.addEventListener("input", appliquerFiltresMembres);
}

/* ---------- LIVRAISONS (livraisons.html) ------------------------------ */
let _livraisonsCache = [];
let _livraisonsTrieesParDate = false;

async function chargerLivraisons() {
  const conteneur = document.getElementById("liste-livraisons");
  if (!conteneur) return;
  try {
    const reponse = await fetch(`${API_URL}/livraisons`);
    const data = await reponse.json();
    if (!reponse.ok) {
      conteneur.innerHTML = `<tr><td colspan='4'>${data.erreur || "Le serveur a renvoyé une erreur."}</td></tr>`;
      return;
    }
    _livraisonsCache = data;
    afficherLivraisons(_livraisonsCache);
  } catch (e) {
    conteneur.innerHTML = "<tr><td colspan='4'>Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).</td></tr>";
    console.error(e);
  }
}

function afficherLivraisons(livraisons) {
  const conteneur = document.getElementById("liste-livraisons");
  conteneur.innerHTML = livraisons
    .map(
      (l) => `
    <tr>
      <td>${l.membre_nom}</td>
      <td>${l.culture}</td>
      <td>${l.quantite} kg</td>
      <td>${formaterDate(l.date)}</td>
    </tr>`
    )
    .join("");
}

function initTriLivraisons() {
  const bouton = document.getElementById("btn-trier-livraisons");
  if (!bouton) return;
  bouton.addEventListener("click", () => {
    afficherLivraisons(trierLivraisonsParDate(_livraisonsCache));
  });
}

function initFormLivraison() {
  const form = document.getElementById("form-livraison");
  if (!form) return;

  form.addEventListener("submit", async (evt) => {
    evt.preventDefault();
    const donnees = {
      membre_id: Number(document.getElementById("f-membre").value),
      culture: document.getElementById("f-culture").value,
      quantite: document.getElementById("f-quantite").value,
    };

    const messageErreur = document.getElementById("message-erreur-livraison");
    const messageSucces = document.getElementById("message-succes-livraison");

    if (!validerFormulaireLivraison(donnees)) {
      messageErreur.hidden = false;
      messageSucces.hidden = true;
      return;
    }
    messageErreur.hidden = true;

    try {
      const reponse = await fetch(`${API_URL}/livraisons`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...donnees, quantite: Number(donnees.quantite) }),
      });
      const resultat = await reponse.json();

      if (resultat.succes) {
        messageSucces.textContent = `Livraison enregistrée ! Nouveau solde : ${formaterMontant(resultat.solde)}`;
        messageSucces.hidden = false;
        form.reset();
        chargerLivraisons();
      } else {
        messageErreur.textContent = resultat.anomalies.join(" ");
        messageErreur.hidden = false;
      }
    } catch (e) {
      messageErreur.textContent = "Impossible de contacter le serveur.";
      messageErreur.hidden = false;
      console.error(e);
    }
  });
}

/* ---------- PAIEMENTS (paiements.html) --------------------------------- */
async function chargerPaiements() {
  const conteneur = document.getElementById("liste-paiements");
  if (!conteneur) return;
  try {
    const reponse = await fetch(`${API_URL}/paiements`);
    const data = await reponse.json();
    if (!reponse.ok) {
      conteneur.innerHTML = `<tr><td colspan='3'>${data.erreur || "Le serveur a renvoyé une erreur."}</td></tr>`;
      return;
    }

    conteneur.innerHTML = data.paiements
      .map(
        (p) => `
      <tr>
        <td>${p.membre_nom}</td>
        <td>${formaterMontant(p.montant)}</td>
        <td>${p.mode_paiement || ""}</td>
        <td>${formaterDate(p.date)}</td>
      </tr>`
      )
      .join("");

    const totalCible = document.getElementById("total-paiements");
    if (totalCible) {
      totalCible.textContent = formaterMontant(calculerTotalPaiements(data.paiements));
    }
  } catch (e) {
    conteneur.innerHTML = "<tr><td colspan='3'>Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).</td></tr>";
    console.error(e);
  }
}

function initFormPaiement() {
  const form = document.getElementById("form-paiement");
  if (!form) return;

  form.addEventListener("submit", async (evt) => {
    evt.preventDefault();
    const donnees = {
      membre_id: Number(document.getElementById("p-membre").value),
      montant: document.getElementById("p-montant").value,
      mode_paiement: document.getElementById("p-mode-paiement").value,
    };

    const messageErreur = document.getElementById("message-erreur-paiement");
    const messageSucces = document.getElementById("message-succes-paiement");

    if (!validerFormulairePaiement(donnees)) {
      messageErreur.textContent = "Merci de vérifier les champs du formulaire.";
      messageErreur.hidden = false;
      messageSucces.hidden = true;
      return;
    }
    messageErreur.hidden = true;

    try {
      const reponse = await fetch(`${API_URL}/paiements`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...donnees, montant: Number(donnees.montant) }),
      });
      const resultat = await reponse.json();

      if (resultat.succes) {
        messageSucces.textContent = `${resultat.recu} Nouveau solde : ${formaterMontant(resultat.nouveau_solde)}`;
        messageSucces.hidden = false;
        form.reset();
        chargerPaiements();
      } else {
        messageErreur.textContent = resultat.anomalies.join(" ");
        messageErreur.hidden = false;
      }
    } catch (e) {
      messageErreur.textContent = "Impossible de contacter le serveur.";
      messageErreur.hidden = false;
      console.error(e);
    }
  });
}

/* ---------- VENTES & STOCK (ventes.html) ------------------------------- */
async function initVentesStock() {
  const cible = document.getElementById("cartes-stock");
  if (!cible) return;

  let data;
  try {
    const reponse = await fetch(`${API_URL}/ventes-stock`);
    data = await reponse.json();
    if (!reponse.ok) {
      cible.innerHTML = data.erreur || "Le serveur a renvoyé une erreur.";
      return;
    }
  } catch (e) {
    cible.innerHTML = "Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).";
    console.error(e);
    return;
  }

  try {
    const stockMax = Math.max(...Object.values(data.stock_disponible), 1);
    cible.innerHTML = Object.entries(data.stock_disponible)
      .map(([culture, qte]) => {
        const badge = getBadgeStock(qte);
        const pourcentage = Math.round((qte / stockMax) * 100);
        return `
        <div class="card" data-pourcentage="${pourcentage}">
          <h3>${culture}</h3>
          <p>${qte} kg disponible</p>
          <span class="badge">${badge}</span>
          <div class="barre-stock-fond">
            <div class="barre-stock-remplissage" style="width:${pourcentage}%"></div>
          </div>
        </div>`;
      })
      .join("");
  } catch (e) {
    cible.innerHTML = "Cartes de stock : vérifiez getBadgeStock() dans functions.js.";
    console.error(e);
  }

  try {
    const listeVentes = document.getElementById("liste-ventes");
    if (listeVentes) {
      listeVentes.innerHTML = data.ventes
        .map(
          (v) => `
        <tr>
          <td>${v.acheteur_nom}</td>
          <td>${v.culture}</td>
          <td>${v.quantite} kg</td>
          <td>${formaterMontant(v.prix_kg)}/kg</td>
        </tr>`
        )
        .join("");
    }
  } catch (e) {
    console.error("Section liste-ventes :", e);
  }
}

/* ---------- STATISTIQUES & RAPPORT BAILLEUR (statistiques.html) -------- */
async function initStatistiques() {
  const cible = document.getElementById("classement-membres");
  if (!cible) return;

  let data;
  try {
    const reponse = await fetch(`${API_URL}/statistiques`);
    data = await reponse.json();
    if (!reponse.ok) {
      cible.innerHTML = data.erreur || "Le serveur a renvoyé une erreur.";
      return;
    }
  } catch (e) {
    cible.innerHTML = "Impossible de joindre l'API. Vérifiez que le backend est démarré (python app.py).";
    console.error(e);
    return;
  }

  try {
    const classement = trierClassementParVolume(data.classement_membres);
    cible.innerHTML = classement
      .map((c) => `<li>${c.nom} — ${c.volume_total} kg</li>`)
      .join("");
  } catch (e) {
    cible.innerHTML = "Classement : vérifiez trierClassementParVolume() dans functions.js.";
    console.error(e);
  }

  try {
    const tableauCultures = document.getElementById("tableau-cultures");
    if (tableauCultures) {
      tableauCultures.innerHTML = Object.entries(data.statistiques_par_culture)
        .map(([culture, stats]) => `
        <tr>
          <td>${culture}</td>
          <td>${stats.volume_total} kg</td>
          <td>${formaterMontant(stats.valeur_totale)}</td>
        </tr>`)
        .join("");
    }
  } catch (e) {
    console.error("Section tableau-cultures :", e);
  }

  try {
    const topAcheteurCible = document.getElementById("top-acheteur");
    if (topAcheteurCible && data.top_acheteur && data.top_acheteur.acheteur_nom) {
      topAcheteurCible.textContent = `${data.top_acheteur.acheteur_nom} (${data.top_acheteur.volume_total} kg achetés)`;
    }
  } catch (e) {
    console.error("Section top-acheteur :", e);
  }
}

async function initRapportBailleur() {
  const cible = document.getElementById("rapport-bailleur-contenu");
  if (!cible) return;
  try {
    const reponse = await fetch(`${API_URL}/rapport-bailleur`);
    const r = await reponse.json();
    document.getElementById("rb-volume").textContent = r.volume_total_periode + " kg";
    document.getElementById("rb-montant").textContent = formaterMontant(r.montant_ventes_periode);
    document.getElementById("rb-taux").textContent = r.taux_regularite_paiements + " %";
    document.getElementById("rb-membres").textContent = r.nb_membres_actifs;
  } catch (e) {
    console.error(e);
  }
}

/* ---------- COMPTES (comptes.html) — réservé à la Secrétaire ----------- */
async function initComptes() {
  const form = document.getElementById("form-nouveau-compte");
  const listeCible = document.getElementById("liste-comptes");
  const accesRefuse = document.getElementById("acces-refuse-comptes");
  if (!form && !listeCible) return;

  const utilisateur = obtenirUtilisateurConnecte();
  if (!utilisateur) {
    if (accesRefuse) {
      accesRefuse.textContent = "Vous devez être connecté(e) pour accéder à cette page.";
      accesRefuse.hidden = false;
    }
    if (form) form.hidden = true;
    return;
  }

  try {
    const reponseAcces = await fetch(`${API_URL}/verifier-acces`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role: utilisateur.role, action: "gerer_comptes" }),
    });
    const acces = await reponseAcces.json();
    if (!acces.autorise) {
      if (accesRefuse) {
        accesRefuse.textContent = "Accès réservé à la Secrétaire.";
        accesRefuse.hidden = false;
      }
      if (form) form.hidden = true;
      return;
    }
  } catch (e) {
    console.error("Vérification d'accès impossible :", e);
    return;
  }

  async function chargerComptes() {
    if (!listeCible) return;
    try {
      const reponse = await fetch(`${API_URL}/utilisateurs`);
      const comptes = await reponse.json();
      listeCible.innerHTML = comptes
        .map((c) => `<tr><td>${c.nom_utilisateur}</td><td>${c.nom_complet}</td><td>${c.role}</td></tr>`)
        .join("");
    } catch (e) {
      listeCible.innerHTML = "<tr><td colspan='3'>Impossible de charger les comptes.</td></tr>";
      console.error(e);
    }
  }
  chargerComptes();

  if (form) {
    form.addEventListener("submit", async (evt) => {
      evt.preventDefault();
      const donnees = {
        nom_utilisateur: document.getElementById("c-nom-utilisateur").value,
        mot_de_passe: document.getElementById("c-mot-de-passe").value,
        nom_complet: document.getElementById("c-nom-complet").value,
        role: document.getElementById("c-role").value,
      };
      const messageErreur = document.getElementById("message-erreur-compte");
      const messageSucces = document.getElementById("message-succes-compte");

      try {
        const reponse = await fetch(`${API_URL}/utilisateurs`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(donnees),
        });
        const resultat = await reponse.json();

        if (resultat.succes) {
          messageSucces.textContent = `Compte créé pour ${resultat.utilisateur.nom_complet}.`;
          messageSucces.hidden = false;
          messageErreur.hidden = true;
          form.reset();
          chargerComptes();
        } else {
          messageErreur.textContent = resultat.erreur;
          messageErreur.hidden = false;
          messageSucces.hidden = true;
        }
      } catch (e) {
        messageErreur.textContent = "Impossible de contacter le serveur.";
        messageErreur.hidden = false;
        console.error(e);
      }
    });
  }
}

/* ---------- NOUVEAU MEMBRE (membres.html) ------------------------------ */
async function initNouveauMembre() {
  const form = document.getElementById("form-nouveau-membre");
  if (!form) return;

  const selectVillage = document.getElementById("nm-village");
  if (selectVillage) {
    try {
      const reponse = await fetch(`${API_URL}/villages`);
      const villages = await reponse.json();
      selectVillage.innerHTML = `<option value="">-- Choisir un village --</option>` +
        villages.map((v) => `<option value="${v}">${v}</option>`).join("");
    } catch (e) {
      console.error("Impossible de charger les villages :", e);
    }
  }

  form.addEventListener("submit", async (evt) => {
    evt.preventDefault();
    const donnees = {
      prenom: document.getElementById("nm-prenom").value,
      nom: document.getElementById("nm-nom").value,
      village: document.getElementById("nm-village").value,
      contact: document.getElementById("nm-contact").value,
    };
    const erreursCible = document.getElementById("erreurs-nouveau-membre");
    const succesCible = document.getElementById("message-succes-nouveau-membre");

    const validation = validerFormulaireNouveauMembre(donnees);
    if (!validation.valide) {
      erreursCible.innerHTML = "<ul>" + validation.erreurs.map((e) => `<li>${e}</li>`).join("") + "</ul>";
      erreursCible.hidden = false;
      succesCible.hidden = true;
      return;
    }
    erreursCible.hidden = true;

    try {
      const reponse = await fetch(`${API_URL}/membres`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(donnees),
      });
      const resultat = await reponse.json();

      if (resultat.succes) {
        succesCible.textContent = `Membre créé : ${resultat.membre.nom}.`;
        succesCible.hidden = false;
        form.reset();
        initMembres();
      } else {
        erreursCible.innerHTML = "<ul>" + resultat.anomalies.map((a) => `<li>${a}</li>`).join("") + "</ul>";
        erreursCible.hidden = false;
        succesCible.hidden = true;
      }
    } catch (e) {
      erreursCible.textContent = "Impossible de contacter le serveur.";
      erreursCible.hidden = false;
      console.error(e);
    }
  });
}

/* ---------- Démarrage automatique ------------------------------------ */
window.addEventListener("DOMContentLoaded", () => {
  initBarreSession();
  initLogin();
  initDashboard();
  initMembres();
  initFiltresMembres();
  initNouveauMembre();
  chargerLivraisons();
  initFormLivraison();
  initTriLivraisons();
  chargerPaiements();
  initFormPaiement();
  initVentesStock();
  initStatistiques();
  initRapportBailleur();
  initComptes();
});
