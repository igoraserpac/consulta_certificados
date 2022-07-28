from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView

from .forms import CertificadoForm, TransferirCertificadoForm
from .models import *


class TestMixinIsAdmin(UserPassesTestMixin):
    def test_func(self):
        is_admin_or_is_staff = self.request.user.is_superuser or \
            self.request.user.is_staff
        return bool(is_admin_or_is_staff)

    def handle_no_permission(self):
        messages.error(
            self.request, "Você não tem permissões!"
        )
        return redirect("login")


class Login(LoginView):

    model = User
    template_name = 'login.html'
    success_url = 'menu_principal'


class MenuPrincipalView(TemplateView):
    template_name = 'menu_principal.html'


class MenuCadastroView(TemplateView):
    template_name = 'menu_cadastro.html'


class CadastroClienteView(LoginRequiredMixin, TestMixinIsAdmin, CreateView):
    model = Cliente
    login_url = 'login'
    template_name = 'cadastro_clientes.html'
    fields = ['nome', 'responsavel', 'email', 'telefone1', 'telefone2']
    slug_field = 'pk'
    success_url = reverse_lazy('cadastro_certificado')


class CadastroCertificadoView(LoginRequiredMixin, TestMixinIsAdmin, CreateView):
    model = Certificado
    login_url = 'login'
    template_name = 'cadastro_certificado.html'
    fields = [
        'cliente',
        'ticket',
        'produto',
        'emissao',
        'validade',
        'valor',
        'observacao',
    ]
    autocomplete_fields = ['cliente', ]
    success_url = reverse_lazy('menu_principal')


class MenuConsultasView(TemplateView):
    template_name = 'menu_consultas.html'


class ConsultaNomeView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    login_url = 'core:login'
    template_name = 'consulta_nome.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ConsultaNomeView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        result = request.GET
        query = result.get('q', None)
        if query is not None:
            return Cliente.objects.order_by('nome').filter(nome__icontains=query)
        return


class ExibirTodosClientesView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    login_url = 'core:login'
    template_name = 'exibe_clientes.html'

    def get_queryset(self):
        return Cliente.objects.order_by('nome').all()


class VencimentoPorPeriodoView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    login_url = 'core:login'
    template_name = 'vencimento_periodo.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VencimentoPorPeriodoView, self).get_context_data(*args, **kwargs)
        primeiro = self.request.GET.get('p')
        ultimo = self.request.GET.get('u')
        context['primeiro'] = primeiro
        context['ultimo'] = ultimo
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        result = request.GET
        primeiro = result.get('p', None)
        ultimo = result.get('u', None)
        if primeiro is not None and ultimo is not None:
            return Certificado.objects.order_by('-validade').filter(validade__gte=primeiro, validade__lte=ultimo)
        return


class VendidosPorPeriodoView(LoginRequiredMixin, TestMixinIsAdmin, ListView):
    login_url = 'core:login'
    template_name = 'vendidos_periodo.html'
    extra_context = {'soma': 0}

    def get_context_data(self, *args, **kwargs):
        context = super(VendidosPorPeriodoView, self).get_context_data(*args, **kwargs)
        primeiro = self.request.GET.get('p')
        ultimo = self.request.GET.get('u')
        context['primeiro'] = primeiro
        context['ultimo'] = ultimo
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        result = request.GET
        primeiro = result.get('p', None)
        ultimo = result.get('u', None)
        if primeiro is not None and ultimo is not None:
            self.extra_context['soma'] = 0
            certificados = Certificado.objects.order_by('-emissao').filter(emissao__gte=primeiro, emissao__lte=ultimo)
            for c in certificados:
                if c.valor:
                    self.extra_context['soma'] += float(c.valor)
            return certificados
        return


class DetalheClienteView(LoginRequiredMixin, TestMixinIsAdmin, UpdateView):
    model = Cliente
    login_url = 'core:login'
    template_name = 'detalhe_cliente.html'
    fields = ['nome', 'responsavel', 'email', 'telefone1', 'telefone2']
    success_url = reverse_lazy('menu_principal')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetalheClienteView, self).get_context_data(**kwargs)
        certificados = Certificado.objects.filter(cliente=self.get_object())
        context['certificados'] = certificados
        return context


class DeleteClienteView(LoginRequiredMixin, TestMixinIsAdmin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('menu_consultas')
    template_name = 'delete_cliente.html'

    def get_success_url(self):
        messages.success(self.request, "Cliente ecluído com sucesso!")
        return reverse_lazy('menu_consultas')


class DetalheCertificadoView(LoginRequiredMixin, TestMixinIsAdmin, UpdateView):
    model = Certificado
    login_url = 'core:login'
    template_name = 'detalhe_certificado.html'
    form_class = CertificadoForm
    success_url = reverse_lazy('menu_consultas')

    def form_valid(self, form):
        return super().form_valid(form)
