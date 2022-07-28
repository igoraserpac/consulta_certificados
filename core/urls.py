from .views import *
from django.urls import path

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('', MenuPrincipalView.as_view(), name='menu_principal'),
    path('menu-cadastro/', MenuCadastroView.as_view(), name='menu_cadastro'),
    path('cadastro-cliente/', CadastroClienteView.as_view(), name='cadastro_cliente'),
    path('cadastro-certificado/', CadastroCertificadoView.as_view(), name='cadastro_certificado'),
    path('consultas/', MenuConsultasView.as_view(), name='menu_consultas'),
    path('consulta-nome/', ConsultaNomeView.as_view(), name='consulta_nome'),
    path('clientes/', ExibirTodosClientesView.as_view(), name='exibir_clientes_ordem_alfabetica'),
    path('consulta-vencimento/', VencimentoPorPeriodoView.as_view(), name='consulta_vencimento'),
    path('consulta-vendidos/', VendidosPorPeriodoView.as_view(), name='consulta_vendidos'),
    path('cliente/<slug:pk>', DetalheClienteView.as_view(), name='detalhe_cliente'),
    path('excluir-cliente/<slug:pk>', DeleteClienteView.as_view(), name='excluir_cliente'),
    path('certificado/<slug:pk>', DetalheCertificadoView.as_view(), name='detalhe_certificado'),
]
