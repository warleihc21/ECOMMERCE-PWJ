from django.db import models
from django.contrib.auth.models import User


class CadastroCliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    data_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario