import pyglet, random, math
import vehicle, wall, util

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

car = None
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0

sensor_length = 1000

def load_map():
	global game_objects

	x = 0
	y = 0
	f = open("resources/map2.map", "r")
	for s in f.read():
		if s == '\n':
			x = -50
			y += 50
		if s == "1":
			w = wall.Wall(x=x, y=y, batch=main_batch)
			game_objects += [w]
		x += 50
	f.close()


def init():
	global car, game_objects, event_stack_size

	load_map()

	# Clear the event stack of any remaining handlers from other levels
	while event_stack_size > 0:
		game_window.pop_handlers()
		event_stack_size -= 1

	# Initialize the player sprite
	car = vehicle.Vehicle(x=100, y=525, batch=main_batch)

	# Store all objects that update each frame in a list
	game_objects += [car]

	# Add any specified event handlers to the event handler stack
	for obj in game_objects:
		for handler in obj.event_handlers:
			game_window.push_handlers(handler)
			event_stack_size += 1


@game_window.event
def on_draw():

	game_window.clear()
	main_batch.draw()
	pyglet.gl.glLineWidth(50)
	for a in car.sensors:
		x1 = car.x
		y1 = car.y
		x2 = car.x + a.dx * a.val
		y2 = car.y + a.dy * a.val
		pyglet.graphics.draw(4, pyglet.gl.GL_LINES, ("v2f", (x1, y1, x2, y2, x1, y1, x2, y2)))


def updateSensors():
	global car, sensor_length, game_objects

	for i in car.sensors:
		i.val = sensor_length
	for i in range(len(game_objects)):
		if game_objects[i] == car:
			continue
		px = game_objects[i].x
		py = game_objects[i].y
		for j in range(len(car.sensors)):
			dx = car.sensors[j].dx
			dy = car.sensors[j].dy
			delta = util.angle({px, py, 1}, {dx, dy, 1})
			if delta < (math.pi * 2) / 8:
				dist = util.distance((px, py), (car.x, car.y))
				car.sensors[j].val = min(car.sensors[j].val, dist)

def update(dt):
	global car

	updateSensors()
	player_dead = False

	# To avoid handling collisions twice, we employ nested loops of ranges.
	# This method also avoids the problem of colliding an object with itself.
	for i in range(len(game_objects)):
		for j in range(i + 1, len(game_objects)):

			obj_1 = game_objects[i]
			obj_2 = game_objects[j]

			# Make sure the objects haven't already been killed
			if not obj_1.dead and not obj_2.dead:
				if obj_1.collides_with(obj_2):
					obj_1.handle_collision_with(obj_2)
					obj_2.handle_collision_with(obj_1)

	# Let's not modify the list while traversing it
	to_add = []

	for obj in game_objects:
		obj.update(dt)

		to_add.extend(obj.new_objects)
		obj.new_objects = []


	# Get rid of dead objects
	for to_remove in [obj for obj in game_objects if obj.dead]:
		if to_remove == car:
			car.x = 100
			car.y = 525
			car.dead = False

	# Add new objects to the list
	game_objects.extend(to_add)

	# Check for win/lose conditions
	if player_dead:
		# We can just use the length of the player_lives list as the number of lives
		init()

if __name__ == "__main__":
	# Start it up!
	init()

	# Update the game 120 times per second
	pyglet.clock.schedule_interval(update, 1 / 120.0)

	pyglet.app.run()

































