from django import forms
from .models import create_beneficiaire, consult_beneficiaire, distributionform

class c_beneficiaireForm(forms.ModelForm):
    class Meta:
        model = create_beneficiaire
        fields = ['nom', 'prenom', 'num_atrium', 'date_naissance', 'date_rdv', 'nbr_beneficiaire']

class v_beneficiaire(forms.ModelForm):
    class Meta:
        model = consult_beneficiaire
        fields = ['num_atrium', 'nom', 'prenom', 'date_naissance']

"""
class f_distribution(forms.ModelForm):
    class Meta:
        model = distribution
        fields = ['num_atrium', 'nom', 'prenom', 'date_validite', 'nbr_beneficiaire', 'nbr_adulte', 'nbr_enfant', 'historique', 'dist']
"""