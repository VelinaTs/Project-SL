#Vsichki vryzki s otdelnite linkove
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.base_view, name='base_view'),
    path('login/', views.login_view, name='login_view'),
    path('singup/', views.singup_view, name='singup_view'),
    path('save_chas/', views.save_chas_view, name='save_chas_view'),
    path('chat/', views.chat_view, name='chat_view'),
    path('home/', views.home_view, name='home_view'),
]