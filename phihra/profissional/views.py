from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import RedirectView


class ProfissionalSaudeLoginView(LoginView):
    template_name = 'login.html'  # Atualizado para a nova localização do template

class LogoutView(RedirectView):
    url = reverse_lazy('login')  # Substitua pelo nome da URL para a qual você deseja redirecionar após o logout

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)