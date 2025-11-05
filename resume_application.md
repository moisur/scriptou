# Résumé Général de l'Application

Cette application web permet d'analyser des vidéos YouTube en extrayant des informations précieuses à partir de leurs transcriptions et commentaires. Elle offre deux fonctionnalités principales : la génération de mindmaps pour visualiser les concepts clés d'une vidéo et une analyse approfondie des sentiments et des thèmes présents dans les commentaires.

## Fonctionnalités Clés

*   **Récupération de Données YouTube :** Extrait les transcriptions et les commentaires des vidéos via l'API YouTube.
*   **Génération de Mindmap :** Analyse le contenu d'une transcription pour générer une mindmap interactive, offrant une vue d'ensemble visuelle des idées principales.
*   **Analyse de Commentaires :**
    *   **Analyse de Sentiment :** Évalue le sentiment (positif, négatif, neutre) des commentaires.
    *   **Clustering Sémantique :** Regroupe les commentaires par thèmes sémantiques similaires en utilisant des modèles de machine learning (UMAP, HDBSCAN).
*   **Génération de Rapports :** Crée des rapports PDF synthétisant les résultats de l'analyse.
*   **Interaction IA :** Utilise le modèle Gemini de Google pour des analyses et des synthèses avancées.

## Architecture Technique

### Backend (API Flask)

Le backend est une application Flask qui expose plusieurs points de terminaison pour gérer les analyses.

*   **Framework :** Flask
*   **Logique Métier :**
    *   Utilise `google-generativeai` pour interagir avec l'API Gemini.
    *   Emploie la bibliothèque `transformers` de Hugging Face pour le traitement du langage naturel.
    *   Intègre `youtube_transcript_api` pour récupérer les transcriptions.
    *   Réalise le clustering avec `scikit-learn`, `umap-learn`, et `hdbscan`.
    *   Génère des rapports PDF avec `fpdf2`.

### Frontend (Interface Utilisateur)

L'interface est une application monopage (Single Page Application) conçue pour être intuitive et réactive.

*   **Structure :** `index.html` avec deux onglets principaux : "Création de Mindmap" et "Analyse de Commentaires".
*   **Interactivité :** Le JavaScript est utilisé pour les appels AJAX à l'API Flask, la gestion des événements et la manipulation du DOM.
*   **Visualisation :** La bibliothèque `markmap-lib` est utilisée pour afficher les mindmaps interactives.

### Technologies et Dépendances

*   **Backend :** Flask, Flask-Cors
*   **IA & Machine Learning :** google-generativeai, transformers, torch, scikit-learn, umap-learn, hdbscan
*   **API & Données :** youtube_transcript_api
*   **Génération de Documents :** fpdf2
*   **Frontend :** JavaScript (natif), Markmap
*   **Environnement :** Python

## Parcours Utilisateur

### Cas d'Usage 1 : Création d'une Mindmap

1.  L'utilisateur accède à l'onglet "Création de Mindmap".
2.  Il saisit l'URL d'une vidéo YouTube dans le champ prévu.
3.  Il clique sur le bouton pour lancer l'analyse.
4.  Le frontend envoie une requête au backend Flask.
5.  Le backend récupère la transcription de la vidéo, l'analyse avec Gemini pour en extraire la structure et les concepts clés.
6.  Le backend renvoie les données de la mindmap au format Markmap.
7.  Le frontend affiche la mindmap interactive à l'utilisateur.

### Cas d'Usage 2 : Analyse des Commentaires

1.  L'utilisateur sélectionne l'onglet "Analyse de Commentaires".
2.  Il entre l'URL de la vidéo YouTube.
3.  Il lance l'analyse.
4.  Le backend récupère les commentaires de la vidéo.
5.  Il effectue une analyse de sentiment et un clustering sémantique sur les commentaires.
6.  Les résultats (graphiques, thèmes, exemples de commentaires) sont renvoyés au frontend.
7.  L'utilisateur peut explorer les thèmes, voir la répartition des sentiments et télécharger un rapport PDF.
