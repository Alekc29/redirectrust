from django.urls import path

from . import views

app_name = 'redirects'

urlpatterns = [
    path('', views.index, name='index'),
    path('en/', views.index_en, name='index_en'),
]