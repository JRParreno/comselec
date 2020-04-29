from django.db.models import Q
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
        
    return {
        'notification': e_dot,
        'pending': e_dot.count(),
    }