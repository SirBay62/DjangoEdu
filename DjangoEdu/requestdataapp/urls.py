from django.urls import path

from .views import process_get_view, user_form

app_name = 'requestdataapp'

urlpatterns = [
    # path('', process_get_view),
    path('get/', process_get_view),
    path('bio/', user_form, name='user-form'),
]


