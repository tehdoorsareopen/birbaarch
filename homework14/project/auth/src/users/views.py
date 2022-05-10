import base64
import json
import urllib.parse
import urllib.request

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import User
from .serializers import UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, format=None):
        user = request.user
        resp = {'user': user.system_id}
        return Response(resp)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # getting token and redirecting
                app_id = request.session['app_id']
                app_secret = request.session['app_secret']
                creds = base64.b64encode(f'{app_id}:{app_secret}'.encode('ascii')).decode('ascii')
                print(creds)
                headers = {
                    'Authorization': f'Basic {creds}'
                }
                print(headers)
                data = {
                    'grant_type': 'password',
                    'username': username,
                    'password': password
                }
                req = urllib.request.Request(
                    'http://host.docker.internal:3000/o/token/',
                    method='POST',
                    data=urllib.parse.urlencode(data).encode('ascii'),
                    headers=headers
                )
                resp = urllib.request.urlopen(req)
                data = json.loads(resp.read())
                # messages.success(request, data)
                redirect_url = request.session.get('callback_url') + '?token=' + data['access_token']
                # messages.success(request, redirect_url)
                return redirect(redirect_url)
        else:
            messages.error(request, 'username or password not correct')           
    else:
        callback_url = request.GET.get('callback_url')
        app_id = request.GET.get('id')
        app_secret = request.GET.get('secret')
        # Saving data for redirect after login from any page
        if callback_url and app_id and app_secret:
            request.session['callback_url'] = callback_url
            request.session['app_id'] = app_id
            request.session['app_secret'] = app_secret
        messages.success(request, request.session['callback_url'])
        form = AuthenticationForm()
    return render(request,'registration/login.html', {'form': form})