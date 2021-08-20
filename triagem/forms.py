from django import forms
from django.forms import ModelForm


class TriagemForm(forms.Form):
    temperature = forms.FloatField(label='Temperatura em °C', max_value=50, min_value=30, required=True)
    pas = forms.IntegerField(label='Pressão sistólica', required=True)
    pad = forms.IntegerField(label='Pressão diástolica', required=True)
    saturation = forms.IntegerField(label='Satuação do O2 em %', required=True)
    heart_beats = forms.IntegerField(label='Batimentos Cardiacos em BPM', required=True)
    description = forms.CharField(label="Descrição dos sintomas", widget=forms.Textarea())
