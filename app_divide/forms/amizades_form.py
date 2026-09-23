from django import forms

from app_divide.models import Amizade



class ConvidarForm(forms.Form):
    mail_destinatario = forms.EmailField(required=True, 
                                         widget=forms.EmailInput(attrs={'class':'form-controls','placeholder':'Insira um endereço de e-mail', 'autocomplete':'mail'}))