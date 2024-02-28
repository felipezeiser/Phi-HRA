from django.urls import path
from .views import HomeView,ListaPacientesView, PacienteCreateView, ConsultasListView, ConsultaCreateView, ConsultaDetailView, VisualizarSolicitacaoExameView, SolicitacaoExameCreateView, AnexarArquivoView, ArquivosExamesListView

urlpatterns = [
    # suas outras urls aqui
    path('', HomeView.as_view(), name='home'),
    path('lista_pacientes', ListaPacientesView.as_view(), name='lista_pacientes'),
    path('cadastrar', PacienteCreateView.as_view(), name='cadastrar_paciente'),
    path('pacientes/<int:pk>/consultas/', ConsultasListView.as_view(), name='lista_consultas_paciente'),
    path('consultas/nova/', ConsultaCreateView.as_view(), name='cadastrar_consulta'),
    path('consultas/<int:pk>/', ConsultaDetailView.as_view(), name='detalhes_consulta'),
    path('exames/solicitacao/<int:pk>/', VisualizarSolicitacaoExameView.as_view(), name='visualizar_solicitacao_exame'),
    path('exames/solicitar/', SolicitacaoExameCreateView.as_view(), name='solicitar_exame'),
    path('prontuarios/<int:prontuario_id>/anexar/', AnexarArquivoView.as_view(), name='anexar_arquivo'),
    path('paciente/<int:paciente_id>/arquivos-exames/', ArquivosExamesListView.as_view(), name='lista_arquivos_exames_paciente'),

]
