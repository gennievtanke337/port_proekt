from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='lms/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
