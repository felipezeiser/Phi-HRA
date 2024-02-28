from django.urls import path
from .views import ProfissionalSaudeLoginView, LogoutView
from .forms import CustomLoginForm

urlpatterns = [
    path('', ProfissionalSaudeLoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]