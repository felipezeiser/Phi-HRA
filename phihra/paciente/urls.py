from django.urls import path
from .views import HomeView,ListaPacientesView, PacienteCreateView, \
    ConsultasListView, ConsultaCreateView, ConsultaDetailView, \
    VisualizarSolicitacaoExameView, SolicitacaoExameCreateView, \
    AnexarArquivoView, ArquivosExamesListView, \
    UploadArquivoExameView, SucessoUploadExamesView, \
    SolicitacoesExameListView, PreverCIDView, ExamesAssociadosACIDView

urlpatterns = [
    # suas outras urls aqui
    path('', HomeView.as_view(), name='home'),
    path('lista_pacientes', ListaPacientesView.as_view(), name='lista_pacientes'),
    path('cadastrar', PacienteCreateView.as_view(), name='cadastrar_paciente'),
    path('pacientes/<int:pk>/consultas/', ConsultasListView.as_view(), name='lista_consultas_paciente'),
    path('consultas/nova/<int:prontuario_id>/', ConsultaCreateView.as_view(), name='cadastrar_consulta'),
    path('consultas/<int:pk>/', ConsultaDetailView.as_view(), name='detalhes_consulta'),
    path('exames/solicitacao/<int:pk>/', VisualizarSolicitacaoExameView.as_view(), name='visualizar_solicitacao_exame'),
    path('exames/solicitar/', SolicitacaoExameCreateView.as_view(), name='solicitar_exame'),
    path('prontuarios/<int:prontuario_id>/anexar/', AnexarArquivoView.as_view(), name='anexar_arquivo'),
    path('paciente/<int:paciente_id>/arquivos-exames/', ArquivosExamesListView.as_view(), name='lista_arquivos_exames_paciente'),
    # path('upload_exame/<int:solicitacao_id>/', UploadExameView.as_view(), name='upload_exame'),
    path('upload_arquivo_exame/<int:solicitacao_exame_id>/', UploadArquivoExameView.as_view(), name='upload_arquivo_exame'),
    path('upload_sucesso/', SucessoUploadExamesView.as_view(), name='upload_sucesso'),
    path('paciente/<int:paciente_id>/solicitacoes_exame/', SolicitacoesExameListView.as_view(), name='solicitacoes_exame'),
    path('paciente/prever_cid/', PreverCIDView.as_view(), name='prever_cid'),
    path('exames/associados/<str:cid_descricao>/', ExamesAssociadosACIDView.as_view(), name='exames_associados_a_cid'),

]
