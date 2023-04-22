from django import template
from loja_app.models import Imagem

register = template.Library()

@register.filter(name='get_first_imagem')
def ger_first_imagem(product):
    imagem = Imagem.objects.filter(produto=product). first()
    if imagem:        
        return imagem.imagem.url
    else:
        return False