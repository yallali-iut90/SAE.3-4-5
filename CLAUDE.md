# SAE 3-4-5 - E-commerce Linge de Maison

## Vue d'ensemble du projet

Application web e-commerce spécialisée dans la vente de **linge de maison** (sujet 15 : linge/coloris). Projet Flask avec architecture MVC et base de données MariaDB/MySQL.

**Sujet :** 15 (linge / coloris / type_linge)
**Livrable 1 :** ✅ Terminé
**Livrable 2 :** À rendre (vacances de février) - Site e-commerce minimum fonctionnel
**Livrable 3 :** À rendre (avant vacances de Pâques) - Fonctionnalités avancées par étudiant

---

## Structure du projet

```
SAE.3-4-5/
├── Flask/
│   ├── app.py                      # Point d'entrée Flask
│   ├── connexion_db.py             # Configuration connexion MySQL
│   ├── sae_sql.sql                 # Schéma BDD + données de test
│   ├── flask_run.sh                # Script de lancement
│   ├── controllers/                # Logique métier (MVC)
│   │   ├── auth_security.py        # Authentification
│   │   ├── fixtures_load.py        # Initialisation BDD (/base/init)
│   │   ├── client_linge.py         # Catalogue client
│   │   ├── client_panier.py        # Gestion panier
│   │   ├── client_commande.py      # Validation commandes
│   │   ├── client_commentaire.py   # Avis et commentaires
│   │   ├── client_coordonnee.py    # Gestion adresses
│   │   ├── client_liste_envies.py  # Liste d'envies
│   │   ├── admin_linge.py          # CRUD articles
│   │   ├── admin_declinaison_linge.py  # Gestion déclinaisons
│   │   ├── admin_type_linge.py     # Gestion catégories
│   │   ├── admin_commande.py       # Gestion commandes
│   │   ├── admin_dataviz.py        # Visualisations
│   │   └── admin_commentaire.py    # Modération commentaires
│   ├── templates/                  # Vues Jinja2
│   └── static/                     # Assets (CSS, JS, images)
├── consignes.html                  # Document complet des consignes
└── CLAUDE.md                       # Ce fichier
```

---

## Spécificités du Sujet 15 : Linge de Maison

### Tables principales

```sql
-- Table principale (remplace 'article')
linge(
    id_linge,
    nom_linge,
    prix_linge,
    dimension,           -- ex: "240x220", "140x190"
    matiere,             -- ex: "Percaline de coton", "Lin lavé"
    description,
    fournisseur,         -- ex: "TextileFrance", "BioHome"
    marque,              -- ex: "Rêve d'Or", "Naturelle"
    image,
    stock,
    #coloris_id,         -- clé étrangère
    #type_linge_id       -- clé étrangère
)

-- Déclinaison (violet) - propriété de variation
coloris(
    id_coloris,
    nom_coloris          -- ex: "Blanc Pur", "Gris Anthracite", "Bleu Marine"
)

-- Type/Catégorie (vert) - pour le filtre
type_linge(
    id_type_linge,
    nom_type_linge       -- ex: "Linge de Lit", "Linge de Bain", "Linge de Table", "Décoration"
)
```

### Exemples d'articles du jeu de test

| Nom | Type | Coloris | Dimension | Prix |
|-----|------|---------|-----------|------|
| Housse Percaline | Linge de Lit | Blanc Pur | 240x220 | 55.00€ |
| Drap Housse Bio | Linge de Lit | Gris Anthracite | 140x190 | 19.90€ |
| Taie Lin Lavé | Linge de Lit | Vieux Rose | 65x65 | 12.00€ |
| Parure Satinée | Linge de Lit | Bleu Marine | 260x240 | 89.00€ |
| Drap de Douche | Linge de Bain | Vert Sauge | 70x140 | 14.50€ |
| Peignoir Mixte | Linge de Bain | Gris Anthracite | Taille L | 45.00€ |
| Nappe Anti-tache | Linge de Table | Gris Anthracite | 150x250 | 35.00€ |
| Coussin Velours | Décoration | Jaune Moutarde | 45x45 | 15.00€ |

---

## Architecture technique

### Stack
- **Backend :** Python 3 + Flask
- **Base de données :** MariaDB/MySQL (PyMySQL avec DictCursor)
- **Sécurité :** werkzeug.security (scrypt), python-dotenv
- **Frontend :** Bootstrap 5 + Jinja2 templates

### Modèle de données complet

```sql
-- Tables communes à tous les sujets
utilisateur(id_utilisateur, login, email, password, nom, role)
commande(id_commande, date_achat, #utilisateur_id, #etat_id)
ligne_commande(#commande_id, #linge_id, prix, quantite)
ligne_panier(#utilisateur_id, #linge_id, quantite, date_ajout)
etat(id_etat, libelle)  -- "En attente", "Expédié", "Validé", "Annulé"

-- Tables spécifiques sujet 15
coloris(id_coloris, nom_coloris)
type_linge(id_type_linge, nom_type_linge)
linge(id_linge, nom_linge, prix_linge, dimension, matiere, description,
      fournisseur, marque, image, stock, #coloris_id, #type_linge_id)
```

### Conventions de nommage (OBLIGATOIRES)
- **SQL :** snake_case obligatoire
- **Clés étrangères :** format `table_id` (ex: `coloris_id`, `type_linge_id`)
- **Contraintes FK :** `fk_linge_coloris`, `fk_linge_type`

### Conventions de développement

#### Front-end - Contraintes imposées
- **OBLIGATOIRE :** Utiliser UNIQUEMENT le Bootstrap déjà présent dans le projet (`bootstrap.css`)
- **Interdit :** Ajouter d'autres frameworks CSS (Tailwind, Bulma, etc.)
- **Interdit :** Modifier la version de Bootstrap
- **Assets :** `static/assets/css/bootstrap.css` et `static/assets/js/bootstrap.bundle.js`
- **Templates de base :** `layout_client.html`, `layout_admin.html`, `layout.html`

#### Back-end - SQL prioritaire sur Python
- **Règle d'or :** Privilégier **SQL** pour tous les calculs et traitements de données
- **Minimum :** Python peut être utilisé pour les calculs simples si nécessaire
- **Recommandé :** Une seule requête SQL complexe plutôt qu'une boucle Python
- **Exemple à suivre :**
```python
# ✅ CORRECT - Calcul en SQL
sql = """SELECT id_linge, nom_linge,
         COUNT(*) as nb_commentaires,
         AVG(valeur) as moyenne_notes
         FROM linge
         LEFT JOIN commentaire ON ...
         GROUP BY id_linge, nom_linge"""
mycursor.execute(sql)
result = mycursor.fetchall()

# ❌ INCORRECT - Calcul en Python
for linge in linges:
    count = 0
    for commentaire in commentaires:
        if commentaire['linge_id'] == linge['id']:
            count += 1
    linge['nb_comments'] = count
```

#### Format des requêtes SQL
```python
sql = '''SELECT ... FROM ... WHERE condition = %s'''
mycursor.execute(sql, (parametre,))
result = mycursor.fetchall()  # ou fetchone()
```

#### Messages Flash
- `'alert-success'` : Action réussie (vert)
- `'alert-warning'` : Erreur / Avertissement (jaune/orange)

---

## Authentification & Sécurité

### Comptes de test
| Rôle | Login | Password | Route par défaut |
|------|-------|----------|------------------|
| Admin | admin | admin | /admin/commande/index |
| Client | client | client | /client/linge/show |
| Client2 | client2 | client2 | /client/linge/show |

### Gestion des sessions
- Session Flask avec `secret_key`
- Vérification rôle avant chaque requête (`before_request`)
- Hash mots de passe : `scrypt` via werkzeug
- Variable d'environnement : `python-dotenv`

---

## Routes principales

### Public
```
GET  /                    → Redirection selon rôle
GET  /login               → Connexion
POST /login               → Authentification
GET  /signup              → Inscription
POST /signup              → Création compte
GET  /logout              → Déconnexion
GET  /forget-password     → Mot de passe oublié
```

### Client (ROLE_client)
```
GET  /client/linge/show           → Catalogue avec filtres
GET  /client/linge/details        → Détail article
POST /client/panier/add           → Ajouter au panier
POST /client/panier/delete        → Retirer du panier
POST /client/panier/vider         → Vider panier
POST /client/commande/valide      → Validation (étape 1)
POST /client/commande/add         → Création commande
GET  /client/commande/show        → Historique commandes
GET  /client/envie/show           → Liste d'envies
```

### Admin (ROLE_admin)
```
GET  /admin/commande/index        → Dashboard commandes
GET  /admin/linge/show            → Gestion articles
GET/POST /admin/linge/add         → Ajouter article
GET/POST /admin/linge/edit        → Modifier article
GET  /admin/dataviz/etat1         → Stats stocks
GET  /admin/dataviz/etat2         → Carte géographique
```

### Fixtures
```
GET /base/init                    → Réinitialisation BDD complète
```

---

## Livrables détaillés

### ✅ Livrable 1 - Prise en main (TERMINÉ)

**Base de données :**
- [x] Script SQL `sae_sql.sql` avec structure complète
- [x] 15+ articles avec 15 photos différentes
- [x] 4 types de linge minimum
- [x] Jeu de test réaliste (noms, fournisseurs, marques)

**Application :**
- [x] Authentification fonctionnelle (TD)
- [x] Affichage articles et types pour filtre
- [x] Route `/base/init` fonctionnelle
- [x] Git synchronisé
- [x] Variables d'environnement (dotenv)
- [x] Compatible machine IUT / Railway

**Documents :**
- [x] `livrable1_sae_2_4_bdd.ods` complété
- [x] `mcd_projet_v1.loo`
- [x] `MCD_v1.pdf` + `MLD_v1.pdf` (noms + groupe)

---

### 🔄 Livrable 2 - Site minimum fonctionnel

**À rendre :** Pendant les vacances de février
**Objectif :** E-commerce fonctionnel avec gestion panier et commandes

#### Front-Office (Client)
| # | Fonctionnalité | Statut | Fichier concerné |
|---|----------------|--------|------------------|
| 2 | Filtrer par type (session) | ✅ Structure présente | `client_linge.py`, `client_panier.py` |
| 3 | Ajout panier (formulaire) | ⚠️ SQL à compléter | `client_panier.py:12-42` |
| 4 | Supprimer du panier | ⚠️ SQL à compléter | `client_panier.py:44-65` |
| 5 | Modification quantité si déjà présent | ⚠️ SQL à compléter | `client_panier.py` |
| 6 | Validation panier → commande | ⚠️ SQL à compléter | `client_commande.py` |
| 7 | Affichage stock restant | ✅ Présent | Template `panier_linge.html` |
| 8 | Prix total panier | ⚠️ SQL à compléter | `client_linge.py:51-55` |
| 9 | Affichage commandes | ⚠️ SQL à compléter | `client_commande.py:65-86` |
| 10 | Détail d'une commande | ⚠️ SQL à compléter | `client_commande.py:65-86` |
| 11 | Statut commande visible | ⚠️ À implémenter | `client_commande.py` |

#### Back-Office (Admin)
| # | Fonctionnalité | Statut | Fichier concerné |
|---|----------------|--------|------------------|
| 12 | Voir toutes les commandes | ⚠️ À implémenter | `admin_commande.py` |
| 13 | Détail commande (client + articles) | ⚠️ À implémenter | `admin_commande.py` |
| 14 | Changer état commande | ⚠️ À implémenter | `admin_commande.py` |
| 15 | Visualiser stock | ⚠️ SQL à compléter | `admin_linge.py:17-24` |
| 16 | Modifier stock article | ⚠️ SQL à compléter | `admin_linge.py:70-97` |
| - | Gestion stock (pas de commande si stock=0) | ⚠️ À vérifier | SQL à ajouter |

#### SQL à implémenter dans Livrable 2

**client_panier.py :**
- `client_panier_add()` : INSERT/UPDATE ligne_panier, vérifier stock
- `client_panier_delete()` : UPDATE quantité ou DELETE ligne_panier
- `client_panier_vider()` : DELETE toutes les lignes panier

**client_commande.py :**
- `client_commande_valide()` : SELECT panier + calcul prix total
- `client_commande_add()` : INSERT commande + lignes_commande + DELETE panier
- `client_commande_show()` : SELECT commandes + détails

**admin_linge.py :**
- `show_linge()` : Requête admin_linge_1 (liste avec stock)
- `valid_add_linge()` : Requête admin_linge_2 (INSERT)
- `delete_linge()` : Requêtes admin_linge_3,4,5 (vérif + DELETE)
- `edit_linge()` : Requêtes admin_linge_6,7 (SELECT)
- `valid_edit_linge()` : Requêtes admin_linge_8,9 (UPDATE)

---

### 🔄 Livrable 3 - Fonctionnalités avancées

**À rendre :** Quelques semaines avant vacances de Pâques
**Structure :** 1 tâche par étudiant (groupe de 3 ou 4)

#### Étudiant 1 : Gestion des déclinaisons (coloris)

**MLD à adapter :**
```sql
-- Nouvelle table pour gérer plusieurs coloris par linge
linge(id_linge, nom_linge, prix_linge, dimension, matiere, description,
      fournisseur, marque, image, #type_linge_id)
declinaison_linge(id_declinaison, #linge_id, #coloris_id, stock, prix)
coloris(id_coloris, nom_coloris)
```

**Front-Office :**
- [ ] Affichage nb déclinaisons dans boutique (requête SQL)
- [ ] Si plusieurs déclinaisons → interface choix coloris
- [ ] Stock restant par déclinaison
- [ ] Décrémenter/incrémenter stock déclinaison
- [ ] Prix total panier avec déclinaisons
- [ ] Affichage déclinaisons dans panier
- [ ] Commande : afficher prix, qté, déclinaison

**Back-Office :**
- [ ] Tableau articles avec nb déclinaisons et stock total
- [ ] Message si rupture stock déclinaison (=0)
- [ ] Interface compléter stock par déclinaison
- [ ] Interface ajouter/modifier/supprimer déclinaisons
- [ ] Gestion "coloris unique" (id=1)

**Dataviz :**
- [ ] Coût stock par déclinaison (coloris)
- [ ] Nombre articles par déclinaison

#### Étudiant 2 : Gestion commentaires et notes

**MLD à ajouter :**
```sql
commentaire(id_commentaire, texte, date_publication, #utilisateur_id,
            #linge_id, valide, #commentaire_parent_id)  -- parent_id pour réponses admin
note(id_note, valeur, #utilisateur_id, #linge_id)
```

**Front-Office :**
- [ ] Affichage nb commentaires + note moyenne (requête SQL, pas boucle Python)
- [ ] Uniquement client ayant acheté peut commenter/noter
- [ ] Affichage pseudo + id_commentaire
- [ ] Max 3 commentaires par article (vérif serveur + message flash)
- [ ] Une seule note par article (modifiable)
- [ ] Calcul note moyenne en SQL
- [ ] Commentaires ordonnés chronologiquement (inverse)
- [ ] Réponses admin insérées sous chaque commentaire

**Back-Office :**
- [ ] Indication nouveaux commentaires dans liste articles
- [ ] Nombre commentaires total vs validés
- [ ] Liste commentaires : validés (fond jaune), non-validés (fond blanc), réponses admin (fond vert)
- [ ] Répondre à un commentaire
- [ ] Supprimer un commentaire
- [ ] Valider (marquer comme lu) les commentaires
- [ ] Tri : non-validés d'abord (date desc), puis validés (date desc)

**Dataviz :**
- [ ] Tableau : nb notes, note moyenne, nb commentaires par catégorie
- [ ] Graphique note moyenne par catégorie
- [ ] Graphique nb commentaires par catégorie
- [ ] Graphique nb notes par catégorie
- [ ] Interface filtrée par catégorie (tableau + graphiques)

#### Étudiant 3 : Gestion des adresses

**MLD à ajouter :**
```sql
adresse(id_adresse, nom_adresse, rue, code_postal, ville,
        #utilisateur_id, valide, favorite)
-- Adresse liée à commande via copie pour conservation historique
```

**Front-Office :**
- [ ] Tableau adresses avec favorite (bleu) et non-valides (jaune)
- [ ] Nombre de commandes par adresse dans le tableau
- [ ] Afficher nb adresses valides vs total
- [ ] Max 4 adresses valides (vérif serveur + flash)
- [ ] Gestion adresse favorite (règles complexes, voir ci-dessous)
- [ ] Sélection adresse livraison/facturation lors commande (par défaut: favorite)
- [ ] Indication si adresses livraison/facturation identiques
- [ ] Ajout/modification/suppression adresse
- [ ] Vérification possession adresse (message flash orange si pb)
- [ ] Suppression/modification : gestion adresses utilisées en commande
- [ ] Code postal : 5 chiffres (vérif serveur + réaffichage données)
- [ ] Interface modification infos utilisateur (sans doublon email/login)

**Gestion adresse favorite (règles) :**
1. Création adresse → devient favorite
2. Commande passée → adresse utilisée devient favorite
3. Modification adresse favorite → modifiée devient favorite
4. Suppression adresse favorite → dernière utilisée valide devient favorite (date commande récente)

**Gestion suppression/modification adresses utilisées :**
- Adresse utilisée en commande → devient "non valide" (pas supprimée)
- Modification adresse utilisée → création doublon avec nouvelles infos, ancienne devient non valide
- Adresse non utilisée → modifiée/supprimée normalement

**Back-Office :**
- [ ] Voir adresses livraison et facturation dans détail commande

**Dataviz :**
- [ ] Tableau : nb ventes, CA par département (2 chiffres CP)
- [ ] Graphique nb ventes par département
- [ ] Graphique CA par département
- [ ] Carte géographique (France) avec ventes/CA par département

#### Étudiant 4 (groupe de 4 uniquement) : Liste d'envies et historique

**MLD à ajouter :**
```sql
liste_envie(id_liste_envie, #utilisateur_id, #linge_id, date_ajout, ordre)
historique(id_historique, #utilisateur_id, #linge_id, date_consultation, nb_consultations)
```

**Liste d'envies (Wishlist) :**
- [ ] Ajout/suppression via 💛 (coeur jaune/blanc)
- [ ] Article commandé → retiré de la wishlist
- [ ] Affichage décroissant par date d'ajout
- [ ] Affichage nb articles wishlist + historique (requête SQL)
- [ ] Interface monter/descendre articles (ordre personnalisé)
- [ ] Clic article → affichage nb autres clients ayant cet article en wishlist
- [ ] Clic article → affichage nb autres articles même catégorie dans wishlist

**Historique consultations :**
- [ ] Historique = articles consultés (clic photo)
- [ ] Affichage ordre consultation
- [ ] Max 6 articles différents (6 derniers consultés)
- [ ] Stockage nb consultations par article
- [ ] Suppression auto après 1 mois
- [ ] Pas de doublon dans historique

**Dataviz :**
- [ ] Tableau : nb articles wishlist par catégorie
- [ ] Graphique nb articles wishlist par catégorie
- [ ] Graphique nb articles historique sur le mois par catégorie
- [ ] Interface filtrée par catégorie (tableau + graphiques)

---

## Configuration requise

### Variables d'environnement (.env)
```bash
HOST=localhost
USER=root
PASSWORD=votre_mot_de_passe
DATABASE=sae_linge
```

### Lancement
```bash
cd Flask
chmod +x flask_run.sh
./flask_run.sh
# ou
python app.py
```

---

## Points critiques SQL à implémenter

### Livrable 2 - Requêtes essentielles

```python
# client_panier.py - client_panier_add()
# Vérifier si article déjà dans panier
sql_check = """SELECT * FROM ligne_panier
               WHERE utilisateur_id = %s AND linge_id = %s"""

# Si existe : UPDATE quantite
sql_update = """UPDATE ligne_panier
                SET quantite = quantite + %s
                WHERE utilisateur_id = %s AND linge_id = %s"""

# Sinon : INSERT
sql_insert = """INSERT INTO ligne_panier
                (utilisateur_id, linge_id, quantite, date_ajout)
                VALUES (%s, %s, %s, NOW())"""

# Décrémenter stock
sql_stock = """UPDATE linge
               SET stock = stock - %s
               WHERE id_linge = %s AND stock >= %s"""

# client_commande.py - client_commande_add()
# Créer commande
sql_commande = """INSERT INTO commande
                  (date_achat, utilisateur_id, etat_id)
                  VALUES (NOW(), %s, 1)"""  # état 1 = "En attente"

# Récupérer id commande
sql_last_id = """SELECT LAST_INSERT_ID() as last_insert_id"""

# Ajouter lignes commande depuis panier
sql_ligne = """INSERT INTO ligne_commande
               (commande_id, linge_id, quantite, prix)
               SELECT %s, lp.linge_id, lp.quantite, l.prix_linge
               FROM ligne_panier lp
               JOIN linge l ON lp.linge_id = l.id_linge
               WHERE lp.utilisateur_id = %s"""

# Vider panier
sql_delete_panier = """DELETE FROM ligne_panier
                       WHERE utilisateur_id = %s"""
```

### Livrable 3 - Requêtes complexes

```python
# Calcul nb commentaires + note moyenne (sans boucle Python)
sql_stats = """SELECT
    l.id_linge,
    l.nom_linge,
    COUNT(DISTINCT c.id_commentaire) as nb_commentaires,
    AVG(n.valeur) as note_moyenne,
    COUNT(DISTINCT n.id_note) as nb_notes
FROM linge l
LEFT JOIN commentaire c ON l.id_linge = c.linge_id AND c.valide = 1
LEFT JOIN note n ON l.id_linge = n.linge_id
GROUP BY l.id_linge, l.nom_linge"""

# Nombre de clients ayant article en wishlist
sql_wishlist = """SELECT COUNT(DISTINCT utilisateur_id) as nb_clients
                  FROM liste_envie
                  WHERE linge_id = %s AND utilisateur_id != %s"""
```

---

## Ressources et liens

- Schéma BDD : `Flask/sae_sql.sql`
- Consignes complètes : `consignes.html`
- Démonstration Livrable 2 : http://amillet2.pythonanywhere.com/
- Démonstration Livrable 3 : http://amillet4.pythonanywhere.com/
- Exemple linge : https://www.linvosges.com/fr/la-salle-de-bain/tapis-de-bain/

---

## Checklist avant rendu

### Livrable 2
- [ ] `/base/init` fonctionne parfaitement
- [ ] Tests sur machine IUT réussis
- [ ] Panier fonctionnel (ajout/suppression/quantité)
- [ ] Commande créée avec succès
- [ ] Stock vérifié avant ajout panier
- [ ] Admin peut voir/modifier commandes
- [ ] Fichier SQL à jour et complet
- [ ] Archive .zip propre (pas de __pycache__)

### Livrable 3
- [ ] Ma partie fonctionne indépendamment
- [ ] Requêtes SQL optimisées (pas de boucles Python pour les données)
- [ ] Messages flash visibles pour erreurs/succès
- [ ] Dataviz fonctionnelle (graphiques)
- [ ] Jeu de test de qualité (données réalistes)
- [ ] Présentation orale préparée
