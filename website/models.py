from django.db import models

class Painting(models.Model):
	name = models.CharField(max_length=100)
	width = models.PositiveIntegerField()
	height = models.PositiveIntegerField()
	depth = models.PositiveIntegerField()
	technique = models.CharField(max_length=100)
	description = models.TextField()

	def __unicode__(self):
		return self.name
