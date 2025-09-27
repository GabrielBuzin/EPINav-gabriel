from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # <- importante!
from app_EPINav.models.emprestimo import Emprestimo
from app_EPINav.models.equipamento import Equipamento
from app_EPINav.forms.relatorio import RelatorioStatusForm
from app_EPINav.views.decorators import login_required_custom

@login_required_custom
def relatorios(request):
    colaborador = request.GET.get("colaborador")
    equipamento = request.GET.get("equipamento")
    estado = request.GET.get("estado")

    emprestimos = Emprestimo.objects.all()

    if colaborador:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=colaborador)
    if equipamento:
        emprestimos = emprestimos.filter(equipamento__nome__icontains=equipamento)
    if estado:
        emprestimos = emprestimos.filter(equipamento__estado=estado)

    return render(
        request,
        "app_EPINav/pages/relatorio/relatorio_list.html",
        {
            "emprestimos": emprestimos,
            "estados": Equipamento.ESTADOS,
        },
    )

@login_required_custom
def editar_relatorio(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    equipamento = emprestimo.equipamento

    if request.method == "POST":
        form = RelatorioStatusForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            # Mensagem de sucesso
            messages.success(request, "Status do equipamento atualizado com sucesso!")
            return redirect("relatorios")
        else:
            # Mensagem de erro se o formulário for inválido
            messages.error(request, "Erro ao atualizar o status. Verifique os dados e tente novamente.")
    else:
        form = RelatorioStatusForm(instance=equipamento)

    return render(
        request,
        "app_EPINav/pages/relatorio/relatorio_edit.html",
        {
            "form": form,
            "emprestimo": emprestimo,
        },
    )
