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


# TRANSACTION POUR ADD cf. https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    id_client = session['id_user']
    db = get_db()
    mycursor = db.cursor()

    try:
        # Désactiver l'auto-commit pour gérer la transaction manuellement
        db.autocommit = False

        # 1. Sélection du contenu du panier de l'utilisateur
        sql = """
            SELECT lp.id_boisson, lp.id_commande, lp.quantite_panier, b.prix_boisson
            FROM ligne_panier lp
            JOIN boisson b ON lp.id_boisson = b.id_boisson
            JOIN commande c ON lp.id_commande = c.id_commande
            WHERE c.id_utilisateur = %s
        """
        mycursor.execute(sql, (id_client,))
        items_ligne_panier = mycursor.fetchall()

        if items_ligne_panier is None or len(items_ligne_panier) < 1:
            flash(u"Pas d'articles dans le panier", 'alert-warning')
            return redirect('/client/boisson/show')

        # 2. Calcul du montant total
        montant_total = sum(item['prix_boisson'] * item['quantite_panier'] for item in items_ligne_panier)

        # 3. Création de la commande
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO commande (date_commande, montant_total, id_etat, id_utilisateur)
            VALUES (%s, %s, %s, %s)
        """
        mycursor.execute(sql, (date_now, montant_total, 2, id_client))  # id_etat=2 : "En cours de traitement"

        # 4. Récupération de l'id de la commande créée
        mycursor.execute("SELECT last_insert_id() as last_insert_id")
        result = mycursor.fetchone()
        id_nouvelle_commande = result['last_insert_id']

        # 5. Pour chaque article du panier : supprimer la ligne panier et créer la ligne commande
        for item in items_ligne_panier:
            # Suppression de la ligne panier
            sql_delete = """
                DELETE FROM ligne_panier
                WHERE id_boisson = %s AND id_commande = %s
            """
            mycursor.execute(sql_delete, (item['id_boisson'], item['id_commande']))

            # Ajout de la ligne de commande
            sql_insert = """
                INSERT INTO ligne_commande (id_boisson, id_commande, quantite_commande, date_commande)
                VALUES (%s, %s, %s, %s)
            """
            mycursor.execute(sql_insert, (item['id_boisson'], id_nouvelle_commande, item['quantite_panier'], date_now))

        # 6. Tout s'est bien passé : on valide la transaction
        db.commit()
        flash(u'Commande ajoutée', 'alert-success')

    except Exception as e:
        # En cas d'erreur : on annule toutes les modifications
        db.rollback()
        flash(f"Erreur lors de la création de la commande : {e}", 'alert-danger')

    finally:
        mycursor.close()

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
        ORDER BY c.id_etat DESC, c.date_commande DESC
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