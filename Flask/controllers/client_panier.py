#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_linge = request.form.get('id_linge')
    quantite = int(request.form.get('quantite', 1))

    # Vérifier le stock disponible
    sql_stock = "SELECT stock FROM linge WHERE id_linge = %s"
    mycursor.execute(sql_stock, (id_linge,))
    stock_result = mycursor.fetchone()

    if not stock_result or stock_result['stock'] < quantite:
        flash('Stock insuffisant pour cet article', 'alert-warning')
        return redirect('/client/linge/show')

    # Vérifier si l'article est déjà dans le panier
    sql_check = """
        SELECT quantite FROM ligne_panier
        WHERE utilisateur_id = %s AND linge_id = %s
    """
    mycursor.execute(sql_check, (id_client, id_linge))
    panier_existant = mycursor.fetchone()

    if panier_existant:
        # Article déjà dans le panier : mettre à jour la quantité
        nouvelle_quantite = panier_existant['quantite'] + quantite

        # Vérifier que le nouveau total ne dépasse pas le stock
        if nouvelle_quantite > stock_result['stock']:
            flash('Quantité totale demandée supérieure au stock disponible', 'alert-warning')
            return redirect('/client/linge/show')

        sql_update = """
            UPDATE ligne_panier
            SET quantite = %s, date_ajout = NOW()
            WHERE utilisateur_id = %s AND linge_id = %s
        """
        mycursor.execute(sql_update, (nouvelle_quantite, id_client, id_linge))
    else:
        # Nouvel article dans le panier
        sql_insert = """
            INSERT INTO ligne_panier (utilisateur_id, linge_id, quantite, date_ajout)
            VALUES (%s, %s, %s, NOW())
        """
        mycursor.execute(sql_insert, (id_client, id_linge, quantite))

    # Décrémenter le stock
    sql_decrement = "UPDATE linge SET stock = stock - %s WHERE id_linge = %s"
    mycursor.execute(sql_decrement, (quantite, id_linge))

    get_db().commit()
    flash('Article ajouté au panier', 'alert-success')
    return redirect('/client/linge/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_linge = request.form.get('id_linge','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'linge
    # id_declinaison_linge = request.form.get('id_declinaison_linge', None)

    sql = ''' selection de la ligne du panier pour l'linge et l'utilisateur connecté'''
    linge_panier=[]

    if not(linge_panier is None) and linge_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 linge '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'linge disponible
    get_db().commit()
    return redirect('/client/linge/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'linge pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'linge : stock = stock + qté de la ligne pour l'linge'''
        get_db().commit()
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_linge = request.form.get('id_declinaison_linge')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'linge : stock = stock + qté de la ligne pour l'linge'''

    get_db().commit()
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/linge/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/linge/show')
