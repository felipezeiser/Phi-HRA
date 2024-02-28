from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PacienteForm, ConsultaForm, SolicitacaoExameForm, AnexarArquivoForm
from .models import Paciente, Consulta, SolicitacaoExame, Prontuario, Arquivo

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
        return Consulta.objects.filter(prontuario__paciente__pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs.get('pk')  # Assegura que paciente_id esteja disponível no contexto
        return context
    
class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'cadastrar_consulta.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        descricao_exame = form.cleaned_data.get('descricao_exame')
        if descricao_exame:
            self.exame = SolicitacaoExame.objects.create(
                prontuario=self.object.prontuario,
                descricao=descricao_exame
            )
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
    model = Arquivo
    template_name = 'lista_arquivos_exames.html'
    context_object_name = 'arquivos'

    def get_queryset(self):
        # Filtra os arquivos pelo prontuário do paciente, usando o ID do paciente passado na URL
        # Supondo que você tenha uma maneira de associar Arquivos diretamente a um Prontuario
        return Arquivo.objects.filter(prontuario__paciente__pk=self.kwargs.get('paciente_id'))