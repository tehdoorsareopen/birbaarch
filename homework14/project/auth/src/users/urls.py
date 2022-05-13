from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import CurrentUser, UserDetails, UserLogout, user_login, user_profile


app_name = 'users'

urlpatterns = [
    # path('users/', include('django.contrib.auth.urls')),
    path('users/logout/', UserLogout.as_view(), name='logout'),
    path('users/login/', user_login, name='login'),
    path('users/profile/', user_profile, name='profile'),
    path('users/current/', CurrentUser.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
]