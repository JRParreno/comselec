from django import forms
from .models import (
	Campus, 
	College,
	ElectionType,
	Position,
	Party,
	Candidate
	)

class CampusForm(forms.ModelForm):
	
	class Meta:
		model = Campus
		fields=['campus_name']

class CollegeForm(forms.ModelForm):
	
	class Meta:
		model = College
		fields=['college_name']

class ElectionTypeForm(forms.ModelForm):
	
	class Meta:
		model = ElectionType
		fields=['election_name']

class PositionForm(forms.ModelForm):
	
	class Meta:
		model = Position
		fields=['position_name', 'election_type']

class PartyForm(forms.ModelForm):
	
	class Meta:
		model = Party
		fields=['party_name', 'acronym', 'election_type']

class CandidateForm(forms.ModelForm):
	
	class Meta:
		model = Candidate
		fields=['candidate_name', 'position', 
			'party', 'campus',
			'college']