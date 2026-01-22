USE base_lili;

DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255),
    est_actif tinyint(1),

    PRIMARY KEY (id_utilisateur)
)ENGINE=InnoDB DEFAULT CHARSET utf8mb4;

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
                                                                                    (1,'admin','admin@admin.fr',
                                                                                     'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
                                                                                     'ROLE_admin','admin','1'),
                                                                                    (2,'client','client@client.fr',
                                                                                     'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
                                                                                     'ROLE_client','client','1'),
                                                                                    (3,'client2','client2@client2.fr',
                                                                                     'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
                                                                                     'ROLE_client','client2','1');


