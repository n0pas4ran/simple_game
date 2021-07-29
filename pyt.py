
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# Инициализирует pygame, settings и объект экрана.
	pygame.init()
	
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	ship = Ship(ai_settings, screen)
	alien = Alien(ai_settings, screen)
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
# создание группы для хранения пуль 
	bullets = Group()
	play_button = Button(ai_settings, screen, 'Play')
	stats  = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	while True:
		gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)		
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)

run_game()