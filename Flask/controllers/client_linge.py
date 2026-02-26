#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from connexion_db import get_db

client_linge = Blueprint('client_linge', __name__,
                        template_folder='templates')

@client_linge.route('/client/index')
@client_linge.route('/client/linge/show')
def client_linge_show():
    mycursor = get_db().cursor()
    # On récupère l'id de l'utilisateur pour le panier (même si vide pour l'instant)
    id_client = session.get('id_user')

    # 1. Récupération du jeu de test : les linges (avec filtre si présent en session)
    filter_types = session.get('filter_types', [])

    if filter_types:
        # Filtre actif : récupérer seulement les linges des types sélectionnés
        placeholders = ','.join(['%s'] * len(filter_types))
        sql_linge = f'''
            SELECT
                id_linge,
                nom_linge AS nom,
                prix_linge AS prix,
                dimension,
                matiere,
                description,
                fournisseur,
                marque,
                image,
                stock,
                coloris_id,
                type_linge_id
            FROM linge
            WHERE type_linge_id IN ({placeholders})
            ORDER BY nom ASC
        '''
        mycursor.execute(sql_linge, tuple(filter_types))
    else:
        # Pas de filtre : récupérer tous les linges
        sql_linge = '''SELECT
            id_linge,
            nom_linge AS nom,
            prix_linge AS prix,
            dimension,
            matiere,
            description,
            fournisseur,
            marque,
            image,
            stock,
            coloris_id,
            type_linge_id
         FROM linge
         ORDER BY nom ASC'''
        mycursor.execute(sql_linge)

    linges = mycursor.fetchall()

    # 2. Récupération des types de linge pour le filtre
    sql_types = "SELECT * FROM type_linge ORDER BY nom_type_linge ASC;"
    mycursor.execute(sql_types)
    types_linge = mycursor.fetchall()

    # 3. Récupération du panier du client connecté
    sql_panier = '''
        SELECT
            lp.linge_id as id_linge,
            l.nom_linge as nom,
            lp.quantite,
            l.prix_linge as prix,
            l.stock
        FROM ligne_panier lp
        JOIN linge l ON lp.linge_id = l.id_linge
        WHERE lp.utilisateur_id = %s
        ORDER BY lp.date_ajout DESC
    '''
    mycursor.execute(sql_panier, (id_client,))
    linge_panier = mycursor.fetchall()

    # 4. Calcul du prix total du panier
    prix_total = 0
    if len(linge_panier) >= 1:
        sql_prix_total = '''
            SELECT SUM(lp.quantite * l.prix_linge) as total
            FROM ligne_panier lp
            JOIN linge l ON lp.linge_id = l.id_linge
            WHERE lp.utilisateur_id = %s
        '''
        mycursor.execute(sql_prix_total, (id_client,))
        result = mycursor.fetchone()
        if result and result['total'] is not None:
            prix_total = result['total']

    return render_template('client/boutique/panier_linge.html',
                           linges=linges,
                           items_filtre=types_linge,
                           linge_panier=linge_panier,
                           prix_total=prix_total)
