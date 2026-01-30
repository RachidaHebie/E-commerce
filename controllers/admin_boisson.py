#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_boisson = Blueprint('admin_boisson', __name__,
                          template_folder='templates')


@admin_boisson.route('/admin/boisson/show')
def show_boisson():
    mycursor = get_db().cursor()
    sql = '''  requête admin_boisson_1
    '''
    mycursor.execute(sql)
    boissons = mycursor.fetchall()
    return render_template('admin/boisson/show_boisson.html', boissons=boissons)


@admin_boisson.route('/admin/boisson/add', methods=['GET'])
def add_boisson():
    mycursor = get_db().cursor()

    return render_template('admin/boisson/add_boisson.html'
                           #,types_boisson=type_boisson,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_boisson.route('/admin/boisson/add', methods=['POST'])
def valid_add_boisson():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_boisson_id = request.form.get('type_boisson_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_boisson_2 '''

    tuple_add = (nom, filename, prix, type_boisson_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'boisson ajouté , nom: ', nom, ' - type_boisson:', type_boisson_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'boisson ajouté , nom:' + nom + '- type_boisson:' + type_boisson_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/boisson/show')


@admin_boisson.route('/admin/boisson/delete', methods=['GET'])
def delete_boisson():
    id_boisson=request.args.get('id_boisson')
    mycursor = get_db().cursor()
    sql = ''' requête admin_boisson_3 '''
    mycursor.execute(sql, id_boisson)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet boisson : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_boisson_4 '''
        mycursor.execute(sql, id_boisson)
        boisson = mycursor.fetchone()
        print(boisson)
        image = boisson['image']

        sql = ''' requête admin_boisson_5  '''
        mycursor.execute(sql, id_boisson)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un boisson supprimé, id :", id_boisson)
        message = u'un boisson supprimé, id : ' + id_boisson
        flash(message, 'alert-success')

    return redirect('/admin/boisson/show')


@admin_boisson.route('/admin/boisson/edit', methods=['GET'])
def edit_boisson():
    id_boisson=request.args.get('id_boisson')
    mycursor = get_db().cursor()
    sql = '''
    requête admin_boisson_6    
    '''
    mycursor.execute(sql, id_boisson)
    boisson = mycursor.fetchone()
    print(boisson)
    sql = '''
    requête admin_boisson_7
    '''
    mycursor.execute(sql)
    types_boisson = mycursor.fetchall()

    # sql = '''
    # requête admin_boisson_6
    # '''
    # mycursor.execute(sql, id_boisson)
    # declinaisons_boisson = mycursor.fetchall()

    return render_template('admin/boisson/edit_boisson.html'
                           ,boisson=boisson
                           ,types_boisson=types_boisson
                         #  ,declinaisons_boisson=declinaisons_boisson
                           )


@admin_boisson.route('/admin/boisson/edit', methods=['POST'])
def valid_edit_boisson():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_boisson = request.form.get('id_boisson')
    image = request.files.get('image', '')
    type_boisson_id = request.form.get('type_boisson_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
       requête admin_boisson_8
       '''
    mycursor.execute(sql, id_boisson)
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

    sql = '''  requête admin_boisson_9 '''
    mycursor.execute(sql, (nom, image_nom, prix, type_boisson_id, description, id_boisson))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'boisson modifié , nom:' + nom + '- type_boisson :' + type_boisson_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/boisson/show')







@admin_boisson.route('/admin/boisson/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    boisson=[]
    commentaires = {}
    return render_template('admin/boisson/show_avis.html'
                           , boisson=boisson
                           , commentaires=commentaires
                           )


@admin_boisson.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    boisson_id = request.form.get('idboisson', None)
    userId = request.form.get('idUser', None)

    return admin_avis(boisson_id)
