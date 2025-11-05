# Plan de Développement : Authentification, Base de Données et Paiements

Ce document décrit les étapes nécessaires pour transformer l'application d'un site statique à une application web complète avec gestion des utilisateurs, base de données et paiements.

## Où en sommes-nous ?

*   **Frontend** : Une application React fonctionnelle avec des composants d'interface utilisateur (`Hero`, `Pricing`, etc.). L'interface est prête à être connectée à un backend.
*   **Backend** :
    *   Le serveur Python (`app.py`) est configuré pour la base de données et inclut le modèle `User` ainsi que les routes d'authentification (`/api/register`, `/api/login`, `/api/profile`).
    *   Les dépendances Python pour Google OAuth (`google-auth`, `google-auth-oauthlib`) sont installées.
    *   L'intégration de base de Stripe est configurée dans `app.py` avec un endpoint `create-checkout-session` et un webhook.
*   **Base de Données** : Les informations de connexion sont présentes dans le fichier `.env`, et la base de données est configurée via SQLAlchemy. Le modèle `User` est défini.
*   **Authentification** : Les endpoints d'inscription et de connexion sont en place. Les identifiants Google OAuth (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`) sont configurés dans le fichier `.env`.
*   **Paiements** : L'intégration de base de Stripe est configurée dans `app.py` avec un endpoint `create-checkout-session` et un webhook.

## Ce qu'il reste à faire

L'objectif est de mettre en place un système robuste. Voici les grandes phases du projet :

1.  **Phase 0 : Unification du Frontend et Accès Conditionnel** (Nouvelle phase)
2.  **Phase 1 : Backend - Base de Données et Modèle Utilisateur** (Terminée)
3.  **Phase 2 : Backend - API d'Authentification** (En cours : Intégration Google OAuth)
4.  **Phase 3 : Frontend - Intégration de l'Authentification**
5.  **Phase 4 : Intégration des Paiements (Stripe)** (En cours : Finalisation de l'intégration)
6.  **Phase 5 : Gestion des Rôles et Accès**

---

### Phase 0 : Unification du Frontend et Accès Conditionnel

**Objectif :** Servir l'application React ou l'outil d'analyse Flask depuis la même URL (`http://localhost:5001`) en fonction du statut de l'utilisateur (connecté et payant).

*   [ ] **Compiler l'application React :**
    *   Exécuter `npm install` puis `npm run build` dans le répertoire `comment-sense-ai/` pour générer les fichiers statiques.
*   [ ] **Configurer Flask pour servir l'application React :**
    *   Modifier `app.py` pour que Flask serve les fichiers statiques générés par React (depuis `comment-sense-ai/dist`) comme frontend par défaut.
*   [ ] **Modifier la route principale (`@app.route('/')`) dans `app.py` :**
    *   Implémenter une logique pour vérifier le statut d'authentification de l'utilisateur (via un cookie JWT sécurisé).
    *   Si l'utilisateur est authentifié et a le rôle `'paid'`, servir `templates/index.html` (l'outil d'analyse).
    *   Sinon (non authentifié, ou authentifié mais rôle `'user'`), servir l'application React (`comment-sense-ai/dist/index.html`).

### Phase 1 : Backend - Base de Données et Modèle Utilisateur

**Objectif :** Connecter l'application Flask à la base de données et définir la structure pour stocker les informations des utilisateurs.

*   [x] **Installer les dépendances Python :**
    *   `Flask-SQLAlchemy` : Pour interagir avec la base de données.
    *   `Flask-Migrate` : Pour gérer les changements de structure de la base de données.
    *   `psycopg2-binary` (ou autre driver selon votre BDD) : Le connecteur pour PostgreSQL.
    *   `python-dotenv` : Pour charger les variables du fichier `.env`.
    *   `Flask-Bcrypt` : Pour hacher les mots de passe.
    *   `PyJWT` : Pour les tokens d'authentification.
    *   `gunicorn` : Pour le déploiement (ajouté).
    *   `google-auth`, `google-auth-oauthlib` : Pour l'authentification Google.

*   [x] **Configurer la connexion à la BDD :**
    *   Mettre à jour `app.py` pour charger les variables d'environnement et configurer SQLAlchemy.

*   [x] **Créer le modèle `User` :**
    *   Définir une table `users` avec les colonnes :
        *   `id` (Clé primaire)
        *   `email` (Unique, non nul)
        *   `password_hash` (Non nul)
        *   `role` (Ex: 'user', 'paid', 'admin')
        *   `stripe_customer_id` (Pour lier l'utilisateur à un client Stripe)
        *   `created_at` (Date de création)

*   [x] **Initialiser les migrations de la base de données.** (Cette étape est considérée comme "terminée" car la base de données est gérée à distance. Assurez-vous que la table `users` existe avec la structure définie.)

### Phase 2 : Backend - API d'Authentification

**Objectif :** Créer les points d'entrée (endpoints) pour que les utilisateurs puissent s'inscrire et se connecter, y compris via Google.

*   [x] **Créer l'endpoint `/api/register` (POST) :**
    *   Accepte `email` et `password`.
    *   Vérifie si l'email existe déjà.
    *   Hache le mot de passe.
    *   Crée un nouvel utilisateur dans la base de données.
    *   Retourne un message de succès.

*   [ ] **Modifier l'endpoint `/api/login` (POST) :**
    *   Accepte `email` et `password`.
    *   Vérifie les identifiants.
    *   Génère un token d'authentification (JWT).
    *   **Retourne le token dans un cookie HTTPOnly sécurisé** pour une meilleure sécurité et une gestion simplifiée côté serveur.
    *   Retourne également les informations de l'utilisateur (ID, email, rôle) dans le corps de la réponse JSON.

*   [-] **Intégrer la connexion Google (OAuth) :**
    *   [x] **Backend :**
        *   Installer `google-auth` et `google-auth-oauthlib`.
        *   Configurer les identifiants OAuth 2.0 de Google dans `.env` (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
        *   Créer un endpoint `/api/auth/google` pour initier le flux OAuth.
        *   Créer un endpoint `/api/auth/google/callback` pour gérer la redirection après l'authentification Google.
        *   Vérifier le token d'identité Google, créer ou récupérer l'utilisateur dans la BDD, et générer un JWT pour l'application. (Implémentation du code côté backend à faire dans `app.py`).
    *   [ ] **Frontend :**
        *   Utiliser la bibliothèque Google Sign-In ou une implémentation manuelle pour initier le flux OAuth.
        *   Envoyer le code d'autorisation au backend.

*   [x] **Créer un endpoint protégé (ex: `/api/profile`) :**
    *   Pour vérifier que l'authentification fonctionne et récupérer les informations de l'utilisateur connecté.

### Phase 3 : Frontend - Intégration de l'Authentification

**Objectif :** Remplacer le bouton "Commencer" par des formulaires de connexion/inscription et gérer l'état de connexion de l'utilisateur.

*   [ ] **Installer les dépendances React :**
    *   `react-router-dom` pour la navigation.
    *   `axios` pour les requêtes API.

*   [ ] **Créer les pages/composants :**
    *   `LoginPage.tsx` (incluant le bouton de connexion Google)
    *   `SignupPage.tsx` (incluant le bouton de connexion Google)
    *   Un modal ou des pages dédiées pour la connexion et l'inscription.

*   [ ] **Mettre en place un contexte d'authentification (AuthContext) :**
    *   Pour stocker l'état de connexion de l'utilisateur et le rendre accessible dans toute l'application.

*   [ ] **Modifier le `Header.tsx` :**
    *   Si l'utilisateur n'est pas connecté, afficher "Connexion" et "Inscription".
    *   Si l'utilisateur est connecté, afficher "Mon Compte" et "Déconnexion".

*   [ ] **Connecter les formulaires aux endpoints de l'API.**

### Phase 4 : Intégration des Paiements (Stripe)

**Objectif :** Permettre aux utilisateurs de souscrire à un forfait payant.

*   [x] **Backend :**
    *   Installer la librairie `stripe` pour Python.
    *   Créer un endpoint `/api/create-checkout-session` (protégé) :
        *   Prend un `priceId` en paramètre.
        *   Crée une session de paiement Stripe.
        *   Retourne l'ID de la session au frontend.
    *   Créer un webhook `/api/stripe-webhook` :
        *   Pour écouter les événements de Stripe (ex: `checkout.session.completed`).
        *   Mettre à jour le rôle de l'utilisateur en 'paid' dans la BDD lorsque le paiement est réussi. (bien différencier les payment annuel et mensuel via les priceId).
    *  Faire en sorte que l'endpoint soit protégé et accessible uniquement aux utilisateurs authentifiés.
    *  Faire en sorte que quand un utilisateur payant se reconnecte, son rôle soit vérifié et mis à jour si nécessaire.
    *  Faire en sortte que les token soient décomptés a chaque appel aux api payantes.

*   [ ] **Frontend :**
    *   Installer `@stripe/stripe-js`.
    *   Modifier le composant `Pricing.tsx` :
        *   Le clic sur "Choisir le Forfait" appelle `/api/create-checkout-session`.
        *   Redirige l'utilisateur vers la page de paiement Stripe avec l'ID de session reçu.  (bien différencier les payment annuel et mensuel via les priceId).
    *   Gérer les retours après paiement (succès/échec).
    *   Mettre à jour l'interface utilisateur en fonction du statut de l'abonnement de l'utilisateur (ex: afficher un badge "Pro" ou débloquer des fonctionnalités).
    *   Assurer que les appels aux API payantes vérifient le rôle de l'utilisateur avant d'autoriser l'accès.
    *   Gérer le décompte des tokens restants et l'afficher dans l'interface utilisateur.

### Phase 5 : Gestion des Rôles et Accès

**Objectif :** Restreindre l'accès à certaines fonctionnalités en fonction du rôle de l'utilisateur, et gérer l'accès aux outils d'administration.

*   [ ] **Backend :**
    *   Protéger les endpoints de l'API pour qu'ils ne soient accessibles qu'aux utilisateurs ayant le bon rôle (ex: un utilisateur 'paid' peut accéder à plus de fonctionnalités).
    *   **Ajouter des routes d'administration (ex: `/api/admin/users`) accessibles uniquement aux utilisateurs avec le rôle `'admin'` pour la gestion de la base de données.**

*   [ ] **Frontend :**
    *   Afficher ou masquer des éléments de l'interface en fonction du rôle de l'utilisateur (ex: un badge "Pro", accès à des pages spécifiques).
    *   **Créer une interface d'administration (accessible uniquement aux `'admin'`) pour visualiser et gérer les utilisateurs dans la base de données.**

## Prochaines Étapes

1.  **Mettre en œuvre la Phase 0 : Unification du Frontend et Accès Conditionnel.**
2.  **Modifier l'endpoint `/api/login` pour utiliser des cookies HTTPOnly.**
3.  **Implémenter le code pour l'intégration de la connexion Google (OAuth) côté Backend dans `app.py`.**
    *   Cela inclura la gestion de la redirection et la création/récupération d'utilisateurs.
4.  **Assurez-vous que la table `users` est créée dans votre base de données O2SWITCH** avec la structure définie dans le modèle `User` (`id`, `email`, `password_hash`, `role`, `stripe_customer_id`, `created_at`).