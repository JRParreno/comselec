from django.urls import path
from . import views

urlpatterns = [
    path('voter_login/', views.viewPollLogin,
            name='poll-home'),
]