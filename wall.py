import pyglet, math
from pyglet.window import key
from pyglet.gl import *
import resources, physicalobject
import random


img=pyglet.image.load("./resources/wall.jpg")

class Wall:
	global img

	def __init__(self, x1, y1, x2, y2, batch=None):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		self.image = pyglet.sprite.Sprite(img=img, batch=batch)
		self.image.x = x1
		self.image.y = y1
