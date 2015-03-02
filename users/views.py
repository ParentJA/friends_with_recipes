__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

User = get_user_model()


@login_required
def home_view(request):
    return render(request, 'users/home.html')


@login_required
def list_view(request):
    search = request.GET.get('search', '')

    query = Q(
        Q(username__icontains=search) |
        Q(email__icontains=search) |
        Q(first_name__icontains=search) |
        Q(last_name__icontains=search)
    )

    users = User.objects.exclude(username=request.user.username).filter(query)

    return render(request, 'users/list.html', {
        'users': users
    })