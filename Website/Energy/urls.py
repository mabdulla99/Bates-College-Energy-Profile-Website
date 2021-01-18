from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('upload/', views.upload_data, name='upload'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
