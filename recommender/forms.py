from django import forms

class LevelOfEducationForm(forms.Form):
    level_of_education = forms.ChoiceField()