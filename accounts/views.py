from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import RegisterForm
from .models import Profile


def verify_pending(request):
    token = request.session.get("verify_token")

    if not token:
        messages.error(request, "No verification found.")
        return redirect("accounts:register")

    return render(request, "accounts/verify_pending.html", {
        "verify_url": f"/accounts/verify/{token}/"
    })

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            profile = user.profile
            profile.phone_number = form.cleaned_data["phone_number"]
            profile.save()

            # 🔑 store token in session (TEMP but safe)
            request.session["verify_token"] = str(profile.email_token)

            return redirect("accounts:verify_pending")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_email(request, token):
    profile = get_object_or_404(Profile, email_token=token)

    if not profile.is_verified:
        profile.is_verified = True
        profile.user.is_active = True
        profile.user.save()
        profile.save()

    messages.success(request, "Account verified successfully!")
    return redirect("accounts:login")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, "Please verify your account first.")
                return redirect("accounts:login")

            login(request, user)
            return redirect("shop:home")

        messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


