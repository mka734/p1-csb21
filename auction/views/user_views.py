from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models, transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages
from ..models import UserData
from ..forms import RegisterForm


# Vulnerability (all users can view the page) (FLAW 2)
@login_required
def users_view(request):
    id = request.GET.get('id')
    if id is not None:
        # The line below simulates an SQL injection. An
        # attacker could perform an SQL injection by passing
        # similar line as the value of the id GET parameter.
        # id = '0 UNION SELECT * FROM auth_user LEFT JOIN auction_userdata ON auth_user.id = auction_userdata.user_id WHERE auth_user.id = 1'
        
        # Vulnerability (SQL injection) (FLAW 4)
        user = User.objects.raw(
            'SELECT * FROM auth_user LEFT JOIN auction_userdata ON auth_user.id = auction_userdata.user_id WHERE auth_user.id = {}'.format(id))
        # Vulnerability (all data passed) (FLAW 3)
        user_dict = user[0].__dict__
        if 'password' in user_dict:
            del user_dict['password']
        if '_state' in user_dict:
            del user_dict['_state']
        return TemplateResponse(request, 'users/user.html', {'user_page': user_dict})
    else:
        if request.user.is_superuser:
            users = User.objects.all()
            return TemplateResponse(request, 'users/users.html', {'users': users})
        else:
            return redirect('/unauthorized')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create_user(username, email, password)
            userData = UserData(funds='1000', reserved_funds=0)
            userData.user = user
            userData.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'Account has been created successfully.')
                return redirect(to='/items')
            else:
                messages.error(request, 'Account could not be created.')
                return redirect(to='/login')
        else:
            return redirect('/register')
    else:
        form = RegisterForm()
        return TemplateResponse(request, 'auth/register.html', {'form': form})
