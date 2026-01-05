from django.urls import path

from django_project.urls import urlpatterns
from .views import SignUpView

urlpatterns = [
    path ( 'signup/', SignUpView.as_view () )
]