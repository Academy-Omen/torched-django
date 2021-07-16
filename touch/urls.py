from django.urls import path
from . import views

app_name = 'touch'

urlpatterns = [
    path('', views.home, name='home'),
]
