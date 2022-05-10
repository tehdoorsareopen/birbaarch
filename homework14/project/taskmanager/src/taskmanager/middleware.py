import urllib.request
import urllib.parse
from urllib.error import HTTPError

from django.conf import settings
from django.shortcuts import redirect


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
            print(resp.read())
        except HTTPError as e:
            if e.code == 401:  # Unauthorized
                return self.auth_redirect(current_url)
        except Exception as e:
            print(e)





        # tenant_id = request.session.get('tenant_id', -1)
        # user = request.user
        # tenant_user_object = None
        # tenant_user_objects = []

        # if hasattr(user, 'tenants') and tenant_id == -1 and request.path.startswith('/users/profile/'):
        #     default_tenant = user.tenants.first()
        #     tenant_id = default_tenant.pk
        #     request.session['tenant_id'] = int(tenant_id)

        # # Checking if tenant_id in user_tenants
        # if not user.is_superuser and hasattr(user, 'tenant_set') and tenant_id not in [t.id for t in user.tenant_set.all()]:
        #     tenant_id = -1

        # if user.is_authenticated:
        #     if tenant_id == -1:
        #         for tenant in user.tenant_set.all():
        #             tenant_user_objects.append(user.tenantuser_set.get(tenant=tenant))
        #     else:  # if current tenant is set
        #         try:
        #             tenant_user_object = user.tenantuser_set.get(tenant__id=tenant_id)
        #         except Exception:
        #             pass

        # request.tenant_id = tenant_id
        # request.tenant_user_object = tenant_user_object
        # request.tenant_user_objects = tenant_user_objects

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

