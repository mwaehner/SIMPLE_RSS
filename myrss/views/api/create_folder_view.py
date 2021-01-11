from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from http import HTTPStatus
from rest_framework import status
from myrss.forms.subscription_form import SubscriptionForm
from myrss.forms.folder_form import FolderForm
from rest_framework.utils import json
from myrss.models.folder import Folder
from myrss.models.subscription import Subscription
from django.http import JsonResponse

class CreateFolderView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        folder_name = data['name']
        new_folder = Folder(owner=self.request.user)
        new_folder_form = FolderForm(instance=new_folder, data=self.request.POST)
        if new_folder_form.is_valid():
            new_folder = new_folder_form.save()
            response_data = {'success': 'added new folder'}
            status_code = status.HTTP_200_OK
            return JsonResponse(response_data, status=status_code)

        status_code = status.HTTP_400_BAD_REQUEST
        response_data = {'failure': 'you already have a folder with that name'}
        return JsonResponse(response_data, status=status_code)