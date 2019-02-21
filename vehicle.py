import pyglet, math
from pyglet.window import key
import resources, physicalobject

class Vehicle(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Vehicle, self).__init__(img=resources.car_image, *args, **kwargs)
		
		self.rotate_speed = 20.0
		self.speed = 20

		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]


	def process(self, dt, n):
		
		force_x = 0
		force_y = 0
		angle_radians = -math.radians(self.rotation)


		if n < 1.5:
			self.rotation -= self.rotate_speed * dt
			force_x = math.cos(angle_radians) * self.speed / 2
			force_y = math.sin(angle_radians) * self.speed / 2
			return
		if n > 2.5:
			self.rotation += self.rotate_speed * dt
			force_x = math.cos(angle_radians) * self.speed / 2
			force_y = math.sin(angle_radians) * self.speed / 2
			return
		force_x = math.cos(angle_radians) * self.speed
		force_y = math.sin(angle_radians) * self.speed
		if n == 4:
			force_x = -math.cos(angle_radians) * self.speed
			force_y = -math.sin(angle_radians) * self.speed
		self.velocity_x = force_x
		self.velocity_y = force_y
		return

	def update(self, dt):
		super(Vehicle, self).update(dt)
		a = 0

		if self.key_handler[key.LEFT]:
			a = 1
		if self.key_handler[key.UP]:
			a = 2
		if self.key_handler[key.RIGHT]:
			a = 3
		if self.key_handler[key.DOWN]:
			a = 4

		return self.process(dt, a)


	def delete(self):
		super(Vehicle, self).delete()
