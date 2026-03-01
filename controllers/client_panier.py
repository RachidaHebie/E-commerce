#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    db = get_db()
    mycursor = db.cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson')
    quantite = request.form.get('quantite')

    try:
        quantite = int(quantite)
        if quantite <= 0:
            flash("Quantité invalide.", "warning")
            return redirect('/client/boisson/show')
    except:
        flash("Quantité invalide.", "warning")
        return redirect('/client/boisson/show')

    try:
        db.autocommit = False

        # Vérifier le stock
        mycursor.execute("""
            SELECT stock
            FROM boisson
            WHERE id_boisson = %s
        """, (id_boisson,))
        result_stock = mycursor.fetchone()
        if not result_stock or result_stock['stock'] < quantite:
            flash("Stock insuffisant.", "warning")
            return redirect('/client/boisson/show')

        # récupérer le panier actuel ou en créer un
        mycursor.execute("""
            SELECT id_commande
            FROM commande
            WHERE id_utilisateur = %s AND id_etat = 1
            ORDER BY id_commande DESC
            LIMIT 1
        """, (id_client,))
        commande = mycursor.fetchone()

        if not commande:
            mycursor.execute("""
                INSERT INTO commande(date_commande, montant_total, id_etat, id_utilisateur)
                VALUES (NOW(), 0, 1, %s)
            """, (id_client,))
            id_commande = mycursor.lastrowid
        else:
            id_commande = commande['id_commande']

        # vérifier si la boisson est déjà dans le panier
        mycursor.execute("""
            SELECT quantite_panier
            FROM ligne_panier
            WHERE id_boisson = %s AND id_commande = %s
        """, (id_boisson, id_commande))
        ligne = mycursor.fetchone()

        if ligne:
            mycursor.execute("""
                UPDATE ligne_panier
                SET quantite_panier = quantite_panier + %s
                WHERE id_boisson = %s AND id_commande = %s
            """, (quantite, id_boisson, id_commande))
        else:
            mycursor.execute("""
                INSERT INTO ligne_panier(id_boisson, id_commande, quantite_panier, date_creation_panier)
                VALUES (%s, %s, %s, NOW())
            """, (id_boisson, id_commande, quantite))

        # mise à jour du stock
        nouveau_stock = result_stock['stock'] - quantite
        mycursor.execute("""
            UPDATE boisson
            SET stock = %s
            WHERE id_boisson = %s
        """, (nouveau_stock, id_boisson))

        db.commit()
    except Exception as e:
        db.rollback()
        flash("Erreur lors de l'ajout au panier: %s" % e, "danger")
        return redirect('/client/boisson/show')
    finally:
        mycursor.close()

    #id_declinaison_boisson=request.form.get('id_declinaison_boisson',None)
    id_declinaison_boisson = 1

# ajout dans le panier d'une déclinaison d'un boisson (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_boisson))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_boisson = declinaisons[0]['id_declinaison_boisson']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_boisson))
    #     boisson = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_boisson.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , boisson=boisson)

# ajout dans le panier d'un boisson

    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    db = get_db()
    mycursor = db.cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson','')

    try:
        db.autocommit = False

        # récupérer la ligne à supprimer
        mycursor.execute("""
            SELECT lp.id_commande, lp.quantite_panier
            FROM ligne_panier lp
            JOIN commande c ON lp.id_commande = c.id_commande
            WHERE c.id_utilisateur = %s
            AND lp.id_boisson = %s
            AND c.id_etat = 1
            ORDER BY lp.id_commande DESC
            LIMIT 1
        """, (id_client, id_boisson))
        ligne = mycursor.fetchone()

        if not ligne:
            flash("L'article n'est pas dans le panier.", "warning")
            return redirect('/client/boisson/show')

        if ligne['quantite_panier'] > 1:
            mycursor.execute("""
                UPDATE ligne_panier
                SET quantite_panier = quantite_panier - 1
                WHERE id_boisson = %s AND id_commande = %s
            """, (id_boisson, ligne['id_commande']))
        else:
            mycursor.execute("""
                DELETE FROM ligne_panier
                WHERE id_boisson = %s AND id_commande = %s
            """, (id_boisson, ligne['id_commande']))

        # mise à jour du stock
        mycursor.execute("""
            SELECT stock FROM boisson WHERE id_boisson = %s
        """, (id_boisson,))
        stock = mycursor.fetchone()
        nouveau_stock = stock['stock'] + 1

        mycursor.execute("""
            UPDATE boisson
            SET stock = %s
            WHERE id_boisson = %s
        """, (nouveau_stock, id_boisson))

        db.commit()
    except Exception as e:
        db.rollback()
        flash("Erreur lors de la suppression: %s" % e, "danger")
    finally:
        mycursor.close()

    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    db = get_db()
    mycursor = db.cursor()
    client_id = session['id_user']

    try:
        db.autocommit = False

        mycursor.execute("""
            SELECT lp.id_boisson, lp.id_commande, lp.quantite_panier
            FROM ligne_panier lp
            JOIN commande c ON lp.id_commande = c.id_commande
            WHERE c.id_utilisateur = %s
            AND c.id_etat = 1
        """, (client_id,))
        items_panier = mycursor.fetchall()

        for item in items_panier:
            mycursor.execute("""
                DELETE FROM ligne_panier
                WHERE id_boisson = %s AND id_commande = %s
            """, (item['id_boisson'], item['id_commande']))

            mycursor.execute("""
                SELECT stock FROM boisson WHERE id_boisson = %s
            """, (item['id_boisson'],))
            stock = mycursor.fetchone()
            nouveau_stock = stock['stock'] + item['quantite_panier']

            mycursor.execute("""
                UPDATE boisson
                SET stock = %s
                WHERE id_boisson = %s
            """, (nouveau_stock, item['id_boisson']))

        db.commit()
    except Exception as e:
        db.rollback()
        flash("Erreur lors du vidage du panier: %s" % e, "danger")
    finally:
        mycursor.close()

    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    db = get_db()
    mycursor = db.cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson','')

    try:
        db.autocommit = False

        mycursor.execute("""
            SELECT lp.id_commande, lp.quantite_panier
            FROM ligne_panier lp
            JOIN commande c ON lp.id_commande = c.id_commande
            WHERE c.id_utilisateur = %s
            AND lp.id_boisson = %s
            AND c.id_etat = 1
            ORDER BY lp.id_commande DESC
            LIMIT 1
        """, (id_client, id_boisson))
        ligne_panier = mycursor.fetchone()

        if not ligne_panier:
            flash("Ligne introuvable.", "warning")
            return redirect('/client/boisson/show')

        mycursor.execute("""
            DELETE FROM ligne_panier
            WHERE id_boisson = %s AND id_commande = %s
        """, (id_boisson, ligne_panier['id_commande']))

        mycursor.execute("""
            SELECT stock FROM boisson WHERE id_boisson = %s
        """, (id_boisson,))
        stock = mycursor.fetchone()
        nouveau_stock = stock['stock'] + ligne_panier['quantite_panier']

        mycursor.execute("""
            UPDATE boisson
            SET stock = %s
            WHERE id_boisson = %s
        """, (nouveau_stock, id_boisson))

        db.commit()
    except Exception as e:
        db.rollback()
        flash("Erreur lors de la suppression de ligne: %s" % e, "danger")
    finally:
        mycursor.close()

    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/boisson/show')