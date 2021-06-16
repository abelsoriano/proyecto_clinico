# Django
from django.urls import path

# Vistas
from .vistas import HomeView

app_name = 'compartido'

urlpatterns=[
    #...home, about, contact
    path('', HomeView, name='inicio')
]