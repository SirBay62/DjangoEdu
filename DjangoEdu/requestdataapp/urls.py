from django.urls import path

from .views import process_get_view, user_form, handle_file_upload

app_name = 'requestdataapp'

urlpatterns = [
    # path('', process_get_view),
    path('get/', process_get_view),
    path('bio/', user_form, name='user-form'),
    path('upload/', handle_file_upload, name='file-upload'),
]


