import sqlite3
from datetime import date




def create():
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("CREATE TABLE beneficiaire(num_atrium TEXT, nom TEXT, prenom TEXT, date_validite DATE, nbr_beneficiaire INTEGER, nbr_adulte INTEGER, nbr_enfant INTEGER)")
    curseur.execute("CREATE TABLE situation(num_atrium TEXT, avance FLOAT, dette FLOAT, gratuit INTEGER)")
    curseur.execute("CREATE TABLE distribution(num_atrium TEXT, date_distribution DATE, type_paiement TEXT, montant INTEGER)")
    curseur.execute("CREATE TABLE aide(Id INTEGER PRIMARY KEY AUTOINCREMENT, num_atrium TEXT, date_aide DATE, type_aide TEXT, valeur TEXT)")
    curseur.execute("CREATE TABLE parametre(montant FLOAT, ecart_validite INTEGER, aide TEXT)")
    curseur.execute("INSERT INTO parametre(montant, ecart_validite) VALUES(?, ?)", (2,10,))
    curseur.execute("CREATE TABLE list_aide(Id INTEGER PRIMARY KEY AUTOINCREMENT, aide TEXT)")
    curseur.execute("INSERT INTO list_aide(aide) VALUES(?)", ("Bon alimentaire",))
    connexion.commit()
    connexion.close()



def update(array_up, table):
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
   
        
    # Création du tuple de valeurs dans le même ordre que les colonnes de la table
    valeurs = tuple(array_up.get(colonne) for colonne in array_up.keys())
    key =  ', '.join(array_up.keys())
    print(key)
    marqueurs = ', '.join(['?'] * len(array_up.keys()))
    curseur.execute(f'INSERT INTO {table} ({key}) VALUES ({marqueurs})', valeurs)
    
    connexion.commit()
    connexion.close()

def affiche():
    connexion =sqlite3.connect("atrium.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM distribution")
    print(curseur.fetchall())
    connexion.commit()
    connexion.close()
def distrib():
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO distribution (num_atrium, date_distribution, type_paiement) VALUES (?, ?, ?)", ("1235", date.today(), "Dette"))
    connexion.commit()
    connexion.close()
try:
    create()
except:
    print("Base de donnée déjà existante")

