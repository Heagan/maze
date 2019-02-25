import pyglet, random, math
import vehicle, wall, util
import random_forest_regression as rfr
import numpy as np

winx = 800
winy = 600

game_window = pyglet.window.Window(winx, winy)
main_batch = pyglet.graphics.Batch()
keyboard = pyglet.window.key.KeyStateHandler()
game_window.push_handlers(keyboard)

score_label = pyglet.text.Label(text="Score: 0", x=50, y=575, batch=main_batch)

event_stack_size = 0
walls = []
car = None

def load_map():
	global walls, main_batch
	
	x = 0
	y = 0
	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0
	f = open("resources/map.map", "r")
	for s in f.read():
		if s == '\n':
			x = -50
			y += 50
		if s == "1":
			walls.append(wall.Wall(x - 25, y - 25, x + 25, y + 25, batch=main_batch))
		x += 50
	f.close()


def setup_map():
	global walls

	# Bot
	walls.append(wall.Wall(5, 5, winx - 5, 5))
	# Top
	walls.append(wall.Wall(5, winy - 5, winx - 5, winy - 5))
	# Left
	walls.append(wall.Wall(5, 5, 5, winy - 5))
	# Right
	walls.append(wall.Wall(winx - 5, 5, winx - 5, winy - 5))

	# Bot
	walls.append(wall.Wall(100, 100, (winx - 100 ) / 3, 100))
	walls.append(wall.Wall((winx - 100 ) / 3 + (winx - 100 ) / 3 , 100, winx - 100, 100))
	# Top
	walls.append(wall.Wall(100, winy - 100, (winx - 100 ) / 3, winy - 100))
	walls.append(wall.Wall((winx - 100 ) / 3 + (winx - 100 ) / 3, winy - 100, winx - 100, winy - 100))
	# Mid

	walls.append(wall.Wall((winx - 100 ) / 3, 100, (winx - 100 ) / 3, winy - 100))
	walls.append(wall.Wall((winx - 100 ) / 3 + (winx - 100 ) / 3, 100, (winx - 100 ) / 3 + (winx - 100 ) / 3, winy - 100))

	# Left
	walls.append(wall.Wall(100, 100, 100, winy - 100))
	# Right
	walls.append(wall.Wall(winx - 100, 100, winx - 100, winy - 100))


def init():
	global car, event_stack_size

	rfr.setup_ml()

	load_map()
	# setup_map()

	# Clear the event stack of any remaining handlers from other levels
	while event_stack_size > 0:
		game_window.pop_handlers()
		event_stack_size -= 1

	# Initialize the player sprite
	car = vehicle.Vehicle(x=100, y=555, batch=main_batch)

	# Add any specified event handlers to the event handler stack
	for handler in car.event_handlers:
		game_window.push_handlers(handler)
		event_stack_size += 1


@game_window.event
def on_draw():
	global walls, car
	game_window.clear()
	pyglet.gl.glLineWidth(2)

	for s in car.sensor:
		x1 = car.x
		y1 = car.y
		x2 = car.x + s.dx * s.t
		y2 = car.y + s.dy * s.t
		pyglet.graphics.draw(4, pyglet.gl.GL_LINES, ("v2f", (x1, y1, x2, y2, x1, y1, x2, y2)))

	main_batch.draw()

f = open("data.csv", "a")
csv = []
ass = []

def update(dt):
	global car, f, csv, ass, key_handler

	player_dead = False

	# Let's not modify the list while traversing it
	to_add = []

	car.update(dt)

	if car.dead:
		car.rotation = 0
		car.x = 100
		car.y = 525
		car.dead = False

	car.intersect(walls)

	# Write data!
	# if car.key != 0:
	# 	csv = ""
	# 	for s in car.sensor:
	# 		csv += str(s.t) + ";"
	# 	csv += str(car.key) + "\n"
	# 	f.write(csv)


	# Predict using data!
	csv = []
	for s in car.sensor:
		csv.append( s.t )
	csv = np.array(csv).reshape(1, -1)
	ass = csv[:,:-1]
	pv = rfr.predict( np.array(ass) )
	print("Predicted value: " + str(pv) )
	car.process(dt, round(pv[0]) )

	# car.intersect(walls)
	# csv = ""
	# hitWall = False
	# for s in car.sensor:
	# 	csv += str(s.t) + ";"
	# 	if s.t < 50:
	# 		hitWall = True
	# 		break
	# if hitWall == False: 
	# 	csv += str(round(pv[0])) + "\n"
	# 	f.write(csv)

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

































