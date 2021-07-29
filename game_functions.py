import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def get_number_rows(ai_settings, alien_height, ship_height):
	available_space_y = ai_settings.screen_height - ship_height - 3*alien_height
	number_rows = int(available_space_y/2/alien_height)
	return number_rows

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x /(2*alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width*alien_number
	alien.rect.x = alien.x
	alien.y = alien.rect.height + 2*alien.rect.height*row_number
	alien.rect.y = alien.y
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		
def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	

def fire_bullets(ai_settings, screen, ship, bullets):
	if len(bullets)<ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, screen, ai_settings, sb)
def check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, screen, ai_settings, sb):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()

		if play_button.rect.collidepoint(mouse_x, mouse_y):
			pygame.mouse.set_visible(False)
			stats.game_active = True
			stats.reset_stats()
			sb.prep_high_score()
			sb.prep_score()
			sb.prep_ships()
		aliens.empty()
		bullets.empty()
		
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw()
	ship.blitme()
	aliens.draw(screen)
	sb.draw_score()
	if stats.game_active == False:
		play_button.draw_button()
	pygame.display.flip()
	

def remove_bullets(bullets):
	for bullet in bullets.copy():
			if bullet.rect.bottom<=0:
				bullets.remove(bullet)



def check_collision_bullets_aliens(bullets, aliens, ai_settings, ship, screen, stats, sb):
	colissions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if colissions:
		for aliens in colissions.values():
			stats.score += ai_settings.alien_point 
			sb.prep_score()
			check_high_score(stats, sb)
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
	# обновляет позицию пуль и удаляет старые пули
	bullets.update()
	remove_bullets(bullets)
	check_collision_bullets_aliens(bullets, aliens, ai_settings, ship, screen, stats, sb)

def check_fleet_edges(ai_settings, aliens):
	# реагирует на достижение экрана
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_diraction(ai_settings, aliens)
			break
def change_fleet_diraction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_diraction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
	# проверяет достиг ли флот края после чего обновляет позиции всех пришельцев
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	# Decrease number of ships
	if stats.ships_left > 1:
		stats.ships_left -= 1
		sb.prep_ships()
		# Delete all aliens and bullets
		aliens.empty()
		bullets.empty()
		# creating new fleet and set ship pos in center
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.height:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break

def check_high_score(stats, sb):
	ffdata = open('record.txt', 'r', encoding = 'utf-8')
	high = int(ffdata.read())
	ffdata.close()
	if stats.score>high:
		# stats.high_score = stats.score
		data = open('record.txt', 'w', encoding = 'utf-8')
		data.write(str(stats.score))
		sb.prep_high_score()
		data.close()
















