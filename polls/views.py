from django.shortcuts import render

# Create your views here.
def viewPoll(request):
	return render(request, 'polls/login_poll.html')
