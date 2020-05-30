from django.urls import path
from . import views

urlpatterns = [
	path('', views.checkElection,
            name='poll-check'),
    path('voter_login/<int:pk>/', views.viewPollLogin,
            name='poll-login'),
    path('voter_login/get_voter/<str:voter>/', views.getStudentDetail,
            name='poll-voter-detail'),
    path('comselec/official_ballot/<int:pk>/<str:type>/', views.officialBallot,
            name='official-ballot'),
    path('comselec/summary/<int:pk>/<str:type>/', views.SubmitVote,
            name='summary-vote'),
    path('comselec/summary/print/<int:pk>/', views.PrintVote,
            name='print-vote'),
]