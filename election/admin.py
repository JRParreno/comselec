from django.contrib import admin
from .models import (
	College, 
	Campus,
	ElectionType,
	Position,
	Election,
	Party,
	Candidate,
	MajorPosition,
	BoardMember,
	CiscVoter,
	Disqualify,
	Course
	)

admin.site.register(College)
admin.site.register(Campus)
admin.site.register(ElectionType)
admin.site.register(Position)
admin.site.register(Election)
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(MajorPosition)
admin.site.register(BoardMember)
admin.site.register(CiscVoter)
admin.site.register(Disqualify)
admin.site.register(Course)

