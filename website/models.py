#encoding:utf-8
from django.db import models

class Painting(models.Model):
	name = models.CharField(max_length=100, verbose_name='Título')
	width = models.PositiveIntegerField(verbose_name='Ancho', help_text='en cm.')
	height = models.PositiveIntegerField(verbose_name='Alto', help_text='en cm.')
	depth = models.PositiveIntegerField(verbose_name='Profundidad', help_text='en cm.')
	technique = models.CharField(max_length=100, verbose_name='Técnica')
	description = models.TextField(verbose_name='Descripción')
	image = models.ImageField(upload_to='paintings', null=True, blank=True, verbose_name='Imágen Principal')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Cuadro'
		verbose_name_plural = 'Cuadros'
