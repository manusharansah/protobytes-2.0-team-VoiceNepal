from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('speak/', views.speak_text, name='speak_text'),
]
