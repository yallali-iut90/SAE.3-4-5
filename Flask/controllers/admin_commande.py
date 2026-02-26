#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()

    # Récupérer toutes les commandes avec infos client
    sql = '''
        SELECT
            c.id_commande,
            c.date_achat,
            c.etat_id,
            e.libelle,
            u.login,
            SUM(lc.quantite) as nbr_linges,
            SUM(lc.quantite * lc.prix) as prix_total
        FROM commande c
        JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
        JOIN etat e ON c.etat_id = e.id_etat
        LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
        GROUP BY c.id_commande, c.date_achat, c.etat_id, e.libelle, u.login
        ORDER BY c.etat_id ASC, c.date_achat DESC
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    linges_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)

    if id_commande:
        # Détails de la commande (avec infos pour le template)
        sql_details = '''
            SELECT
                lc.linge_id,
                l.nom_linge as nom,
                lc.quantite,
                lc.prix,
                (lc.quantite * lc.prix) as prix_ligne,
                c.etat_id,
                c.id_commande as id
            FROM ligne_commande lc
            JOIN linge l ON lc.linge_id = l.id_linge
            JOIN commande c ON lc.commande_id = c.id_commande
            WHERE lc.commande_id = %s
        '''
        mycursor.execute(sql_details, (id_commande,))
        linges_commande = mycursor.fetchall()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           linges_commande=linges_commande,
                           commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)

    if commande_id:
        # Changer l'état de la commande (1: En attente -> 2: Expédié)
        # ou passer à l'état suivant selon votre logique métier
        sql = '''
            UPDATE commande
            SET etat_id = CASE
                WHEN etat_id = 1 THEN 2 
                WHEN etat_id = 2 THEN 3  
                ELSE etat_id
            END
            WHERE id_commande = %s
        '''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
        flash('État de la commande mis à jour', 'alert-success')

    return redirect('/admin/commande/show')
