from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('api/activate/', views.activate_account, name='activate'),
    path('api/resend-activation/', views.resend_activation_code,
         name='resend_activation'),
]
