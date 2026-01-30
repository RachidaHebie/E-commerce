#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_boisson = Blueprint('admin_declinaison_boisson', __name__,
                         template_folder='templates')


@admin_declinaison_boisson.route('/admin/declinaison_boisson/add')
def add_declinaison_boisson():
    id_boisson=request.args.get('id_boisson')
    mycursor = get_db().cursor()
    boisson=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/boisson/add_declinaison_boisson.html'
                           , boisson=boisson
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_boisson.route('/admin/declinaison_boisson/add', methods=['POST'])
def valid_add_declinaison_boisson():
    mycursor = get_db().cursor()

    id_boisson = request.form.get('id_boisson')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/boisson/edit?id_boisson=' + id_boisson)


@admin_declinaison_boisson.route('/admin/declinaison_boisson/edit', methods=['GET'])
def edit_declinaison_boisson():
    id_declinaison_boisson = request.args.get('id_declinaison_boisson')
    mycursor = get_db().cursor()
    declinaison_boisson=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/boisson/edit_declinaison_boisson.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_boisson=declinaison_boisson
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_boisson.route('/admin/declinaison_boisson/edit', methods=['POST'])
def valid_edit_declinaison_boisson():
    id_declinaison_boisson = request.form.get('id_declinaison_boisson','')
    id_boisson = request.form.get('id_boisson','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_boisson modifié , id:' + str(id_declinaison_boisson) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/boisson/edit?id_boisson=' + str(id_boisson))


@admin_declinaison_boisson.route('/admin/declinaison_boisson/delete', methods=['GET'])
def admin_delete_declinaison_boisson():
    id_declinaison_boisson = request.args.get('id_declinaison_boisson','')
    id_boisson = request.args.get('id_boisson','')

    flash(u'declinaison supprimée, id_declinaison_boisson : ' + str(id_declinaison_boisson),  'alert-success')
    return redirect('/admin/boisson/edit?id_boisson=' + str(id_boisson))
