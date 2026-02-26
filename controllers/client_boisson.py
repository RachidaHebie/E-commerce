#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, session
from connexion_db import get_db

client_boisson = Blueprint('client_boisson', __name__,
                        template_folder='templates')


@client_boisson.route('/client/boisson/show', methods=['GET'])
def client_boisson_show():

    mycursor = get_db().cursor()
    id_client = session['id_user']

    # récupération des filtres depuis la session
    filter_word = session.get('filter_word', '')
    filter_value_min = session.get('filter_value_min', '')
    filter_value_max = session.get('filter_value_max', '')
    filter_types = session.get('filter_types', [])

    # récupération des types pour affichage des checkbox
    mycursor.execute("""
        SELECT id_type_boisson, nom_type_boisson
        FROM type_boisson
        ORDER BY nom_type_boisson
    """)
    types_boisson = mycursor.fetchall()

    # requête principale
    sql = """
        SELECT b.*, tb.nom_type_boisson, f.nom_fruit
        FROM boisson b
        INNER JOIN type_boisson tb ON b.id_type_boisson = tb.id_type_boisson
        INNER JOIN fruit f ON b.id_fruit = f.id_fruit
        WHERE 1 = 1
    """

    params = []

    if filter_word:
        sql += " AND b.nom_boisson LIKE %s"
        params.append('%' + filter_word + '%')

    if filter_value_min:
        sql += " AND b.prix_boisson >= %s"
        params.append(filter_value_min)

    if filter_value_max:
        sql += " AND b.prix_boisson <= %s"
        params.append(filter_value_max)

    if filter_types:
        sql += " AND b.id_type_boisson IN (" + ",".join(["%s"] * len(filter_types)) + ")"
        params.extend(filter_types)

    sql += " ORDER BY b.nom_boisson"

    mycursor.execute(sql, params)
    boissons = mycursor.fetchall()


    sql = """SELECT ligne_panier.*, boisson.*, (boisson.prix_boisson * ligne_panier.quantite_panier) AS prix_total FROM ligne_panier
            Join commande on ligne_panier.id_commande = commande.id_commande
            join utilisateur u on commande.id_utilisateur = u.id_utilisateur
            join boisson on ligne_panier.id_boisson = boisson.id_boisson
            where u.id_utilisateur = %s;"""

    mycursor.execute(sql, id_client)
    boissons_panier = mycursor.fetchall()
    prix_total = None

    return render_template(
        'client/boutique/panier_boisson.html',
        boissons=boissons,
        boissons_panier=boissons_panier,
        items_filtre=types_boisson,
        filter_word=filter_word,
        filter_value_min=filter_value_min,
        filter_value_max=filter_value_max,
        filter_types=filter_types
    )


@client_boisson.route('/client/boisson/filtre', methods=['POST'])
def valid_filtre_boisson():

    session['filter_word'] = request.form.get('filter_word', '')
    session['filter_value_min'] = request.form.get('filter_value_min', '')
    session['filter_value_max'] = request.form.get('filter_value_max', '')
    session['filter_types'] = request.form.getlist('filter_types')

    return redirect('/client/boisson/show')


@client_boisson.route('/client/boisson/filtre/reset')
def reset_filtre_boisson():

    session.pop('filter_word', None)
    session.pop('filter_value_min', None)
    session.pop('filter_value_max', None)
    session.pop('filter_types', None)

    return redirect('/client/boisson/show')