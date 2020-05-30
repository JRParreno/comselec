from django import forms
from election.models import (
	Election,
	Campus, 
	College,
	ElectionType,
	Position,
	Party,
	Candidate,
	BoardMember,
	MajorPosition,
	CiscVoter,
	Disqualify,
	Course,
	SummaryVotes,
	StudentVoter
)

class SummaryVoteForm(forms.ModelForm):

	class Meta:
		model = SummaryVotes
		fields = ['student_number', 'candidate', 'election', 'position']
