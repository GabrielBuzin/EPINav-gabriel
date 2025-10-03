# app_EPINav/views/emprestimo.py
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from app_EPINav.models.emprestimo import Emprestimo
from app_EPINav.forms.emprestimo import EmprestimoForm
from app_EPINav.views.decorators import login_required_custom , block_admin_access

@method_decorator(login_required_custom, name="dispatch")
class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = "app_EPINav/pages/emprestimo/emprestimo_list.html"

    def get_queryset(self):
        # se for colaborador, só mostra os dele
        if self.request.session.get("tipo_usuario") == "colaborador":
            return Emprestimo.objects.filter(colaborador_id=self.request.session["usuario_id"])
        return Emprestimo.objects.all()

@method_decorator(login_required_custom, name="dispatch")
@method_decorator(block_admin_access, name="dispatch")
class EmprestimoCreateView(CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'app_EPINav/pages/emprestimo/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    def form_valid(self, form):
        from app_EPINav.models.colaborador import Colaborador
        colaborador_id = self.request.session.get('usuario_id')
        if self.request.session.get('tipo_usuario') == 'colaborador' and colaborador_id:
            form.instance.colaborador = Colaborador.objects.get(id=colaborador_id)
        return super().form_valid(form)


@method_decorator(login_required_custom, name="dispatch")
@method_decorator(block_admin_access, name="dispatch")
class EmprestimoUpdateView(UpdateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "app_EPINav/pages/emprestimo/emprestimo_form.html"
    success_url = reverse_lazy("emprestimo_list")

    def form_valid(self, form):
        messages.success(self.request, "Empréstimo atualizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar empréstimo.")
        return super().form_invalid(form)


