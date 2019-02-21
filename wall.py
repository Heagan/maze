import pyglet, math
from pyglet.window import key
import resources, physicalobject

class Wall(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Wall, self).__init__(img=resources.wall_image, *args, **kwargs)
		
		self.max_distance = 1000
		self.distance = self.max_distance

	def update(self, dt):
		return

	def delete(self):
		super(Wall, self).delete()