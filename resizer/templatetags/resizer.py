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
	if not (mode[0] == mode[-1] and mode[0] in ('"', "'")):
		raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
	return ResizerNode(image, format, mode)


class ResizerNode(template.Node):
	WIDTH = 'width'
	HEIGHT = 'height'

	def __init__(self, image, format, mode):
		try:
			self.image = template.Variable(image)
			self.format= format[1:-1]
			self.dimensions = {'width':int(self.format.split('x')[0]), 'height':int(self.format.split('x')[0]),}
			self.path = os.path.join(settings.MEDIA_ROOT, 'resizer_cache')
			self.mode = mode[1:-1]

			# create cache directoty
			if not(os.path.exists(self.path) and os.path.isdir(self.path)):
				os.mkdir(self.path)

		except template.VariableDoesNotExist:
			return ''
		

	def render(self, context):
		
		img_obj = self.image.resolve(context)
		basename = os.path.basename(img_obj.name)

		resized_name = self.get_name(basename, self.format, self.mode)
		resized_path = os.path.join(self.path, resized_name)

		final_width = self.dimensions['width']
		final_height = self.dimensions['height']

		if (os.path.exists(resized_path) == False):
			# check if file exists
			if (os.path.exists(img_obj.path)):
				newimg = Image.open(img_obj.path)

				if (self.mode == 'crop'):
					if (img_obj.width/self.dimensions['width']>img_obj.height/self.dimensions['height']):
						master =  ResizerNode.HEIGHT
					else:
						master = ResizerNode.WIDTH
				else:
					if (img_obj.width/self.dimensions['width']>img_obj.height/self.dimensions['height']):
						master = ResizerNode.WIDTH
					else:
						master =  ResizerNode.HEIGHT

				if (master == ResizerNode.WIDTH):
					final_height = img_obj.height * final_width / img_obj.width
				elif (master == ResizerNode.HEIGHT):
					final_width = img_obj.width * final_height / img_obj.height

				final_width = int(round(final_width))
				final_height = int(round(final_height))

				newimg = newimg.resize((final_width, final_height), Image.ANTIALIAS)

				if (self.mode == 'crop'):
					left = int(round((final_width - self.dimensions['width']) / 2))
					top = int(round((final_height - self.dimensions['height']) / 2))
					right = left + self.dimensions['width']
					bottom = top + self.dimensions['height']
					newimg = newimg.crop((left, top, right, bottom))

				newimg.save(resized_path)

			else:
				raise template.TemplateSyntaxError("%r path does not exist" % img_obj.path)

		# return the path from the MEDIA_URL on. Not the full OS path
		return resized_path[resized_path.index(settings.MEDIA_URL):]

	def get_name(self, name, format, mode):
		return mode + '_' + format + '_' + name

register.tag('resizer', do_resizer)