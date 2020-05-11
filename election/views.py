from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
	BoardMemberForm,
	MajorPositionForm,
	CiscVoterForm
	)
from .models import (
	Campus, 
	College,
	ElectionType,
	Position,
	Election,
	Party,
	Candidate,
	BoardMember,
	MajorPosition,
	CiscVoter
	)
from django.shortcuts import get_list_or_404, get_object_or_404

@login_required
def home(request):
    return render(request, 'election/home.html')

 
@login_required
def createSSCForm(request, name, id):
	model = Position.objects.all().filter(election_type=id)
	context = {
		'positions': model,
		'electionTypeId': id,
		'PositionName': name
	}
	return render(request,'election/administrator/ssc/create_ssc_form.html', context)

@login_required
def saveSSCForm(request, type):
	if type == 'Major Position':
		if request.method == 'POST':
			names = request.POST.getlist('major_name')
			positions = request.POST.getlist('position')
			extras = request.POST.getlist('extras')
			electionType = request.POST.get('electionType')
			c = len(names)
			
			electioTypeId = ElectionType.objects.get(id=electionType)
			p_form = Party.objects.create(
				party_name=extras[0],
				acronym=extras[1],
				election_type = electioTypeId)
			p_form.save()
			for i in range(c):
				if names[i] != '':
					form = MajorPositionForm({'candidate_name': names[i],
					'position': positions[i],
					'party': p_form.id})
					if form.is_valid():
						form.save()
						return redirect('filter-ssc-form', type, p_form.id, electionType)

	else:
		if request.method == 'POST':
			ids = request.POST.getlist('collegeId')
			names = request.POST.getlist('inputName')
			electionType = request.POST.get('electionType')
			c = len(ids)
			college_id = None
			for i in range(c):
				dct = json.loads(ids[i])
				form = BoardMemberForm({'candidate_name': names[i],
					'position': dct['positionId'],
					'campus': dct['campusId'],
					'college': dct['collegeId']})
				college_id = dct['collegeId']
				if form.is_valid():
					form.save()

					return redirect('filter-ssc-form', type, college_id, electionType)

	return redirect(request.META['HTTP_REFERER'])

@login_required
def viewSSCForm(request, type, id):
	m_model = None
	c_model = None
	candidate_model = None
	p_model = None
	recent = None
	model = None
	check_count = 0
	available_pos = None
	if type == 'Major Position':
		first_model = Party.objects.filter(election_type=id).order_by('party_name').first()
		model = Party.objects.all().filter(election_type=id)
		#candidate_model = MajorPosition.objects.all()
		if first_model != None:
			recent = first_model.id
			p_model = Position.objects.all()
			candidate_model = MajorPosition.objects.select_related('position').filter(party_id=first_model.id)
			check_count = model.count()
			exclude_candidate = candidate_model.values_list().values('position_id')
			set_pos = Position.objects.exclude(id__in=exclude_candidate)
			available_pos = set_pos.exclude(position_name="Board Member").count()
	else:
		
		board = BoardMember.objects.select_related('college', 'campus').first()
		if board != None:
			recent = board.college.id #get the first id of board member with college id
			colleges = College.objects.all().values_list('id', 'college_name', 'campus_id').order_by('id')
			campuses = Campus.objects.all()
			p_model = BoardMember.objects.all()
			check_count = p_model.count()
			candidate_model = BoardMember.objects.all().filter(college_id=board.college.id)
			model = []
			for college in colleges:
				item = {"id": college[0]}
				for campus in campuses:
					if college[2] == campus.id:
						item['college_name'] = college[1]
						item['campus_name'] = campus.campus_name
						model.append(item)

	context = {
		'models': model,
		'types': type,
		'candidates': candidate_model,
		'positions': p_model,
		'objectCount': check_count,
		'electionType': id,
		'recent_id': recent,
		'check_position':available_pos
	}
	
	return render(request,'election/administrator/ssc/view_ssc.html', context)

@login_required
def filterSSCForm(request, type, id, election_id):
	m_model = None
	c_model = None
	candidate_model = None
	p_model = None
	available_pos = None
	if type == 'Major Position':
		get_election_type = Party.objects.get(id=id)
		model = Party.objects.all().filter(election_type_id=get_election_type.election_type_id)
		p_model = Position.objects.all()
		candidate_model = MajorPosition.objects.select_related('position').filter(party_id=id)
		check_count = model.count()
		exclude_candidate = candidate_model.values_list().values('position_id')
		set_pos = Position.objects.exclude(id__in=exclude_candidate)
		available_pos = set_pos.exclude(position_name="Board Member").count()
	else:
		colleges = College.objects.all().values_list('id', 'college_name', 'campus_id').order_by('id')
		campuses = Campus.objects.all()
		p_model = BoardMember.objects.all()
		check_count = p_model.count()
		candidate_model = BoardMember.objects.all().filter(college_id=id)
		model = []
		for college in colleges:
			item = {"id": college[0]}
			for campus in campuses:
				if college[2] == campus.id:
					item['college_name'] = college[1]
					item['campus_name'] = campus.campus_name
					model.append(item)

	context = {
		'models': model,
		'types': type,
		'recent_id': id,
		'candidates': candidate_model,
		'electionType': election_id,
		'positions': p_model,
		'objectCount': check_count,
		'check_position':available_pos
	}
	
	return render(request,'election/administrator/ssc/view_ssc.html', context)



@login_required
def updateCandidate(request, id, type):
	newName = request.POST.get('inputEdit')
	if request.method == 'POST':	
		if type == 'Major Position':
			MajorPosition.objects.filter(pk=id).update(candidate_name=newName)
			#Candidate.objects.all().filter(id=id).delete()
		else:
			BoardMember.objects.filter(pk=id).update(candidate_name=newName)
		messages.info(request, customAlert.UpdateAlert(newName))

	return redirect(request.META['HTTP_REFERER'])
	#return to current page


@login_required
def deleteCandidate(request, id, type):
	if request.method == 'POST':
		if type == 'Major Position':
			MajorPosition.objects.all().filter(pk=id).delete()
			#Candidate.objects.all().filter(id=id).delete()
			return redirect(request.META['HTTP_REFERER'])
		else:
			BoardMember.objects.all().filter(pk=id).delete()
			return redirect(request.META['HTTP_REFERER'])
		
		messages.warning(request, customAlert.DeleteAlert())

	return redirect(request.META['HTTP_REFERER'])


@login_required
def deletePartylist(request, type, id, election_id):
	if request.method == 'POST':
		Party.objects.all().filter(id=id).delete()		
		messages.warning(request, customAlert.DeleteAlert())

	
	return redirect('view-ssc-form', type, election_id)

@login_required
def updatePartylist(request, type, id, election_id):
	if request.method == 'POST':
		first_name = request.POST.get('firstInput')
		second_name = request.POST.get('secondInput')
		Party.objects.all().filter(id=id).update(party_name=first_name)
		Party.objects.all().filter(id=id).update(acronym=second_name)
		
		messages.warning(request, customAlert.UpdateAlert('Party'))

	
	return redirect(request.META['HTTP_REFERER'])

@login_required
def addSSCVoter(request, id):
	p_model = None
	councilors = None
	c_model = None

	if request.method == 'POST':
		voter_names = request.POST.getlist('voterInputs')
		college_id = request.POST.get('collegeId')
		position_id = request.POST.getlist('positionId')
		c = len(voter_names)
		for i in range(c):
			form = CiscVoterForm({'voter_name': voter_names[i],
				'position': position_id[i],
				'college': college_id})

			if form.is_valid():
				messages.success(request, customAlert.SaveAlert(voter_names[i]))
				form.save()
		return redirect('filter-ssc-voter', college_id)

	else:
		voter_model = CiscVoter.objects.all().filter(college=id)
		e_model = ElectionType.objects.get(election_name='Central/College and Institute Student Council')
		c_model = College.objects.all().filter(id=id).values_list('id', 'college_name', 'campus_id')
		councilors = []
		if voter_model == None:
			p_model = Position.objects.all().filter(election_type_id=e_model.id)
			
			for i in p_model:
				if i.position_name == 'Councilor':
					item = {"id": i.id}
					for x in range(5):
						item['college_name'] = i.position_name
						councilors.append(item)
		else:
			#test = voter_model.exclude(position_id__in=Position.objects.all().values('id'))
			p_model = Position.objects.filter(election_type_id=e_model.id).exclude(id__in=voter_model.values('position'))
			get_councilor_id = Position.objects.get(position_name='Councilor')
			temp_councilor_count = voter_model.filter(position_id=get_councilor_id).count()
			if temp_councilor_count <= 5:
				for x in range(5 - temp_councilor_count):
					item = {"id": get_councilor_id.id}
					item['college_name'] = 'Councilor'
					councilors.append(item)
	context = {
		'positions': p_model,
		'councilors': councilors,
		'getCollege': c_model
	}
	return render(request, 'election/administrator/ssc/add_ssc_voter.html',
		context)

@login_required
def viewSSCVoter(request):
	get_first_college = CiscVoter.objects.all().order_by('college').first()
	c_model = Campus.objects.get(id=College.objects.all().filter(id=get_first_college.college_id).values_list('campus_id')[:1])
	v_model = CiscVoter.objects.all().select_related('position').filter(college=get_first_college.college_id).order_by('position')

	context = {
		'models': v_model,
		'college_id': get_first_college.college_id,
		'campus': c_model
	}
	return render(request, 'election/administrator/ssc/view_ssc_voter.html',
		context)

@login_required
def filterSSCVoter(request, id):
	c_model = Campus.objects.get(id=College.objects.all().filter(id=id).values_list('campus_id')[:1])
	v_model = CiscVoter.objects.all().filter(college=id).order_by('position')

	context = {
		'models': v_model,
		'college_id': id,
		'campus': c_model
	}
	return render(request, 'election/administrator/ssc/view_ssc_voter.html',
		context)

@login_required
def updateSSCVoter(request, id):
		 
	if request.method == 'POST':
		newName = request.POST.get('inputEdit')
		CiscVoter.objects.filter(pk=id).update(voter_name=newName)
		messages.success(request, customAlert.UpdateAlert(newName))

	return redirect(request.META['HTTP_REFERER'])

@login_required
def deleteSSCVoter(request, id):
		 
	if request.method == 'POST':
		CiscVoter.objects.filter(pk=id).delete()
		messages.warning(request, customAlert.DeleteAlert())

	return redirect(request.META['HTTP_REFERER'])

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

#Views of elections

@login_required
def viewElection(request, name):
	text = None
	e_dot = ElectionType.objects.all()
	p_dot = None
	if name == 'pending':
		p_dot = Party.objects.all().filter(election__isnull=True)
		text = name
		print(e_dot)
	else:
		text = name

	context = {
		'partylists': p_dot[:2],
		'electionTypes': e_dot,
		'text': text
	}
	return render(request, 'election/administrator/candidates/election_view.html', 
		context)

@login_required
def addCandidate(request, type, partyid, election_id):
	if request.method == 'POST':
		major_names = request.POST.getlist('major_name')
		positions = request.POST.getlist('position')
		names = len(major_names)
		val = 0
		for i in range(names):
			if major_names[i] != '':
				val = 1
		#loop array from the form
		if val > 0:
			for i in range(names):
				if major_names[i] != '':
					form = MajorPositionForm({'candidate_name': major_names[i],
					'position': positions[i],
					'party': partyid})
					if form.is_valid():
						form.save()
					messages.success(request, customAlert.SaveAlert(major_names[i]))

					return redirect('filter-ssc-form', type, partyid, election_id)
		else:
			messages.success(request, customAlert.InfoAlertInput())

			return redirect(request.META['HTTP_REFERER'])
		
	else:
		party = Party.objects.get(id=partyid)
		c_model = MajorPosition.objects.all().filter(party_id=partyid)
		exclude_candidate = c_model.values_list().values('position_id')
		set_pos = Position.objects.exclude(id__in=exclude_candidate)
		available_pos = set_pos.exclude(position_name="Board Member").filter(election_type_id=party.election_type_id)
		position =  Position.objects.all()
		check_val = 0
		#check if board member is available
		for x in c_model:
			if x.position_id == 3:
				check_val = 1
		context = {
			'partylists': party,
			'available_positions': available_pos,
			'positions': position,
			'types': type,
			'electionType': election_id,
		}
		return render(request, 'election/administrator/ssc/add_ssc_form.html',
			context)
	
	return render(request, 'election/administrator/ssc/add_ssc_form.html')


#end views of partylist and candidates
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
	model = BoardMember.objects.all()
	context = {
		'times': model
	}
	return render(request, 'election/administrator/ssc/test.html', context)

