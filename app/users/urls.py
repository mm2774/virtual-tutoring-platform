from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
    path('profile/', views.profile, name='profile'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='templates/users/password/password_reset_done.html'), name='password_reset_done'),

    path("password_reset", views.password_reset_request, name="password_reset"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="templates/users/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='templates/users/password/password_reset_complete.html'), name='password_reset_complete'),      

]
