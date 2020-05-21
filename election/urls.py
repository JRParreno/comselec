from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='election-home'),
    #CRUD ssc elections
    path('create/<str:name>/<int:id>/', views.createSSCForm, name='create-ssc-form'),
    path('save/<str:type>', views.saveSSCForm, name='save-ssc-form'),
    path('delete/<str:type>/<int:id>/<int:election_id>/', views.deletePartylist, name='delete-partylist'),
    path('add/election/candidate/<str:type>/<int:partyid>/<int:election_id>/',
        views.addCandidate, 
        name='add-candidate'),
    path('update/<str:type>/<int:id>/<int:election_id>/', views.updatePartylist, name='update-partylist'),
    path('view/<str:type>/<int:id>/', views.viewSSCForm, name='view-ssc-form'),
    path('filter/<str:type>/<int:id>/<int:election_id>/', views.filterSSCForm, name='filter-ssc-form'),
    path('delete/election/candidate/<int:id>/<str:type>/',
        views.deleteCandidate, 
        name='candidate-delete'),
    path('delete/election/disqualify/<int:id>/',
        views.deleteDisqualify, 
        name='disqualify-delete'),
    path('save/election/candidate/<int:id>/<str:type>/update/',
        views.updateCandidate, 
        name='candidate-update'),
    #disqualify
    path('disqualify/election/candidate/<int:id>/<str:type>/',
        views.disqualifyCandidate, 
        name='candidate-disqualify'),
    #view and add voters
    path('add/voter/college/<int:id>', views.addSSCVoter, name='add-ssc-voter'),
    path('view/voter/college/', views.viewSSCVoter, name='view-ssc-voter'),
    path('view/voter/college/filter/<int:id>/', views.filterSSCVoter, name='filter-ssc-voter'),
    path('view/voter/college/update/<int:id>/', views.updateSSCVoter, name='update-ssc-voter'),
    path('view/voter/college/delete/<int:id>/', views.deleteSSCVoter, name='delete-ssc-voter'),
    path('validate/voter/', views.validateStudentNumber, name='validate-ssc-voter'),
    path('check/student_number/voter/', views.checkStudentNumber, name='check-ssc-voter'),
    #view of list utilities
    path('utilities/', views.utilities, name='view-utilities'),
    #CRUD for Campus
    path('utilities/campus_utilities/edit/', 
    	views.createUtilitiesCampus, 
    	name='campus-edit'),
    path('utilities/campus_utilities/add/',
    	views.saveUtilitiesCampus, 
    	name='campus-add'),
    path('utilities/campus_utilities/<int:id>/update/',
        views.updateUtilitiesCampus, 
        name='campus-update'),
    path('utilities/campus_utilities/<int:id>/delete/',
        views.deleteUtilitiesCampus, 
        name='campus-delete'),
    #CRUD for college
    path('utilities/college_utilities/edit', 
        views.createUtilitiesCollege, 
        name='college-edit'),
    path('utilities/college_utilities/edit/<int:id>/', 
        views.filterUtilitiesCollege, 
        name='college-edit-filter'),
    path('utilities/college_utilities/add/',
        views.saveUtilitiesCollege, 
        name='college-add'),
    path('utilities/college_utilities/<int:id>/update/',
        views.updateUtilitiesCollege, 
        name='college-update'),
    path('utilities/college_utilities/<int:id>/delete/',
        views.deleteUtilitiesCollege, 
        name='college-delete'),
    #CRUD for Election
    path('utilities/election_utilities/edit/', 
        views.createUtilitiesElection, 
        name='election-edit'),
    path('utilities/election_utilities/add/',
        views.saveUtilitiesElection, 
        name='election-add'),
    path('utilities/election_utilities/<int:id>/update/',
        views.updateUtilitiesElection, 
        name='election-update'),
    path('utilities/election_utilities/<int:id>/delete/',
        views.deleteUtilitiesElection, 
        name='election-delete'),
    #View pending and active elections CRUD
    path('view/election/<str:name>/',
        views.viewElection, 
        name='view-election'),
    #CRUD for position
    path('utilities/position_utilities/<str:action>', 
        views.createUtilitiesPosition, 
        name='position-edit'),
    path('utilities/position_utilities/sort_save/', 
        views.updateArrangePosition, 
        name='position-arrange-save'),
    path('utilities/position_utilities/<str:action>/<int:id>', 
        views.arrangeUtilitiesPosition, 
        name='position-arrange'),
    path('utilities/position_utilities/<str:action>/<int:id>/', 
        views.filterUtilitiesPosition, 
        name='position-edit-filter'),
    path('utilities/position_utilities/add/',
        views.saveUtilitiesPosition, 
        name='position-add'),
    path('utilities/position_utilities/<int:id>/update/',
        views.updateUtilitiesPosition, 
        name='position-update'),
    path('utilities/position_utilities/<int:id>/delete/',
        views.deleteUtilitiesPosition, 
        name='position-delete'),
    path('test/', views.saveDesign, 
    	name='test'),
]