__author__ = 'parentj@eab.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

User = get_user_model()


@login_required
def home_view(request):
    return render(request, 'recipes/home.html')