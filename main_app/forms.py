from django import forms

class NameForm(forms.Form):
	summoner_name = forms.CharField(label = 'Please enter your summoner name', max_length=20)
