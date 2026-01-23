DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS boisson;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS type_boisson;
DROP TABLE IF EXISTS fruit;


CREATE TABLE fruit(
                      id_fruit INT AUTO_INCREMENT,
                      nom_fruit VARCHAR(50),
                      PRIMARY KEY(id_fruit)
);

CREATE TABLE type_boisson(
                             id_type_boisson INT AUTO_INCREMENT,
                             nom_type_boisson VARCHAR(50),
                             PRIMARY KEY(id_type_boisson)
);

CREATE TABLE utilisateur(
                             id_utilisateur INT AUTO_INCREMENT,
                             nom VARCHAR(50),
                             prenom VARCHAR(50),
                             login VARCHAR(50),
                             email VARCHAR(50),
                             password VARCHAR(50),
                             role VARCHAR(50),
                             est_actif tinyint(1),
                             date_inscription VARCHAR(50),
                             PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
                     id_etat INT AUTO_INCREMENT,
                     libelle_etat VARCHAR(50),
                     PRIMARY KEY(id_etat)
);

CREATE TABLE boisson(
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
);

CREATE TABLE commande(
                         id_commande INT AUTO_INCREMENT,
                         date_commande DATETIME,
                         montant_total DECIMAL(15,2),
                         id_etat INT NOT NULL,
                         id_utilisateur INT NOT NULL,
                         PRIMARY KEY(id_commande),
                         FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
                         FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
                               id_boisson INT,
                               id_commande INT,
                               quantite_commande VARCHAR(50),
                               date_commande DATETIME,
                               PRIMARY KEY(id_boisson, id_commande),
                               FOREIGN KEY(id_boisson) REFERENCES boisson(id_boisson),
                               FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
                             id_boisson INT,
                             id_commande INT,
                             quantite_panier VARCHAR(50),
                             date_creation_panier VARCHAR(50),
                             PRIMARY KEY(id_boisson, id_commande),
                             FOREIGN KEY(id_boisson) REFERENCES boisson(id_boisson),
                             FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);



