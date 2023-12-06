from django.urls import path

from . import views

app_name = 'redirects'

urlpatterns = [
    path('', views.index, name='index'),
    path('en/', views.index_en, name='index_en'),
    path('unisenders/', views.user_get_link, name='unisenders'),
    path('unisenders/result', views.user_get_result, name='uni_result'),
    path('mailos/', views.user_get_link_mailo, name='mailos'),
    path('mailos/result', views.user_get_result_mailo, name='mailos_result'),
    path('selzys/', views.user_get_link_selzy, name='selzys'),
    path('selzys/result', views.user_get_result_selzy, name='selzys_result'),
    path('stats/', views.user_get_stats, name='stats'),
    path('feedbacks/', views.create_feedback, name='feedbacks'),
    path('feedbacks/thanks/', views.FeedbackThanks.as_view(), name='thanks'),
    path('emails/', views.check_email, name='emails'),
    path('ghunts/', views.ghunt_email, name='ghunts'),
]