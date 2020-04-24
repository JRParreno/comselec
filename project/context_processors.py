from election.models import College, Campus

def sideNavContext(request):
    return {
        'campus': Campus,
        'college': College
    }