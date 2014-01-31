import os
from django import template
from django.conf import settings
from PIL import Image

register = template.Library()

def do_resizer(parser, token):
	try:
		tag_name, image, format, mode = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
	if not (format[0] == format[-1] and format[0] in ('"', "'")):
		raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
	return ResizerNode(image, format, mode)


class ResizerNode(template.Node):
	def __init__(self, image, format, mode):
		try:
			self.image = template.Variable(image)
			self.format_str = format[1:-1]
			self.format = tuple(self.format_str.split('x'))
			self.path = os.path.join(settings.MEDIA_ROOT, 'resizer_cache')
			
			self.mode = mode

			# create cache directoty
			if not(os.path.exists(self.path) and os.path.isdir(self.path)):
				os.mkdir(self.path)

		except template.VariableDoesNotExist:
			return ''
		

	def render(self, context):
		# check if file exists
		img_obj = self.image.resolve(context)
		
		print os.path.basename(img_obj.name)

		if (os.path.exists(img_obj.path)):
			img = Image.open(img_obj.path)
			nueva = img.resize(self.format, Image.ANTIALIAS)
			nueva.save(os.path.join(self.path,'thumb_'+self.format_str+'_'+os.path.basename(img_obj.name)))

		return os.path.join(self.path,'thumb_'+os.path.basename(img_obj.name))

register.tag('resizer', do_resizer)