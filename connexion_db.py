from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g


from dotenv import load_dotenv
import os

load_dotenv()

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # à activer sur les machines personnelles :
        activate_db_options(db)
    return db

def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')   # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY  ok')   # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')   # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else :
            print('MYSQL : variable globale lower_case_table_names=0  ok')    # mettre en commentaire
    cursor.close()
'''





#--------- Mettre en commentaire pour lili et Matteo --------

def activate_db_options(db):
    cursor = db.cursor()

    try:
        cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
        result = cursor.fetchone()
        if result:
            modes = result['Value'].split(',')
            if 'ONLY_FULL_GROUP_BY' not in modes:
                cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
                db.commit()
    except Exception as e:
        print(f"Erreur lors du réglage sql_mode : {e}")


    try:
        cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
        result = cursor.fetchone()
        if result:
            val = result['Value']
            if val == '0':
                print("MYSQL : Casse des tables respectée (Style Linux/Production)")
            else:
                print(f"MYSQL : Casse des tables ignorée (Style Windows, valeur: {val})")
    except Exception as e:
        print(f"Erreur lors de la lecture des variables système : {e}")

    cursor.close()'''