import datetime

from django.db import models
from django.utils import timezone

# Models

# An account on Jitterbunk
class User(models.Model):

	username = models.CharField(max_length=50) # Name of user
	photo = models.CharField(max_length=2000) # TBD

	def __str__(self):
		return self.username

# A 'Bunk'
class Bunk(models.Model):

	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user') # FK of sending user
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user') # FK of receiving user
	time = models.DateTimeField('time of bunk') # Time that bunk was bunk'd

	def __str__(self):
		return 'TODO'