from django import forms 

class LoginForm(forms.Form):

    usuario = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

class RegistroForm(forms.Form):

    usuario = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))