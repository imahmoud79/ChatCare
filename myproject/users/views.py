from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, f'Account created successfully! You are now logged in.')
            return redirect('chat_home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form}) 