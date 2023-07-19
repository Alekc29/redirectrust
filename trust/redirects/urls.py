from django.urls import path

from . import views

app_name = 'redirects'

urlpatterns = [
    path('', views.index, name='index'),
    path('en/', views.index_en, name='index_en'),
    path('unisender/', views.user_get_link, name='unisender'),
    path('unisender/result', views.user_get_result, name='uni_result'),
    path('stats/', views.user_get_stats, name='stats'),
    path('feedback/', views.create_feedback, name='feedback'),
    path('feedback/thank/', views.FeedbackThanks.as_view(), name='thanks'),
]