#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, redirect
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    
    sql_commands = [
        "DROP TABLE IF EXISTS ligne_panier",
        "DROP TABLE IF EXISTS ligne_commande",
        "DROP TABLE IF EXISTS linge",
        "DROP TABLE IF EXISTS commande",
        "DROP TABLE IF EXISTS utilisateur",
        "DROP TABLE IF EXISTS etat",
        "DROP TABLE IF EXISTS type_linge",
        "DROP TABLE IF EXISTS coloris",
        
        "CREATE TABLE coloris (id_coloris INT AUTO_INCREMENT, nom_coloris VARCHAR(50) NOT NULL, PRIMARY KEY (id_coloris)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
        
        "CREATE TABLE type_linge (id_type_linge INT AUTO_INCREMENT, nom_type_linge VARCHAR(50) NOT NULL, PRIMARY KEY (id_type_linge)) CHARSET=utf8mb4",
        
        "CREATE TABLE etat (id_etat INT AUTO_INCREMENT, libelle VARCHAR(50) NOT NULL, PRIMARY KEY (id_etat)) CHARSET=utf8mb4",
        
        "CREATE TABLE utilisateur (id_utilisateur INT AUTO_INCREMENT, login VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, nom VARCHAR(255) NOT NULL, role VARCHAR(50) NOT NULL, PRIMARY KEY (id_utilisateur)) CHARSET=utf8mb4",
        
        "CREATE TABLE linge (id_linge INT AUTO_INCREMENT, nom_linge VARCHAR(100) NOT NULL, prix_linge DECIMAL(10,2) NOT NULL, dimension VARCHAR(50), matiere VARCHAR(50), description TEXT, fournisseur VARCHAR(100), marque VARCHAR(100), image VARCHAR(255), stock INT DEFAULT 0, coloris_id INT, type_linge_id INT, PRIMARY KEY (id_linge), CONSTRAINT fk_linge_coloris FOREIGN KEY (coloris_id) REFERENCES coloris(id_coloris), CONSTRAINT fk_linge_type FOREIGN KEY (type_linge_id) REFERENCES type_linge(id_type_linge)) CHARSET=utf8mb4",
        
        "INSERT INTO coloris (nom_coloris) VALUES ('Blanc Pur'), ('Gris Anthracite'), ('Bleu Marine'), ('Vieux Rose'), ('Vert Sauge'), ('Jaune Moutarde')",
        
        "INSERT INTO type_linge (nom_type_linge) VALUES ('Linge de Lit'), ('Linge de Bain'), ('Linge de Table'), ('Décoration')",
        
        "INSERT INTO etat (libelle) VALUES ('En attente'), ('Expédié'), ('Validé'), ('Annulé')",
        
        "INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES (1,'admin','admin@admin.fr','scrypt:32768:8:1$irSP6dJEjy1yXof2$56295be51bb989f467598b63ba6022405139656d6609df8a71768d42738995a21605c9acbac42058790d30fd3adaaec56df272d24bed8385e66229c81e71a4f4','ROLE_admin','admin'), (2,'client','client@client.fr','scrypt:32768:8:1$iFP1d8bdBmhW6Sgc$7950bf6d2336d6c9387fb610ddaec958469d42003fdff6f8cf5a39cf37301195d2e5cad195e6f588b3644d2a9116fa1636eb400b0cb5537603035d9016c15910','ROLE_client','client')",
        
        "INSERT INTO linge (nom_linge, prix_linge, dimension, matiere, image, type_linge_id) VALUES ('Housse Percaline', 55.00, '240x220', 'Coton', 'housse_blanc.jpg', 1), ('Drap Housse Bio', 19.90, '140x190', 'Coton bio', 'drap_gris.jpg', 1), ('Taie Lin Lavé', 12.00, '65x65', 'Lin', 'taie_rose.jpg', 1), ('Parure Satinée', 89.00, '260x240', 'Satin', 'parrure_marine.jpg', 1), ('Drap de Douche', 14.50, '70x140', 'Éponge', 'serviette_verte.jpg', 2), ('Peignoir Mixte', 45.00, 'L', 'Coton', 'peignoir_gris.jpg', 2), ('Gant de toilette', 3.50, '15x21', 'Éponge', 'gant_blanc.jpg', 2), ('Tapis de Bain', 22.00, '50x80', 'Microfibre', 'tapis_jaune.jpg', 2), ('Nappe Anti-tache', 35.00, '150x250', 'Polyester', 'nappe_grise.jpg', 3), ('Serviettes Table (x4)', 16.00, '40x40', 'Lin', 'serviette_table.jpg', 3), ('Chemin de Table', 18.00, '40x140', 'Coton', 'chemin_table.jpg', 3), ('Plaid Polaire XL', 29.90, '180x220', 'Polyester', 'plaid_marine.jpg', 4), ('Coussin Velours', 15.00, '45x45', 'Velours', 'coussin_jaune.jpg', 4), ('Rideau Occultant', 39.00, '140x260', 'Tissage', 'rideau_gris.jpg', 4), ('Torchon Cuisine', 5.50, '50x70', 'Coton', 'torchon_blanc.jpg', 3)"
    ]

    
    for command in sql_commands:
        mycursor.execute(command)        
    get_db().commit()
    return redirect('/')
