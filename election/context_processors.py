from .models import ( 
	College, 
	Campus,
	ElectionType
	)

def add_variable_to_context(request):
    colleges = College.objects.all().values_list('id', 'college_name', 'campus_id').order_by('id')
    	
    return {
        'campuses': Campus.objects.all().order_by('id'),
        'electionTypes': ElectionType.objects.all().order_by('id'),
        'colleges': colleges
    }