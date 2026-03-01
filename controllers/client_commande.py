#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("""
        SELECT lp.id_boisson, lp.quantite_panier, b.nom_boisson, b.prix_boisson
        FROM ligne_panier lp
        JOIN boisson b ON lp.id_boisson = b.id_boisson
        JOIN commande c ON lp.id_commande = c.id_commande
        WHERE c.id_utilisateur = %s AND c.id_etat = 1
    """, (id_client,))
    boissons_panier = mycursor.fetchall()

    if boissons_panier:
        prix_total = sum(item['prix_boisson'] * item['quantite_panier'] for item in boissons_panier)
    else:
        prix_total = None

    return render_template(
        'client/boutique/panier_validation_adresses.html',
        boissons_panier=boissons_panier,
        prix_total=prix_total,
        validation=1
    )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("""
        SELECT c.id_commande
        FROM commande c
        WHERE c.id_utilisateur = %s AND c.id_etat = 1
        LIMIT 1
    """, (id_client,))
    commande_panier = mycursor.fetchone()

    if not commande_panier:
        flash(u'Pas de boissons dans le panier', 'alert-warning')
        return redirect('/client/boisson/show')

    id_commande = commande_panier['id_commande']

    mycursor.execute("""
        SELECT lp.id_boisson, lp.quantite_panier, b.prix_boisson
        FROM ligne_panier lp
        JOIN boisson b ON lp.id_boisson = b.id_boisson
        WHERE lp.id_commande = %s
    """, (id_commande,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash(u'Pas de boissons dans le panier', 'alert-warning')
        return redirect('/client/boisson/show')

    total_commande = 0
    for item in items_ligne_panier:
        mycursor.execute("""
            INSERT INTO ligne_commande(id_commande, id_boisson, quantite_commande)
            VALUES (%s, %s, %s)
        """, (id_commande, item['id_boisson'], item['quantite_panier']))
        total_commande += item['prix_boisson'] * item['quantite_panier']

    mycursor.execute("""
        UPDATE commande
        SET montant_total = %s, id_etat = 2
        WHERE id_commande = %s
    """, (total_commande, id_commande))

    mycursor.execute("""
        DELETE FROM ligne_panier
        WHERE id_commande = %s
    """, (id_commande,))

    get_db().commit()
    flash(u'Commande ajoutÃ©e', 'alert-success')
    return redirect('/client/boisson/show')


@client_commande.route('/client/commande/show', methods=['get', 'post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("""
        SELECT c.*, e.libelle_etat,
            (SELECT SUM(lc.quantite_commande)
             FROM ligne_commande lc
             WHERE lc.id_commande = c.id_commande) AS nbr_boissons
        FROM commande c
        LEFT JOIN etat e ON c.id_etat = e.id_etat
        WHERE c.id_utilisateur = %s
        ORDER BY c.id_etat, c.date_commande DESC
    """, (id_client,))
    commandes = mycursor.fetchall()

    boissons_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande:
        mycursor.execute("""
            SELECT lc.*, b.nom_boisson, b.prix_boisson, (lc.quantite_commande * b.prix_boisson) AS prix_ligne
            FROM ligne_commande lc
            JOIN commande c ON lc.id_commande = c.id_commande
            JOIN boisson b ON lc.id_boisson = b.id_boisson
            WHERE c.id_commande = %s
        """, (id_commande,))
        boissons_commande = mycursor.fetchall()

    return render_template(
        'client/commandes/show.html',
        commandes=commandes,
        boissons_commande=boissons_commande,
        commande_adresses=commande_adresses
    )