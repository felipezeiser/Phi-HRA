from django.contrib import admin

from .models import Consulta, Prontuario, Paciente, Exame, SolicitacaoExame, ItemSolicitacaoExame, CID

# Register your models here.
admin.site.register(Consulta)
admin.site.register(Prontuario)
admin.site.register(Paciente)
admin.site.register(Exame)
admin.site.register(SolicitacaoExame)
admin.site.register(ItemSolicitacaoExame)
admin.site.register(CID)
