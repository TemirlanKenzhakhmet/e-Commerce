from django.urls import path

from .views import (
    index,
    contact,
    SignUpView,
    LogInView,
    LogOutView,
)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),

]