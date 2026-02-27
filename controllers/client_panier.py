#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson')
    quantite = request.form.get('quantite')
    
    sql = '''
    SELECT stock
    FROM boisson
    WHERE id_boisson = %s;
    '''

    mycursor.execute(sql, (id_boisson,))
    stock = mycursor.fetchone()

    if int(stock['stock']) >= int(quantite):
        # On verifie si le panier existe déjà
        mycursor.execute("""
            SELECT id_commande
            FROM commande
            WHERE id_utilisateur = %s
            AND id_etat = 1
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


        # On verifie si la ligne existe déjà
        mycursor.execute("""
            SELECT quantite_panier
            FROM ligne_panier
            WHERE id_boisson = %s AND id_commande = %s
            """, (id_boisson, id_commande))

        ligne = mycursor.fetchone()

        # Update si la ligne existe
        if ligne:
            mycursor.execute("""
                UPDATE ligne_panier
                SET quantite_panier = quantite_panier + %s
                WHERE id_boisson = %s AND id_commande = %s
            """, (quantite, id_boisson, id_commande))

        # On creer une ligne si elle n'existe pas
        else:
            mycursor.execute("""
                INSERT INTO ligne_panier(id_boisson, id_commande, quantite_panier, date_creation_panier)
                VALUES (%s, %s, %s, NOW())
                """, (id_boisson, id_commande, quantite))
            
        get_db().commit()

        # On retire le stock
        nouveau_stock = int(stock['stock']) - int(quantite)

        sql = '''
        UPDATE boisson
        SET stock = %s
        WHERE id_boisson = %s;'''

        mycursor.execute(sql, (nouveau_stock, id_boisson))
        get_db().commit()

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
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'boisson
    # id_declinaison_boisson = request.form.get('id_declinaison_boisson', None)

    sql = ''' SELECT ligne_panier.* FROM ligne_panier
                Join commande on ligne_panier.id_commande = commande.id_commande
                join utilisateur u on commande.id_utilisateur = u.id_utilisateur
                where u.id_utilisateur = %s; '''

    mycursor.execute(sql, (id_client,))
    ligne_panier = mycursor.fetchone()

    if not(ligne_panier is None) and ligne_panier['quantite_panier'] > 1:
        sql = '''
            UPDATE ligne_panier
            SET quantite_panier = quantite_panier - 1
            WHERE id_boisson = %s AND id_commande = %s;'''
        mycursor.execute(sql, (id_boisson, ligne_panier['id_commande']))
    else:
        sql = ''' DELETE FROM ligne_panier WHERE id_boisson = %s; '''
        mycursor.execute(sql, (id_boisson,))
        
    #mise à jour du stock

    sql = '''
        UPDATE boisson
        SET stock = stock + 1
        WHERE id_boisson = %s;'''

    mycursor.execute(sql, (id_boisson,))

    # mise à jour du stock de l'boisson disponible
    get_db().commit()
    return redirect('/client/boisson/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = sql = ''' SELECT ligne_panier.* FROM ligne_panier
                Join commande on ligne_panier.id_commande = commande.id_commande
                join utilisateur u on commande.id_utilisateur = u.id_utilisateur
                where u.id_utilisateur = %s; '''

    mycursor.execute(sql, (client_id,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        id_boisson = item['id_boisson']

         # suppression de la ligne du panier
        sql = ''' DELETE FROM ligne_panier WHERE id_boisson = %s; '''
        mycursor.execute(sql, (id_boisson,))
        
        #mise à jour du stock
        sql='''Select stock from boisson Where id_boisson = %s;'''
        mycursor.execute(sql, (id_boisson,))
        stock = mycursor.fetchone()
        
        nouveau_stock = stock['stock'] + item['quantite_panier']

        sql = '''
            UPDATE boisson
            SET stock = %s
            WHERE id_boisson = %s;'''

        mycursor.execute(sql, (nouveau_stock, id_boisson))

    get_db().commit()
    return redirect('/client/boisson/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_boisson = request.form.get('id_boisson','')
    quantite = request.form.get('quantite')
    #id_declinaison_boisson = request.form.get('id_declinaison_boisson')
    # selection de ligne du panier
    sql = ''' SELECT ligne_panier.* FROM ligne_panier
                Join commande on ligne_panier.id_commande = commande.id_commande
                join utilisateur u on commande.id_utilisateur = u.id_utilisateur
                where u.id_utilisateur = %s; '''

    mycursor.execute(sql, (id_client,))

    ligne_panier = mycursor.fetchone()

    # suppression de la ligne du panier
    sql = ''' DELETE FROM ligne_panier WHERE id_boisson = %s; '''
    mycursor.execute(sql, (id_boisson,))
    
    #mise à jour du stock
    sql='''Select stock from boisson Where id_boisson = %s;'''
    mycursor.execute(sql, (id_boisson,))
    stock = mycursor.fetchone()
    
    nouveau_stock = stock['stock'] + ligne_panier['quantite_panier']

    sql = '''
        UPDATE boisson
        SET stock = %s
        WHERE id_boisson = %s;'''

    mycursor.execute(sql, (nouveau_stock, id_boisson))


    sql = """SELECT quantite_panier FROM ligne_panier WHERE id_boisson = %s"""
    mycursor.execute(sql, (id_boisson,))
    quantite = mycursor.fetchone()

    sql = """SELECT stock FROM boisson WHERE id_boisson = %s"""
    mycursor.execute(sql, (id_boisson,))
    stock = mycursor.fetchone()
    nouveau_stock = int(stock['stock']) + int(quantite['quantite_panier'])

    # suppression de la ligne du panier
    sql = ''' DELETE FROM ligne_panier WHERE id_boisson = %s; '''
    # mise à jour du stock de l'boisson : stock = stock + qté de la ligne pour l'boisson
    sql2=''' UPDATE boisson SET stock = %s WHERE id_boisson = %s; '''
    mycursor.execute(sql, (id_client,))
    mycursor.execute(sql2, (nouveau_stock,id_boisson,))


    get_db().commit()

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
