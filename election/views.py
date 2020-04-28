from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from . import customAlert
from .forms import (
	CampusForm, 
	CollegeForm,
	ElectionTypeForm,
	PositionForm,
	PartyForm,
	CandidateForm,
	)
from .models import (
	Campus, 
	College,
	ElectionType,
	Position,
	Election,
	Party,
	Candidate
	)
from django.shortcuts import get_list_or_404, get_object_or_404

@login_required
def home(request):
    return render(request, 'election/home.html')

 
@login_required
def create(request, name,id):
	context = {
		'positions': Position.objects.all(),
		'electionTypeId': id,
		'electionTypeName': name
	}
	return render(request,'election/administrator/candidates/create_ssc_form.html', context)

@login_required
def saveCandidateForm(request):
	
	if request.is_ajax():
		#from ajax request
		extras = request.POST.getlist('Extras[]')
		electionType = request.POST.get('ElectionType')
		candidates = request.POST.getlist('CandidateNames[]')
		ids = request.POST.getlist('Ids[]')
		c = len(ids)

		#insert extras (partylist name)
		electioTypeId = ElectionType.objects.get(id=electionType)
		p_form = Party.objects.create(
			party_name=extras[0],
			acronym=extras[1],
			election_type = electioTypeId)
		p_form.save()
		#loop array from the form
		for i in range(c):
			dct = json.loads(ids[i])
			c_form = CandidateForm({'candidate_name': candidates[i],
				'position': dct['positionId'],
				'party': p_form.id,
				'campus': dct['campusId'],
				'college': dct['collegeId']})
			if c_form.is_valid():
				c_form.save()
				messages.success(request, customAlert.SaveAlert('TEST'))
		
		context = {
		'candidates' : Candidates.objects.all().filter(id=p_form.id)
		}
		return render(request,'election/administrator/candidates/view_ssc_form.html', context)

@login_required
def utilities(request):
	return render(request, 'election/administrator/utilities/view_utilities.html')


#views of Campus
@login_required
def createUtilitiesCampus(request):
	model = Campus.objects.all().order_by('id')
	context = {
		'campuses': model,
		'objectCount': model.count()
	}
	
	return render(request, 'election/administrator/utilities/edit_campus_utilities.html', 
	context)


@login_required
def saveUtilitiesCampus(request):
	if request.method == 'POST':
		campuses = request.POST.getlist('inputName')
		c = len(campuses)
		for i in range(c):	
			form = CampusForm({'campus_name': campuses[i]})

			if form.is_valid():
				messages.success(request, customAlert.SaveAlert(campuses[i]))
				form.save()
		return HttpResponseRedirect(reverse('campus-edit'))
	else:
		
		return render(request, 'election/administrator/utilities/create_campus_utilities.html')

@login_required
def updateUtilitiesCampus(request, id=None):
	newName = request.POST.get('inputEdit')

	if request.method == 'POST':
		Campus.objects.filter(pk=id).update(campus_name=newName)
		messages.info(request, customAlert.UpdateAlert(newName))
		
	else:
		form = CampusForm(instance=campus)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/campus_utilities/edit/'))


@login_required
def deleteUtilitiesCampus(request, id=None):
	if request.method == 'POST':
		messages.warning(request, customAlert.DeleteAlert())
		College.objects.all().filter(campus_id=id).delete()
		Campus.objects.filter(pk=id).delete()
	else:
		form = CampusForm(instance=campus)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/campus_utilities/edit/'))

#end of views Campus

#views of College
@login_required
def createUtilitiesCollege(request):
	model = College.objects.all().values_list()
	context = {
		'collegeFilter': model,
		'objectCount': model.count()
	}
	return render(request, 'election/administrator/utilities/edit_college_utilities.html'
		, context)

@login_required
def filterUtilitiesCollege(request, id):
	model = None
	if id == 0:
		model = College.objects.all().values_list().order_by('id')
	else:
		model = College.objects.all().filter(campus_id=id).values_list().order_by('id')
	
	context = {
		'collegeFilter': model,
		'collegeId': id,
		'objectCount': model.count()
	}

	return render(request, 'election/administrator/utilities/edit_college_utilities.html'
		, context)

@login_required
def saveUtilitiesCollege(request):
	context = {
		'campuses': Campus.objects.all().order_by('id')
	}

	if request.method == 'POST':
		colleges = request.POST.getlist('inputName')
		c = len(colleges)
		for i in range(c):
			selectedCampus = request.POST['campusId']
			form = CollegeForm({'college_name': colleges[i]})
			if form.is_valid():
				set_college = form.save()
				set_college.campus_id.add(selectedCampus)
				messages.success(request, customAlert.SaveAlert(colleges[i]))
		
		return HttpResponseRedirect(reverse('college-edit'))
	else:
		
		return render(request, 'election/administrator/utilities/create_college_utilities.html'
			, context)

@login_required
def updateUtilitiesCollege(request, id=None):
	newName = request.POST.get('inputEdit')

	if request.method == 'POST':
		College.objects.filter(pk=id).update(college_name=newName)
		messages.info(request, customAlert.UpdateAlert(newName))
		
	else:
		form = CollegeForm(instance=college)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/college_utilities/edit/'))

@login_required
def deleteUtilitiesCollege(request, id=None):
	if request.method == 'POST':
		College.objects.filter(pk=id).delete()
		College.objects.all().filter(id=id).delete()
		messages.warning(request, customAlert.DeleteAlert())
		
	else:
		form = CollegeForm(instance=college)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/college_utilities/edit/'))

#end of views Colleges

#views of Election
@login_required
def createUtilitiesElection(request):
	e_model = ElectionType.objects.all().order_by('election_name')
	e_count = ElectionType.objects.all().count()
	context = {
		'elections': e_model,
		'objectCount': e_count
	}
	
	return render(request, 'election/administrator/utilities/edit_election_utilities.html', 
	context)


@login_required
def saveUtilitiesElection(request):
	if request.method == 'POST':
		elections = request.POST.getlist('inputName')
		c = len(elections)
		for i in range(c):	
			form = ElectionTypeForm({'election_name': elections[i]})
			if form.is_valid():
				messages.success(request, customAlert.SaveAlert(elections[i]))
				form.save()
		return HttpResponseRedirect(reverse('election-edit'))
	else:
		
		return render(request, 'election/administrator/utilities/create_election_utilities.html')

@login_required
def updateUtilitiesElection(request, id=None):
	model = ElectionType
	newName = request.POST.get('inputEdit')
	if request.method == 'POST':
		model.objects.filter(pk=id).update(election_name=newName)
		messages.success(request, customAlert.UpdateAlert(newName))
		
	else:
		form = ElectionTypeForm(instance=model)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/election_utilities/edit/'))

@login_required
def deleteUtilitiesElection(request, id=None):
	model = ElectionType
	if request.method == 'POST':
		#College.objects.all().filter(campus_id=id).delete()
		messages.warning(request, customAlert.DeleteAlert())
		model.objects.filter(pk=id).delete()

	else:
		form = ElectionTypeForm(instance=election)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/election_utilities/edit/'))

#end of views Election

#views of Position
@login_required
def createUtilitiesPosition(request, action):
	e_model = ElectionType.objects.all().order_by('election_name')
	p_model = Position.objects.all().values_list().order_by('sort_number')
	queryId = None
	for i in e_model:
		queryId = Position.objects.all().filter(election_type_id=i.id).values_list().count()
		if queryId > 0:
			queryId = i.id
		break

	context = {
		'electionTypeFilters': e_model,
		'positionFilters': p_model,
		'objectCount': p_model.count(),
		'electionTypeId': queryId,
		'action': action
	}
	return render(request, 'election/administrator/utilities/edit_position_utilities.html'
		, context)

@login_required
def arrangeUtilitiesPosition(request, action, id):
	e_model = ElectionType.objects.all().filter(id=id).order_by('election_name')
	p_model = Position.objects.all().filter(election_type=id).values_list().order_by('sort_number')	
	context = {
		'electionTypeFilters': e_model,
		'positionFilters': p_model,
		'action': action,
		'electionId': id
	}
	return render(request, 'election/administrator/utilities/edit_position_utilities.html'
		, context)

@login_required
def updateArrangePosition(request):
	
	if request.method == 'POST':
		sorts = request.POST.getlist('sortPosition')
		s = len(sorts)
		num = 0
		for i in range(s):
			num = i + 1
			Position.objects.filter(pk=sorts[i]).update(sort_number=num)
			#messages.info(request, customAlert.UpdateAlert(dct['']))	
		
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/position_utilities/edit/'))

	else:
		return render(request, 'election/administrator/candidates/view_ssc_form.html')
	#return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/position_utilities/edit/'))


@login_required
def filterUtilitiesPosition(request, action, id):
	model = None
	if id == 0:
		model = Position.objects.all().values_list().order_by('sort_number')
	else:
		model = Position.objects.all().filter(election_type=id).values_list().order_by('sort_number')
	context = {
		'electionTypeFilters': ElectionType.objects.all().order_by('id'),
		'positionFilters': model,
		'electionTypeId': id,
		'objectCount': model.count(),
		'action': action
	}
	return render(request, 
		'election/administrator/utilities/edit_position_utilities.html', context)

@login_required
def saveUtilitiesPosition(request):
	context = {
		'electionTypes': ElectionType.objects.all().order_by('id')
	}

	if request.method == 'POST':
		positions = request.POST.getlist('inputName')
		id = request.POST['electionTypeId']
		c = len(positions)
		num = 0
		for i in range(c):
			p_model = Position.objects.all().filter(election_type=id).values_list()
			if p_model.count() > 0:
				num = p_model.count() + 1
			else :
				num = 1

			form = PositionForm({'position_name': positions[i], 
				'election_type': id,
				'sort_number': num})
			if form.is_valid():
				form.save()

				messages.success(request, customAlert.SaveAlert(positions[i]))
		
		return redirect('position-edit', 'edit')
	else:
		
		return render(request, 'election/administrator/utilities/create_position_utilities.html'
			, context)

@login_required
def updateUtilitiesPosition(request, id=None):
	newName = request.POST.get('inputEdit')

	if request.method == 'POST':
		Position.objects.filter(pk=id).update(position_name=newName)
		messages.info(request, customAlert.UpdateAlert(newName))
		
	else:
		form = PositionForm(instance=position)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/position_utilities/edit/'))

@login_required
def deleteUtilitiesPosition(request, id=None):
	if request.method == 'POST':
		Position.objects.filter(pk=id).delete()
		Position.objects.all().filter(id=id).delete()
		messages.warning(request, customAlert.DeleteAlert())
		
	else:
		form = PositionForm(instance=position)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'utilities/position_utilities/edit/'))

#end of views Colleges

@login_required
def saveDesign(request):
	return render(request, 'election/administrator/candidates/view_ssc_form.html')

