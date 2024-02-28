from django import forms
from .models import Paciente, Consulta, SolicitacaoExame

class SolicitacaoExameForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoExame
        fields = ['descricao']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'cns', 'data_nascimento', 'endereco', 'telefone']

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
    
class ConsultaForm(forms.ModelForm):
    descricao_exame = forms.CharField(required=False, label='Descrição do Exame')

    class Meta:
        model = Consulta
        fields = ['prontuario', 'anotacoes', 'descricao_exame']

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class AnexarArquivoForm(forms.Form):
    arquivo = forms.FileField(label='Selecionar arquivo')

    def __init__(self, *args, **kwargs):
        super(AnexarArquivoForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })