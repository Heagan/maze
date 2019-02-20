import pyglet, math
from pyglet.window import key
import resources, physicalobject

sensor_length = 1000

class Sensor:
	def __init__(self, angle):
		self.dx = math.cos(angle)
		self.dy = math.sin(angle)
		self.val = sensor_length


class Vehicle(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Vehicle, self).__init__(img=resources.car_image, *args, **kwargs)
		
		self.rotate_speed = 200.0
		self.speed = 200

		# Tell the game handler about any event handlers
		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

		self.sensorAngle = (math.pi * 2 * -math.radians(self.rotation)) / 8 
		self.sensors = []

		angle = 0
		while (angle < math.pi * 2):
			self.sensors.append(Sensor(angle))
			angle += self.sensorAngle

	def updateSensorAngles(self):
		if not self.rotation:
			return

		self.sensorAngle = (math.pi * 2) / 8
		print(self.rotation)
		self.sensors = []

		angle = 0
		while (angle < math.pi * 2):
			self.sensors.append(Sensor(angle))
			angle += self.sensorAngle

	def update(self, dt):

		# Do all the normal physics stuff
		super(Vehicle, self).update(dt)

		self.updateSensorAngles()

		if self.key_handler[key.LEFT]:
			self.rotation -= self.rotate_speed * dt
		if self.key_handler[key.RIGHT]:
			self.rotation += self.rotate_speed * dt
		
		force_x = 0
		force_y = 0
		if self.key_handler[key.UP]:
			# Note: pyglet's rotation attributes are in "negative degrees"
			angle_radians = -math.radians(self.rotation)
			force_x = math.cos(angle_radians) * self.speed
			force_y = math.sin(angle_radians) * self.speed
		self.velocity_x = force_x
		self.velocity_y = force_y


	def delete(self):
		super(Vehicle, self).delete()
