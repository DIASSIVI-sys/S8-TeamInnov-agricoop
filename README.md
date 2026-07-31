# AgriCoop Connect — Coopérative COMAKI, Kintélé

Bienvenue dans votre startup. Ce dépôt est le **squelette** de l'application : un mini-site de 8 pages pour digitaliser la gestion de la coopérative COMAKI (authentification, membres, livraisons, paiements, ventes, stock, statistiques). La structure est déjà en place ; **votre équipe complète les fonctions manquantes et construit les pages**.

Vous avez **quelques jours comme prevu dans le document** pour ce projet.

> Cette version intègre les résultats de l'analyse menée par les équipes Business Analyst à partir du cahier des charges COMAKI : un module d'authentification (la Secrétaire assure le rôle d'administratrice) et la création de nouveaux membres directement dans l'application.

## Lancer le projet en local

**1. Démarrer l'API (un seul terminal, à laisser ouvert)**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

L'API tourne sur `http://localhost:5000`. Laissez ce terminal ouvert tout le temps où vous travaillez.

**2. Ouvrir le site**

Ouvrez simplement `frontend/login/login.html` dans votre navigateur (double-clic, ou clic droit → ouvrir avec votre navigateur).

**Si vous utilisez VS Code, l'extension Live Server fonctionne aussi très bien** (clic droit sur le fichier HTML → "Open with Live Server").

**C'est tout : un seul terminal pour l'API, et vous ouvrez vos pages HTML directement.** Tant que `python app.py` tourne, n'importe quelle page du site peut appeler l'API normalement.

### Comptes de test (module Authentification)

| Rôle | Nom d'utilisateur | Mot de passe |
| --- | --- | --- |
| Secrétaire (Admin) | `smalonga` | `Secretaire2026` |
| Président | `floubota` | `President2026` |
| Trésorière | `abikindou` | `Tresoriere2026` |
| Responsable dépôt | `jmabiala` | `Depot2026` |
| Membre | `ankounkou` | `Membre2026` |

**Attention pédagogique :** ces mots de passe sont stockés en clair dans `data/comaki.json`, volontairement, parce que ce projet porte sur la logique métier (qui a le droit de faire quoi) et non sur la cryptographie. Ce n'est **pas** une pratique à reproduire dans un vrai projet — un vrai système hasherait les mots de passe. C'est un choix de simplification assumé pour rester dans le niveau du cours.

### Si une page ne s'affiche pas comme attendu

- **Une carte ou une section reste vide** : c'est normal si la fonction Python ou JavaScript correspondante n'est pas encore codée. Les autres sections de la page continuent de s'afficher normalement — seule la section concernée reste vide en attendant votre code.
- **Un message d'erreur apparaît sur la page** : lisez-le, il indique quelle fonction regarder. Le détail technique complet (traceback Python) est toujours visible dans le terminal où tourne `python app.py`.
- **Rien ne s'affiche du tout** : vérifiez d'abord que le terminal de l'API est bien ouvert et actif (pas d'erreur affichée dedans). Si vous venez de modifier `main.js` ou `functions.js`, faites un rafraîchissement forcé de la page (Ctrl+Maj+R ou Cmd+Maj+R) — le navigateur met parfois en cache l'ancienne version du fichier.

## Qui fait quoi

| Parcours | Effectif | Vous complétez | Vous ne touchez PAS |
| --- | --- | --- | --- |
| **Data Science** | 1 à 3 personnes | `backend/logic.py` (20 fonctions) | `app.py`, `controllers.py` |
| **Full Stack** | >2 personnes | *voir répartition ci-dessous* | `main.js` |

**Le nommage des champs est déjà fixé dans le code** (docstrings de `logic.py`, structure de `data/comaki.json`, IDs des éléments HTML). Vous n'avez pas à deviner ces noms — regardez les docstrings et le jeu de données pour comprendre le contrat technique attendu.

## Répartition Full Stack

Chaque page est dans son propre sous-dossier avec son fichier CSS dédié. L'essentiel de votre note porte sur vos **pages HTML/CSS** (structure sémantique, box model, Flexbox/Grid, responsive mobile/tablette/desktop). Chacun complète aussi 2 à 3 fonctions JS dans `frontend/functions.js`.

| Qui | Dossier & pages | Fonctions JS |
| --- | --- | --- |
| Dev FS1 | `frontend/login/login.html` **+** `frontend/dashboard/dashboard.html` | `validerFormulaireLogin`, `compterJoursActifs` |
| Dev FS2 | `frontend/membres/membres.html` **+** `frontend/comptes/comptes.html` | `filtrerMembresParStatut`, `rechercherMembreParNom`, `validerFormulaireNouveauMembre` |
| Dev FS3 | `frontend/livraisons/livraisons.html` | `validerFormulaireLivraison`, `trierLivraisonsParDate` |
| Dev FS4 | `frontend/paiements/paiements.html` | `validerFormulairePaiement`, `calculerTotalPaiements` |
| Dev FS5 | `frontend/ventes/ventes.html` | `getBadgeStock`, `formaterMontant` |
| Dev FS6 | `frontend/statistiques/statistiques.html` | `trierClassementParVolume`, `formaterDate` |

Chaque page contient des commentaires `<!-- TODO -->` indiquant le travail attendu, avec le layout, les éléments à construire et les classes déjà utilisées par `main.js` pour injecter le contenu dynamique. **Les éléments marqués "NE PAS MODIFIER" (IDs, scripts, formulaires) sont le câblage vers le backend — ne les changez pas, sinon les données ne s'afficheront plus.**

**Nouveauté — page Login (Dev FS1) :** c'est la première page que tout le monde voit. Gardez-la volontairement simple : un formulaire centré, pas de navigation complexe.

**Nouveauté — page Comptes (Dev FS2) :** réservée à la Secrétaire. `main.js` vérifie automatiquement le rôle de la personne connectée (via `/api/verifier-acces`) et affiche un message de refus si ce n'est pas elle — vous n'avez rien à coder pour cette vérification, seulement à styliser les deux états (formulaire visible / message de refus).

**Nouveauté — formulaire Nouveau membre (Dev FS2, sur la page Membres) :** un formulaire à 4 champs (prénom, nom, village, contact) en bas de la page Membres existante.

## Équipe Data Science — workflow

```bash
cd backend
pip install -r requirements.txt
python -m pytest -v        # ROUGE au départ (39 tests)
```

Complétez `backend/logic.py` (20 fonctions réparties en **4 zones** — voir les commentaires de section dans le fichier). Répartition suggérée :

- **2 Data Scientists** : Personne 1 = Zone A + Zone C (11 fonctions), Personne 2 = Zone B + Zone D (9 fonctions).
- **3 Data Scientists** : Personne 1 = Zone A (6), Personne 2 = Zone B (7), Personne 3 = Zone C + D (7).

Relancez les tests jusqu'au **VERT**.

Pour vérifier vos résultats via l'API une fois les tests au vert, lancez `python app.py` (voir "Lancer le projet en local" ci-dessus) puis testez dans le navigateur :

```
http://localhost:5000/api/dashboard
http://localhost:5000/api/membres
http://localhost:5000/api/livraisons
http://localhost:5000/api/paiements
http://localhost:5000/api/ventes-stock
http://localhost:5000/api/statistiques
http://localhost:5000/api/rapport-bailleur
http://localhost:5000/api/utilisateurs
http://localhost:5000/api/villages
```

Pour les routes qui exigent un envoi de données (POST), testez avec `curl` ou l'onglet Réseau du navigateur une fois le formulaire correspondant construit par l'équipe Full Stack — par exemple :

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"nom_utilisateur":"smalonga","mot_de_passe":"Secretaire2026"}'
```

## Équipe Full Stack — workflow

1. Ouvrez `frontend/functions.test.html` dans le navigateur → **ROUGE au départ** (25 tests).
2. Complétez vos fonctions dans `frontend/functions.js`.
3. Construisez vos pages HTML/CSS dans votre/vos sous-dossier(s).
4. Pour voir le rendu de votre page connectée aux vraies données, suivez la section "Lancer le projet en local" ci-dessus (backend démarré, puis ouvrez simplement votre fichier HTML).

## La règle d'or (JS)

Vous n'écrivez que des **fonctions pures** : des paramètres entrent, une valeur sort (`return`). Pas de réseau, pas de DOM — tout ça est déjà branché dans `main.js`. Votre note JS reste secondaire face à vos pages.

## Le jeu de données

`backend/data/comaki.json` contient :

- 8 membres (avec nom, village, contact) — 25 livraisons (avril-juillet 2026) — 8 paiements (avec mode de paiement) — 3 acheteurs — 9 ventes
- 5 comptes utilisateurs (module Authentification)
- 6 villages de référence (pour le formulaire Nouveau membre)

C'est la source unique de vérité : ne modifiez pas ce fichier, sinon vos résultats ne correspondront plus à ceux calculés par les autres personnes de l'équipe.

## Règles métier à connaître

| Règle | Description |
| --- | --- |
| RM-1 | Une livraison à quantité ≤ 0 est refusée. |
| RM-2 | Seuls Manioc, Maïs et Arachide sont acceptés comme cultures. |
| RM-3 | Un paiement ne peut jamais dépasser le solde restant dû à un membre. |
| RM-4 | Une vente ne peut jamais dépasser le stock disponible. |
| RM-5 | Le rapport partenaire ne contient jamais de donnée nominative (aucun nom de membre). |
| RM-6 | Un utilisateur ne peut accéder qu'aux actions autorisées pour son rôle (module Authentification). |
| RM-7 | Un doublon quasi certain de membre propose la fiche existante plutôt que d'en créer une nouvelle. |

## Livrable & soutenance (Demo Day)

Votre équipe pitche son produit comme une vraie startup : démo live (connexion avec un compte de test, navigation sur les 8 pages, enregistrement d'une vraie livraison et d'un vrai paiement, création d'un nouveau membre), avec explication des règles métier respectées.

Bonne construction.
