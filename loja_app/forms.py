from django import forms
from .models import OrdemPedido, Cliente, Produto
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render




class Checar_PedidoForm(forms.ModelForm):
    class Meta:
        model = OrdemPedido
        fields = ["solicitante", "endereco_envio", "telefone", "email", "pagamento_method"]



class OrdemPedidoForm(forms.ModelForm):
    class Meta:
        model = OrdemPedido
        fields = ["solicitante", "endereco_envio", "telefone", "email", "pagamento_method"]
        widgets = {
            'solicitante': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Pedido por"
            }),

            'endereco_envio': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Endereço de Envio"
            }),

            'telefone': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Telefone"
            }),

            'email': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Email"
            }),
        }



class ClienteRegistrarform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Usuário"
            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Senha"
            }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Email"
            }))
    class Meta:
        model = Cliente
        fields = ["username", "password", "email", "nome_completo", "endereco"]
        widgets = {

            'nome_completo': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Nome Completo"
            }),

            'endereco': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Endereço"
            }),
        }

        def clean_username(self):
            uname = self.cleaned_data.get("username")
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError("Este usuário já existe!")
            return uname 


class ClienteEntrarForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Usuário"
            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Senha"
            }))
    


    
    
  


"""
class AdminAddProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["titulo", "categoria", "preco_mercado", "venda", "descricao", "garantia", "return_devolucao"]
        widgets = {
            'titulo': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Título do produto"
            }),

            'categoria': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Categoria"
            }),

            'preco_mercado': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Preço de mercado"
            }),

            'venda': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Preço de venda"
            }),

            'descricao': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Descrição"
            }),

            'garantia': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Garantia"
            }),

            'return_devolucao': TextInput(attrs={
                'class': "form-control",
                'style': "max-width: 300px;",
                'placeholder': "Política de devolução"
            }),
        }

"""







        
