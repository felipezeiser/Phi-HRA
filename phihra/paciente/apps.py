from django.apps import AppConfig
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os

class PacienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paciente'

    def ready(self):
        import paciente.signals
        global tokenizer, model
        tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        model = BertForSequenceClassification.from_pretrained('paciente/model/', num_labels=5, local_files_only=True)
        model.eval()  # Coloca o modelo em modo de avaliação