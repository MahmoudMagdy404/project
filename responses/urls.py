from django.urls import path
from . import views

urlpatterns = [
    path('generate-user/', views.generate_user, name='generate_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('submit-response/', views.submit_response, name='submit_response'),
]
