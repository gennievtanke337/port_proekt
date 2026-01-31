from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('login/', auth_views.LoginView.as_view(template_name='lms/login.html'), name='login'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('register/', views.register, name='register'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_lesson/<int:module_id>/', views.create_lesson, name='create_lesson'),
    path('select_module/', views.select_module, name='select_module'),
    path('lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('assignment/create/<int:lesson_id>/', views.create_assignment, name='create_assignment'),
    path('assignment/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('assignment/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('manage_roles/', views.manage_roles, name='manage_roles'),
]
