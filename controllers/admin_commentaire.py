#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/boisson/commentaires', methods=['GET'])
def admin_boisson_details():
    mycursor = get_db().cursor()
    id_boisson =  request.args.get('id_boisson', None)
    sql = '''    requête admin_type_boisson_1    '''
    commentaires = {}
    sql = '''   requête admin_type_boisson_1_bis   '''
    boisson = []
    sql = '''   requête admin_type_boisson_1_3   '''
    nb_commentaires = []
    return render_template('admin/boisson/show_boisson_commentaires.html'
                           , commentaires=commentaires
                           , boisson=boisson
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/boisson/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_boisson = request.form.get('id_boisson', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_boisson_2   '''
    tuple_delete=(id_utilisateur,id_boisson,date_publication)
    get_db().commit()
    return redirect('/admin/boisson/commentaires?id_boisson='+id_boisson)


@admin_commentaire.route('/admin/boisson/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_boisson = request.args.get('id_boisson', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/boisson/add_commentaire.html',id_utilisateur=id_utilisateur,id_boisson=id_boisson,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_boisson = request.form.get('id_boisson', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_boisson_3   '''
    get_db().commit()
    return redirect('/admin/boisson/commentaires?id_boisson='+id_boisson)


@admin_commentaire.route('/admin/boisson/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_boisson = request.args.get('id_boisson', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_boisson_4   '''
    get_db().commit()
    return redirect('/admin/boisson/commentaires?id_boisson='+id_boisson)