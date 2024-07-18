from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', views.register, name='register'),
    path('first_login_password_change/', views.first_login_password_change, name='first_login_password_change'),
    path("password_reset2/", views.password_reset_request, name="password_reset2"),
]
