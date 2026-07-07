from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import RegexValidator
from accounts.models import User


# ─── فرم‌ها ───────────────────────────────────────────────

class WebLoginForm(forms.Form):
    username = forms.CharField(label="شماره موبایل")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)


class WebSignupForm(forms.Form):
    phone_validator = RegexValidator(
        regex=r"^\+98\d{10}$",
        message="شماره موبایل باید با +98 شروع شود. مثال: +989123456789",
    )
    phone = forms.CharField(
        label="شماره موبایل",
        validators=[phone_validator],
    )
    role = forms.ChoiceField(
        label="نقش",
        choices=[("MANAGER", "مدیر ساختمان"), ("RESIDENT", "ساکن")],
    )
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("این شماره قبلاً ثبت شده است.")
        return phone

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
        phone = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"خوش آمدید!")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "شماره موبایل یا رمز عبور اشتباه است.")

    return render(request, "accounts/login.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = WebSignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        phone    = form.cleaned_data["phone"]
        role     = form.cleaned_data["role"]
        password = form.cleaned_data["password1"]

        user = User.objects.create_user(phone=phone, password=password, role=role)
        login(request, user)
        messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
        return redirect("/")

    return render(request, "accounts/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "از حساب خود خارج شدید.")
    return redirect("/accounts/web/login/")
