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
                             password VARCHAR(255),
                             role VARCHAR(50),
                             est_actif tinyint(1),
                             date_inscription VARCHAR(50),
                             PRIMARY KEY(id_utilisateur)
)ENGINE=InnoDB DEFAULT CHARSET utf8mb4;

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


INSERT INTO type_boisson (nom_type_boisson) VALUES
                                                ('Jus'),
                                                ('Gazeuse'),
                                                ('Énergisante');

INSERT INTO fruit (nom_fruit) VALUES
                                  ('Pomme'),
                                  ('Orange'),
                                  ('Ananas'),
                                  ('Raisin'),
                                  ('Mangue'),
                                  ('Fraise'),
                                  ('citron');

INSERT INTO utilisateur (id_utilisateur, nom, prenom, login, email, password, role, est_actif, date_inscription) VALUES
                                                                                                                     (1,'admin', 'admin','admin','admin@admin.fr',
                                                                                                                      'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
                                                                                                                      'ROLE_admin','1','01-01-2001'),
                                                                                                                     (2,'client','client', 'client','client@client.fr',
                                                                                                                      'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
                                                                                                                      'ROLE_client','1','01-01-2001'),
                                                                                                                     (3,'client2','client2','client2','client2@client2.fr',
                                                                                                                      'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
                                                                                                                      'ROLE_client','1','01-01-2001');

INSERT INTO etat (libelle_etat) VALUES
                                    ('En attente'),
                                    ('En cours'),
                                    ('Livrée'),
                                    ('Annulée');

-- Jus
INSERT INTO boisson (id_boisson, nom_boisson, prix_boisson, marque, founisseur, volume, description, photo, stock, id_type_boisson, id_fruit) VALUES
                                                                                                                                      (NULL, 'Jus de pomme', 2.50, 'Pomme d\'Or', 'Fournisseur A', 1.0, 'Jus de pomme 100% pur', 'pomme.png', 50, 1, 1),
                                                                                                                                      (NULL, 'Jus d\'orange', 2.75, 'Tropicana', 'Fournisseur B', 1.0, 'Jus d\'orange pressé', 'orange.png', 45, 1, 2),
                                                                                                                                      (NULL, 'Jus d\'ananas ', 3.00, 'Ananas Sun', 'Fournisseur C', 1.0, 'Jus d\'ananas', 'ananas.png', 30, 1, 3),
                                                                                                                                      (NULL,'Jus de raisin', 2.90, 'Vignoble', 'Fournisseur D', 0.75, 'Jus de raisin noir', 'raisin.png', 25, 1, 4),
                                                                                                                                      (NULL, 'Jus de mangue ', 3.20, 'Mango Delight', 'Fournisseur E', 1.0, 'Jus de mangue sucré', 'mangue.png', 20, 1, 5),
                                                                                                                                      (NULL, 'fraise ', 3.20, 'fraise Delight', 'Fournisseur E', 1.0, 'Jus de fraise', 'mangue.png', 22, 1, 6);

-- Gazeuses
INSERT INTO boisson (id_boisson, nom_boisson, prix_boisson, marque, founisseur, volume, description, photo, stock, id_type_boisson, id_fruit) VALUES
                                                                                                                                      (NULL,'Cola', 1.80, 'ColaCo', 'Fournisseur F', 1.5, 'Soda cola classique', 'coca.png', 100, 2, 6),
                                                                                                                                      (NULL,'Limonade', 1.90, 'CitronFizz', 'Fournisseur G', 1.0, 'Limonade pétillante', 'limonade.png', 80, 2, 7),
                                                                                                                                      (NULL,'Eau gazeuse', 1.50, 'BullePure', 'Fournisseur H', 1.0, 'Eau minérale gazeuse', 'eau_gazeuse.png', 60, 2, 1),
                                                                                                                                      (NULL,'Orange soda', 2.00, 'FizzOrange', 'Fournisseur I', 0.33, 'Soda à l\'orange', 'orange_soda.png', 40, 2, 2);

-- Énergisantes
INSERT INTO boisson (id_boisson, nom_boisson, prix_boisson, marque, founisseur, volume, description, photo, stock, id_type_boisson, id_fruit) VALUES
                                                                                                                                      (NULL,'Boom Energy', 3.50, 'BoomCo', 'Fournisseur J', 0.25, 'Boisson énergétique fruitée', 'boom.png', 35, 3, 3),
                                                                                                                                      (NULL,'PowerUp', 3.75, 'PowerDrink', 'Fournisseur K', 0.5, 'Boisson énergétique citron', 'power.png', 30, 3, 4),
                                                                                                                                      (NULL,'Vitality', 3.90, 'VitaMax', 'Fournisseur L', 0.33, 'Boisson énergétique tropicale', 'vitality.png', 25, 3, 5),
                                                                                                                                      (NULL,'FruitPunch Energy', 3.80, 'FruitPunch', 'Fournisseur N', 0.33, 'Boisson énergétique aux fruits rouges', 'punch.png', 15, 3, 6);


INSERT INTO commande (date_commande, montant_total, id_etat, id_utilisateur) VALUES
                                                                                 ('2026-01-23 10:00:00', 15.50, 2, 1),
                                                                                 ('2026-01-22 15:30:00', 8.75, 3, 2),
                                                                                 ('2026-01-21 12:45:00', 22.00, 1, 3);




INSERT INTO ligne_commande (id_boisson, id_commande, quantite_commande, date_commande) VALUES
                                                                                           (1, 1, 2, '2026-01-23 10:00:00'),
                                                                                           (6, 1, 1, '2026-01-23 10:00:00'),
                                                                                           (2, 2, 1, '2026-01-22 15:30:00'),
                                                                                           (7, 2, 3, '2026-01-22 15:30:00'),
                                                                                           (11, 3, 2, '2026-01-21 12:45:00'),
                                                                                           (12, 3, 1, '2026-01-21 12:45:00');
INSERT INTO ligne_panier (id_boisson, id_commande, quantite_panier, date_creation_panier) VALUES
                                                                                              (3, 1, 1, '2026-01-23 09:45:00'),
                                                                                              (8, 2, 2, '2026-01-22 15:20:00'),
                                                                                              (10, 3, 1, '2026-01-21 12:30:00');
