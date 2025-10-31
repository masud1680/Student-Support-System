from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def Home(request):
    return render(request, 'auth/index.html')