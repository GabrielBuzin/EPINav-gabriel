from django import forms
from app_EPINav.models.equipamento import Equipamento

class RelatorioStatusForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["estado"]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
