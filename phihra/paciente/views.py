from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.base import RedirectView, View, TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PacienteForm, ConsultaForm, SolicitacaoExameForm, AnexarArquivoForm, ArquivoForm, ArquivoItemSolicitacaoExameForm
from .models import Paciente, Consulta, SolicitacaoExame, Prontuario, Arquivo, ItemSolicitacaoExame, CID


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .apps import tokenizer, model  # Certifique-se de importar corretamente
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from sklearn.preprocessing import LabelEncoder
import joblib
import json


import os
print(os.listdir())
# label_encoder = LabelEncoder().fit(['lista', 'de', 'cids'])
label_encoder = joblib.load('paciente/labelEncoder.joblib')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redireciona para a listagem de pacientes se o usuário estiver logado
            return redirect(reverse_lazy('lista_pacientes'))  # Certifique-se de que 'lista_pacientes' é o nome correto da sua URL
        else:
            # Redireciona para a página de login ou home para usuários não autenticados
            return redirect(reverse_lazy('home_non_authenticated'))  # Substitua 'home_non_authenticated' pela sua URL de homepage para usuários não autenticados

class ListaPacientesView(ListView):
    model = Paciente
    template_name = 'lista_pacientes.html'
    context_object_name = 'pacientes'

    def get_context_data(self, **kwargs):
        context = super(ListaPacientesView, self).get_context_data(**kwargs)
        # Adiciona a contagem de pacientes, consultas e exames ao contexto
        context['quantidade_pacientes'] = Paciente.objects.count()
        context['quantidade_consultas'] = Consulta.objects.count()
        context['quantidade_exames'] = ItemSolicitacaoExame.objects.filter(arquivo__isnull=False).count()
        return context
    
class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'cadastrar_paciente.html'
    # success_url = reverse_lazy('lista_pacientes')  # Substitua 'lista_pacientes' pela sua URL de sucesso

    def get_success_url(self):
        # Redireciona para a lista de consultas do paciente recém-criado
        return reverse('lista_consultas_paciente', kwargs={'pk': self.object.pk})

class ConsultasListView(ListView):
    model = Consulta
    template_name = 'lista_consultas.html'
    context_object_name = 'consultas'

    def get_queryset(self):
        # Filtra as consultas pelo ID do paciente fornecido na URL
        self.paciente = get_object_or_404(Paciente, pk=self.kwargs.get('pk'))  # Armazena o paciente para uso posterior
        return Consulta.objects.filter(prontuario__paciente=self.paciente)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.paciente  # Adiciona o objeto paciente ao contexto
        context['paciente_id'] = self.kwargs.get('pk')  # Assegura que paciente_id esteja disponível no contexto
        context['prontuario_id'] = self.paciente.prontuario.id if hasattr(self.paciente, 'prontuario') else None

        return context
    
class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'cadastrar_consulta.html'

    def get_form_kwargs(self):
        kwargs = super(ConsultaCreateView, self).get_form_kwargs()
        # Aqui você define como obter o prontuario_id. Pode ser do usuário logado, da URL, etc.
        prontuario_id = self.kwargs.get('prontuario_id')  # Exemplo: obtendo de URL
        kwargs['prontuario_id'] = prontuario_id
        return kwargs

    def form_valid(self, form):
        # print(form)
        self.object = form.save(commit=False)
        self.object.save()
        # descricao_exame = form.cleaned_data.get('descricao_exame')
        # exames_selecionados = form.cleaned_data['exames']
        
        cids = form.cleaned_data.get('cids')
        exames = form.cleaned_data.get('exames')
        print(cids, exames)

        if exames:
            self.exame = SolicitacaoExame.objects.create(prontuario=self.object.prontuario)
            for exame in exames:
                ItemSolicitacaoExame.objects.create(solicitacao_exame=self.exame, exame=exame)
        else:
            self.exame = None
        return super(ConsultaCreateView, self).form_valid(form)

    def get_success_url(self):
        if self.exame:
            # Redireciona para a página de visualização do QR Code da solicitação de exame
            return reverse('visualizar_solicitacao_exame', kwargs={'pk': self.exame.pk})
        else:
            # Se não houver exame, redirecione para outra página, como a lista de consultas
            return reverse('lista_consultas_paciente', kwargs={'pk': self.object.prontuario.paciente.pk})
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prontuario_id = self.kwargs.get('prontuario_id')
        prontuario = Prontuario.objects.get(id=prontuario_id)
        context['paciente'] = prontuario.paciente  # Adiciona o objeto paciente ao contexto
        return context
    
class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = 'consulta_detalhes.html'  # Especifique o caminho do seu template de detalhes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs.get('pk')  # Assume que 'pk' é o ID do paciente passado na URL
        return context

class SolicitacaoExameCreateView(CreateView):
    model = SolicitacaoExame
    form_class = SolicitacaoExameForm
    template_name = 'solicitar_exame.html'

    def form_valid(self, form):
        # Definir o prontuário antes de salvar a solicitação de exame
        form.instance.prontuario = self.get_prontuario()
        return super().form_valid(form)

    def get_prontuario(self):
        # Aqui você deve obter o prontuário ao qual a solicitação de exame será associada
        # Isso pode ser feito, por exemplo, buscando um prontuário por ID passado na URL
        # ou de alguma outra forma que faça sentido no seu caso
        pass

    def get_success_url(self):
        # Redireciona para a página desejada após a criação bem-sucedida da solicitação de exame
        # Por exemplo, de volta à lista de consultas ou prontuários
        return reverse_lazy('sua_url_de_sucesso')


class VisualizarSolicitacaoExameView(DetailView):
    model = SolicitacaoExame
    template_name = 'visualizar_solicitacao_exame.html'

class AnexarArquivoView(FormView):
    template_name = 'anexar_arquivo.html'
    form_class = AnexarArquivoForm
    # success_url = reverse('lista_consultas_paciente', kwargs={'pk': self.object.prontuario.paciente.pk})  # Ajuste conforme necessário

    def form_valid(self, form):
        arquivo_carregado = form.cleaned_data['arquivo']
        prontuario_id = self.kwargs.get('prontuario_id')
        prontuario = Prontuario.objects.get(id=prontuario_id)

        # Cria uma nova instância de Arquivo e salva o arquivo carregado
        novo_arquivo = Arquivo(arquivo=arquivo_carregado)
        novo_arquivo.save()

        # Adiciona a nova instância de Arquivo ao campo ManyToMany 'arquivos' do Prontuario
        prontuario.arquivos.add(novo_arquivo)
        prontuario.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        prontuario_id = self.kwargs.get('prontuario_id')
        prontuario = Prontuario.objects.get(id=prontuario_id)
            
        return reverse('lista_consultas_paciente', kwargs={'pk': prontuario.paciente.pk})

class ArquivosExamesListView(ListView):
    model = ItemSolicitacaoExame
    template_name = 'lista_arquivos_exames.html'
    context_object_name = 'arquivos'

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        self.paciente = Paciente.objects.get(id=paciente_id)
        return ItemSolicitacaoExame.objects.filter(
            solicitacao_exame__prontuario__paciente__id=paciente_id,
            arquivo__isnull=False
        )
    def get_context_data(self, **kwargs):
        context = super(ArquivosExamesListView, self).get_context_data(**kwargs)
        context['paciente'] = self.paciente  # Adiciona o objeto paciente ao contexto
        return context

class UploadArquivoExameView(FormView):
    template_name = 'upload_exame.html'
    form_class = ArquivoItemSolicitacaoExameForm
    # Defina o success_url conforme necessário, por exemplo:
    success_url = reverse_lazy('upload_sucesso')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['solicitacao_exame_id'] = self.kwargs['solicitacao_exame_id']
        return kwargs

    def form_valid(self, form):
        item_solicitacao_exame_id = form.cleaned_data['item_solicitacao_exame_id'].id
        arquivo = form.cleaned_data['arquivo']
        item_solicitacao_exame = ItemSolicitacaoExame.objects.get(id=item_solicitacao_exame_id)
        item_solicitacao_exame.arquivo = arquivo
        item_solicitacao_exame.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitacao_exame_id = self.kwargs.get('solicitacao_exame_id')
        solicitacao_exame = SolicitacaoExame.objects.get(id=solicitacao_exame_id)
        context['itens'] = solicitacao_exame.itens.all()
        
        paciente = solicitacao_exame.prontuario.paciente
        context['paciente'] = paciente

        return context


class SucessoUploadExamesView(TemplateView):
    template_name = 'sucesso_upload_exames.html'


class SolicitacoesExameListView(ListView):
    model = SolicitacaoExame
    template_name = 'solicitacoes_exame_list.html'
    context_object_name = 'solicitacoes_exame'

    def get_queryset(self):
        paciente_id = self.kwargs.get('paciente_id')
        self.paciente = Paciente.objects.get(id=paciente_id)  # Obtém o paciente para uso em get_context_data
        return SolicitacaoExame.objects.filter(prontuario__paciente__id=paciente_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente'] = self.paciente  # Adiciona o objeto paciente ao contexto
        return context
    
@method_decorator(csrf_exempt, name='dispatch')
class PreverCIDView(View):
    def post(self, request, *args, **kwargs):
        # Desserializa o corpo da requisição JSON
        data = json.loads(request.body)
        texto = data.get('texto_prontuario')
        
        # Assegura que um texto foi recebido
        if texto:
            # Prepara o texto para o modelo
            inputs = tokenizer(texto, padding=True, truncation=True, return_tensors="pt")
            # Realiza a predição
            with torch.no_grad():
                outputs = model(**inputs)
            # Obtém o índice da maior predição
            predicao = outputs.logits.argmax(dim=1).tolist()
            # Converte o índice para o CID correspondente
            cid_predito = label_encoder.inverse_transform(predicao)[0]
            print(cid_predito, len(cid_predito))
            
            if cid_predito == 'Normal':
                cid_predito = 'Z00 - Exame Geral E Investigação De Pessoas Sem Queixas Ou Diagnóstico Relatado'
            elif cid_predito == 'DM':
                cid_predito = 'E11 - Diabetes Mellitus Não Insulino Dependente'
            elif cid_predito == 'DPOC':
                cid_predito = 'J449 - Doença Pulmonar Obstrutiva Crônica Não Especificada'
            elif cid_predito == 'HAS':
                cid_predito = 'I10 - Hipertensão essencial'
            elif cid_predito == 'Depressão':
                cid_predito = 'F32 - Episódios Depressivos'

            # Retorna o CID predito como resposta JSON
            return JsonResponse({'cid_predito': cid_predito})
        else:
            return JsonResponse({'error': 'Nenhum texto fornecido'}, status=400)
        

class ExamesAssociadosACIDView(View):
    def get(self, request, *args, **kwargs):
        cid_descricao = kwargs.get('cid_descricao')
        print(cid_descricao.split(' - '))
        cid = CID.objects.filter(descricao=cid_descricao.split(' - ')[1]).first()
        print(cid, 'essa')
        if not cid:
            return JsonResponse({'exames': []})
        exames = cid.exames_comuns.values_list('id', flat=True)
        print(exames)
        return JsonResponse({'exames': list(exames)})