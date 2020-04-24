from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

#Campus model
class Campus(models.Model):
	campus_name = models.CharField(max_length=100)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.campus_name

#College Model
class College(models.Model):
	college_name = models.CharField(max_length=100)
	campus_id = models.ManyToManyField(Campus, related_name='campus_id')

	def __str__(self):
		return self.college_name

#Election type: Org or Scc election
class ElectionType(models.Model):
	election_name = models.CharField(max_length=100)

	def __str__(self):
		return self.election_name

#positions accordingly to election type
class Position(models.Model):
	position_name = models.CharField(max_length=100)
	election_type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)

	def __str__(self):
		return self.position_name

class Election(models.Model):
	election_type = models.ForeignKey(ElectionType, 
		on_delete=models.CASCADE,
		null=True, blank=True)
	election_year = models.DateField(default=datetime.today)
	election_start = models.DateTimeField(null=True, blank=True)
	election_end = models.DateTimeField(null=True, blank=True)

class Party(models.Model):
	party_name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=70)
	election = models.ForeignKey(Election, 
		on_delete=models.CASCADE,
		null=True, blank=True)
	election_type = models.ForeignKey(ElectionType, 
		on_delete=models.CASCADE)

	def __str__(self):
		return self.party_name

class Candidate(models.Model):
	candidate_name =  models.CharField(max_length=100)
	position = models.ForeignKey(Position, on_delete=models.CASCADE)
	party = models.ForeignKey(Party, on_delete=models.CASCADE)
	campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
	college = models.ForeignKey(College, on_delete=models.CASCADE)

	def __str__(self):
		return self.candidate_name
