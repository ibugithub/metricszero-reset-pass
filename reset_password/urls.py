from django.urls import path
from . import views

urlpatterns = [
    path('reset_password/', views.reset_password, name='reset_password'),
]