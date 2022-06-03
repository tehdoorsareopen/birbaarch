import json

import urllib.request
import urllib.parse
from urllib.error import HTTPError

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect

from .models import User


class AppAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.auth_app_id = settings.AUTH_APP_ID
        self.auth_app_secret = settings.AUTH_APP_SECRET
        self.auth_app_get_current_user_url = settings.AUTH_APP_GET_CURRENT_USER_URL
        self.auth_app_login_form_url = settings.AUTH_APP_LOGIN_FORM_URL

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Trying to get token from request = redirected from login
        auth_app_login_token = request.GET.get('token')
        if auth_app_login_token:
            request.session['AUTH_APP_TOKEN'] = auth_app_login_token

        current_url = request.build_absolute_uri()
        auth_app_token = request.session.get('AUTH_APP_TOKEN')

        if not auth_app_token:
            return self.auth_redirect(current_url)
            # auth_app_token = 'uloyLp2mCC4kPswoSmv16Jw2Y1Bziy'
            # self.auth_redirect(current_url)

        # trying to get current user from auth app
        try:
            headers = {
                'Authorization': f'Bearer {auth_app_token}'
            }
            req = urllib.request.Request(self.auth_app_get_current_user_url, headers=headers)
            resp = urllib.request.urlopen(req)
            resp_data = json.loads(resp.read())
            user_system_id = resp_data['user']
            user = User.objects.get(system_id=user_system_id)
            request.user = user
        except HTTPError as e:
            del request.user
            if e.code == 401:  # Unauthorized
                return self.auth_redirect(current_url)
        except Exception as e:
            print(e)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # Custom Methods

    def auth_redirect(self, current_url):
        qparams = {
            'callback_url': current_url,
            'id': self.auth_app_id,
            'secret': self.auth_app_secret,
        }
        redirect_url = self.auth_app_login_form_url + '?' + urllib.parse.urlencode(qparams)
        return redirect(redirect_url)
