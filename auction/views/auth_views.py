from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models, transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages
from ..models import Item, Log
from ..forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('name')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect(to='/items')
            else:
                messages.error(request, 'Incorrect username or password.')
                return redirect(to='/login')

    form = LoginForm()
    return TemplateResponse(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(to='/login')


def unauthorized_view(request):
    return TemplateResponse(request, 'auth/unauthorized.html', {})
