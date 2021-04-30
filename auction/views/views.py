from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models, transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages
from ..models import Item, UserData, Log


def homepage_view(request):
    return TemplateResponse(request, 'index.html', {'items': []})


@login_required
def logs_view(request):
    if request.user.is_superuser:
        logs = Log.objects.all()
        return TemplateResponse(request, 'logs.html', {'logs': logs})
    else:
        return redirect('/unauthorized')

