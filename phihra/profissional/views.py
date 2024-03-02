from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.shortcuts import redirect


class ProfissionalSaudeLoginView(LoginView):
    template_name = 'login.html'  # Atualizado para a nova localização do template

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('lista_pacientes')  # Substitua pelo nome da sua URL para a página home
        return super().get(request, *args, **kwargs)

class LogoutView(RedirectView):
    url = reverse_lazy('login')  # Substitua pelo nome da URL para a qual você deseja redirecionar após o logout

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)