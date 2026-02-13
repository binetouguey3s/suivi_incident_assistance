import mysql.connector
import bcrypt

cursor = None 
conn = None 
utilisateur_connecter = None
les_tickets = None

# Fonction pour etablir une connexion à la base de données MySQL
def get_connection():
    global conn
    global cursor
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="crud_user",
            password="Crud@1234!",
            database="sen_assistance"
        )
        print("="*50)
        print("Vous etes bien connectés à la base de données!")
        return conn  
    except mysql.connector.Error as e:
        print("Erreur de connexion à la base de données", e)
        return None
    
conn = get_connection()  
print("="*50)

# Inscription d'un utilisateur  
def inscription():
    global conn
    global cursor
    print("\n Inscription d'un nouvel utilisateur")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    email = input("Email : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()
    
    salt = bcrypt.gensalt() 
    mot_de_passe_hash = bcrypt.hashpw(mot_de_passe.encode('utf-8'), salt)  
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)" 
            cursor.execute(sql, (nom, prenom, email, mot_de_passe_hash.decode('utf-8'))) 
            conn.commit() 
            print("Inscription réussie ! ")
        except mysql.connector.IntegrityError:
            print("Cet email existe deja")
        except Exception as e:
            print("Erreur inscription :", e)
            conn.rollback()

# Connexion de l'utilisateur
def connexion():
    global conn
    global utilisateur_connecter
    print("\n Connexion de l'utilisateur")
    email = input("Email : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT id_utilisateur, nom, prenom, email, mot_de_passe, role FROM utilisateurs WHERE email = %s"
            cursor.execute(sql, (email,))
            utilisateur = cursor.fetchone()
            
            if utilisateur:
                if bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur[4].encode('utf-8')):
                    utilisateur_connecter = {
                        'id': utilisateur[0],
                        'nom': utilisateur[1],
                        'prenom': utilisateur[2],
                        'email': utilisateur[3],
                        'role': utilisateur[5]  
                    }
                    print(f"Connexion réussie! \n Bienvenue {utilisateur[2]} {utilisateur[1]}")
                    print(f"Role : {utilisateur[5]}")
                    
                    # Rediriger vers le bon menu selon le rôle
                    if utilisateur[5] == 'admin':
                        menu_admin()
                    else:
                        menu_utilisateur()
                else:
                    print("Mot de passe incorrect.")
            else:
                print("Email non trouvé.")
        except Exception as e:
            print("Erreur connexion :", e)

# Créer un admin 
def creer_admin():
    print("\n Création d'un administrateur")
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    email = input("Email : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()
    
    salt = bcrypt.gensalt()
    mot_de_passe_hash = bcrypt.hashpw(mot_de_passe.encode('utf-8'), salt)
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, 'admin')"
            cursor.execute(sql, (nom, prenom, email, mot_de_passe_hash.decode('utf-8')))
            conn.commit()
            print("Administrateur créé avec succès !")
        except mysql.connector.IntegrityError:
            print("Cet email existe")
        except Exception as e:
            print("Erreur création admin :", e)
            conn.rollback()

def creer_ticket():
    global conn
    global cursor
    global utilisateur_connecter
    
    if not utilisateur_connecter:
        print("Vous devez être connecté pour créer un ticket.")
        return
    
    print("\n Creation d'un ticket")
    titre = input("Titre : ").strip()
    description = input("Description detaillee : ").strip()
    
    print("Niveau d'urgence : (Faible, Moyenne, Élevée)")
    niveau_urgence = input("Votre choix : ").strip()
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO tickets (id_utilisateur, titre, description, niveau_urgence) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (utilisateur_connecter['id'], titre, description, niveau_urgence))
            conn.commit()
            print("Ticket créé avec succès!")
        except Exception as e:
            print("Erreur dans la création de ticket:", e)
            conn.rollback()

def mes_tickets():
    global utilisateur_connecter
    global conn
    global cursor
    
    if not utilisateur_connecter:
        print("Vous devez être connecté.")
        return
    
    print(f"\nMES TICKETS : {utilisateur_connecter['prenom']} {utilisateur_connecter['nom']}")
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT numero_ticket, titre, description, niveau_urgence, statut FROM tickets WHERE id_utilisateur = %s"
            cursor.execute(sql, (utilisateur_connecter['id'],))
            tickets = cursor.fetchall()
            
            if not tickets:
                print("Aucun ticket trouvé.")
                return
            
            print("\n" + "="*90)
            print(f"{'N°':<5} | {'Titre':<25} | {'Description':<30} | {'Urgence':<10} | {'Statut':<15}")
            print("-"*90)
            
            for ticket in tickets:
                print(f"{ticket[0]:<5} | {ticket[1][:25]:<25} | {ticket[2][:30]:<30} | {ticket[3]:<10} | {ticket[4]:<15}")
            print("="*90)
            
        except Exception as e:
            print("Erreur affichage tickets :", e)

def tous_les_tickets():
    global utilisateur_connecter
    global conn
    global cursor
    
    if not utilisateur_connecter:
        print("Vous devez être connecté.")
        return
    
    if utilisateur_connecter['role'] != 'admin':
        print("Accès refusé. Réservé aux administrateurs.")
        return
    
    print("\nTOUS LES TICKETS (Seulement pour l'admin)")
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = sql = "SELECT t.numero_ticket, u.nom, u.prenom, t.titre, t.niveau_urgence, t.statut FROM tickets t JOIN utilisateurs u ON t.id_utilisateur = u.id_utilisateur ORDER BY t.numero_ticket DESC"
            cursor.execute(sql)
            tickets = cursor.fetchall()
            
            if not tickets:
                print("Aucun ticket dans la base.")
                return
            
            print("\n" + "="*100)
            print(f"{'N°':<5} | {'Auteur':<20} | {'Titre':<25} | {'Urgence':<10} | {'Statut':<15}")
            
            for ticket in tickets:
                auteur = f"{ticket[2]} {ticket[1]}"
                print(f"{ticket[0]:<5} | {auteur[:20]:<20} | {ticket[3][:25]:<25} | {ticket[4]:<10} | {ticket[5]:<15}")
            
        except Exception as e:
            print("Erreur affichage tickets :", e)

def modifier_statut_ticket():
    global utilisateur_connecter
    global conn
    global cursor
    
    if not utilisateur_connecter:
        print("Vous devez être connecté.")
        return
    
    if utilisateur_connecter['role'] != 'admin':
        print("Accès refusé. Réservé aux administrateurs.")
        return
    
    # Afficher d'abord tous les tickets
    tous_les_tickets()
    
    try:
        numero_ticket = int(input("\nNuméro du ticket à modifier : "))
    except ValueError:
        print("Le numéro doit être un nombre.")
        return
    
    print("\nNouveau statut :")
    print("1. En attente")
    print("2. En cours")
    print("3. Résolu")
    choix_statut = input("Votre choix : ").strip()
    
    statut_actuel = {'1': 'En attente', '2': 'En cours', '3': 'Résolu'}
    nouveau_statut = statut_actuel.get(choix_statut, 'En attente')
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE tickets SET statut = %s WHERE numero_ticket = %s"
            cursor.execute(sql, (nouveau_statut, numero_ticket))
            conn.commit()
            print(f"Statut du ticket {numero_ticket} mis à jour : {nouveau_statut}")
        except Exception as e:
            print("Erreur modification statut :", e)
            conn.rollback()

# Affichage des utilisateurs
def afficher_utilisateurs():
    global conn
    global cursor
    
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT id_utilisateur, nom, prenom, email, role FROM utilisateurs"  
            cursor.execute(sql)
            utilisateurs = cursor.fetchall()

            if not utilisateurs:
                print("Aucun utilisateur dans la base de données")
                return
            
            print("\nLISTE DES UTILISATEURS\n")
            print("="*70)
            print(f"{'ID':<5} | {'Nom':<15} | {'Prenom':<15} | {'Email':<25} | {'Role':<10}")
            print("-"*70)
            
            for user in utilisateurs:
                print(f"{user[0]:<5} | {user[1]:<15} | {user[2]:<15} | {user[3]:<25} | {user[4]:<10}")
            print("="*70)
            
        except Exception as e:
            print("Erreur:", e)

# Menu admin
def menu_admin():
    global utilisateur_connecter
    
    while True:
        print("\n" + "="*50)
        print(f"TABLEAU DE BORD - {utilisateur_connecter['prenom']} {utilisateur_connecter['nom']}")
        print(f"Role : {utilisateur_connecter['role']}")
        print("="*50)
        print("1. Creer un ticket")
        print("2. Mes tickets")
        print("3. Consulter tous les tickets")
        print("4. Modifier statut d'un ticket")
        print("5. Gérer les utilisateurs")
        print("6. Deconnexion")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            creer_ticket()
        elif choix == "2":
            mes_tickets()
        elif choix == "3":
            tous_les_tickets()
        elif choix == "4":
            modifier_statut_ticket()
        elif choix == "5":
            afficher_utilisateurs()
        elif choix == "6":
            utilisateur_connecter = None
            print("Deconnexion reussie")
            break
        else:
            print("Choix invalide.")

# Menu utilisateur
def menu_utilisateur():
    global utilisateur_connecter
    
    while True:
        print("\n" + "="*50)
        print(f"TABLEAU DE BORD - {utilisateur_connecter['prenom']} {utilisateur_connecter['nom']}")
        print(f"Role : {utilisateur_connecter['role']}")
        print("="*50)
        print("1. Creer un ticket")
        print("2. Mes tickets")
        print("3. Deconnexion")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            creer_ticket()
        elif choix == "2":
            mes_tickets()
        elif choix == "3":
            utilisateur_connecter = None
            print("Deconnexion reussie")
            break
        else:
            print("Choix invalide.")

# Menu principal
def menu():
    while True:
        print("\n" + "="*50)
        print("BIENVENUE DANS SEN ASSISTANCE")
        print("Gérer vos tickets en toute sécurité")
        print("="*50)
        print("1. Inscription")
        print("2. Connexion")
        print("3. Afficher utilisateurs")
        print("4. Creer administrateur")
        print("5. Quitter")
        
        choix = input("Votre choix : ").strip()
        
        if choix == "1":
            inscription()
        elif choix == "2":
            connexion()
        elif choix == "3":
            afficher_utilisateurs()
        elif choix == "4":
            creer_admin()
        elif choix == "5":
            print("Au revoir!")
            fermer_connexion()
            break
        else:
            print("Choix invalide.")

# Fonction de fermeture de la connexion à la base de données
def fermer_connexion():
    global conn
    if conn and conn.is_connected():
        conn.close()
        print("Connexion fermée")

# Lancement du programme
menu()
fermer_connexion()