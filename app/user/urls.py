from django.urls import path
from . import views

app_name = 'user'

# Still must update this in our main app urls.py
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
