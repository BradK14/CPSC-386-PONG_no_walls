# Program: PONG no walls
# Programmer: Bradley Keizer

import pygame, sys, random
from pygame.locals import *

pygame.init()
main_clock = pygame.time.Clock()

def draw_text(text, color, font, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = x, y
    surface.blit(textobj, textrect)

def press_any_key():
    pressed = False
    while not pressed:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return

# Window size
WINDOWW = 1200
WINDOWH = (int)(WINDOWW / 2)        # Landscape view
window_surface = pygame.display.set_mode((WINDOWW, WINDOWH), 0, 32)
pygame.display.set_caption('PONG No Walls')

# Text font
FONT_SIZE = int(WINDOWH / 10)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Paddle setup
LRHEIGHT = (int)(WINDOWW / 7.5)
LRWIDTH = (int)(LRHEIGHT / 8)
TBHEIGHT = LRWIDTH
TBWIDTH = LRHEIGHT

r_paddle = pygame.Rect(WINDOWW - LRWIDTH - 1, (int)((WINDOWH / 2) - (LRHEIGHT / 2)), LRWIDTH, LRHEIGHT)
r_paddle_image = pygame.image.load('Player_RPaddle.png')
r_paddle_image_fit = pygame.transform.scale(r_paddle_image, (LRWIDTH, LRHEIGHT))
tr_paddle = pygame.Rect((int)(WINDOWW - (WINDOWW / 4) - (TBWIDTH / 2)), 1, TBWIDTH, TBHEIGHT)
tr_paddle_image = pygame.image.load('Player_TBPaddle.png')
tr_paddle_image_fit = pygame.transform.scale(tr_paddle_image, (TBWIDTH, TBHEIGHT))
br_paddle = pygame.Rect((int)(WINDOWW - (WINDOWW / 4) - (TBWIDTH / 2)), WINDOWH - TBHEIGHT - 1, TBWIDTH, TBHEIGHT)
br_paddle_image = pygame.image.load('Player_TBPaddle.png')
br_paddle_image_fit = pygame.transform.scale(tr_paddle_image, (TBWIDTH, TBHEIGHT))
l_paddle = pygame.Rect(1, (int)((WINDOWH / 2) - (LRHEIGHT / 2)), LRWIDTH, LRHEIGHT)
l_paddle_image = pygame.image.load('Opponent_LPaddle.png')
l_paddle_image_fit = pygame.transform.scale(l_paddle_image, (LRWIDTH, LRHEIGHT))
tl_paddle = pygame.Rect((int)((WINDOWW / 4) - (TBWIDTH / 2)) , 1, TBWIDTH, TBHEIGHT)
tl_paddle_image = pygame.image.load('Opponent_TBPaddle.png')
tl_paddle_image_fit = pygame.transform.scale(tl_paddle_image, (TBWIDTH, TBHEIGHT))
bl_paddle = pygame.Rect((int)((WINDOWW / 4) - (TBWIDTH / 2)), WINDOWH - TBHEIGHT - 1, TBWIDTH, TBHEIGHT)
bl_paddle_image = pygame.image.load('Opponent_TBPaddle.png')
bl_paddle_image_fit = pygame.transform.scale(bl_paddle_image, (TBWIDTH, TBHEIGHT))
paddles = (tr_paddle, br_paddle, tl_paddle, bl_paddle, l_paddle, r_paddle)

# Paddle movement
P_PADDLE_MOVESPEED = 6
O_PADDLE_MOVESPEED = 4
moveL = False
moveR = False
moveU = False
moveD = False

# Net setup
NETW = (int)(LRWIDTH / 2)
NETH = (int)(WINDOWH / 9)
net1 = pygame.Rect((int)((WINDOWW / 2) - (NETW / 2)), 0, NETW, NETH)
net2 = pygame.Rect((int)((WINDOWW / 2) - (NETW / 2)), NETH * 2, NETW, NETH)
net3 = pygame.Rect((int)((WINDOWW / 2) - (NETW / 2)), NETH * 4, NETW, NETH)
net4 = pygame.Rect((int)((WINDOWW / 2) - (NETW / 2)), NETH * 6, NETW, NETH)
net5 = pygame.Rect((int)((WINDOWW / 2) - (NETW / 2)), NETH * 8, NETW, NETH * 2)
nets = (net1, net2, net3, net4, net5)

# Ball setup
BALLW = LRWIDTH
BALLH = BALLW
ball = pygame.Rect((int)((WINDOWW / 2) - (BALLW / 2)), (int)((WINDOWH / 2) - (BALLH / 2)), BALLW, BALLH)
ball_image = pygame.image.load('Ball.png')
ball_image_fit = pygame.transform.scale(ball_image, (BALLW, BALLH))

# Ball movement
XBALL_MOVESPEED = random.randint(4, 8)
YBALL_MOVESPEED = random.randint(4, 8)
ball_active = True
ball_up = False
ball_right = False
ball_left = False
ball_down = False
new_direction = random.randint(1, 4)
if new_direction == 1:
    ball_up = True
    ball_right = True
    ball_left = False
    ball_down = False
elif new_direction == 2:
    ball_up = True
    ball_right = False
    ball_left = True
    ball_down = False
elif new_direction == 3:
    ball_up = False
    ball_right = True
    ball_left = False
    ball_down = True
elif new_direction == 4:
    ball_up = False
    ball_right = False
    ball_left = True
    ball_down = True

# Score
p_score = 0
o_score = 0
p_wins = 0
o_wins = 0

# Sounds
paddle_hit_sound = pygame.mixer.Sound('Paddle_hit.wav')
small_win_sound = pygame.mixer.Sound('small_win.wav')
big_win_sound = pygame.mixer.Sound('big_win.wav')
loss_sound = pygame.mixer.Sound('loss.wav')

# Begin game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveR = False
                moveL = True
            if event.key == K_RIGHT or event.key == K_d:
                moveL = False
                moveR = True
            if event.key == K_UP or event.key == K_w:
                moveD = False
                moveU = True
            if event.key == K_DOWN or event.key == K_s:
                moveU = False
                moveD = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveL = False
            if event.key == K_RIGHT or event.key == K_d:
                moveR = False
            if event.key == K_UP or event.key == K_w:
                moveU = False
            if event.key == K_DOWN or event.key == K_s:
                moveD = False

    # Keep track of paddle position before
    before = (tr_paddle.left, br_paddle.left, tl_paddle.left, bl_paddle.left, l_paddle.top, r_paddle.top)

    # Player Paddle Movement
    if moveD and r_paddle.bottom < WINDOWH:
        r_paddle.top += P_PADDLE_MOVESPEED
    if moveU and r_paddle.top > 0:
        r_paddle.top -= P_PADDLE_MOVESPEED
    if moveL and (tr_paddle.left > (WINDOWW / 2) or br_paddle.left > (WINDOWW / 2)):
        tr_paddle.left -= P_PADDLE_MOVESPEED
        br_paddle.left -= P_PADDLE_MOVESPEED
    if moveR and (tr_paddle.right < WINDOWW or br_paddle.right < WINDOWW):
        tr_paddle.right += P_PADDLE_MOVESPEED
        br_paddle.right += P_PADDLE_MOVESPEED

    # Computer Paddle Movement
    if l_paddle.top + (LRHEIGHT / 2) > ball.bottom:
        if l_paddle.top > 0:
            l_paddle.top -= O_PADDLE_MOVESPEED
    elif (l_paddle.bottom - (LRHEIGHT / 2) < ball.top):
        if l_paddle.bottom < WINDOWH:
            l_paddle.bottom += O_PADDLE_MOVESPEED
    if tl_paddle.left + (TBWIDTH / 2) > ball.right:
        if tl_paddle.left > 0:
            tl_paddle.left -= O_PADDLE_MOVESPEED
            bl_paddle.left -= O_PADDLE_MOVESPEED
    elif tl_paddle.right - (TBWIDTH / 2) < ball.left:
        if tl_paddle.right < (WINDOWW / 2):
            tl_paddle.right += O_PADDLE_MOVESPEED
            bl_paddle.right += O_PADDLE_MOVESPEED

    # Ball Collision Detection with paddle
    if ball_up and ball_right:
        if ball.colliderect(r_paddle):
            ball_left = True
            ball_right = False
        elif ball.colliderect(l_paddle):
            ball_left = True
            ball_right = False
        elif ball.colliderect(tr_paddle):
            ball_down = True
            ball_up = False
        elif ball.colliderect(tl_paddle):
            ball_down = True
            ball_up = False
    elif ball_up and ball_left:
        if ball.colliderect(r_paddle):
            ball_left = False
            ball_right = True
        elif ball.colliderect(l_paddle):
            ball_left = False
            ball_right = True
        elif ball.colliderect(tr_paddle):
            ball_down = True
            ball_up = False
        elif ball.colliderect(tl_paddle):
            ball_down = True
            ball_up = False
    elif ball_down and ball_right:
        if ball.colliderect(r_paddle):
            ball_left = True
            ball_right = False
        elif ball.colliderect(l_paddle):
            ball_left = True
            ball_right = False
        elif ball.colliderect(br_paddle):
            ball_down = False
            ball_up = True
        elif ball.colliderect(bl_paddle):
            ball_down = False
            ball_up = True
    elif ball_down and ball_left:
        if ball.colliderect(r_paddle):
            ball_left = False
            ball_right = True
        elif ball.colliderect(l_paddle):
            ball_left = False
            ball_right = True
        elif ball.colliderect(br_paddle):
            ball_down = False
            ball_up = True
        elif ball.colliderect(bl_paddle):
            ball_down = False
            ball_up = True

    # Friction
    after = (tr_paddle.left, br_paddle.left, tl_paddle.left, bl_paddle.left, l_paddle.top, r_paddle.top)
    count = 0
    for paddle in paddles:
        if ball.colliderect(paddle):
            if count < 4:
                if after[count] > before[count]:
                    if ball_left:
                        XBALL_MOVESPEED -= 1
                    elif ball_right:
                        XBALL_MOVESPEED += 1
                elif after[count] < before[count]:
                    if ball_left:
                        XBALL_MOVESPEED += 1
                    elif ball_right:
                        XBALL_MOVESPEED -= 1
            elif count > 3:
                if after[count] > before[count]:
                    if ball_up:
                        YBALL_MOVESPEED -= 1
                    elif ball_down:
                        YBALL_MOVESPEED += 1
                elif after[count] < before[count]:
                    if ball_up:
                        YBALL_MOVESPEED += 1
                    elif ball_down:
                        YBALL_MOVESPEED -= 1
        count += 1

    # Paddle Collision Sound
    if ball.colliderect(l_paddle) or ball.colliderect(tl_paddle) or ball.colliderect(bl_paddle) or \
            ball.colliderect(r_paddle) or ball.colliderect(tr_paddle) or ball.colliderect(br_paddle):
        paddle_hit_sound.play()

    # Ball out of bounds and score update
    if ball.top < 0 or ball.bottom > WINDOWH or ball.left < 0 or ball.right > WINDOWW:
        ball_active = False
        if ball.centerx < int(WINDOWW / 2):
            p_score += 1
        elif ball.centerx > int(WINDOWW / 2):
            o_score += 1

    # Wins update
    if p_score > 10 and ((o_score + 1) < p_score):
        p_score = 0
        o_score = 0
        p_wins += 1
        if p_wins < 3:
            small_win_sound.play()
        elif p_wins == 3:
            big_win_sound.play()
    elif o_score > 10 and ((p_score + 1) < o_score):
        o_score = 0
        p_score = 0
        o_wins += 1
        loss_sound.play()

    # Reset ball if out of play
    if ball_active == False:
        ball.top = int((WINDOWH / 2) - (BALLH / 2))
        ball.left = int((WINDOWW / 2) - (BALLW / 2))
        new_direction = random.randint(1, 4)
        if new_direction == 1:
            ball_up = True
            ball_right = True
            ball_left = False
            ball_down = False
        elif new_direction == 2:
            ball_up = True
            ball_right = False
            ball_left = True
            ball_down = False
        elif new_direction == 3:
            ball_up = False
            ball_right = True
            ball_left = False
            ball_down = True
        elif new_direction == 4:
            ball_up = False
            ball_right = False
            ball_left = True
            ball_down = True
        XBALL_MOVESPEED = random.randint(4, 8)
        YBALL_MOVESPEED = random.randint(4, 8)
        ball_active = True

    # Ball Movement
    if ball_up:
        ball.top -= YBALL_MOVESPEED
    if ball_down:
        ball.bottom += YBALL_MOVESPEED
    if ball_right:
        ball.right += XBALL_MOVESPEED
    if ball_left:
        ball.left -= XBALL_MOVESPEED

    # Draw Background
    window_surface.fill(BLACK)

    # Draw Score
    col = RED
    font = pygame.font.Font(None, FONT_SIZE)
    draw_text('Opponent: ' + str(o_score), col, font, window_surface, int(WINDOWW / 6), int(WINDOWH / 5))
    draw_text('Out of 11', col, font, window_surface, int(WINDOWW / 6), int(WINDOWH / 3))
    draw_text('Wins: ' + str(o_wins), col, font, window_surface, int(WINDOWW / 6), int(WINDOWH / 2))
    draw_text(('Out of 3'), col, font, window_surface, int(WINDOWW / 6), int(2 * WINDOWH / 3))
    col = BLUE
    draw_text('Player: ' + str(p_score), col, font, window_surface, int(2 * WINDOWW / 3), int(WINDOWH / 5))
    draw_text('Out of 11', col, font, window_surface, int(2 * WINDOWW / 3), int(WINDOWH / 3))
    draw_text('Wins: ' + str(p_wins), col, font, window_surface, int(2 * WINDOWW / 3), int(WINDOWH / 2))
    draw_text(('Out of 3'), col, font, window_surface, int(2 * WINDOWW / 3), int(2 * WINDOWH / 3))

    # Draw Paddles
    window_surface.blit(r_paddle_image_fit, r_paddle)
    window_surface.blit(tr_paddle_image_fit, tr_paddle)
    window_surface.blit(br_paddle_image_fit, br_paddle)
    window_surface.blit(l_paddle_image_fit, l_paddle)
    window_surface.blit(tl_paddle_image_fit, tl_paddle)
    window_surface.blit(bl_paddle_image_fit, bl_paddle)
    
    # Draw Net
    for net in nets:
        pygame.draw.rect(window_surface, WHITE, net)

    # Draw Ball
    window_surface.blit(ball_image_fit, ball)

    # Check for a finished game
    if o_wins == 3:
        col = RED
        draw_text('YOU LOSE', col, font, window_surface, int((WINDOWW / 3) + 90), int(WINDOWH / 3))
        draw_text('Press any key to play again', YELLOW, font, window_surface, int((WINDOWW / 3) - 60), int(2 * WINDOWH / 3))
        pygame.display.update()
        press_any_key()
        p_score = 0
        p_wins = 0
        o_score = 0
        o_wins = 0
    elif p_wins == 3:
        col = BLUE
        draw_text('YOU WIN', col, font, window_surface, int((WINDOWW / 3) + 100), int(WINDOWH / 3))
        draw_text('Press any key to play again', YELLOW, font, window_surface, int((WINDOWW / 3) - 60), int(2 * WINDOWH / 3))
        pygame.display.update()
        press_any_key()
        p_score = 0
        p_wins = 0
        o_score = 0
        o_wins = 0

    pygame.display.update()
    main_clock.tick(40)
