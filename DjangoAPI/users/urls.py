# urls.py
from django.urls import path
from .views import UserView, TokenView

urlpatterns = [
    path('users/', UserView.as_view(), name='user-getall'),
    path('users/<int:id>/', UserView.as_view(), name='user-get'),
    path('tokens/', TokenView.as_view(), name='token-getall')
]