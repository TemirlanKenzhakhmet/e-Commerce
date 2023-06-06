from django.urls import path

from .views import indexView

app_name = 'dashboard'

urlpatterns = [
    path('', indexView.as_view(), name='index')
]