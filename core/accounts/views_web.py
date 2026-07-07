from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import User


# ─── فرم‌ها ───────────────────────────────────────────────

class WebLoginForm(forms.Form):
    email    = forms.EmailField(label="ایمیل")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)


class WebSignupForm(forms.Form):
    email = forms.EmailField(label="ایمیل")
    role  = forms.ChoiceField(
        label="نقش",
        choices=[("MANAGER", "مدیر ساختمان"), ("RESIDENT", "ساکن")],
    )
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "رمزهای عبور با هم مطابقت ندارند.")
        return cleaned


# ─── ویوها ───────────────────────────────────────────────

def home_view(request):
    return render(request, "core/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = WebLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email    = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "خوش آمدید!")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "ایمیل یا رمز عبور اشتباه است.")

    return render(request, "accounts/login.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = WebSignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email    = form.cleaned_data["email"]
        role     = form.cleaned_data["role"]
        password = form.cleaned_data["password1"]

        # چون USERNAME_FIELD = "email"، create_user اول email می‌گیره
        user = User(email=email, role=role)
        user.set_password(password)
        user.save()

        login(request, user)
        messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
        return redirect("/")

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "از حساب خود خارج شدید.")
    return redirect("/accounts/web/login/")
