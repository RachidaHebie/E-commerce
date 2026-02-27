#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_boisson = Blueprint('admin_type_boisson', __name__,
                        template_folder='templates')

@admin_type_boisson.route('/admin/type-boisson/show')
def show_type_boisson():
    mycursor = get_db().cursor()
    sql = '''  SELECT t.id_type_boisson, t.nom_type_boisson, COUNT(b.id_boisson) AS nbr_boissons
        FROM type_boisson t
        LEFT JOIN boisson b ON t.id_type_boisson = b.id_type_boisson
        GROUP BY t.id_type_boisson, t.nom_type_boisson;   '''
    mycursor.execute(sql)
    types_boisson = mycursor.fetchall()

    return render_template('admin/type_boisson/show_type_boisson.html', types_boisson=types_boisson)

@admin_type_boisson.route('/admin/type-boisson/add', methods=['GET'])
def add_type_boisson():
    return render_template('admin/type_boisson/add_type_boisson.html')

@admin_type_boisson.route('/admin/type-boisson/add', methods=['POST'])
def valid_add_type_boisson():
    nom_type_boisson = request.form.get('nom_type_boisson', '')
    tuple_insert = (nom_type_boisson,)
    mycursor = get_db().cursor()
    sql = "insert into type_boisson (nom_type_boisson) values (%s)"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+nom_type_boisson
    flash(message, 'alert-success')
    return redirect('/admin/type-boisson/show') #url_for('show_type_boisson')

@admin_type_boisson.route('/admin/type-boisson/delete', methods=['GET'])
def delete_type_boisson():
    id_type_boisson = request.args.get('id_type_boisson', '')

    mycursor = get_db().cursor()

    sql = """SELECT boisson.id_boisson FROM ligne_commande
          JOIN boisson ON boisson.id_boisson = ligne_commande.id_boisson
          WHERE boisson.id_type_boisson = %s;"""
    mycursor.execute(sql, (id_type_boisson,))
    presence_boisson = mycursor.fetchall()

    if presence_boisson:
        ids_boissons = [str(boisson['id_boisson']) for boisson in presence_boisson]
        ids_str = ", ".join(ids_boissons)
        print("Impossible de supprimer le type de boisson, commande en cours de id : ", {ids_str})
        message = f'Impossible de supprimer le type de boisson, commande en cours de id : ' + ids_str
        flash(message, 'alert-danger')
    else :
        sql = '''
            DELETE FROM type_boisson
            WHERE id_type_boisson = %s
        '''
        mycursor.execute(sql, (id_type_boisson,))
        get_db().commit()

        flash(u'Suppression type boisson, id : ' + id_type_boisson, 'alert-success')
    return redirect('/admin/type-boisson/show')

@admin_type_boisson.route('/admin/type-boisson/edit', methods=['GET'])
def edit_type_boisson():
    id_type_boisson = request.args.get('id_type_boisson', '')
    mycursor = get_db().cursor()
    sql = ''' select id_type_boisson,nom_type_boisson from type_boisson where id_type_boisson = %s;  '''
    mycursor.execute(sql, (id_type_boisson,))
    type_boisson = mycursor.fetchone()
    return render_template('admin/type_boisson/edit_type_boisson.html', type_boisson=type_boisson)

@admin_type_boisson.route('/admin/type-boisson/edit', methods=['POST'])
def valid_edit_type_boisson():
    mycursor = get_db().cursor()
    nom_type_boisson = request.form['nom_type_boisson']
    id_type_boisson = request.form.get('id_type_boisson', '')
    tuple_update = (nom_type_boisson, id_type_boisson)

    sql = '''update type_boisson set nom_type_boisson=%s where id_type_boisson = %s    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type boisson modifié, id: ' + id_type_boisson + " libelle : " + nom_type_boisson, 'alert-success')
    return redirect('/admin/type-boisson/show')








