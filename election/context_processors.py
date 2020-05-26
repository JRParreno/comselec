from django.db.models import Q
from .models import ( 
	College, 
	Campus,
	ElectionType,
    Party,
    BoardMember,
    MajorPosition,
    Election
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
    election = Election.objects.all()
    election_type = ElectionType.objects.all()
    ssc_dot_active = 0
    ssc_dot_pending = 0

    #for ssc election
    #check if the party not started
    
    major_pending = (i.party_id for i in MajorPosition.objects.all())
    party =  Party.objects.all().filter(id__in=major_pending)
    ssc_dot_pending = party.filter(election__isnull=True).values('election_type').distinct().count()
    ssc_dot_active = party.filter(election__isnull=False).values('election_type').distinct().count()
   
    #end ssc election
    
    total_notification = ssc_dot_active + ssc_dot_pending
    print(ssc_dot_pending)
    return {
        'pending_notification': ssc_dot_pending,
        'active_notification': ssc_dot_active,
        'total_notification': total_notification,
        'check_election': election_type.count()
    }