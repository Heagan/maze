import pyglet, math
from pyglet.window import key
import resources, physicalobject

class Wall(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Wall, self).__init__(img=resources.wall_image, *args, **kwargs)
		
		self.length = 200
		self.angle = 0

	def update(self, dt):
		return

	def delete(self):
		super(Wall, self).delete()