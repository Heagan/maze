import pyglet, math
from pyglet.window import key
import resources, physicalobject

class Wall(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Wall, self).__init__(img=resources.wall_image, *args, **kwargs)
		
		# Tell the game handler about any event handlers
		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

	def update(self, dt):
		return

	def delete(self):
		super(Wall, self).delete()