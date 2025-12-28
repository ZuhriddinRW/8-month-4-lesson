from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import *
from serializers import *
from rest_framework.permissions import *

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = AllowAny









