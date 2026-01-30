#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_boisson = Blueprint('client_boisson', __name__,
                        template_folder='templates')

@client_boisson.route('/client/index')
@client_boisson.route('/client/boisson/show')              # remplace /client
def client_boisson_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = ''' SELECT * FROM boisson; '''
    #list_param = []
    #condition_and = ""

    mycursor.execute(sql)
    boissons = mycursor.fetchall()


    # utilisation du filtre
    sql3=''' SELECT * FROM ligne_panier
            INNER JOIN boisson ON boisson.id_boisson = ligne_panier.id_boisson'''



    # pour le filtre
    types_boisson = []


    boissons_panier = []

    if len(boissons_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_boisson.html'
                           , boissons=boissons
                           , boissons_panier=boissons_panier
                           #, prix_total=prix_total
                           , items_filtre=types_boisson
                           )
