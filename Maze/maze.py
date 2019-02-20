import pyglet, random, math
import vehicle, wall

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

car = None
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0

def load_map():
	global game_objects

	x = 0
	y = 0
	f = open("resources/map2.map", "r")
	for s in f.read():
		x = 0
		for c in s:
			print(c)
			if c == "1":
				w = wall.Wall(x=x, y=y, batch=main_batch)
				game_objects += [w]
			x += 100
		y += 10


def init():
	global car, game_objects, event_stack_size

	load_map()

	# Clear the event stack of any remaining handlers from other levels
	while event_stack_size > 0:
		game_window.pop_handlers()
		event_stack_size -= 1

	# Initialize the player sprite
	car = vehicle.Vehicle(x=400, y=300, batch=main_batch)

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


def update(dt):
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
			player_dead = True
		# If the dying object spawned any new objects, add those to the 
		# game_objects list later
		to_add.extend(to_remove.new_objects)

		# Remove the object from any batches it is a member of
		to_remove.delete()

		# Remove the object from our list
		game_objects.remove(to_remove)

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

































