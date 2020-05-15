from django.db.models import Q
from .models import ( 
	College, 
	Campus,
	ElectionType,
    Party,
    BoardMember
	)

def add_variable_to_context(request):
    colleges = College.objects.all().values_list('id', 'college_name', 'campus_id').order_by('id')
    party = Party.objects.all()
    board_member = BoardMember.objects.all()
    return {
        'campuses': Campus.objects.all().order_by('id'),
        'electionTypes': ElectionType.objects.all().order_by('id'),
        'colleges': colleges,
        'ssc_party': party,
        'board_member': board_member.count()
    }

def election_notifications(request):
    e_dot = Party.objects.all().filter(election__isnull=True)
    election = ElectionType.objects.all()
    p_model = Party.objects.all().filter(election__isnull=True)
    b_model  = BoardMember.objects.all().filter(election__isnull=True)
    check = 0
    if p_model or b_model:
        check = 1

    return {
        'notification': e_dot,
        'pending': e_dot.count(),
        'checkElection': check
    }