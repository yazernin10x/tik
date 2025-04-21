
# TiK - Backend


Voici un diagramme illustrant les relations entre les entités de ton application de gestion de tickets de bug :  

### **Modèle relationnel des entités**  

- **Utilisateur (User)**  
  - ⬤───◯ (1,n) → **Ticket** (Un utilisateur peut créer plusieurs tickets, un ticket est créé par un seul utilisateur)  
  - ⬤───◯ (1,n) → **Projet** (Un utilisateur peut créer plusieurs projets, un projet est créé par un seul utilisateur)  
  - ⬤───◯ (1,n) → **Commentaire** (Un utilisateur peut créer plusieurs commentaires, un commentaire est créé par un seul utilisateur)  

- **Projet (Project)**  
  - ⬤───◯ (1,n) → **Ticket** (Un projet peut contenir plusieurs tickets, un ticket appartient à un seul projet)  

- **Ticket**  
  - ⬤───◯ (1,n) → **Commentaire** (Un ticket peut avoir plusieurs commentaires, un commentaire appartient à un seul ticket)  
  - ⬤───⬤ (1,1) → **Niveau (Level)** (Un ticket appartient à un seul niveau, un niveau peut avoir plusieurs tickets)  
  - ⬤───⬤ (1,1) → **Catégorie (Category)** (Un ticket appartient à une seule catégorie, une catégorie peut avoir plusieurs tickets)  
  - ⬤───⬤ (1,1) → **Statut (Status)** (Un ticket a un seul statut parmi une liste définie)  

---
