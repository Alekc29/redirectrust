from django.urls import path

from . import views

app_name = 'redirects'

urlpatterns = [
    path('', views.index, name='index'),
    path('en/', views.index_en, name='index_en'),
    path('office/', views.user_get_link, name='office'),
    path('office/result', views.user_get_result, name='result'),
]