from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paciente, Prontuario

@receiver(post_save, sender=Paciente)
def criar_prontuario_para_paciente(sender, instance, created, **kwargs):
    if created:
        Prontuario.objects.create(paciente=instance)
