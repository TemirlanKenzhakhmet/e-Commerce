from django.urls import path

from .views import (
    new_conversation,
    inbox,
    detail,
    new_message,
    detail_message,
    update_message,
    delete_message,
)

app_name = 'conversation'

urlpatterns = [
    path('', inbox, name='inbox'),
    path('<int:pk>/', detail, name='detail'),
    path('new/<int:item_pk>/', new_conversation, name='new'),
    path('message-new/', new_message, name='new-message'),
    path('message-detail/<int:pk>/', detail_message, name='detail-message'),
    path('message-update/<int:pk>/', update_message, name='update-message'),
    path('meesage-delete/<int:pk>/', delete_message, name='delete-message'),
]