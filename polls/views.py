from django.shortcuts import render
from django.contrib import messages
from election.models import (
	Election,
	Position
	)
# Create your views here.
def viewPollLogin(request):
	
	def pollCheck():
		p_model = None
		check_election = Election.objects.all().filter(election_start__isnull=True, election_end__isnull=True)
		if check_election:
			pollContinue()
	
	def pollContinue():
		check_election = Election.objects.all()
		p_model = Position.objects.all().filter(election_type=check_election.first())
		context = {
			'positions': p_model
		}

		return render(request, 'polls/login_poll.html', context)

	return render(request, 'polls/no_election_found.html')
