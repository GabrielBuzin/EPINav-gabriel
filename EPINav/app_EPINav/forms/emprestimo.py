from django import forms
from app_EPINav.models.emprestimo import Emprestimo
from app_EPINav.models.equipamento import Equipamento
from django.utils import timezone

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['equipamento', 'data_prevista_devolucao', 'observacao_devolucao']
        widgets = {
            'data_prevista_devolucao': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'equipamento': forms.Select(attrs={'class': 'form-select'}),
            'observacao_devolucao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean_data_prevista_devolucao(self):
        data = self.cleaned_data.get('data_prevista_devolucao')
        if data and data <= timezone.now():
            raise forms.ValidationError(
                "A data prevista para devolução deve ser posterior à data e hora atual."
            )
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = Equipamento.objects.exclude(estado="emprestado")

        # Se for edição, inclui também o equipamento já vinculado ao empréstimo
        if self.instance and self.instance.pk and self.instance.equipamento:
            qs = qs | Equipamento.objects.filter(pk=self.instance.equipamento.pk)

        self.fields["equipamento"].queryset = qs
