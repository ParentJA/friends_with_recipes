__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render

# Local imports...
from .forms import LogInForm
from .forms import ProfileForm
from .forms import SignUpForm


def home_view(request):
    return render(request, 'accounts/home.html')


def sign_up_view(request):
    form = SignUpForm(request)

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)

        if form.is_valid():
            login(request, form.save())

            return redirect(reverse('users:feed'))

    return render(request, 'accounts/sign_up.html', {
        'form': form
    })


def log_in_view(request):
    form = LogInForm()

    if request.method == 'POST':
        form = LogInForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            return redirect(reverse('users:feed'))

    return render(request, 'accounts/log_in.html', {
        'form': form
    })


@login_required
def log_out_view(request):
    logout(request)

    return redirect(reverse('home'))


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()

            return redirect(reverse('profile'))

    return render(request, 'accounts/profile_edit.html', {
        'form': form
    })