import pygame
from sys import exit
from pygame.locals import * 
import random

SCREEM_WIDTH = 480
SCREEM_HEIGHT = 800
'''
class Bullet(pygame.sprite.Sprite):
	"""docstring for Bullet"""
	def __init__(self, bullet_img, init_pos):
		super(Bullet, self).__init__()
		self.bullet_img = bullet_img
		self.init_pos = init_pos
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.midbottom = init_pos
		self.speed = 10
	def move(self):
		self.rect.top -= self.speed

class Player(pygame.sprite.Sprite):
	"""docstring for Player"""
	def __init__(self, plane_img, player_rect, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = []
		for i in range(len(player_rect)):
			self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
		self.rect = player_rect[0]
		self.rect.topleft = init_pos
		self.speed = 8
		self.bullets = pygame.sprite.Group()
		self.img_index = 0
		self.is_hit = False
		self.plane_img = plane_img
		self.player_rect = player_rect
		self.init_pos = init_pos
'''
	
pygame.init()

screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Shoooooting')
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')
plane_img = pygame.image.load('resources/image/shoot.png')
player = plane_img.subsurface(pygame.Rect(0, 99, 102, 126))

while True:
	screen.fill(0)
	screen.blit(background, (0, 0))
	screen.blit(player, [200, 600])
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()