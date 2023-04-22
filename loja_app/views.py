from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.edit import CreateView, FormView
from loja_app.models import Produto, Categoria, Carrinho, CarrinhoProduto, OrdemPedido
from django.urls import reverse_lazy
from .forms import OrdemPedidoForm, ClienteRegistrarform, ClienteEntrarForm
from loja_app import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from email import message
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import date
from .models import Categoria, Produto, Imagem
from django import forms
from PIL import Image, ImageDraw
from io import BytesIO
import sys
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
import stripe
import locale
from django.contrib.auth.decorators import login_required
import mercadopago





class LojaMixin(object):
    def dispatch(self, request, *args, **kwargs):
        carrinho_id = request.session.get("carrinho_id")
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            if request.user.is_authenticated and request.user.cliente:
                carrinho_obj.cliente = request.user.cliente
                carrinho_obj.save()                
        return super().dispatch(request, *args, **kwargs)




class index(LojaMixin, TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_produtos = Produto.objects.all().order_by("-id")
        paginator = Paginator(all_produtos,9)
        page_number = self.request.GET.get('page')
        produto_list = paginator.get_page(page_number)
        context['produto_list'] = produto_list
        return context


class TodosProdutosView(LojaMixin, TemplateView):
    template_name = "todosprodutos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todascategorias'] = Categoria.objects.all().order_by("-id")

        return context

class ProdutoDetalheView(LojaMixin, TemplateView):
    template_name = "produtodetalhe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        produto.visualizacao +=1
        produto.save()
        context['produto'] = produto
        return context


class AddCarrinhoView(LojaMixin, TemplateView):
    template_name = "addcarrinho.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carrinho_id = self.request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            produto_no_carrinho = carrinho_obj.carrinhoproduto_set.filter(produto=produto_obj)

            if produto_no_carrinho.exists():

                carrinhoproduto = produto_no_carrinho.last()
                carrinhoproduto.quantidade += 1
                carrinhoproduto.subtotal += produto_obj.venda
                carrinhoproduto.save()
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()

            else:
                carrinhoproduto = CarrinhoProduto.objects.create(
                    carrinho = carrinho_obj,
                    produto = produto_obj,
                    valor = produto_obj.venda,
                    quantidade = 1,
                    subtotal = produto_obj.venda,
                )
                carrinho_obj.total += produto_obj.venda
                carrinho_obj.save()            

        else:            
            carrinho_obj = Carrinho.objects.create(total=0)
            self.request.session["carrinho_id"]=carrinho_obj.id
            carrinhoproduto = CarrinhoProduto.objects.create(
                carrinho = carrinho_obj,
                produto = produto_obj,
                valor = produto_obj.venda,
                quantidade = 1,
                subtotal = produto_obj.venda,
            )
            carrinho_obj.total += produto_obj.venda
            carrinho_obj.save()
            
            return context


class ManipularCarrinhoView(LojaMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_obj = CarrinhoProduto.objects.get(id=cp_id)
        carrinho_obj = cp_obj.carrinho
        
        if acao =="inc":
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.valor
            cp_obj.save()
            carrinho_obj.total += cp_obj.valor
            carrinho_obj.save()
        elif acao =="dcr":
            cp_obj.quantidade -= 1
            cp_obj.subtotal -= cp_obj.valor
            cp_obj.save()
            carrinho_obj.total -= cp_obj.valor
            carrinho_obj.save()
            if cp_obj.quantidade == 0:
                cp_obj.delete()
            
        elif acao =="rmv":
            carrinho_obj.total -= cp_obj.subtotal
            carrinho_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect("loja_app:meucarrinho")




class LimparCarrinhoView(LojaMixin, View):
    def get(self, request, *args, **kwargs):        
        carrinho_id = request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
            carrinho.carrinhoproduto_set.all().delete()
            carrinho.total = 0
            carrinho.save()
            messages.add_message(request, messages.SUCCESS, "O Carrinho foi esvaziado com sucesso!" )
        return redirect("loja_app:meucarrinho")



class MeuCarrinhoView(LojaMixin, TemplateView):
    template_name = "meucarrinho.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        carrinho_id = self.request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho = None
        context['carrinho'] = carrinho
        return context


class ProcessarCompraView(LojaMixin, CreateView):
    template_name = "processarcompra.html"
    form_class = OrdemPedidoForm
    success_url = reverse_lazy("loja_app:index")

    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect("/entrar/?next=/processar-compra/")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        carrinho_id = self.request.session.get("carrinho_id", None)
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
        else:
            carrinho_obj = None
        context['carrinho'] = carrinho_obj
        return context

    def form_valid(self, form):
        carrinho_id = self.request.session.get("carrinho_id")
        if carrinho_id:
            carrinho_obj = Carrinho.objects.get(id=carrinho_id)
            form.instance.carrinho = carrinho_obj
            form.instance.subtotal = carrinho_obj.total
            form.instance.desconto = 0
            form.instance.total = carrinho_obj.total
            form.instance.pedido_status = "Pedido Recebido"
            del self.request.session['carrinho_id']
            pm = form.cleaned_data.get("pagamento_method")
            pedido = form.save()
            if pm == "khalti":
                return redirect(reverse("loja_app:pagamento"))
        else:
            return redirect("loja_app:index")
        return super().form_valid(form)  





stripe.api_key = settings.STRIPE_SECRET_KEY
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def process_payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')
        amount = float(amount.replace(',', '.'))  # substitui a vírgula por ponto e converte para float

        try:
            charge = stripe.Charge.create(
                amount = int(amount * 100),
                currency='BRL',
                source=token,
                description='Payment Description'
            )

            # Salvar a transação na base de dados
            # Redirecionar para uma página de sucesso
            return redirect('success')
        except stripe.error.CardError as e:
            # Erro ao processar o pagamento
            return render(request, 'payment_error.html', {'error': e.error.message})
        
    return render(request, 'process_payment.html')



#mercado pago


    





    





    

class ClienteRegistrarView(CreateView):
    template_name = "clienteregistrar.html"
    form_class = ClienteRegistrarform
    success_url = reverse_lazy("loja_app:index")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url   
         


class SobreView(LojaMixin, TemplateView):
    template_name = "sobre.html"


class ClientePerfilView(TemplateView):
    template_name = "clienteperfil.html"
    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("clienteentrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        cliente = self.request.user.cliente
        context['cliente'] = cliente

        pedidos = OrdemPedido.objects.filter(carrinho__cliente=cliente).order_by("-id")
        context['pedidos'] = pedidos
        return context


class ClientePedidoDetalheView(DetailView):
    template_name = "clientepedidodetalhe.html"
    model = OrdemPedido
    context_object_name="pedido_obj"
    def dispatch(self,request, *args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            pedido = OrdemPedido.objects.get(id=order_id)
            if request.user.cliente != pedido.carrinho.cliente:
                return redirect("loja_app:clienteperfil")
            
        else:
            return redirect("clienteentrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)



class ClienteSairView(View):
    def get(self, request):
        logout(request)
        return redirect("loja_app:index")

class ClienteEntrarView(FormView):
    template_name = "clienteentrar.html"
    form_class = ClienteEntrarForm
    success_url = reverse_lazy("loja_app:index")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Cliente.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Usuário e/ou senha inválidos!"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


# Classe do Admin

class AdminLoginView(FormView):
    template_name = "admin_paginas/adminlogin.html"
    form_class = ClienteEntrarForm
    success_url = reverse_lazy("loja_app:adminindex")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Suas credenciais não correspondem!"})
        return super().form_valid(form)


class AdminRequireMixin(object):
        
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
                pass
            else:
                return redirect("/admin-login/")
            return super().dispatch(request, *args, **kwargs)
        


class AdminIndexView(AdminRequireMixin, TemplateView):
    template_name = "admin_paginas/adminindex.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PedidosPendentes"] = OrdemPedido.objects.filter(pedido_status="Pedido Recebido").order_by("-id")
        return context
    

    
class AdminPedidoDetalheView(AdminRequireMixin, DetailView):
    template_name = "admin_paginas/adminpedidodetalhe.html"

    model = OrdemPedido

    context_object_name = "pedido_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todosstatus"] = PEDIDO_STATUS
        return context




    
class AdminPedidoListaView(AdminRequireMixin, ListView):
    template_name = "admin_paginas/adminpedidolista.html"

    queryset = OrdemPedido.objects.all().order_by("-id")
    context_object_name = "todospedido"





class AdminPedidoMudarStatusView(AdminRequireMixin, View):
        def post(self, request, *args, **kwargs):
            pedido_id = self.kwargs["pk"]
            pedido_obj = OrdemPedido.objects.get(id=pedido_id)
            novo_status = request.POST.get("status")
            pedido_obj.pedido_status = novo_status
            pedido_obj.save()
            messages.add_message(request, messages.INFO, "Status do pedido alterado!" )

            return redirect(reverse_lazy("loja_app:adminpedidodetalhe", kwargs={"pk": pedido_id}))
    



class PesquisarView(TemplateView):
    template_name = "pesquisar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Produto.objects.filter(
            Q(titulo__icontains=kw) | Q(descricao__icontains=kw) | Q(return_devolucao__icontains=kw))
        context["results"] = results

        return context
    
@login_required
def add_produto(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'admin_paginas/add_produto.html', {'categorias': categorias})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        preco_compra = request.POST.get('preco_compra')
        preco_mercado = request.POST.get('preco_mercado')
        venda = request.POST.get('venda')
        descricao = request.POST.get('descricao')
        garantia = request.POST.get('garantia')
        return_devolucao = request.POST.get('return_devolucao')
        slug = request.POST.get('slug')
        imagens = request.FILES.getlist('imagens')

        produto = Produto(titulo=titulo,
                           categoria_id=categoria,
                             preco_compra=preco_compra,
                               preco_mercado=preco_mercado,
                                 venda=venda,
                                   descricao=descricao,
                                     garantia=garantia,
                                       return_devolucao=return_devolucao,
                                        slug=slug)
        
        produto.save()

        for f in request.FILES.getlist('imagens'):
            img = Imagem(imagem = f, produto=produto)
            img.save()
            messages.add_message(request, messages.SUCCESS, "Produto cadastrado com sucesso!" )
        return redirect(reverse('loja_app:add_produto'))
    




    



