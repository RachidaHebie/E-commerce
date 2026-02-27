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
    sql = '''  SELECT * FROM boisson; '''
    mycursor.execute(sql)
    boissons = mycursor.fetchall()
    return render_template('admin/boisson/show_boisson.html', boissons=boissons)


@admin_boisson.route('/admin/boisson/add', methods=['GET'])
def add_boisson():
    mycursor = get_db().cursor()

    sql = "SELECT id_type_boisson, nom_type_boisson FROM type_boisson ORDER BY nom_type_boisson;"
    mycursor.execute(sql)
    types_boisson = mycursor.fetchall()


    sql = "SELECT id_fruit, nom_fruit FROM fruit ORDER BY nom_fruit;"
    mycursor.execute(sql)
    fruits = mycursor.fetchall()


    return render_template('admin/boisson/add_boisson.html',
                           types_boisson=types_boisson,
                           fruits=fruits)


@admin_boisson.route('/admin/boisson/add', methods=['POST'])
def valid_add_boisson():
    mycursor = get_db().cursor()
    stock= request.form.get('stock', '')
    nom = request.form.get('nom', '')
    id_fruit = request.form.get('id_fruit', '')
    id_type_boisson = request.form.get('id_type_boisson', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''
          INSERT INTO boisson (nom_boisson, image, prix_boisson, id_type_boisson,id_fruit,
                                description ,stock)
          VALUES (%s, %s, %s, %s, %s,%s,%s) 
          '''

    tuple_add = (nom, filename, prix, id_type_boisson,id_fruit, description,stock)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'boisson ajouté , nom: ', nom, ' - type_boisson:', id_type_boisson, ' - prix:', prix,
          ' - description:', description, ' - image:', image, ' - stock:', stock)
    message = u'boisson ajouté , nom:' + nom + '- type_boisson:' + id_type_boisson + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
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
    SELECT * FROM boisson WHERE id_boisson=%s   
    '''
    mycursor.execute(sql, id_boisson)
    boisson = mycursor.fetchone()
    print(boisson)
    sql = '''
   SELECT nom_type_boisson, id_type_boisson FROM type_boisson ORDER BY id_type_boisson ASC
    '''
    mycursor.execute(sql)
    type_boisson = mycursor.fetchall()

    # sql = '''
    # requête admin_boisson_6
    # '''
    # mycursor.execute(sql, id_boisson)
    # declinaisons_boisson = mycursor.fetchall()

    return render_template('admin/boisson/edit_boisson.html'
                           ,boisson=boisson
                           ,type_boisson=type_boisson
                         #  ,declinaisons_boisson=declinaisons_boisson
                           )


@admin_boisson.route('/admin/boisson/edit', methods=['POST'])
def valid_edit_boisson():
    mycursor = get_db().cursor()
    nom_boisson = request.form.get('nom_boisson')
    id_boisson = request.form.get('id_boisson')
    image = request.files.get('image', '')
    id_type_boisson = request.form.get('id_type_boisson', '')
    prix_boisson= request.form.get('prix_boisson', '')
    description = request.form.get('description')
    stock = request.form.get('stock')
    sql = '''
        UPDATE boisson SET nom_boisson= %s, id_boisson = %s, prix_boisson= %s,description= %s, stock = %s, image = %s,id_type_boisson=%s
          WHERE id = %s 
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
    mycursor.execute(sql, (nom_boisson, image_nom, prix_boisson, id_type_boisson, description, id_boisson,stock))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'boisson modifié , nom:' + nom_boisson + '- type_boisson :' + id_type_boisson + ' - prix:' + prix_boisson  + ' - image:' + image + ' - description: ' + description
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
