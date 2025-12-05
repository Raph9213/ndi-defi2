# 🌿 NDI 2025 - Défi 2 : L'Appli Éco-Responsable

Bienvenue sur le projet de l'équipe **Red Code Chili Peppers** pour la Nuit de l'Info 2025 !
Cette application web ludique encourage les utilisateurs à réduire leur empreinte carbone en accomplissant des missions écologiques, seul ou en tribu.

## 🚀 Fonctionnalités Réalisées

### Gestion des utilisateurs
- **Inscription & Connexion** : Création de compte sécurisée avec email et mot de passe.
- **Tableau de Bord Personnel** : Vue d'ensemble de votre impact écologique (CO2 économisé) et de votre tribu.
- **Sécurité** : Vérification de session pour protéger l'accès au tableau de bord.

### Système de Tribus
- **Création de Tribu** : Fondez votre propre village écologique.
- **Rejoindre une Tribu** : Rejoignez vos amis via un code d'invitation unique.
- **Score d'Équipe** : Cumulez vos points avec ceux de votre tribu pour grimper dans le classement.

### 🌍 Missions & Quêtes
- **Catalogue de Quêtes** : Liste de défis écologiques variés (ex: "Manger végétarien", "Zéro déchet").
- **Validation** : Complétez des missions pour gagner des points (g de CO2 évités) en temps réel.
- **Impact Visuel** : Visualisez concrètement votre contribution à la planète.

### 🏆 Classement (Leaderboard)
- **Classement en Temps Réel** : Comparez la performance de votre tribu avec les autres villages.
- **Mise à jour dynamique** : Les scores sont recalculés instantanément à chaque mission validée.

---

## 🛠️ Guide d'Installation et de Lancement (De A à Z)

Suivez ces étapes pour lancer le projet complet sur votre machine.

### Prérequis
- **Python 3.8+** (pour le backend)
- **Node.js 16+** (pour le frontend)
- **npm** ou **yarn**

### 1. Backend (API Flask)

Le backend gère la base de données, l'authentification et la logique métier.

1.  Ouvrez un terminal dans le dossier racine du projet (`ndi-defi2`).
2.  Installez les dépendances Python :
    ```bash
    pip install flask flask_sqlalchemy pyjwt werkzeug
    ```
3.  Lancez le serveur :
    ```bash
    python app.py
    ```
    *Le serveur démarrera par défaut sur `http://localhost:5000`.*

### 2. Frontend (Nuxt.js)

Le frontend est l'interface utilisateur moderne construite avec Nuxt 3 et Tailwind CSS.

1.  Ouvrez un **nouveau terminal** et naviguez vers le dossier frontend :
    ```bash
    cd defi2-frontend
    ```
2.  Installez les dépendances Node :
    ```bash
    npm install
    ```
3.  Lancez le serveur de développement :
    ```bash
    npm run dev
    ```
4.  Ouvrez votre navigateur et accédez à l'URL indiquée (généralement `http://localhost:3000`).

### ⚠️ Note Importante sur la Configuration API

Actuellement, l'application frontend est configurée pour communiquer avec une URL distante (ngrok) pour faciliter les tests en réseau.
Si vous souhaitez faire tourner le projet **entièrement en local**, vous devez modifier l'URL de l'API dans les fichiers suivants du frontend pour qu'elle pointe vers `http://localhost:5000` :

- `app/components/NavBar.vue`
- `app/components/QuestCard.vue`
- `app/pages/users/[id].vue`
- `app/pages/classement.vue`
- `app/components/NoTribe.vue`

Remplacez `http://4.tcp.eu.ngrok.io:12316` par `http://localhost:5000`.

---

## 👥 L'Équipe
Projet réalisé avec ❤️ et ☕ par les **Red Code Chili Peppers**.
