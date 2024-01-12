from django.db import models
from django import forms
from decimal import Decimal
import sqlite3



def convert_to_date(date):
    if '/' in date:
        date = date.split("/")
        date = date[2]+"-"+date[1]+"-"+date[0]
    if '-' in date:
        date = date.split("-")
        date = date[2]+"/"+date[1]+"/"+date[0]
    return date


def convert_dec(nbr):
    if ',' in nbr:
        nbr=nbr.replace(',', '.')
    return Decimal(nbr)




class TableauSQLField(forms.CharField):
    def __init__(self, sql_query=None, *args, **kwargs):
        super(TableauSQLField, self).__init__(*args, **kwargs)
        self.sql_query = sql_query

    def as_custom_div(self):
        if self.sql_query == None:
            # Lors de l'appel de la page
            connection =sqlite3.connect("atrium.db")
            cursor = connection.cursor()
            cursor.execute("SELECT date_distribution, type_paiement, montant FROM distribution")
            results = cursor.fetchone()
            connection.commit()
            connection.close()
            table_html = "<table>"
            table_html += "<thead><tr>"
            for column in cursor.description:
                table_html += f"<th>{column[0]}</th>"
            table_html += "</tr></thead>"
            table_html +="</table>"
        else:
            # Exécuter la requête SQL pour obtenir les résultats
            connection = sqlite3.connect("atrium.db")
            cursor = connection.cursor()
            cursor.execute(self.sql_query)
            results = cursor.fetchall()

            # Générer le code HTML du tableau avec les résultats de la requête SQL
            table_html = "<table>"
            table_html += "<thead><tr>"
            for column in cursor.description:
                table_html += f"<th>{column[0]}</th>"
            table_html += "</tr></thead>"
            table_html += "<tbody>"
            for row in results:
                table_html += "<tr>"
                for value in row:
                    table_html += f"<td>{value}</td>"
                table_html += "</tr>"
            table_html += "</tbody></table>"

        # Ajouter le code HTML généré comme valeur initiale du champ
       
        return table_html
        


class parametreform(forms.Form):
    montant = forms.CharField(max_length=50, label="Prix du colis")
    ecart_validite = forms.CharField(max_length=50, label="Ecart date de validité en jour")
    intitule_aide = forms.CharField(max_length=50, label="Intitulé du colis", required=False)

class situationform(forms.Form):
    attrs = {'class':'custom-fields'}
    atrium_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)
    credit = forms.CharField(max_length=50, label="Créditer", widget=forms.TextInput(attrs=attrs))
    avance = forms.CharField(max_length=50, label="Reste avance", widget=forms.TextInput(attrs=attrs))
    dette = forms.CharField(max_length=50, label="Montant Dette", widget=forms.TextInput(attrs=attrs))
    gratuit = forms.CharField(max_length=50, label="Nombre de Gratuit", widget=forms.TextInput(attrs=attrs))

class update_beneficiaire(forms.Form):
    attrs = {'class':'custom-fields'}
    num_atrium = forms.CharField(max_length=50, label="numéro Atrium", widget=forms.TextInput(attrs=attrs), required=False)
    nom = forms.CharField(max_length=50, label="Nom", widget=forms.TextInput(attrs=attrs), required=False)
    prenom = forms.CharField(max_length=50, label="Prenom", widget=forms.TextInput(attrs=attrs), required=False)
    date_validite = forms.DateField(label="Date de validité", widget=forms.TextInput(attrs=attrs), required=False)
    nbr_beneficiaire = forms.CharField(max_length=50,label="Total de Bénéficiaires", widget=forms.TextInput(attrs=attrs), required=False)
    nbr_adulte = forms.CharField(max_length=50,label="Nombre d'Adulte", widget=forms.TextInput(attrs=attrs), required=False)
    nbr_enfant = forms.CharField(max_length=50,label="Nombre d'Enfant", widget=forms.TextInput(attrs=attrs), required=False)

    def __init__(self, *args, **kwargs):
        super(update_beneficiaire, self).__init__(*args, **kwargs)
        self.fields['nbr_beneficiaire'].widget.attrs['readonly'] = True
       

class create_beneficiaire(forms.Form):
    attrs = {'class':'custom-fields'}
    num_atrium = forms.CharField(max_length=50, label="numéro Atrium", widget=forms.TextInput(attrs=attrs))
    nom = forms.CharField(max_length=50, label="Nom", widget=forms.TextInput(attrs=attrs))
    prenom = forms.CharField(max_length=50, label="Prenom", widget=forms.TextInput(attrs=attrs))
    date_validite = forms.DateField(label="Date de validité", widget=forms.TextInput(attrs=attrs))
    #nbr_beneficiaire = forms.CharField(max_length=50,label="Total de Bénéficiaires", widget=forms.TextInput(attrs=attrs))
    nbr_adulte = forms.CharField(max_length=50,label="Nombre d'Adulte", widget=forms.TextInput(attrs=attrs))
    nbr_enfant = forms.CharField(max_length=50,label="Nombre d'Enfant", widget=forms.TextInput(attrs=attrs))

class consult_beneficiaire(models.Model):
    num_atrium = models.CharField(max_length = 50)
    nom = models.CharField(max_length = 50)
    prenom = models.CharField(max_length = 50)
    date_naissance = models.DateField(max_length = 50)

class aideform(forms.Form):
    num_atrium = forms.CharField(max_length=50, label="numéro Atrium", required=False, widget=forms.TextInput(attrs={'class': 'inline-fields'}))
    nom = forms.CharField(max_length=50, label="Nom", required=False, widget=forms.TextInput(attrs={'class': 'name-fields'}))
    prenom = forms.CharField(max_length=50, label="Prenom", required=False, widget=forms.TextInput(attrs={'class': 'name-fields'}))
    date_validite = forms.DateField(label="Date de validité", required=False, widget=forms.TextInput(attrs={'class': 'inline-fields'}))
    nbr_beneficiaire = forms.CharField(max_length=50,label="Total de Bénéficiaires", required=False, widget=forms.TextInput(attrs={'class': 'number-fields'}))
    nbr_adulte = forms.CharField(max_length=50,label="Nombre d'Adulte", required=False, widget=forms.TextInput({'class': 'number-fields'}))
    nbr_enfant = forms.CharField(max_length=50,label="Nombre d'Enfant", required=False, widget=forms.TextInput({'class': 'number-fields'}))
   
    
    def __init__(self, *args, **kwargs):
        super(aideform, self).__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs['readonly'] = True
        self.fields['prenom'].widget.attrs['readonly'] = True
        self.fields['date_validite'].widget.attrs['readonly'] = True
        self.fields['nbr_beneficiaire'].widget.attrs['readonly'] = True
        self.fields['nbr_adulte'].widget.attrs['readonly'] = True
        self.fields['nbr_enfant'].widget.attrs['readonly'] = True

class distributionform(forms.Form):
    attrs = {'display':'flex'}
    TYPE_CHOICES = [
        ("Avance", "Avance"),
        ("Dette", "Dette"),
        ("Caisse", "Caisse"),
        ("Gratuit", "Gratuit"),
    ]

    num_atrium = forms.CharField(max_length=50, label="numéro Atrium", required=False, widget=forms.TextInput(attrs={'class': 'inline-fields'}))
    nom = forms.CharField(max_length=50, label="Nom", required=False, widget=forms.TextInput(attrs={'class': 'name-fields'}))
    prenom = forms.CharField(max_length=50, label="Prenom", required=False, widget=forms.TextInput(attrs={'class': 'name-fields'}))
    date_validite = forms.DateField(label="Date de validité", required=False, widget=forms.TextInput(attrs={'class': 'inline-fields'}))
    nbr_beneficiaire = forms.CharField(max_length=50,label="Total de Bénéficiaires", required=False, widget=forms.TextInput(attrs={'class': 'number-fields'}))
    nbr_adulte = forms.CharField(max_length=50,label="Nombre d'Adulte", required=False, widget=forms.TextInput({'class': 'number-fields'}))
    nbr_enfant = forms.CharField(max_length=50,label="Nombre d'Enfant", required=False, widget=forms.TextInput({'class': 'number-fields'}))
    dist = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'dist'}), choices=TYPE_CHOICES, label="Distribution")
    
    def __init__(self, *args, **kwargs):
        super(distributionform, self).__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs['readonly'] = True
        self.fields['prenom'].widget.attrs['readonly'] = True
        self.fields['date_validite'].widget.attrs['readonly'] = True
        self.fields['nbr_beneficiaire'].widget.attrs['readonly'] = True
        self.fields['nbr_adulte'].widget.attrs['readonly'] = True
        self.fields['nbr_enfant'].widget.attrs['readonly'] = True
        #self.fields['historique'].widget.attrs['readonly'] = True

# Create your models here.
