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
    # sql = '''         '''
    # mycursor.execute(sql)
    # types_boisson = mycursor.fetchall()
    types_boisson=[]
    return render_template('admin/type_boisson/show_type_boisson.html', types_boisson=types_boisson)

@admin_type_boisson.route('/admin/type-boisson/add', methods=['GET'])
def add_type_boisson():
    return render_template('admin/type_boisson/add_type_boisson.html')

@admin_type_boisson.route('/admin/type-boisson/add', methods=['POST'])
def valid_add_type_boisson():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    mycursor = get_db().cursor()
    sql = '''         '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-boisson/show') #url_for('show_type_boisson')

@admin_type_boisson.route('/admin/type-boisson/delete', methods=['GET'])
def delete_type_boisson():
    id_type_boisson = request.args.get('id_type_boisson', '')
    mycursor = get_db().cursor()

    flash(u'suppression type boisson , id : ' + id_type_boisson, 'alert-success')
    return redirect('/admin/type-boisson/show')

@admin_type_boisson.route('/admin/type-boisson/edit', methods=['GET'])
def edit_type_boisson():
    id_type_boisson = request.args.get('id_type_boisson', '')
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, (id_type_boisson,))
    type_boisson = mycursor.fetchone()
    return render_template('admin/type_boisson/edit_type_boisson.html', type_boisson=type_boisson)

@admin_type_boisson.route('/admin/type-boisson/edit', methods=['POST'])
def valid_edit_type_boisson():
    libelle = request.form['libelle']
    id_type_boisson = request.form.get('id_type_boisson', '')
    tuple_update = (libelle, id_type_boisson)
    mycursor = get_db().cursor()
    sql = '''   '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type boisson modifié, id: ' + id_type_boisson + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-boisson/show')








