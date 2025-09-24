from django.urls import path
from . import views

urlpatterns = [
    path('reset_password/', views.reset_password, name='reset_password'),
    path('webhook/password-reset/', views.password_reset_webhook, name='password_reset_webhook'),
]