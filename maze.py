import pyglet, random, math
import vehicle, wall, util
import random_forest_regression as rfr
import numpy as np

game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()
score_label = pyglet.text.Label(text="Score: 0", x=50, y=525, batch=main_batch)
car = None
game_objects = []
event_stack_size = 0

mexit = False

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

	rfr.setup_ml()

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

	global mexit
	if mexit:
		exit()


# f = open("data.csv", "a")
csv = []
ass = []
def update(dt):
	global car, f, csv, ass

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
	direction = 0

	for obj in game_objects:
		a = obj.update(dt)

		if obj == car:
			direction = a
			if car.dead:
				car.rotation = 0
				car.x = 100
				car.y = 525
				car.dead = False
		else:
			obj.distance = util.distance((car.x, car.y), (obj.x, obj.y))
			score_label.text = "Score :-" + str(game_objects[0].distance)

	
	if direction != 0:
		csv = []
		for obj in game_objects:
			if obj == car:
				continue
			csv.append(obj.distance)
		csv = np.array(csv).reshape(1, -1)
		ass = csv[:,:-1]
		pv = rfr.predict( np.array(ass) )
		print("Predicted value: " + str(pv) )
		car.process(dt, pv)
		# csv += str(a) + "\n"
		# f.write(csv)


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

































