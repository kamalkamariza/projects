from django import forms
from .models import Match

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

class EditMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'home_score', 'away_team', 'away_score']

class AddMatchForm(forms.ModelForm):
    home_team_name = forms.CharField(max_length=100)
    away_team_name = forms.CharField(max_length=100)

    class Meta:
        model = Match
        fields = ['home_team_name', 'home_score', 'away_team_name', 'away_score']