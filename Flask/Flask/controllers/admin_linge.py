#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_linge = Blueprint('admin_linge', __name__,
                          template_folder='templates')


@admin_linge.route('/admin/linge/show')
def show_linge():
    mycursor = get_db().cursor()
    sql = '''  requête admin_linge_1
    '''
    mycursor.execute(sql)
    linges = mycursor.fetchall()
    return render_template('admin/linge/show_linge.html', linges=linges)


@admin_linge.route('/admin/linge/add', methods=['GET'])
def add_linge():
    mycursor = get_db().cursor()

    return render_template('admin/linge/add_linge.html'
                           #,types_linge=type_linge,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_linge.route('/admin/linge/add', methods=['POST'])
def valid_add_linge():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_linge_id = request.form.get('type_linge_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_linge_2 '''

    tuple_add = (nom, filename, prix, type_linge_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'linge ajouté , nom: ', nom, ' - type_linge:', type_linge_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'linge ajouté , nom:' + nom + '- type_linge:' + type_linge_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/linge/show')


@admin_linge.route('/admin/linge/delete', methods=['GET'])
def delete_linge():
    id_linge=request.args.get('id_linge')
    mycursor = get_db().cursor()
    sql = ''' requête admin_linge_3 '''
    mycursor.execute(sql, id_linge)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet linge : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_linge_4 '''
        mycursor.execute(sql, id_linge)
        linge = mycursor.fetchone()
        print(linge)
        image = linge['image']

        sql = ''' requête admin_linge_5  '''
        mycursor.execute(sql, id_linge)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un linge supprimé, id :", id_linge)
        message = u'un linge supprimé, id : ' + id_linge
        flash(message, 'alert-success')

    return redirect('/admin/linge/show')


@admin_linge.route('/admin/linge/edit', methods=['GET'])
def edit_linge():
    id_linge=request.args.get('id_linge')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_linge_6    
    '''
    mycursor.execute(sql, id_linge)
    linge = mycursor.fetchone()
    print(linge)
    sql = '''
    requête admin_linge_7
    '''
    mycursor.execute(sql)
    types_linge = mycursor.fetchall()

    # sql = '''
    # requête admin_linge_6
    # '''
    # mycursor.execute(sql, id_linge)
    # declinaisons_linge = mycursor.fetchall()

    return render_template('admin/linge/edit_linge.html'
                           ,linge=linge
                           ,types_linge=types_linge
                         #  ,declinaisons_linge=declinaisons_linge
                           )


@admin_linge.route('/admin/linge/edit', methods=['POST'])
def valid_edit_linge():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_linge = request.form.get('id_linge')
    image = request.files.get('image', '')
    type_linge_id = request.form.get('type_linge_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_linge_8
       '''
    mycursor.execute(sql, id_linge)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''  requête admin_linge_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_linge_id, description, id_linge))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'linge modifié , nom:' + nom + '- type_linge :' + type_linge_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/linge/show')







@admin_linge.route('/admin/linge/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    linge=[]
    commentaires = {}
    return render_template('admin/linge/show_avis.html'
                           , linge=linge
                           , commentaires=commentaires
                           )


@admin_linge.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    linge_id = request.form.get('idlinge', None)
    userId = request.form.get('idUser', None)

    return admin_avis(linge_id)
