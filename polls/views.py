from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from datetime import datetime
from django.views.decorators.cache import cache_control
import json
from election.models import (
	Campus, 
	College,
	ElectionType,
	Position,
	Election,
	Party,
	Candidate,
	BoardMember,
	MajorPosition,
	CiscVoter,
	Disqualify,
	Course,
	Election,
	SummaryVotes
	)
from .forms import (
	SummaryVoteForm
	)
def checkElection(request):
	check_election = Election.objects.filter(election_start__isnull=False, election_end__isnull=True).values('id', 'election_type')

	if check_election:
		if check_election.count() > 1:
			return render(request, 'polls/no_election_found.html')
		else:
			election_id = check_election.values('id').first()
			return redirect('poll-login', election_id['id'])
	else:
		return render(request, 'polls/no_election_found.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewPollLogin(request, pk):
	election = Election.objects.filter(id=pk).values().first()
	url = 'polls/login_poll_student.html'
	#del request.session['student_online']
	#election_type = election.values('election_type_id', 'voter_campus').first()
	if election['voter_campus'] == None:
		url = 'polls/login_poll.html'

	context = {
		'voter_type': election['voter_campus'],
		'election_id': pk
	}
	return render(request, url, context)

def getStudentDetail(request, voter):
	student = None
	if request.method == 'POST':
		student_number = request.POST.get('student_number')
		if voter == 'cisc':
			get_student = CiscVoter.objects.select_related('college', 'position').filter(student_number=student_number)
			#print(student[0].college.college_name)
			set_json = {
				'college': get_student[0].college.college_name,
				'position': get_student[0].position.position_name,
				'student_name': get_student[0].voter_name,
				'student_number': get_student[0].student_number
			}
			
			student = json.dumps(set_json, indent = 3)
			return JsonResponse(student, safe=False)
		else:
			student = CiscVoter.objects.all()
			post_serialized = serializers.serialize('json', student)
			return JsonResponse(post_serialized, safe=False)

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def officialBallot(request, pk, type):
	election = Election.objects.filter(id=pk).values().first()
	p_model = None
	b_model = None
	#this is for cisc voter
	if request.method == 'POST':
		if type == 'ssc':
			student_number = request.POST.get('student_number')
			student_name = request.POST.get('voter_name')
			college = request.POST.get('selected')
			election_name = ElectionType.objects.get(id=election['election_type_id'])
			dct = json.loads(college)
			p_model = Party.objects.all().filter(election_type=election['election_type_id'])
			m_model = MajorPosition.objects.select_related('position', 'party')
			positions = Position.objects.all().filter(election_type=election['election_type_id']).order_by('sort_number')
			b_model = BoardMember.objects.all().filter(college=dct['id'])
			candidates = []
			set_candidates = None
			for i in positions:
				set_candidates = MajorPosition.objects.filter(position_id=i.id).values()
				if set_candidates:
					item = {"position": i.id}
					item['candidate'] = set_candidates
					candidates.append(item)
			request.session.modified = True
			request.session['student_online'] = student_number
			#positions = Position.objects.all().exclude(id=b_model[0].position_id).filter(election_type=e_model.id)
			context = {
				'election': election_name,
				'positions': positions,
				'partylists': p_model,
				'major_candidates': candidates,
				#'major_candidates': m_model,
				'board_members': b_model,
				'college': dct['college_name'],
				'student_name': student_name,
				'student_number': student_number,
				'type': type,
				'election_id': pk
			}
			return render(request, 'polls/ballot.html', context)
	return redirect('poll-check')

def SubmitVote(request, pk, type):
	if request.method == 'POST':
		if 'student_online' in request.session:
			election = Election.objects.filter(id=pk).values().first()
			positions = Position.objects.all().filter(election_type=election['election_type_id']).order_by('sort_number')
			for i in positions:
				candidate_form_id = request.POST.get(str(i.id))
				if candidate_form_id !=None:
					form = SummaryVoteForm({'student_number': request.session['student_online'],
						'candidate': candidate_form_id,
						'election': pk,
						'position': i.id})
					if form.is_valid():
						print(candidate_form_id)
						form.save()
			return redirect('print-vote', pk)
			#del request.session['student_online']
	return redirect('poll-check')

def PrintVote(request, pk):
	election = SummaryVotes.objects.all().filter(election=pk, student_number=request.session['student_online']).values()
	print(election)
	
	summary_candidate = (i['position_id'] for i in election)
	m_model = MajorPosition.objects.filter(position__in=summary_candidate)
	b_model =  BoardMember.objects.filter(position__in=summary_candidate)
	print(m_model)
	print(b_model)
	return render(request, 'polls/ballot_print.html')
