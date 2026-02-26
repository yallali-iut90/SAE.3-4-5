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

    # 1. Récupération des filtres en session
    filter_types = session.get('filter_types', [])
    filter_word = session.get('filter_word', '')
    filter_prix_min = session.get('filter_prix_min', '')
    filter_prix_max = session.get('filter_prix_max', '')

    # Construction de la requête SQL avec filtres dynamiques
    where_conditions = []
    params = []

    # Filtre par type
    if filter_types:
        placeholders = ','.join(['%s'] * len(filter_types))
        where_conditions.append(f'type_linge_id IN ({placeholders})')
        params.extend(filter_types)

    # Filtre par nom (recherche)
    if filter_word:
        where_conditions.append('nom_linge LIKE %s')
        params.append(f'%{filter_word}%')

    # Filtre par prix min
    if filter_prix_min:
        try:
            prix_min = float(filter_prix_min)
            where_conditions.append('prix_linge >= %s')
            params.append(prix_min)
        except ValueError:
            pass

    # Filtre par prix max
    if filter_prix_max:
        try:
            prix_max = float(filter_prix_max)
            where_conditions.append('prix_linge <= %s')
            params.append(prix_max)
        except ValueError:
            pass

    # Construction de la requête finale
    sql_base = '''
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
    '''

    if where_conditions:
        sql_linge = sql_base + ' WHERE ' + ' AND '.join(where_conditions) + ' ORDER BY nom ASC'
        mycursor.execute(sql_linge, tuple(params))
    else:
        sql_linge = sql_base + ' ORDER BY nom ASC'
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
