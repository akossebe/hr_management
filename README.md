# 🏢 HR Pulse - Système de Gestion des Ressources Humaines

Application web complète de gestion des ressources humaines (RH) développée avec **Django** et **Django REST Framework**.

---

## 🚀 Fonctionnalités Principales

- 👥 **Gestion des Employés** : Profils, départements, postes, contrats et documents.
- 📅 **Gestion des Congés** : Demandes d'absence, types de congés et validation administrative.
- ⏱️ **Suivi des Présences** : Pointage, heures d'arrivée/départ, suivi des retards.
- 💵 **Gestion de la Paie** : Fiches de paie, calcul du salaire net, primes et déductions.
- 📊 **Tableau de Bord RH** : Vue d'ensemble avec statistiques clés et indicateurs de performance.
- 🔌 **API REST** : Endpoints pour l'intégration avec d'autres systèmes.

---

## 🛠️ Prérequis

- **Python** 3.10+
- **pip** et **virtualenv**

---

## 📦 Installation et Démarrage

### 1. Cloner le projet
```bash
git clone <URL_DU_DEPOT>
cd hr_management
```

### 2. Créer et activer un environnement virtuel
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations de la base de données
```bash
python manage.py migrate
```

### 5. (Optionnel) Initialiser avec des données de démonstration
```bash
python seed_db.py
```
> 💡 Cette commande crée un compte administrateur :
> - **Identifiant** : `admin`
> - **Mot de passe** : `admin123`

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```
Accédez à l'application sur : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📁 Architecture du Projet

```text
hr_management/
├── api/          # Endpoints API REST
├── attendance/   # Module de gestion des présences
├── core/         # Dashboard et fonctionnalités centrales
├── employees/    # Gestion des départements, postes et employés
├── hr_config/    # Configuration globale Django (settings, urls)
├── leaves/       # Module de gestion des congés
├── payroll/      # Module de gestion de la paie
├── static/       # Fichiers statiques (CSS, JS, images)
├── templates/    # Templates HTML
├── manage.py     # Script d'administration Django
├── seed_db.py    # Script de peuplement initial de données
└── requirements.txt
```
