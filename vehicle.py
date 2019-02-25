import pyglet, math
from pyglet.window import key
import resources, physicalobject, util

class Sensor:
	def __init__(self, angle):
		self.angle = angle
		self.dx = 0
		self.dy = 0
		self.t = 1000

	def collides(self, a=(0,0), b=(0, 0, 0, 0)):
		
		angle = math.atan2(self.dx, self.dy)

		d = util.intersect(angle, a, b)
		if d <= 0:
			return self.t
		if d < self.t:
			self.t = d
		return self.t

class Vehicle(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Vehicle, self).__init__(img=resources.car_image, *args, **kwargs)
		
		self.rotation = 270
		self.rotate_speed = 200.0
		self.speed = 100

		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

		self.totalSensors = 50
		self.sensorAngle = (math.pi * 2) / self.totalSensors
		self.sensor = []

		self.key = 0

		angle = 0
		while angle < math.pi * 2:
			self.sensor.append(Sensor(angle))
			angle += self.sensorAngle

	def intersect(self, walls):
		for s in self.sensor:
			s.t = 1000
			for w in walls:
				s.collides((self.x, self.y), (w.x1, w.y1, w.x2, w.y2))

	def process(self, dt, n):
		force_x = 0
		force_y = 0
		angle_radians = -math.radians(self.rotation)
		if n == 1:
			self.rotation -= self.rotate_speed * dt
			force_x = -math.cos(angle_radians) * self.speed / 2
			force_y = -math.sin(angle_radians) * self.speed / 2
		if n == 3:
			self.rotation += self.rotate_speed * dt
			force_x = -math.cos(angle_radians) * self.speed / 2
			force_y = -math.sin(angle_radians) * self.speed / 2
		if n == 2:
			force_x = -math.cos(angle_radians) * self.speed# * dt
			force_y = -math.sin(angle_radians) * self.speed# * dt
		if n == 4:
			force_x = math.cos(angle_radians) * self.speed# * dt
			force_y = math.sin(angle_radians) * self.speed# * dt
		# if self.velocity_x < self.speed:
		# 	self.velocity_x += force_x
		# if self.velocity_y < self.speed:
		# 	self.velocity_y += force_y
		self.velocity_x = force_x
		self.velocity_y = force_y


	def update(self, dt):
		super(Vehicle, self).update(dt)

		for s in self.sensor:
			s.dx = -math.cos(-math.radians(self.rotation) + s.angle)
			s.dy = -math.sin(-math.radians(self.rotation) + s.angle)

		self.process(dt, 0)
		self.key = 0
		if self.key_handler[key.UP]:
			self.key = 2
			self.process(dt, 2)
		if self.key_handler[key.DOWN]:
			self.key = 4
			self.process(dt, 4)
		if self.key_handler[key.LEFT]:
			self.key = 1
			self.process(dt, 1)
		if self.key_handler[key.RIGHT]:
			self.key = 3
			self.process(dt, 3)


	def delete(self):
		super(Vehicle, self).delete()
