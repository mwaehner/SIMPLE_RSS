from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def welcome(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    else:
        return render(request, 'myrss/welcome.html')




@login_required()
def home(request):
    return render(request, 'appUser/home.html')



class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "appUser/signup_form.html"
    success_url = reverse_lazy('user_home')
