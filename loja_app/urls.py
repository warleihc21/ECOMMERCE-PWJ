from django.urls import path
from loja_app import views
from . import views
from .views import *
from django.contrib.auth.views import LogoutView
from .views import process_payment


app_name = 'loja_app'
urlpatterns = [
    
    path('', index.as_view(), name='index'),
    path('todos-produtos/', TodosProdutosView.as_view(), name='TodosProdutos'),
    path('produto/<slug:slug>', ProdutoDetalheView.as_view(), name='ProdutoDetalhe'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('addcarrinho-<int:pro_id>', AddCarrinhoView.as_view(), name='addcarrinho'),
    path('meu-carrinho/', MeuCarrinhoView.as_view(), name='meucarrinho'),
    path("manipular-carrinho/<int:cp_id>/", ManipularCarrinhoView.as_view(), name='manipularcarrinho'),
    path("limpar-carrinho/", LimparCarrinhoView.as_view(), name='limparcarrinho'),
    path("processar-compra/", ProcessarCompraView.as_view(), name='processarcompra'),


    path('process_payment/', process_payment, name='process_payment'),
    




    path("registrar/", ClienteRegistrarView.as_view(), name='clienteregistrar'),
    path("sair/", ClienteSairView.as_view(), name='clientesair'),
    path("entrar/", ClienteEntrarView.as_view(), name='clienteentrar'),
    path("perfil/", ClientePerfilView.as_view(), name='clienteperfil'),
    path("perfil/pedido-<int:pk>/", ClientePedidoDetalheView.as_view(), name='clientepedidodetalhe'),

    path("admin-login/", AdminLoginView.as_view(), name='adminlogin'),
    path("admin-index/", AdminIndexView.as_view(), name='adminindex'),
    path("admin-pedido/<int:pk>/", AdminPedidoDetalheView.as_view(), name='adminpedidodetalhe'),
    path("admin-todos-pedidos/", AdminPedidoListaView.as_view(), name='adminpedidolista'),
    path("admin-pedido-<int:pk>-mudar/", AdminPedidoMudarStatusView.as_view(), name='adminpedidomudar'),

    path("add_produto/", views.add_produto, name='add_produto'),


    path("pesquisar/", PesquisarView.as_view(), name='pesquisar'),

    
    

    
    
]
