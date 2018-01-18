from django.urls import path
from . import views

urlpatterns = [
	path('', views.get_name, name='get_name'),
	path('summoner_name/', views.get_name, name='get_name'),
]
