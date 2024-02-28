from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class ProfissionalSaude(AbstractUser):
    nome = models.CharField(max_length=100,null=True,)
    cpf = models.CharField(max_length=11, unique=True, null=True,)
    data_nascimento = models.DateField(null=True,)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, null=True, related_name='profissionais')
    registro_profissional = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.especialidade.nome if self.especialidade else 'Sem Especialidade'}"
