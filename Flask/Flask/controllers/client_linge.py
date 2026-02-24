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

    # 1. Récupération du jeu de test : les linges
    sql_linge = '''SELECT     
    id_linge, 
    nom_linge  AS nom,
    prix_linge  AS prix,
    dimension ,
    matiere ,
    description ,
    fournisseur ,
    marque ,
    image ,
    stock ,
    coloris_id ,
    type_linge_id 
     FROM linge 
     ORDER BY nom ASC;'''
    mycursor.execute(sql_linge)
    linges = mycursor.fetchall()

    # 2. Récupération des types de linge pour le futur filtre
    sql_types = "SELECT * FROM type_linge ORDER BY nom_type_linge ASC;"
    mycursor.execute(sql_types)
    types_linge = mycursor.fetchall()

    # Initialisation des variables pour éviter les erreurs Jinja2 dans le template
    linge_panier = []
    prix_total = None

    return render_template('client/boutique/panier_linge.html',
                           linges=linges,
                           items_filtre=types_linge,
                           linge_panier=linge_panier,
                           prix_total=prix_total)

    if len(linge_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_linge.html'
                           , linge=linge
                           , linge_panier=linge_panier
                           #, prix_total=prix_total
                           , items_filtre=types_linge
                           )
