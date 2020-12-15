from django.shortcuts import render, redirect
from django.views import View


class WelcomeView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('user_home')
        else:
            return render(request, 'myrss/welcome.html')