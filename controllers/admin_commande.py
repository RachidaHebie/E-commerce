#! /usr/bin/python
# -*- coding:utf-8 -*-
from http.cookiejar import debug

from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']

    sql = '''SELECT c.id_commande, 
                    c.date_commande, 
                    u.nom AS login, 
                    SUM(lc.quantite_commande) AS nbr_boissons,
                    SUM(lc.quantite_commande * b.prix_boisson) AS prix_total,
                    e.libelle_etat AS libelle,
                    c.id_etat AS etat_id
            FROM commande c
            JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
            JOIN ligne_commande lc ON c.id_commande = lc.id_commande
            JOIN boisson b ON lc.id_boisson = b.id_boisson
            JOIN etat e ON c.id_etat = e.id_etat
            GROUP BY c.id_commande, c.date_commande, u.nom, e.libelle_etat, c.id_etat
            ORDER BY c.date_commande DESC; '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()


    boissons_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = '''  SELECT b.nom_boisson AS nom, 
                               lc.quantite_commande AS quantite, 
                               b.prix_boisson AS prix, 
                               (b.prix_boisson * lc.quantite_commande) AS prix_ligne,
                               c.id_etat AS etat_id,
                               c.id_commande AS id
                        FROM ligne_commande lc
                        JOIN boisson b ON lc.id_boisson = b.id_boisson
                        JOIN commande c ON lc.id_commande = c.id_commande
                        WHERE lc.id_commande = %s;;  '''
        mycursor.execute(sql, (id_commande,))
        boissons_commande = mycursor.fetchall()
        commande_adresses = []
        sql = '''
             SELECT u.nom AS nom_livraison, 
                   u.prenom AS prenom_livraison,
                   'Non renseignée' AS rue_livraison, 
                   '' AS code_postal_livraison, 
                   '' AS ville_livraison,
                   u.email,
                   'adresse_identique' AS adresse_identique
            FROM commande c
            JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
            WHERE c.id_commande = %s;
              '''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchall()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , boissons_commande=boissons_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET id_etat = 1 WHERE id_commande = %s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
