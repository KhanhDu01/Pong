from sys import exit

import pygame
import random

# Run the game and sound mixer
pygame.init()
pygame.mixer.init()

# Calling the sound names and importing the sound files
hit = pygame.mixer.Sound('sound/ball_hit.wav')
lose = pygame.mixer.Sound('sound/lose.wav')
click = pygame.mixer.Sound('sound/click.wav')
womp_womp = pygame.mixer.Sound('sound/downer_noise.mp3')

# Setting a position for the ball
ball_x = 500
ball_y = 350

# Choosing between the ball going left or right
add_x = random.choice([2, -2])
# Choosing between going very high up, up, mid, down, down low
add_y = random.randint(-2, 2)

# Scores for player 1 and 1
score_1 = 0
score_2 = 0

# Creating the screen and setting the name
screen = pygame.display.set_mode((1000, 700))
screen_rect = screen.get_rect()
pygame.display.set_caption('Pong')

# Creating the fonts title, normal text, and small text
title = pygame.font.Font('Font/PixeloidSansBold-PKnYd.ttf', 100)
font = pygame.font.Font('Font/PixeloidSansBold-PKnYd.ttf', 50)
subtext = pygame.font.Font('Font/PixeloidSansBold-PKnYd.ttf', 25)
image = pygame.font.Font(None, 20)

# Surface and rectangle of score displayed
text_surf_1 = font.render(str(score_1), False, 'Grey')
text_rect_1 = text_surf_1.get_rect()
text_rect_1.midbottom = (400, 80)

text_surf_2 = font.render(str(score_2), False, 'Grey')
text_rect_2 = text_surf_2.get_rect()
text_rect_2.midbottom = (600, 80)

# The platform's y point of each player
player_1_y = 350
player_2_y = 350
bot_y = 350
# Setting the FPS
clock = pygame.time.Clock()

# Checking the times the ball has been hit by each player
times_hit = 0

# Surface and rectangle of player 1
player_1_surf = pygame.surface.Surface((10, 50))
player_1_rect = player_1_surf.get_rect()
player_1_surf.fill('White')

# Surface and rectangle of player 2
player_2_surf = pygame.surface.Surface((10, 50))
player_2_rect = player_2_surf.get_rect()
player_2_surf.fill('White')

# Surface and rectangle of bot if team option is chosen
bot_surf = pygame.surface.Surface((10, 50))
bot_rect = bot_surf.get_rect()
bot_surf.fill('White')

# Setting the position of each player
player_1_rect.center = (20, 350)
player_2_rect.center = (980, 350)
bot_rect.center = (980, 350)

# Dividing each platform into 5 to determine where the ball would go when hit at a certain position
player_1_small_rect_height = player_1_rect.height / 5
player_2_small_rect_height = player_2_rect.height / 5
bot_small_rect_height = bot_rect.height / 5

# Game text Press SPACE
game_text = font.render('Press SPACE to play', False, 'White')
game_text_rect = game_text.get_rect()
game_text_rect.center = 500, 500

# Game text press ESC
game_text_esc = subtext.render('Press ESC to return to menu', False, 'White')
game_text_esc_rect = game_text_esc.get_rect()
game_text_esc_rect.center = 500, 550

# Menu text "team"
menu_team = font.render('TEAM', False, 'White')
# Different type of screen, True will represent the screen with that value is active otherwise not
game_active = False
game_scored = False
player1_menu = False
menu = False
intro = True
options = False

# For mouse to hover over each button, default is False but when detected collision will turn True
hover1 = False
hover2 = False
hover_exit = False
hover_option = False
hover_pause = False
hover_team = False

# Drawing and establishing the block to be available for when the game runs
block_1 = pygame.draw.rect(screen, 'White', (300, 250, 400, 100), 2 if not hover1 else 0)
block_2 = pygame.draw.rect(screen, 'White', (300, 375, 400, 100), 2 if not hover2 else 0)
block_option = pygame.draw.rect(screen, 'White', (850, 650, 50, 50), 2 if not hover_option else 0)
block_exit = pygame.draw.rect(screen, 'White', (300, 500, 400, 100), 2 if not hover_exit else 0)
block_pause = pygame.draw.rect(screen, 'White', (10, 640, 100, 50), 2 if not hover_pause else 0)
block_team = pygame.draw.rect(screen, 'White', (300, 500, 400, 100), 2 if not hover_team else 0)

# Setting the value of player2 to see if there is another player, default is True
player2 = True

c_player_index = 0
c_bg_index = 0
c_score_index = 0
c_ball_index = 0
color_player = ['White', 'Red', 'Black', 'Blue', 'Pink', 'Purple', 'Grey']
color_bg = ['Black', 'White', 'Red', 'Grey', 'Blue', 'Pink', 'Purple']
color_score = ['Grey', 'White', 'Red', 'Blue', 'Pink', 'Purple', 'Black']
color_ball = ['White', 'Grey', 'Red', 'Blue', 'Pink', 'Purple', 'Black']

hover_player = False
hover_bg = False
hover_score = False
hover_ball = False

# The ball
ball = pygame.draw.circle(screen, color_ball[c_ball_index] if not hover_ball else color_ball[c_ball_index + 1],
						  (ball_x, ball_y), 5)
pause_back = subtext.render('BACK', False, color_player[c_player_index] if not hover_pause else color_bg[c_bg_index])
pause_back_rect = pause_back.get_rect()

n = 0
transparency = 1
game_by_x = -300

game_by = title.render('GAME BY', False, (0, 0, 0))
khanh_du = font.render('Khanh DU', False, (0, 0, 0))

appear = False
team_game = False

while True:

	# So that the game works less if the game isn't running
	mouse = pygame.mouse.get_pos()

	# Filling each frame at the start with black as to delete the frame of the previous run
	if not options:
		screen.fill(color_bg[c_bg_index])

	# dash is used for creating the dotted lines as show after
	dash = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if game_active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_active = False

		elif menu:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if block_1.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					# player1_menu = True
					game_scored = True
					menu = False
					player2 = False
				elif block_2.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					game_scored = True
					menu = False
					player2 = True
				elif block_option.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					menu = False
					options = True
				elif block_team.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					menu = False
					game_scored = True
					team_game = True
				elif block_exit.collidepoint(mouse):
					exit()

		elif options:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if text_rect_2.collidepoint(mouse) or text_rect_1.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					c_score_index += 1
				elif screen_rect.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					c_bg_index += 1
				elif ball.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					c_ball_index += 1
				elif player_1_rect.collidepoint(mouse) or player_2_rect.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					c_player_index += 1
				elif pause_back_rect.collidepoint(mouse):
					pygame.mixer.Sound.play(click)
					options = False
					menu = True
		elif game_scored:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_scored = False
					game_active = True
				elif event.key == pygame.K_ESCAPE:
					team_game = False
					game_scored = False
					menu = True
		else:
			if event.type == pygame.MOUSEBUTTONDOWN and block_pause.collidepoint(mouse):
				pygame.mixer.Sound.play(click)
				add_x = random.choice([2, -2])
				add_y = random.randint(-2, 2)
				player_1_y = 350
				player_2_y = 350
				bot_y = 350
				score_1, score_2 = 0, 0
				menu = True
				team_game = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_active = True

	player_1_surf.fill(color_player[c_player_index])
	player_2_surf.fill(color_player[c_player_index])
	if team_game:
		bot_surf.fill(color_player[c_player_index])
	# creating the surface and text of the score
	text_surf_1 = font.render(str(score_1), False, color_score[c_score_index])
	text_surf_2 = font.render(str(score_2), False, color_score[c_score_index])

	# Setting the position of the rectangle of each player platform
	player_1_rect.center = (20, player_1_y)
	player_2_rect.center = (980 if not team_game else 80, player_2_y)
	if team_game:
		bot_rect.center = (980, bot_y)

	# if one player has scored a point
	if intro:
		if transparency == 650:
			intro = False
			menu = True
		game_by_x += 3
		game_by = title.render('GAME BY', False, (255, 255, 255))
		game_by_rect = game_by.get_rect()
		game_by_rect.center = game_by_x, 300

		khanh_du = font.render('Khanh Du', False, (255, 255, 255))
		khanh_du_rect = khanh_du.get_rect()
		khanh_du_rect.center = game_by_x, 400

		screen.blit(game_by, game_by_rect)
		screen.blit(khanh_du, khanh_du_rect)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
			intro = False
			menu = True

		transparency += 1

	# if player1_menu:
	# 	n += 1
	# 	# if n == 5:
	# 	# 	pygame.mixer.Sound.play(womp_womp)
	# 	screen.fill('Black')
	# 	text = title.render('No friends?', False, color_player[c_player_index])
	# 	text_rect = text.get_rect()
	# 	text_rect.center = 500, 350
	# 	screen.blit(text, text_rect)
	# 	if n == 200:
	# 		player1_menu = False
	# 		game_scored = True
	elif game_scored:
		# display the message press SPACE and press ESC
		game_text = font.render('Press SPACE to play', False, color_player[c_player_index])
		game_text_esc = subtext.render('Press ESC to return to menu', False, color_player[c_player_index])
		screen.blit(game_text, game_text_rect)
		screen.blit(game_text_esc, game_text_esc_rect)

	# During the menu
	elif menu:
		# Ball back to default position
		ball_x = 500
		ball_y = 350

		# Score back to 0
		score_1 = 0
		score_2 = 0

		# menu option for player 1, 2, exit, and settings
		menu_1player = font.render('1 PLAYER', False,
								   color_player[c_player_index] if not hover1 else color_bg[c_bg_index])
		menu_1player_rect = menu_1player.get_rect()
		menu_1player_rect.center = (500, 300)

		menu_2player = font.render('2 PLAYERS', False,
								   color_player[c_player_index] if not hover2 else color_bg[c_bg_index])
		menu_2player_rect = menu_2player.get_rect()
		menu_2player_rect.center = (500, 425)

		menu_team = font.render('TEAM', False, color_player[c_player_index] if not hover_team else color_bg[c_bg_index])
		menu_team_rect = menu_team.get_rect()
		menu_team_rect.center = 500, 550

		menu_exit = subtext.render('EXIT', False,
								   color_player[c_player_index] if not hover_exit else color_bg[c_bg_index])
		menu_exit_rect = menu_exit.get_rect()
		menu_exit_rect.bottomleft = 30, 685

		menu_option = subtext.render('Settings', False,
									 color_player[c_player_index] if not hover_option else color_bg[c_bg_index])
		menu_option_rect = menu_option.get_rect()
		menu_option_rect.topleft = 850, 650

		# title Pong
		pong = title.render('PONG', False, color_player[c_player_index])
		pong_rect = pong.get_rect()
		pong_rect.center = (500, 150)

		# Render the title
		screen.blit(pong, pong_rect)

		# Render in the text and the block around the text
		block_1 = pygame.draw.rect(screen, color_player[c_player_index], (300, 250, 400, 100), 2 if not hover1 else 0)
		screen.blit(menu_1player, menu_1player_rect)
		block_2 = pygame.draw.rect(screen, color_player[c_player_index], (300, 375, 400, 100), 2 if not hover2 else 0)
		screen.blit(menu_2player, menu_2player_rect)
		block_menu = pygame.draw.rect(screen, color_player[c_player_index], (300, 500, 400, 100),
									  2 if not hover_team else 0)
		screen.blit(menu_team, menu_team_rect)

		block_exit = pygame.draw.rect(screen, color_player[c_player_index], (15, 645, 100, 50),
									  2 if not hover_exit else 0)
		screen.blit(menu_exit, menu_exit_rect)

		block_option = pygame.draw.rect(screen, color_player[c_player_index], (830, 640, 165, 50),
										2 if not hover_option else 0)
		screen.blit(menu_option, menu_option_rect)

		# Checking if the mouse ever goes inside the rectangles around the texts in menu
		if block_1.collidepoint(mouse):
			hover1 = True
		else:
			hover1 = False

		if block_2.collidepoint(mouse):
			hover2 = True
		else:
			hover2 = False

		if block_option.collidepoint(mouse):
			hover_option = True
		else:
			hover_option = False

		if block_exit.collidepoint(mouse):
			hover_exit = True
		else:
			hover_exit = False

		if block_menu.collidepoint(mouse):
			hover_team = True
		else:
			hover_team = False

	elif options:
		if c_score_index == 6:
			c_score_index = -1
		if c_bg_index == 6:
			c_bg_index = -1
		if c_player_index == 6:
			c_player_index = -1
		if c_ball_index == 6:
			c_ball_index = -1

		player_1_y = 350
		player_2_y = 350
		bot_y = 350

		player_1_surf.fill(color_player[c_player_index] if not hover_player else color_player[c_player_index + 1])
		player_2_surf.fill(color_player[c_player_index] if not hover_player else color_player[c_player_index + 1])
		# bot_surf.fill(color_player[c_player_index] if not hover_player else color_player[c_player_index + 1])

		screen.fill(color_bg[c_bg_index] if not hover_bg else color_bg[c_bg_index + 1])
		screen_rect = screen.get_rect()
		screen_rect.topleft = 0, 500

		pygame.draw.rect(screen, color_player[c_player_index], (10, 10, 100, 50), 2 if not hover_pause else 0)

		pause_back = subtext.render('BACK', False,
									color_player[c_player_index] if not hover_pause else color_bg[c_bg_index])
		pause_back_rect = pause_back.get_rect()
		pause_back_rect.topleft = (23, 20)

		# drawing the back text and rectangle of text
		screen.blit(pause_back, pause_back_rect)

		pygame.draw.line(screen, 'Orange', (0, 500), (1000, 500), 3)

		text_surf_1 = font.render(str(score_1), False, color_score[c_score_index] if not hover_score else
		color_score[(c_score_index + 1)])
		text_surf_2 = font.render(str(score_2), False, color_score[c_score_index] if not hover_score else
		color_score[(c_score_index + 1)])
		screen.blit(text_surf_1, text_rect_1)
		screen.blit(text_surf_2, text_rect_2)

		# drawing the dotted lines
		for i in range(35):
			pygame.draw.line(screen,
							 color_score[c_score_index] if not hover_score else color_score[(c_score_index + 1)],
							 [500, 1 + dash], [500, dash + 10], 3)
			dash += 20

		# The ball
		ball = pygame.draw.circle(screen, color_ball[c_ball_index] if not hover_ball else color_ball[c_ball_index + 1],
								  (ball_x, ball_y), 5)

		# The players
		screen.blit(player_1_surf, player_1_rect)
		screen.blit(player_2_surf, player_2_rect)
		# if team_game:
		screen.blit(bot_surf, bot_rect)

		if text_rect_2.collidepoint(mouse) or text_rect_1.collidepoint(mouse):
			hover_score = True
		else:
			hover_score = False

		if screen_rect.collidepoint(mouse):
			hover_bg = True
		else:
			hover_bg = False

		if ball.collidepoint(mouse):
			hover_ball = True
		else:
			hover_ball = False

		if player_1_rect.collidepoint(mouse) or player_2_rect.collidepoint(mouse):
			hover_player = True
		else:
			hover_player = False

		if pause_back_rect.collidepoint(mouse):
			hover_pause = True
		else:
			hover_pause = False


	# If game is paused
	elif not game_active and not intro:
		# Drawing the two white bars representing pause
		pygame.draw.rect(screen, color_player[c_player_index], (400, 250, 50, 200))
		pygame.draw.rect(screen, color_player[c_player_index], (550, 250, 50, 200))

		# rectangle for back button
		block_pause = pygame.draw.rect(screen, color_player[c_player_index], (10, 640, 100, 50),
									   2 if not hover_pause else 0)

		# render the text for back and set position for rectangle of text
		pause_back = subtext.render('BACK', False,
									color_player[c_player_index] if not hover_pause else color_bg[c_bg_index])
		pause_back_rect = pause_back.get_rect()
		pause_back_rect.bottomleft = (23, 682)

		# drawing the back text and rectangle of text
		screen.blit(pause_back, pause_back_rect)

		# checking for collision between rectangle and mouse
		if block_pause.collidepoint(mouse):
			hover_pause = True
		else:
			hover_pause = False
	# if in the game paused or active
	if not menu and not player1_menu and not intro:

		# displaying score
		screen.blit(text_surf_1, text_rect_1)
		screen.blit(text_surf_2, text_rect_2)

		# drawing the dotted lines
		for i in range(35):
			pygame.draw.line(screen, color_score[c_score_index], [500, 1 + dash], [500, dash + 10], 3)
			dash += 20

		# The ball
		if not options:
			pygame.draw.circle(screen, color_ball[c_ball_index], (ball_x, ball_y), 5)

		# The players
		screen.blit(player_1_surf, player_1_rect)
		screen.blit(player_2_surf, player_2_rect)
		if team_game:
			screen.blit(bot_surf, bot_rect)

	# Dividing each player's platform into 5 and having its position the same as each player's respective platform
	small_rects_1 = []
	for i in range(5):
		small_rect_1 = pygame.Rect(player_1_rect.left, player_1_rect.top + i * player_1_small_rect_height,
								   player_1_rect.width, player_1_small_rect_height)
		small_rects_1.append(small_rect_1)
	small_rects_2 = []
	for i in range(5):
		small_rect_2 = pygame.Rect(player_2_rect.left, player_2_rect.top + i * player_2_small_rect_height,
								   player_2_rect.width, player_2_small_rect_height)
		small_rects_2.append(small_rect_2)
	small_rects_bot = []
	for i in range(5):
		small_rect_bot = pygame.Rect(bot_rect.left, bot_rect.top + i * bot_small_rect_height,
									 bot_rect.width, bot_small_rect_height)
		small_rects_bot.append(small_rect_bot)
	# if the game is running, change the position of the ball
	if game_active:
		ball_x += add_x
		ball_y += add_y

	# if the game is active or the game is paused or has scored
	if game_active or game_scored:
		# checking if the player has gone too far off the screen and preventing it
		if 30 > player_1_y:
			player_1_y = 30
		elif player_1_y > 675:
			player_1_y = 675

		# player 1 movement keys
		if pygame.key.get_pressed()[pygame.K_w]:
			player_1_y -= 3.5
		elif pygame.key.get_pressed()[pygame.K_s]:
			player_1_y += 3.5

		# checking if the player has gone too far off the screen and preventing it
		if 30 > player_2_y:
			player_2_y = 30
		elif player_2_y > 675:
			player_2_y = 675

		if 30 > bot_y:
			bot_y = 30
		elif bot_y > 675:
			bot_y = 675

		# movement keys for player 2
		if pygame.key.get_pressed()[pygame.K_UP]:
			if not player2:
				player_1_y -= 3.5 if not pygame.key.get_pressed()[pygame.K_w] else 0
			else:
				player_2_y -= 3.5
		elif pygame.key.get_pressed()[pygame.K_DOWN]:
			if not player2:
				player_1_y += 3.5 if not pygame.key.get_pressed()[pygame.K_s] else 0
			else:
				player_2_y += 3.5
		if not player2 and not team_game:
			# the platform move automatically, following the y-position of the ball
			if ball_y < player_2_y:
				player_2_y -= 1.85
			elif ball_y > player_2_y:
				player_2_y += 1.85
		if team_game:
			if ball_y < bot_y:
				bot_y -= 1.95
			elif ball_y > bot_y:
				bot_y += 1.95

	# if the ball hits the top or bottom of the screen
	if ball_y >= 695 or ball_y <= 0:
		pygame.mixer.Sound.play(hit)
		# reverse the direction of the y-movement
		add_y = -add_y
	# if the ball has gone far to the right, meaning player 1 scored
	if ball_x >= 1000:
		pygame.mixer.Sound.play(lose)

		# reset the times hit
		times_hit = 0

		# ball position default
		ball_x = 500
		ball_y = 350

		# the name game, the ball will move to player 1's side
		add_x = -2

		# The ball will randomly go up or down
		add_y = random.randint(-2, 2)

		# score of player 1 increase by 1
		score_1 += 1

		# game active becomes false and the screen of game scored becomes true
		game_scored = True
		game_active = False
	# else if player 2 scores
	elif ball_x <= 0:
		# play sound
		pygame.mixer.Sound.play(lose)

		# reset times hit
		times_hit = 0

		# default ball position
		ball_x = 500
		ball_y = 350

		# score increase by 1
		score_2 += 1

		# ball goes to player 2, up or down in random
		add_y = random.randint(-2, 2)
		add_x = 2

		# screen of game scored becomes True and game is not active
		game_scored = True
		game_active = False

	# if platform of player 1 collide with the ball
	if player_1_rect.collidepoint((ball_x, ball_y)):
		# play sound hit
		pygame.mixer.Sound.play(hit)

		# depending on where it is hit, upper top, top, mid, bot, lower bot
		# the ball will fly up high, up, mid, down, down low
		if small_rects_1[0].collidepoint(ball_x, ball_y):
			add_y = -2
		elif small_rects_1[1].collidepoint(ball_x, ball_y):
			add_y = -1
		elif small_rects_1[2].collidepoint(ball_x, ball_y):
			add_y = random.choice([-0.5, -0.5, 0, 0.5, 0.5])
		elif small_rects_1[3].collidepoint(ball_x, ball_y):
			add_y = 1
		elif small_rects_1[4].collidepoint(ball_x, ball_y):
			add_y = 2

		# direction of ball changes and the number of times hit is increased by 1
		add_x = -add_x
		times_hit += 1
	# else if platform of player 2 collide with the ball
	if player_2_rect.collidepoint((ball_x, ball_y)):
		# play sound
		pygame.mixer.Sound.play(hit)
		add_x = -add_x
		times_hit += 1
		print(add_x)

		# depending on where it is hit, upper top, top, mid, bot, lower bot
		# the ball will fly up high, up, mid, down, down low
		if small_rects_2[0].collidepoint(ball_x, ball_y):
			add_y = -2
		elif small_rects_2[1].collidepoint(ball_x, ball_y):
			add_y = -1
		elif small_rects_2[2].collidepoint(ball_x, ball_y):
			add_y = random.choice([-0.5, -0.5, 0, 0.5, 0.5])
		elif small_rects_2[3].collidepoint(ball_x, ball_y):
			add_y = 1
		elif small_rects_2[4].collidepoint(ball_x, ball_y):
			add_y = 2

		# direction of ball changes and the number of times hit is increased by 1

	if bot_rect.collidepoint((ball_x, ball_y)):
		# play sound hit
		pygame.mixer.Sound.play(hit)

		# depending on where it is hit, upper top, top, mid, bot, lower bot
		# the ball will fly up high, up, mid, down, down low
		if small_rects_bot[0].collidepoint(ball_x, ball_y):
			add_y = -2
		elif small_rects_bot[1].collidepoint(ball_x, ball_y):
			add_y = -1
		elif small_rects_bot[2].collidepoint(ball_x, ball_y):
			add_y = random.choice([-0.5, -0.5, 0, 0.5, 0.5])
		elif small_rects_bot[3].collidepoint(ball_x, ball_y):
			add_y = 1
		elif small_rects_bot[4].collidepoint(ball_x, ball_y):
			add_y = 2

		add_x = -add_x
		times_hit += 1

	# if number of times hit is 8, 16, 40, 70, 120, increase the speed respectively
	if times_hit == 8:
		if add_x < 0:
			add_x = -4
		else:
			add_x = 4
	elif times_hit == 16:
		if add_x < 0:
			add_x = -6
		else:
			add_x = 6
	elif times_hit == 40:
		if add_x < 0:
			add_x = -10
		else:
			add_x = 10
	elif times_hit == 70:
		if add_x < 0:
			add_x = -15
		else:
			add_x = 15
	elif times_hit == 120:
		if add_x < 0:
			add_x = -20
		else:
			add_x = 20

	# update the display
	pygame.display.update()

	# FPS is 120
	clock.tick(120)
