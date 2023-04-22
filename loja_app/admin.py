from django.contrib import admin
from loja_app.models import *
from .models import Categoria, Produto


admin.site.register([Admin, Cliente, Carrinho, CarrinhoProduto, OrdemPedido])
admin.site.register(Categoria)

class add_produto(admin.ModelAdmin):
	list_display = ('__str__', 'slug')
	class meta:
		model = Produto

admin.site.register(Produto, add_produto)