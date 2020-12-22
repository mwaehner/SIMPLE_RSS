from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy



class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "myrss/signup_form.html"
    success_url = reverse_lazy('user_home')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        #return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse_lazy('user_home'))
