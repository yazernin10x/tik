### 📌 **Comment utiliser Alembic pour gérer les migrations de base de données ?**  

Alembic est un outil de migration de schéma SQL pour SQLAlchemy. Il permet de gérer l'évolution d'une base de données sans perdre de données.  

---

## 🚀 **1. Installation d'Alembic**
Si ce n'est pas encore fait, installe Alembic avec :

```bash
pip install alembic
```

---

## 🏗 **2. Initialiser Alembic dans un projet**
Dans ton projet, exécute :

```bash
alembic init alembic
```

Cela va créer un dossier `alembic/` avec les fichiers de configuration.

---

## 🛠 **3. Configurer Alembic**
Dans le fichier `alembic.ini`, modifie la ligne contenant **`sqlalchemy.url`** pour y mettre ta connexion à la base de données.  

Exemple pour PostgreSQL :

```ini
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

Ou pour SQLite :

```ini
sqlalchemy.url = sqlite:///./database.db
```

Ensuite, dans `alembic/env.py`, remplace l’import `target_metadata` par celui de ton modèle SQLAlchemy.

Exemple si ton modèle est dans `app/models.py` :

```python
from app.models import Base
target_metadata = Base.metadata
```

---

## 📌 **4. Générer une première migration**
Une fois la configuration prête, exécute :

```bash
alembic revision --autogenerate -m "Initial migration"
```

Cela va créer un fichier dans `alembic/versions/` contenant les instructions pour créer les tables.

Tu peux vérifier ce fichier et modifier les instructions si nécessaire.

---

## 📜 **5. Appliquer la migration à la base de données**
Exécute :

```bash
alembic upgrade head
```

Cela va appliquer la migration et créer les tables dans la base de données.

---

## 🔄 **6. Modifier le schéma et générer une nouvelle migration**
Si tu modifies tes modèles SQLAlchemy, crée une nouvelle migration avec :

```bash
alembic revision --autogenerate -m "Ajout d'un champ user"
```

Puis applique la migration :

```bash
alembic upgrade head
```

---

## 🚑 **7. Annuler une migration**
Si une migration pose problème, tu peux la rétrograder :

```bash
alembic downgrade -1
```

Ou revenir à un état spécifique :

```bash
alembic downgrade base
```

---

## 🔥 **8. Lister les migrations**
Pour voir l’historique des migrations :

```bash
alembic history
```

Pour voir le statut actuel de la base :

```bash
alembic current
```

---

### 🎯 **Résumé rapide des commandes utiles**
| Commande | Description |
|----------|-------------|
| `alembic init alembic` | Initialise Alembic dans le projet |
| `alembic revision --autogenerate -m "message"` | Génère une nouvelle migration basée sur les modèles |
| `alembic upgrade head` | Applique les dernières migrations |
| `alembic downgrade -1` | Annule la dernière migration |
| `alembic history` | Liste les migrations passées |
| `alembic current` | Affiche la version actuelle de la base |

---

### 🎯 **Bonnes pratiques**
1. **Toujours vérifier les fichiers de migration** avant de les appliquer.
2. **Ne pas modifier une migration appliquée** sur un environnement de production.
3. **Faire des sauvegardes** avant de rétrograder (`downgrade`).

---

Tu as un cas spécifique où tu veux utiliser Alembic ? 😊





---


### 📌 **Où placer ce script dans un projet Alembic ?**  

Ce script doit être placé dans le **dossier des migrations Alembic**, sous le répertoire **`versions/`**.  

---

### 🔹 **1. Générer une migration Alembic**  
Avant d’ajouter ce script, assure-toi que **Alembic est bien initialisé** dans ton projet. Si ce n’est pas encore fait :  

```bash
alembic init alembic
```
Cela crée une structure de projet avec un dossier **`alembic/`** contenant un sous-dossier **`versions/`**.

Ensuite, pour générer une nouvelle migration :  
```bash
alembic revision -m "Ajout des catégories par défaut"
```
👉 Cette commande **crée un fichier** dans `alembic/versions/` avec un nom du type :  

```
alembic/versions/20250205_ajout_categories.py
```
(Le nom peut varier en fonction de la date et de l’horodatage.)

---

### 🔹 **2. Modifier le fichier de migration**
Après avoir généré le fichier, **ouvre-le** dans un éditeur et **remplace son contenu** par le script corrigé :  

📌 **Emplacement du fichier :**  
```
alembic/versions/20250205_ajout_categories.py
```
📌 **Contenu du fichier (modifié)** :
```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.models import Category  # Import du modèle Category

# Identifiants de migration
revision = '20250205_ajout_categories'
down_revision = 'yyyy'  # Remplace par l'ID de la migration précédente
branch_labels = None
depends_on = None

def insert_default_categories(session: Session):
    """Insère des catégories par défaut dans la base de données."""
    categories = [
        "Bug",
        "Feature Request",
        "Improvement",
        "Task",
        "Performance",
        "Security",
        "UI/UX",
        "Testing",
        "Configuration"
    ]
    for category_name in categories:
        category = Category(name=category_name)
        session.add(category)
    
    session.commit()  # Valide les changements

def upgrade():
    """Ajoute les catégories par défaut lors de la migration."""
    bind = op.get_bind()
    session = Session(bind=bind)  
    insert_default_categories(session)  # Insère les données

def downgrade():
    """Supprime toutes les catégories insérées lors du rollback."""
    bind = op.get_bind()
    session = Session(bind=bind)
    session.query(Category).delete()  # Supprime toutes les catégories
    session.commit()
```

---

### 🔹 **3. Exécuter la migration**  
Une fois le script en place, applique la migration avec :  
```bash
alembic upgrade head
```
Cela insérera les catégories dans la base de données.  

Si tu veux annuler cette migration :  
```bash
alembic downgrade -1
```
Cela supprimera les catégories insérées.  

---

### 🔹 **4. Vérifications à faire**  
✅ **`src.models.Category` est bien défini ?**  
✅ **La base de données est connectée ?** (`alembic.ini` bien configuré)  
✅ **La migration précédente (`down_revision`) est correcte ?**  

Si tout est bon, ton script fonctionnera sans problème. 🚀




Voici une liste des catégories courantes que peut avoir un ticket de bug :

Bug : Un problème ou une erreur dans le logiciel qui doit être corrigé.
Feature Request : Une demande pour une nouvelle fonctionnalité ou une amélioration.
Improvement : Une suggestion pour améliorer une fonctionnalité existante.
Task : Une tâche générale qui doit être accomplie.
Documentation : Un problème ou une mise à jour concernant la documentation.
Performance : Un problème lié aux performances du logiciel.
Security : Un problème de sécurité qui doit être résolu.
UI/UX : Un problème ou une amélioration concernant l'interface utilisateur ou l'expérience utilisateur.
Testing : Un problème ou une tâche liée aux tests du logiciel.
Configuration : Un problème ou une tâche liée à la configuration du logiciel.