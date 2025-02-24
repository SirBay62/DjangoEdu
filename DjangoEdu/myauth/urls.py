from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import path
from .views import login_view
from .views import (
    get_cookie_view,
    get_session_view,
    set_session_view,
    set_cookie_view,
    logout_view
)

app_name = 'myauth'

urlpatterns = [
    # path('login/', login_view, name='login'),
    path ( 'login/',
           LoginView.as_view ( template_name='myauth/login.html',
                               redirect_authenticated_user=True ),
           name='login' ),

    path( 'logout/',logout_view, name='logout' ),

    path ( 'cookie/get', get_cookie_view, name='cookie_get' ),
    path ( 'session/get', get_session_view, name='session_get' ),

    path ( 'cookie/set', set_cookie_view, name='cookie_set' ),
    path ( 'session/set',  set_session_view, name='session_set' ),
]
