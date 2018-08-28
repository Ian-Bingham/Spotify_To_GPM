from django import forms


class GPMLoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)