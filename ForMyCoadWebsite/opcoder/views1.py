from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import FeedbackForm
from .models import UserFeedback

# For login logic and comment logic.

def error_page(request):
    return render(request, 'opcoder/error.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User Already Exists.")

        user = User.objects.create_user(
            first_name=first_name,
            email=email,
            username=username
        )
        user.set_password(password)
        user.save()

        return redirect('/login/')

    return render(request, "opcoder/signup.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect password")
        else:
            login(request, user)
            return redirect("/")

    return render(request, "opcoder/login.html")


def logout_page(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/login')
        else:
            messages.error(request, "Input fields are not valid.")

    return render(request, "opcoder/change_password.html")


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            if request.user.is_authenticated:
                new_feedback.user = request.user

            new_feedback.save()
            messages.success(request, 'Thank you! Your feedback has been successfully submitted.')
            return redirect("/feedback")
        else:
            messages.error(request, "Admission form is showing invalid.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['name'] = request.user.get_full_name() or request.user.username
            initial_data['email'] = request.user.email

        form = FeedbackForm(initial=initial_data)

    context = {'form': form}
    return render(request, "opcoder/feedback.html", context)
