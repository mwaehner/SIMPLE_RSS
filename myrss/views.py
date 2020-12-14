from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    else:
        return render(request, 'myrss/welcome.html')
