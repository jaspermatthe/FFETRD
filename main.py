import pygame as pg
from math import *
import random



"""CHANGE DIFFICULTY HERE [closer to 0 is most diffult]"""

difficulty = 300


"""Initial Set Up"""

# initialize window and naming
pg.init()
pg.font.init()

text_size = 20
my_font = pg.font.SysFont('Myriad Pro', text_size)

scr_width = 600
scr_height = 600

scr = pg.display.set_mode((scr_width, scr_height))
scr_rect = scr.get_rect()
pg.display.set_caption('Forest Fire Extinguishing and Tree Replanting Drone')


# specify tile display colours
red = (255, 0, 0)  		# fire
green = (0, 255, 0)		# trees
blue = (0, 0, 255)		# water
brown = (131,101,57) 	# soil
bg = (0,0,0)


# Grid Size
rows = 15
cols = 15
number_sectors = rows * cols
sector_width = scr_width // cols
sector_height = scr_height // rows


# initialize clock
clock = pg.time.Clock()
fps = 60

timer_interval = rows * difficulty # timer delay per fire start
timer_event = pg.USEREVENT + 1
pg.time.set_timer(timer_event, timer_interval)

burn_time = 2000 # 10 seconds before tree turns into soil

# load, scale, and get dimensions of drone
drone_large = pg.image.load('drone.png')
drone_scaled = pg.transform.scale(drone_large, (sector_width, sector_height))
drone_rect = drone_scaled.get_rect()
speed = scr_width / rows / 10

# define states of tiles
soil = 0
tree = 1
fire = 2
water = 3

# level speed multiplier
level_speed = 100 # 5 second delay



"""Classes"""

# Grid Class
class grid():
	def __init__(self):
		self.width = sector_width
		self.height = sector_height
	
	# shape grid
	def create_grid(self):
		self.sectors = []

		for row in range(rows):
			# reset row
			sector_row = []

			for col in range(cols):
				sector_x = self.width * col
				sector_y = self.height * row
				sector_rect =  pg.Rect(sector_x, sector_y, self.width, self.height)

				# default state of sector
				sector_state = soil # nothing
				burn_state = 0

				a_sector = [sector_rect, sector_state, burn_state]

				sector_row.append(a_sector)

			self.sectors.append(sector_row)

	# randomize state of sectors
	def randomize_grid(self):
		for row in self.sectors:
			for sector in row:
				sector[1] = random.randint(0,1)

	def draw_grid(self):
		for row in self.sectors:
			for sector in row:
				if sector[1] == soil:
					sector_colour = brown
				elif sector[1] == tree:
					sector_colour = green
				elif sector[1] == fire:
					sector_colour = red
				elif sector[1] == water:
					sector_colour == blue
				
				pg.draw.rect(scr, sector_colour, sector[0])

	def random_fire(self):
		random_row = random.randrange(len(self.sectors))
		random_col = random.randrange(len(self.sectors))
		if self.sectors[random_row][random_col][1] != soil and self.sectors[random_row][random_col][1] != water and self.sectors[random_row][random_col][1] != fire:
			self.sectors[random_row][random_col][1] = fire


# Drone class
class drone():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.speed = speed
	
	# Keyboard Input for Drone Movement
	def move(self):
		key = pg.key.get_pressed()

		if key[pg.K_UP]:
			self.y -= self.speed

		if key[pg.K_DOWN]:
			self.y += self.speed

		if key[pg.K_LEFT]:
			self.x -= self.speed

		if key[pg.K_RIGHT]:
			self.x += self.speed
		
	# extinguish, plant, water
	def drone_modes(self):
		key = pg.key.get_pressed()
		for row in grid.sectors:
			for sector in row:
				if drone_rect.colliderect(sector[0]):
					
					# prevent game "cheat" by having all keys pressed at once and moving to clear the whole grid
					if key[pg.K_e] and key[pg.K_r]:
						pass

					# extinguish fire
					elif key[pg.K_e] and sector[1] == fire:
						sector[1] = soil

					# replant tree
					elif key[pg.K_r] and sector[1] == soil:
						sector[1] = tree

	def fire_check(self):
		# turn fire into soil if over burn time
		for row in grid.sectors:
			for sector in row:
				if sector[1] == fire:
					sector[2] += 1
				if sector[2] >= burn_time:
					sector[1] = soil
		

	def draw_drone(self):
		drone_rect.center = (self.x, self.y)
		drone_rect.clamp_ip(scr_rect) 			# keeps drone within limits of screen
		scr.blit(drone_scaled, drone_rect)
		


# level checker
class level():

	# def win_lose(self):
	# 	running = True
	# 	you_lose = False
	# 	you_win = False
	# 	fire_count = 0
	# 	tree_count = 0
	# 	soil_count = 0
	# 	for row in grid.sectors:
	# 		for sector in row:
	# 			if sector[1] == fire:
	# 				fire_count += 1
	# 			elif sector[1] == tree:
	# 				tree_count += 1
	# 			elif sector[1] == soil:
	# 				soil_count += 1
		
	# 	if fire_count == number_sectors - soil_count or soil_count == number_sectors:
	# 		you_lose = True
			
	# 		if you_lose == True:
	# 			you_lose_text = my_font.render("YOU LOSE", False, (0,0,0))
	# 			scr.blit(you_lose_text, (scr_width/2,scr_height/2))

	# 			running = False


	# 	elif tree_count == number_sectors:
	# 		you_win_text = my_font.render("YOU WIN", False, (0,0,0))
	# 		scr.blit(you_win_text, (0,0))

	# 	return running


	def win_lose(self):
		running = True
		you_lose = False
		you_win = False
		fire_count = 0
		tree_count = 0
		soil_count = 0
		for row in grid.sectors:
			for sector in row:
				if sector[1] == fire:
					fire_count += 1
				elif sector[1] == tree:
					tree_count += 1
				elif sector[1] == soil:
					soil_count += 1
		
		if fire_count == number_sectors - soil_count or soil_count == number_sectors:
			you_lose = True
			
			if you_lose == True:
				print("You Lose")

				running = False


		elif tree_count == number_sectors:
			you_win = True

			if you_win == True:
				print("You Win")
				running = False

		return running
	

class instructions():
	def instruction_list(self):

		text_arrows = my_font.render("Use arrow keys to move drone", False, (0,0,0))
		text_E = my_font.render("Use 'E' key to extinguish fire", False, (0,0,0))
		text_R = my_font.render("Use 'R' key to plant trees", False, (0,0,0))
		text_lose = my_font.render("You LOSE if there are no more trees", False, (0,0,0))
		text_win = my_font.render("You WIN if there are only trees", False, (0,0,0))
		text_author = my_font.render("Created by Jasper Matthé", False, (0,0,0))



		scr.blit(text_arrows, (0,text_size * 0))
		scr.blit(text_E, (0,text_size * 1))
		scr.blit(text_R, (0,text_size * 2))
		scr.blit(text_lose, (0,text_size * 3))
		scr.blit(text_win, (0,text_size * 4))

		scr.blit(text_author, (0,scr_height - text_size))





# initialize the grid
grid = grid()
level = level()
instructions = instructions()

drone = drone(scr_width/2, scr_height/2)

grid.create_grid()
grid.randomize_grid()





"""Game Loop"""
running = True

while running:
	clock.tick(fps)


	running = level.win_lose()
	# set background to a colour
	scr.fill(bg)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		
		# random fire 
		if event.type == timer_event:
			grid.random_fire()



	# update position and state of game elements
	drone.move()
	drone.drone_modes()
	drone.fire_check()

	# draw game elements=
	grid.draw_grid()
	drone.draw_drone()
	instructions.instruction_list()

	



	# display all updated elements with a fps delay
	pg.display.update()


pg.quit()

