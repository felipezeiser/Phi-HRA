from django import forms
from .models import Paciente, Consulta, SolicitacaoExame, CID, Arquivo, Exame, ItemSolicitacaoExame

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
    descricao_exame = forms.CharField(required=False, label='Motivo do Exame')
    cids = forms.ModelMultipleChoiceField(queryset=CID.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    exames = forms.ModelMultipleChoiceField(queryset=Exame.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    # print(print(dir(cids)))
    
    class Meta:
        model = Consulta
        fields = ['prontuario', 'anotacoes', 'descricao_exame', 'cids', 'exames']
        widgets = {'prontuario': forms.HiddenInput()}  # Torna o campo prontuário um campo oculto

    def __init__(self, *args, **kwargs):
        prontuario_id = kwargs.pop('prontuario_id', None)
        super(ConsultaForm, self).__init__(*args, **kwargs)
        
        if prontuario_id:
            self.fields['prontuario'].initial = prontuario_id
            self.fields['prontuario'].disabled = True  # Opcional, para garantir que não seja alterado

        for fieldname, field in self.fields.items():
            # print(fieldname)
            if fieldname != 'cids' and fieldname != 'exames':
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-check-label'
                })
        

class AnexarArquivoForm(forms.Form):
    arquivo = forms.FileField(label='Selecionar arquivo')

    def __init__(self, *args, **kwargs):
        super(AnexarArquivoForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo']


class ArquivoItemSolicitacaoExameForm(forms.ModelForm):
    item_solicitacao_exame_id = forms.ModelChoiceField(
        queryset=ItemSolicitacaoExame.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),  # Adiciona a classe form-control ao select
        empty_label=None
    )

    class Meta:
        model = Arquivo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),  # Adiciona a classe form-control ao input de arquivo
        }

    def __init__(self, *args, **kwargs):
        solicitacao_exame_id = kwargs.pop('solicitacao_exame_id', None)
        super(ArquivoItemSolicitacaoExameForm, self).__init__(*args, **kwargs)
        if solicitacao_exame_id:
            self.fields['item_solicitacao_exame_id'].queryset = ItemSolicitacaoExame.objects.filter(solicitacao_exame_id=solicitacao_exame_id)
