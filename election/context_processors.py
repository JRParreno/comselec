from django.db.models import Q
from django.contrib.auth.models import User
from .models import ( 
	College, 
	Campus,
	ElectionType,
    Party
	)

def add_variable_to_context(request):
    colleges = College.objects.all().values_list('id', 'college_name', 'campus_id').order_by('id')
    	
    return {
        'campuses': Campus.objects.all().order_by('id'),
        'electionTypes': ElectionType.objects.all().order_by('id'),
        'colleges': colleges
    }

def election_notifications(request):
    e_dot = Party.objects.all().filter(election__isnull=True)
    first_name = request.user.first_name
    last_name = request.user.last_name
    full_name = first_name + " " + last_name
    return {
        'notification': e_dot,
        'name': full_name
    }