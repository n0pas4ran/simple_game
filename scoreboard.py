import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	def __init__(self, ai_settings, screen, stats):
		# инициализируует атрибуты подсчета очков
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		# настройка шрифта для вывода счета
		self.text_color = (45, 45, 45)
		self.font = pygame.font.SysFont(None, 48)
		self.prep_ships()
		self.prep_score()
		self.prep_high_score()

	def prep_score(self):
		round_score = round(self.stats.score, -1)
		score_str = '{:,}'.format(round_score)

		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

		# вывод счета в правой верхней части экрана 
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def draw_score(self):
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		fdata = open('record.txt', 'r', encoding = 'utf-8') 
		high_score_str = fdata.read()
		fdata.close()
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = 20

	def prep_ships(self):
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number*(ship.rect.width+10)
			ship.rect.y = 10
			self.ships.add(ship)









