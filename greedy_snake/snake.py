import pygame 
from pygame.locals import * 
import time 
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GREEN = (94, 213, 209)
LIGHT_PINK = (241, 170, 166)
DARK_PINK = (255, 110, 151)

LENGTH_UNIT = 40
LENGTH = 16
HEIGHT = 8
SCREEN = [LENGTH * LENGTH_UNIT, (HEIGHT+1) * LENGTH_UNIT]

MAX_SPEED = 7
TIME_UNIT = 80000
TIME_BASE = 640000
class Game(object):
	"""docstring for Game"""
	def __init__(self):
		super(Game, self).__init__()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SCREEN)
		pygame.display.set_caption("Greedy Snake")

		self.target_pos = pygame.Rect(random.randint(0, LENGTH-1) * LENGTH_UNIT,
									  random.randint(0, HEIGHT-1) * LENGTH_UNIT, 
									  LENGTH_UNIT, LENGTH_UNIT)

		self.snake_pos_x = 40
		self.snake_pos_y = 0
		self.snake_pos_list = []
		self.snake_pos = pygame.Rect(self.snake_pos_x, self.snake_pos_y, LENGTH_UNIT, LENGTH_UNIT)
		self.snake_tail_pos = pygame.Rect(0, 0, LENGTH_UNIT, LENGTH_UNIT)
		self.snake_pos_list.append(self.snake_pos)
		self.snake_pos_list.append(self.snake_tail_pos)
		self.move_dir = "right"
		self.score = 0
		pygame.font.init()
	def move_snake(self):

		if len(self.snake_pos_list) > 1:
			for i in range(len(self.snake_pos_list)-1, 0, -1):
				self.snake_pos_list[i].top = self.snake_pos_list[i-1].top
				self.snake_pos_list[i].left = self.snake_pos_list[i-1].left


		if self.move_dir == "up":
			# if self.snake_pos_y - LENGTH_UNIT >= 0:
				self.snake_pos_y -= LENGTH_UNIT 
				# self.snake_pos = self.snake_pos.move(0, -LENGTH_UNIT).copy()
				self.snake_pos_list[0].top = self.snake_pos_y
		elif self.move_dir == "down":
			# if self.snake_pos_y	+ LENGTH_UNIT < HEIGHT * LENGTH_UNIT:
				self.snake_pos_y += LENGTH_UNIT
				self.snake_pos_list[0].top = self.snake_pos_y
		elif self.move_dir == "left":
			# if self.snake_pos_x - LENGTH_UNIT >= 0:
				self.snake_pos_x -= LENGTH_UNIT
				self.snake_pos_list[0].left = self.snake_pos_x
		elif self.move_dir == "right":
			# if self.snake_pos_x + LENGTH_UNIT < LENGTH * LENGTH_UNIT:
				self.snake_pos_x += LENGTH_UNIT
				self.snake_pos_list[0].left = self.snake_pos_x


	def get_target(self):
		if self.snake_pos_x == self.target_pos.left:
			if self.snake_pos_y + LENGTH_UNIT == self.target_pos.top  and self.move_dir == "down":
				return True
			if self.snake_pos_y - LENGTH_UNIT == self.target_pos.top and self.move_dir == "up":
				return True
		elif self.snake_pos_y == self.target_pos.top:
			if self.snake_pos_x + LENGTH_UNIT == self.target_pos.left and self.move_dir == "right":
				return True
			if self.snake_pos_x - LENGTH_UNIT == self.target_pos.left and self.move_dir == "left":
				return True
		else:
			return False

	def check_boundry(self):
		if self.snake_pos_x < 0 or self.snake_pos_x >= LENGTH * LENGTH_UNIT:
			return False
		if self.snake_pos_y < 0 or self.snake_pos_y >= HEIGHT * LENGTH_UNIT:
			return False

		for i in range(1, len(self.snake_pos_list)):
			b1 = self.snake_pos_list[0].top == self.snake_pos_list[i].top
			b2 = self.snake_pos_list[0].left == self.snake_pos_list[i].left
			if b1 and b2:
				return False

	def lengthen_snake(self):
		self.snake_pos_x = self.target_pos.left
		self.snake_pos_y = self.target_pos.top

		new_rect = self.target_pos.copy()
		self.snake_pos_list.insert(0, new_rect)

	def create_target(self):
		self.target_pos = None

		flag = True
		while flag:

			self.target_pos = pygame.Rect(random.randint(0, LENGTH-1) * LENGTH_UNIT,
									  random.randint(0, HEIGHT-1) * LENGTH_UNIT, 
									  LENGTH_UNIT, LENGTH_UNIT)
			flag = False
			for i in self.snake_pos_list:
				if i.left == self.target_pos.left and i.top == self.target_pos.top:
					flag = True


	def draw_snake(self):
		for i in range(len(self.snake_pos_list)):
			if i == 0:
				pygame.draw.rect(self.screen, DARK_PINK, self.snake_pos_list[i])
			else:
				pygame.draw.rect(self.screen, LIGHT_PINK, self.snake_pos_list[i])

	def run(self):
		pygame.mouse.set_visible(0)

		time_cnt = TIME_BASE
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						print("up")
						self.move_dir = "up"
					elif event.key == pygame.K_a:
						print("left")
						self.move_dir = "left"
					elif event.key == pygame.K_d:
						print("right")
						self.move_dir = "right"
					elif event.key == pygame.K_s:
						print("down")
						self.move_dir = "down"

			
			if time_cnt == max(TIME_BASE - self.score * TIME_UNIT, TIME_BASE - MAX_SPEED * TIME_UNIT):
				
				if self.get_target():
					self.lengthen_snake()
					self.create_target()
					self.score = self.score + 1
				else:
					self.move_snake()
					if self.check_boundry() == False:
						pygame.quit()
						sys.exit()
				self.screen.fill(WHITE)
				pygame.draw.rect(self.screen, LIGHT_GREEN, self.target_pos)
				self.draw_snake()
				
				font = pygame.font.Font(None, 25)
				self.score_text = font.render("Score: " + str(self.score), 1, BLACK)
				self.screen.blit(self.score_text, 
								 ( LENGTH_UNIT, HEIGHT*LENGTH_UNIT+(LENGTH_UNIT-self.score_text.get_height())/2 )
								)
				self.speed_text = font.render("Speed: " + str(TIME_BASE//TIME_UNIT + 1 - time_cnt // TIME_UNIT), 1, BLACK)
				self.screen.blit(self.speed_text, 
								 ( font.size("Score: " + str(self.score))[0] + 2 * LENGTH_UNIT, HEIGHT*LENGTH_UNIT+(LENGTH_UNIT-self.speed_text.get_height())/2 )
								)

				for raw_index in range(1, HEIGHT+1):
					pygame.draw.line(self.screen, GRAY, (0, raw_index * LENGTH_UNIT), 
								    (LENGTH * LENGTH_UNIT, raw_index * LENGTH_UNIT), 2)
				for col_index in range(1, LENGTH):
					pygame.draw.line(self.screen, GRAY, (col_index * LENGTH_UNIT, 0), 
								    (col_index * LENGTH_UNIT, HEIGHT * LENGTH_UNIT), 2)

				pygame.display.update()
				time_cnt = 0

			time_cnt = time_cnt + 1


if __name__ == '__main__':
	game = Game()
	game.run()

