 Dans le travail sur Système de suivi d'incidents (Helpdesk) avec authentification sécurisée , on a suivi les étapes suivantes :
 
host="localhost"
user="crud_user" 
password="Crud@1234!"
database="sen_assistance"

Création de tickets_assistance.py et fichier sen_assistance.sql

Utilisation commun
Menu principal

1. Inscription
2. Connexion
3. Afficher utilisateurs
4. Créer administrateur
5. Quitter

Menu utilisateur (apprenant ou staff)
1. Créer un ticket
2. Mes tickets
3. Déconnexion

Menu administrateur
1. Créer un ticket
2. Mes tickets
3. Consulter tous les tickets
4. Modifier statut d'un ticket
5. Gérer les utilisateurs
6. Déconnexion

Tests de sécurité
Scénario	Résultat attendu
User A connecté	Voit uniquement ses tickets
User B connecté	Ne voit pas les tickets de User A
Sans authentification	Impossible d'accéder aux tickets
Admin connecté	Voit tous les tickets


