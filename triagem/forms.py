from django import forms
from django.forms import ModelForm


class TriagemForm(forms.Form):
    priority_enum = (
        (0, 'Normal'),
        (1, 'Moderada'),
        (2, 'Alta')
    )
    temperature = forms.FloatField(label='Temperatura em °C', max_value=50, min_value=30, required=True)
    pas = forms.IntegerField(label='Pressão sistólica', required=True, min_value=0, max_value=400)
    pad = forms.IntegerField(label='Pressão diástolica', required=True, min_value=0, max_value=400)
    saturation = forms.IntegerField(label='Satuação do O2 em %', required=True, min_value=0, max_value=100)
    heart_beats = forms.IntegerField(label='Batimentos Cardiacos em BPM', required=True, min_value=0, max_value=600)
    description = forms.CharField(label="Descrição dos sintomas", widget=forms.Textarea())
    priority = forms.ChoiceField(label="Prioridade", choices=priority_enum)
