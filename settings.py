import pygame
class Settings():
	"""Класс для хранения всех настроек игры Alien Invasion."""
	def __init__(self):
		"""Инициализирует нацстройки игры"""
		# Параметры экрана
		
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (240, 240, 240)
		
		#параметры пули
		
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (255, 215, 0)
		# максимальное уол-во пуль на экране
		self.bullets_allowed = 5 
		
		# скорость снижения флота пришельцев
		self.fleet_drop_speed = 10
		
		# параметры игры
		self.ship_limit = 3
		self.speedup_scale = 0.8
		self.alien_point = 10

		# темп роста стоимости пришельцев 
		self.point_scale = 2
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_diraction = 1

	def increase_speed(self):
		self.ship_speed_factor += self.speedup_scale
		self.bullet_speed_factor += self.speedup_scale
		self.alien_speed_factor += self.speedup_scale
		self.alien_point = self.alien_point*self.point_scale









