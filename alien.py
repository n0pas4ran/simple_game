import pygame 
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		# инициализирует алиена и задает его начальную позицию
		super().__init__()
		self.screen = screen
		self.image = pygame.image.load('images/alien.bmp')
		self.ai_settings = ai_settings
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		# Каждый новый пришелец появляется в левом верхнем углу экрана.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)

	def blitme(self):
		# выводит пришельца на экран 
		self.screen.blit(self.image, self.rect)
	def check_edges(self):
		self.screen_rect = self.screen.get_rect()
		if self.rect.right>= self.screen_rect.right:
			return True
		elif self.rect.left<=0:
			return True
	def update(self):
		self.rect.x +=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_diraction)

		
