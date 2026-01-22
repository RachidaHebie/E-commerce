# TODO Livrable 1 – SAE 2.04 BDD

## **1. Préparation des fichiers et documents**
- [ ] Télécharger le fichier `livrable1_sae_2_4_bdd.ods` depuis Moodle.
- [ ] Remplir le fichier `livrable1_sae_2_4_bdd.ods` avec :
  - L’URL de votre projet hébergé sur PythonAnywhere.
  - Les informations sur le groupe de SAE (noms, groupe de TP, groupe de SAE).

---

## **2. Modélisation (MCD/MLD)**
- [ ] **Créer le MCD** avec Loom (ou autre logiciel) :
  - Inclure toutes les entités et associations nécessaires pour un site e-commerce (version minimum).
  - Entités obligatoires : "utilisateur", "commande", "ligne_commande", "ligne_panier", "etat", + 3 tables spécifiques à votre sujet.
- [ ] **Exporter le MCD en PDF** (`MCD_v1.pdf`) :
  - Format A4, utiliser toute la page.
  - Ajouter : noms des étudiants, groupe de TP, groupe de SAE.
- [ ] **Créer le MLD** à partir du MCD.
- [ ] **Exporter le MLD en PDF** (`MLD_v1.pdf`) :
  - Format A4, utiliser toute la page.
  - Ajouter : noms des étudiants, groupe de TP, groupe de SAE.

---

## **3. Base de données (SQL)**
- [ ] **Créer le script SQL** (`sae_sql.sql`) :
  - Inclure la création de toutes les tables du MLD.
  - Ajouter un jeu de test réaliste (minimum 15 articles, 4 types d’articles).
  - Les articles doivent avoir des colonnes variées (prix, description, stock, etc.).
- [ ] **Trouver 15 images réalistes et attractives** pour les articles (pas de doublons).
- [ ] **Intégrer les images** dans le projet (ex : dossier `static/images`).
- [ ] **Vérifier la qualité du jeu de test** : données cohérentes et crédibles.

---

## **4. Application Flask**
- [ ] **Copier le système d’authentification** vu en TD :
  - Utilisateurs par défaut : "client" (mdp: "client"), "client2" (mdp: "client2"), "admin" (mdp: "admin").
- [ ] **Afficher les articles et types d’articles** depuis la base de données.
- [ ] **Créer la route `/base/init`** :
  - Fonctionnalité : supprime et recrée les tables, puis insère les enregistrements (fixtures).
- [ ] **Tester localement** l’application avant le déploiement.

---

## **5. Hébergement sur PythonAnywhere**
- [ ] **Créer un compte PythonAnywhere** (si ce n’est pas déjà fait).
- [ ] **Uploader le code** de l’application Flask :
  - Utiliser l’interface web ou la ligne de commande (SCP, Git).
  - Documentation : [Uploading and Downloading Files - PythonAnywhere](https://help.pythonanywhere.com/pages/UploadingAndDownloadingFiles/)
- [ ] **Configurer la base de données** sur PythonAnywhere :
  - Importer le script `sae_sql.sql`.
  - Vérifier que les tables et données sont bien créées.
- [ ] **Tester l’application** sur PythonAnywhere :
  - Vérifier l’authentification.
  - Vérifier l’affichage des articles et types d’articles.
  - Vérifier la route `/base/init`.

---

## **6. Versioning avec GitHub/GitLab**
- [ ] **Créer un dépôt GitHub ou GitLab** pour le projet.
- [ ] **Synchroniser le code local avec le dépôt** :
  - Utiliser les commandes `git add`, `git commit`, `git push`.
- [ ] **Synchroniser PythonAnywhere avec le dépôt** :
  - Utiliser les commandes shell pour cloner ou pull le dépôt sur PythonAnywhere.
- [ ] **Configurer dotenv** pour les variables d’environnement (ex : identifiants BDD).

---

## **7. Vérifications finales**
- [ ] Vérifier les noms des fichiers PDF (`MCD_v1.pdf`, `MLD_v1.pdf`).
- [ ] Vérifier la présence des noms et groupes sur les PDF.
- [ ] Vérifier que l’URL du projet est bien indiquée dans le fichier ODS.
- [ ] Vérifier que toutes les tables sont présentes dans `sae_sql.sql`.
- [ ] Vérifier que les images sont uniques et réalistes.

---

## **8. Dépôt sur Moodle**
- [ ] Déposer le fichier `livrable1_sae_2_4_bdd.ods` sur Moodle.
- [ ] Déposer les fichiers PDF (`MCD_v1.pdf`, `MLD_v1.pdf`) sur Moodle.
- [ ] Déposer le script SQL (`sae_sql.sql`) sur Moodle.

---
