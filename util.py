import pyglet, math
import numpy as np

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def intersect(angle, o=(0, 0), w=(0, 0, 0, 0)):
	if math.sin(angle) == 0 or math.cos(angle) == 0:
		return 0

	txmin = (w[0] - o[0]) / math.sin(angle)
	tymin = (w[1] - o[1]) / math.cos(angle)
	txmax = (w[2] - o[0]) / math.sin(angle)
	tymax = (w[3] - o[1]) / math.cos(angle)

	if txmin > txmax:
		tmp = txmin
		txmin = txmax
		txmax = tmp
		
	if tymin > tymax:
		tmp = tymin
		tymin = tymax
		tymax = tmp

	if (txmin > tymax) or (tymin > txmax):
		return 0

	tmin = txmin
	tmax = txmax

	if tymin > txmin:
		tmin = tymin

	if tymax > txmax:
		tmax = tymax
	
	if tmax < tmin:
		t = tmax
	else:
		t = tmin

	return t
