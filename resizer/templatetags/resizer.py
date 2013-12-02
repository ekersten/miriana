from django import template

register = template.Library()

def do_resizer(parser, token):
	try:
		tag_name, msg = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
	if not (msg[0] == msg[-1] and msg[0] in ('"', "'")):
		raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
	return ResizerNode(msg[1:-1])


class ResizerNode(template.Node):
	def __init__(self, msg):
		self.msg = msg

	def render(self, context):
		return 'Recieved %s' % self.msg

register.tag('resizer', do_resizer)