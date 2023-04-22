from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .utils import unique_slug_generator
from django.db.models.signals import pre_save




class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    image = models.ImageField(upload_to="admins")
    tel = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    data_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo



class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)    
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    preco_mercado = models.DecimalField(max_digits=10, decimal_places=2)
    venda = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    garantia = models.CharField(max_length=300, null=True, blank=True)
    return_devolucao = models.CharField(max_length=300, null=True, blank=True)
    visualizacao = models.PositiveIntegerField(default=0) 
      

    def __str__(self):
        return self.titulo
    
    def gerar_desconto(self, desconto):
        return self.venda - ((self.venda * desconto) / 100)
    
    def lucro(self):
        lucro = self.venda - self.preco_compra
        return (lucro * 100) / self.preco_compra
    
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender = Produto)



    
class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imagem_produto")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    
    



class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Carrinho:" + str(self.id)


class CarrinhoProduto(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Carrinho:" + str(self.carrinho.id) + "CarrinhoProduto:" + str(self.id)

PEDIDO_STATUS=(
    ("Pedido Recebido", "Predido Recebido"),
    ("Pedido Processado", "Predido Processado"),
    ("Pedido Caminho", "Predido Caminho"),
    ("Pedido Completado", "Predido Completado"),
    ("Pedido Cancelado", "Predido Cancelado"),
)

METHOD = (
    ("Pix", "Pix"),
    ("Stripe", "Stripe"),
)
    
class OrdemPedido(models.Model):
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=200)
    endereco_envio = models.CharField(max_length=200)
    telefone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    endereco_recebimento = models.CharField(max_length=200)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)
    criado_em = models.DateField(auto_now_add=True)
    pagamento_method = models.CharField(max_length=20, choices=METHOD, default="Pix")
    pagamento_completo = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "OrdemPedido:" + str(self.id) 
    

