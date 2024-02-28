import qrcode
from io import BytesIO
import base64

from django.urls import reverse

from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=False)
    cns = models.CharField(max_length=15, unique=False)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='prontuario')
    data_criacao = models.DateField(auto_now_add=True)
    anotacoes = models.TextField(blank=True)
    arquivos = models.ManyToManyField('Arquivo')  # Supondo que você tenha um modelo 'Arquivo'


    def __str__(self):
        return f"Prontuário do {self.paciente.nome}"

class Consulta(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='consultas')
    data_consulta = models.DateTimeField(auto_now_add=True)
    anotacoes = models.TextField(blank=True)

    def __str__(self):
        return f"Consulta em {self.data_consulta.strftime('%d/%m/%Y %H:%M')} - {self.prontuario.paciente.nome}"

class Exame(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='exames')
    tipo_exame = models.CharField(max_length=100)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='exames/')
    data_exame = models.DateField()

    def __str__(self):
        return f"Exame: {self.tipo_exame} - {self.prontuario.paciente.nome}"


class SolicitacaoExame(models.Model):
    prontuario = models.ForeignKey('Prontuario', on_delete=models.CASCADE, related_name='solicitacoes_exames')
    descricao = models.CharField(max_length=255)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    qr_code = models.TextField(blank=True, null=True)  # Para armazenar o QR Code em base64

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Garantir que o ID seja gerado
            super().save(*args, **kwargs)
            # Gerar o QR Code apenas se ele ainda não existe
            self.qr_code = self.gerar_qr_code()
            # Precisamos chamar save novamente para salvar o QR Code gerado
            super().save(update_fields=['qr_code'])

    def gerar_qr_code(self):
        # Lógica para gerar o QR Code e retorná-lo como uma string base64
        url = self.get_absolute_url()  # Método para obter a URL da solicitação de exame
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=5,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def get_absolute_url(self):
        # Retorna a URL absoluta para a visualização da solicitação de exame
        return reverse('anexar_arquivo', kwargs={'prontuario_id': self.prontuario.pk})

class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='prontuarios/')