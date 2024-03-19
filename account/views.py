from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .validators import check_phone_number
from .forms import SignupForm, LoginForm, UserDetailsForm
from .models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
    form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            phone_number = form.cleaned_data.get('phone_number')
            if not check_phone_number(phone_number):
                messages.error(request, "Telefon raqam noto'g'ri kiritildi")
                return redirect('register')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            if password1 != password2:
                messages.error(request, "Parollar bir-biriga mos kelmadi")
                return redirect('register')
            user = User.objects.create_user(username=username,
                                            password=password1,
                                            phone_number=phone_number,
                                            email=email)
            login(request, user)
            return redirect('/')
    form = SignupForm()
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='/account/login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/account/login/')
def user_detail(request):
    user = request.user
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if not check_phone_number(phone_number):
                messages.error(request,
                               "Telefon raqamn +998 dan boshlanishi, "
                               "faqat raqamlardan tashkil topgan bo'lishi va "
                               "uzunligi 13 ta bo'lishi kerak ")
                return redirect('user-detail')
            form.save()
            messages.success(request,
                             "Ma'lumotlar muvofaqqiyatli o'zgartirildi")
            return redirect('user-detail')
    else:
        form = UserDetailsForm(instance=user)
    return render(request, 'account/user_detail.html', {'form': form})
