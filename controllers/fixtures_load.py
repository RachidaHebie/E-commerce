#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    # DROP TABLES
    sql='''DROP TABLE IF EXISTS ligne_panier;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS ligne_commande;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS commande;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS boisson;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS etat;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS utilisateur;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS type_boisson;'''
    mycursor.execute(sql)
    sql='''DROP TABLE IF EXISTS fruit;'''
    mycursor.execute(sql)

    # CREATE TABLE
    sql='''CREATE TABLE fruit(
                                 id_fruit INT AUTO_INCREMENT,
                                 nom_fruit VARCHAR(50),
                                 PRIMARY KEY(id_fruit)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE type_boisson(
                                        id_type_boisson INT AUTO_INCREMENT,
                                        nom_type_boisson VARCHAR(50),
                                        PRIMARY KEY(id_type_boisson)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE utilisateur(
                                       id_utilisateur INT AUTO_INCREMENT,
                                       nom VARCHAR(50),
                                       prenom VARCHAR(50),
                                       login VARCHAR(50),
                                       email VARCHAR(50),
                                       password VARCHAR(255),
                                       role VARCHAR(50),
                                       est_actif tinyint(1),
                                       date_inscription VARCHAR(50),
                                       PRIMARY KEY(id_utilisateur)
           )ENGINE=InnoDB DEFAULT CHARSET utf8mb4;'''
    mycursor.execute(sql)

    sql='''CREATE TABLE etat(
                                id_etat INT AUTO_INCREMENT,
                                libelle_etat VARCHAR(50),
                                PRIMARY KEY(id_etat)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE boisson(
                                   id_boisson INT AUTO_INCREMENT,
                                   nom_boisson VARCHAR(50),
                                   prix_boisson DECIMAL(15,2),
                                   marque VARCHAR(50),
                                   founisseur VARCHAR(50),
                                   volume DECIMAL(15,2),
                                   description VARCHAR(50),
                                   photo VARCHAR(50),
                                   stock INT,
                                   id_type_boisson INT NOT NULL,
                                   id_fruit INT NOT NULL,
                                   PRIMARY KEY(id_boisson),
                                   FOREIGN KEY(id_type_boisson) REFERENCES type_boisson(id_type_boisson),
                                   FOREIGN KEY(id_fruit) REFERENCES fruit(id_fruit)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE commande(
                                    id_commande INT AUTO_INCREMENT,
                                    date_commande DATETIME,
                                    montant_total DECIMAL(15,2),
                                    id_etat INT NOT NULL,
                                    id_utilisateur INT NOT NULL,
                                    PRIMARY KEY(id_commande),
                                    FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
                                    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE ligne_commande(
                                          id_boisson INT,
                                          id_commande INT,
                                          quantite_commande VARCHAR(50),
                                          date_commande DATETIME,
                                          PRIMARY KEY(id_boisson, id_commande),
                                          FOREIGN KEY(id_boisson) REFERENCES boisson(id_boisson),
                                          FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
           );'''
    mycursor.execute(sql)

    sql='''CREATE TABLE ligne_panier(
                                        id_boisson INT,
                                        id_commande INT,
                                        quantite_panier VARCHAR(50),
                                        date_creation_panier VARCHAR(50),
                                        PRIMARY KEY(id_boisson, id_commande),
                                        FOREIGN KEY(id_boisson) REFERENCES boisson(id_boisson),
                                        FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
           );'''
    mycursor.execute(sql)

    # INSERT
    sql='''INSERT INTO utilisateur (id_utilisateur, nom, prenom, login, email, password, role, est_actif, date_inscription) VALUES
                                                                                                                                (1,'admin', 'admin','admin','admin@admin.fr',
                                                                                                                                 'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
                                                                                                                                 'ROLE_admin','1','01-01-2001'),
                                                                                                                                (2,'client','client', 'client','client@client.fr',
                                                                                                                                 'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
                                                                                                                                 'ROLE_client','1','01-01-2001'),
                                                                                                                                (3,'client2','client2','client2','client2@client2.fr',
                                                                                                                                 'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
                                                                                                                                 'ROLE_client','1','01-01-2001'); \

        '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
