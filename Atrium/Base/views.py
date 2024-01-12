from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import distributionform, create_beneficiaire, situationform, parametreform, update_beneficiaire, convert_dec, aideform, convert_to_date
import sqlite3
from django.http import JsonResponse
from datetime import date, datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
def index(request):
    return render(request, 'menu.html')



def get_radio_choices(request):
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT aide FROM list_aide")
    l_aide = curseur.fetchall()
    choices = [{'value': aide, 'label': aide} for aide in l_aide]
    print(choices)
    return JsonResponse(choices, safe=False) 



def del_aide(request):
    id_aide = request.GET.get('id')
    print(id_aide)
    connexion = sqlite3.connect('atrium.db')
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM list_aide WHERE Id = ?", (id_aide,))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def del_baide(request):
    id_aide = request.GET.get('id')
    print(id_aide)
    connexion = sqlite3.connect('atrium.db')
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM aide WHERE Id = ?", (id_aide,))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def verification_validite(request):
    num_atrium = request.GET.get('num_atrium')
    connexion = sqlite3.connect('atrium.db')
    curseur = connexion.cursor()
    curseur.execute("SELECT * from beneficiaire WHERE num_atrium = ?",(num_atrium,))
    exist = curseur.fetchone()
    if exist is None:
        return JsonResponse({"error":"OK"}, status=200)
    curseur.execute("SELECT date_validite FROM beneficiaire WHERE num_atrium = ?", (num_atrium,))
    date_validite = curseur.fetchone()[0]
    date_validite = convert_to_date(date_validite)
    curseur.execute("SELECT ecart_validite FROM parametre")
    ecart = curseur.fetchone()[0]
    today = datetime.strptime(str(date.today()), "%Y-%m-%d" )
    date_validite = datetime.strptime(str(date_validite), "%d/%m/%Y")
    ecart_jours = (today - date_validite).days
    if ecart_jours >= ecart:
        return JsonResponse({"date":"OK"}, status=200)
    else:
         return JsonResponse({"Status":"OK"}, status=200)
def attributer_aide(request):
    f1 = aideform()
    f2 = situationform()
    return render(request, 'aide.html', {'form1':f1, 'form2':f2, 'titre':'Attribuer une aide'})

def maj_beneficiaire(request):
    form = update_beneficiaire()
    return render(request, 'mbeneficiaire.html', {'form1':form, 'titre':'Mise à Jour du Bénéficiaire', "message": "message"})

def modifier_beneficiaire(request):

    num_atrium = request.GET.get("num_atrium")
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    date_validite = convert_to_date(request.GET.get('date_validite'))
    nbr_adulte = request.GET.get('nbr_adulte')
    nbr_enfant = request.GET.get('nbr_enfant')
    nbr_beneficiaire = int(nbr_adulte)+int(nbr_enfant)
    connexion = sqlite3.connect('atrium.db')
    curseur = connexion.cursor()
    curseur.execute("UPDATE beneficiaire SET nom = ?, prenom = ?, date_validite = ? , nbr_beneficiaire = ?, nbr_adulte = ?, nbr_enfant = ? WHERE num_atrium = ?", (nom, prenom, date_validite, nbr_beneficiaire, nbr_adulte, nbr_enfant, num_atrium,))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def cree_beneficiaire(request):
    num_atrium = request.GET.get('num_atrium')
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    date_validite = convert_to_date(request.GET.get("date_validite"))
    print(date_validite)
    nbr_enfant = request.GET.get("nbr_enfant")
    nbr_adulte = request.GET.get("nbr_adulte")
    nbr_beneficiaire = int(nbr_adulte)+int(nbr_enfant)
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO beneficiaire (num_atrium, nom, prenom, date_validite, nbr_beneficiaire, nbr_enfant, nbr_adulte) VALUES (?,?,?,?,?,?,?)", (num_atrium, nom, prenom, date_validite, nbr_beneficiaire, nbr_enfant, nbr_adulte))
    curseur.execute("INSERT INTO situation (num_atrium, avance, dette, gratuit) VALUES (?, ?, ?, ?)", (num_atrium, 0, 0, 0))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def creer_beneficiaire(request):
    f = create_beneficiaire()

    return render(request, 'cbeneficiaire.html', {'form1':f, 'titre':'Creation d\'un Beneficiaire', "message": "message"})

def modifier_distribution(request):
    num_atrium = request.GET.get('num_atrium')
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT type_paiement, montant FROM distribution WHERE num_atrium = ? AND date_distribution = ? AND type_paiement !='Credit'", (num_atrium, str(date.today())))
    data = curseur.fetchone() 
    type = data[0]
    montant = data[1]
    curseur.execute("SELECT avance, dette, gratuit FROM situation WHERE num_atrium = ?", (num_atrium,))
    situation = curseur.fetchone()
    avance = situation[0]
    dette = situation[1]
    gratuit = situation[2]
    if type == "Avance":
        avance+=montant
    if type == "Dette":
        dette-=montant
    if type == "Gratuit":
        gratuit-=1
    curseur.execute("UPDATE situation SET avance = ?, dette = ?, gratuit = ? WHERE num_atrium = ?", (avance, dette, gratuit, num_atrium,))
    curseur.execute("DELETE FROM distribution WHERE num_atrium = ? AND date_distribution = ? AND type_paiement !='Credit'", (num_atrium, str(date.today())))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def modifier_aide(request):
    num_atrium = request.GET.get('num_atrium')
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM aide WHERE num_atrium = ? AND date_aide = ?", (num_atrium, str(date.today())))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)




def crediter(request):
    num_atrium = request.GET.get('num_atrium')
    credit = convert_dec(request.GET.get('credit'))
    last_avance = convert_dec(request.GET.get('avance'))
    dette = convert_dec(request.GET.get('dette'))
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    avance = last_avance + (credit - dette)
    dette -= credit 
    if dette <0 : dette = 0
    curseur.execute("UPDATE situation SET avance = ?, dette = ? WHERE num_atrium = ?", (avance, dette, num_atrium,))
    curseur.execute("INSERT INTO distribution (num_atrium, date_distribution, type_paiement, montant) VALUES (?, ?, ?, ?)", (num_atrium, date.today(), "Credit", credit))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)

def creer_aide(request):
    num_atrium = request.GET.get('num_atrium')
    type_aide = request.GET.get('dist')
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("INSERT INTO aide (num_atrium, date_aide, type_aide) VALUES (?, ?, ?)", (num_atrium, date.today(), type_aide))
    connexion.commit()
    connexion.close()
    return JsonResponse({"Status":"OK"}, status=200)
    
def creer_distribution(request):
    num_atrium = request.GET.get('num_atrium')
    type_paiement = request.GET.get('dist')
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT date_distribution, type_paiement FROM distribution WHERE num_atrium = ?",(num_atrium,))
    last_day = curseur.fetchall()
    today = str(date.today())
    already_exists = False
    for day in last_day:
        if today == day[0] and day[1]!="Credit":
            already_exists = True
            break #Prevoir dans ce cas l'apparition d'un message informant déjà d'une saisie, apparition d'un bouton modifier et annuler
    if already_exists:
        print("existe)")
        messages.warning(request, 'Une saisie pour la date d\'aujourd\'hui existe déjà. Vous pouvez modifier ou annuler.')
                # Vous pouvez renvoyer un contexte supplémentaire pour informer le template
        return JsonResponse({"error":"True"}, status=200)
    else:
        curseur.execute("SELECT montant FROM parametre")
        montant = curseur.fetchone()[0]
        curseur.execute("SELECT avance, dette, gratuit FROM situation WHERE num_atrium = ?", (num_atrium,))
        situation = curseur.fetchone()
        avance = situation[0]
        dette = situation[1]
        gratuit = situation[2]
        curseur.execute("INSERT INTO distribution (num_atrium, date_distribution, type_paiement, montant) VALUES (?, ?, ?, ?)", (num_atrium, date.today(), type_paiement, montant))
        if type_paiement == "Avance":
            avance-=montant
        if type_paiement == "Dette":
            dette+=montant
        if type_paiement =="Gratuit":
            gratuit+=1
        curseur.execute("UPDATE situation SET avance = ?, dette = ?, gratuit = ? WHERE num_atrium = ?", (avance, dette, gratuit, num_atrium,))
        connexion.commit()
        connexion.close()
        return JsonResponse({"Status":"OK"}, status=200)
    
def recherche_parametre(request):
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT montant, ecart_validite FROM parametre")
    data = curseur.fetchone()
    montant = data[0]
    ecart = data[1]
    curseur.execute("SELECT Id, aide FROM list_aide")
    rows = curseur.fetchall()
    columns = [col[0] for col in curseur.description]   
    aide_dict = [dict(zip(columns, row)) for row in rows]
    response_data = {
        "montant" : montant,
        "ecart_validite" : ecart,
        "aide":aide_dict,
    }
    return JsonResponse(response_data)

def recherche(request):
    num_atrium = request.GET.get('num_atrium')
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT nom, prenom, date_validite, nbr_beneficiaire, nbr_adulte, nbr_enfant FROM beneficiaire WHERE num_atrium = ?", (num_atrium,))
    beneficiaire = curseur.fetchone()
    curseur.execute("SELECT date_distribution, type_paiement, montant FROM distribution WHERE num_atrium = ? ORDER BY date_distribution DESC", (num_atrium,))
    rows = curseur.fetchall()
    columns = [col[0] for col in curseur.description]   
    historique = [dict(zip(columns, row)) for row in rows]
    for element in historique:
        if 'date_distribution' in element:
            element['date_distribution']= convert_to_date(element['date_distribution'])
    curseur.execute("SELECT Id, date_aide, type_aide FROM aide WHERE num_atrium = ? ORDER BY date_aide DESC", (num_atrium,))
    rows = curseur.fetchall()
    columns = [col[0] for col in curseur.description]   
    aide = [dict(zip(columns, row)) for row in rows]
    for element in aide:
        if 'date_aide' in element:
            element['date_aide']= convert_to_date(element['date_aide'])
    
    curseur.execute("SELECT avance, dette, gratuit FROM situation WHERE num_atrium = ?", (num_atrium,))
    situation = curseur.fetchone()
    
    connexion.close()
    if beneficiaire:
        response_data = {
            'num_atrium':num_atrium,
            'atrium_hidden':num_atrium,
            'nom':beneficiaire[0],
            'prenom':beneficiaire[1],
            'date_validite': beneficiaire[2],  
            'nbr_beneficiaire': beneficiaire[3],
            'nbr_adulte': beneficiaire[4],
            'nbr_enfant': beneficiaire[5],
            'historique':historique,
            'aide':aide,
            'avance':situation[0],
            'dette':situation[1],
            'gratuit':situation[2],
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Bénéficiaire non trouvé'}, status=200)
    
def distribution(request):
    f1 = distributionform()
    f2 = situationform()

        
    return render(request, 'distribution.html', {'form1':f1, 'form2':f2, 'titre':'Distribution', "message": "message"})

def parametre(request):
    connexion = sqlite3.connect("atrium.db")
    curseur = connexion.cursor()

    if request.method == "POST":
        form = parametreform(request.POST)
        if form.is_valid():
            aide = request.POST.get("intitule_aide")
            montant = convert_dec(request.POST.get("montant"))
            ecart = request.POST.get("ecart_validite")
            curseur.execute("UPDATE parametre SET montant = ?, ecart_validite = ?", (montant, ecart))
            if aide !="":
                curseur.execute("INSERT INTO list_aide (aide) VALUES (?)", (aide,))
            connexion.commit()
            connexion.close()
            redirect('parametre')

    
    else:
        form = parametreform()
    return render(request, 'parametre.html', {'form1':form, 'titre':'Parametre',})

