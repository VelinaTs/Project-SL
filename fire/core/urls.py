#Vsichki vryzki s otdelnite linkove
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.base_view, name='base_view'),
    path('login/', views.login_view, name='login_view'),
    path('singup/', views.singup_view, name='singup_view'),
    path('save_chas/', views.save_chas_view, name='save_chas_view'),
    path('chat/', views.chat_view, name='chat_view'),
    path('home/', views.home_view, name='home_view'),
    path('home_admin/', views.home_admin_view, name='home_admin_view'),
    path('add_barber/', views.add_barber_view, name='add_barber_view'),
    path('logout/', views.logout, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
