from django import forms
from django.utils import timezone
from app_EPINav.models.equipamento import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'descricao', 'fabricante', 'estado', 'quantidade', 'observacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observacao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            allowed_choices = [
                ('emprestado', 'Emprestado'),
                ('em_uso', 'Em uso'),
                ('fornecido', 'Fornecido'),
            ]
            self.fields['estado'].choices = allowed_choices
