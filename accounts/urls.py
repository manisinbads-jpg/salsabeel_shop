from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, profile_view, verify_email, verify_pending
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/registration/login.html'
        ),
        name='login'
    ),
]

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("verify-pending/", verify_pending, name="verify_pending"),
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),


]
