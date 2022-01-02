import pygame
from pygame.locals import *

pygame.init()
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BREAKOUT GAME")

# define font
font1 = pygame.font.SysFont('comicsansms', 24)
font2 = pygame.font.SysFont('Constantia', 50)
# define color
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)
BLUE  = (0,0,255)

# define game variabel
cols = 12
rows = 12
clock = pygame.time.Clock()
fps = 30
live_ball = 0
live = False
game_over = 0
score = 0

# create sounds
bounce_sound = pygame.mixer.Sound("sound_game_pong_2.wav")
# function for outputting text onto the screen
def draw_text(text,font,WHITE,x,y):
    img = font.render(text, True, WHITE)
    screen.blit(img,(x,y))

# brick wall class
class wall():
    def __init__(self):
        self.width = WIDTH//cols
        self.height = 30
    def create_wall(self):
        self.blocks = []
        # define empty list for an individual black
        block_individual = []
        for row in range(rows):
            # preset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # gengrate x and y posisitons for each block and createa rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x,block_y+40, self.width, self.height)
                # essign block strength besad on row
                if row < 4 :
                    strength =3
                elif row < 8 :
                    strength  =2
                elif row < 12:
                    strength = 1
                # create a list at this point to store the rect the and colour data 
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of block
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strangth
                if block[1] == 3:
                    block_col = BLUE
                elif block[1] == 2:
                    block_col = GREEN
                elif block[1] == 1:
                    block_col = RED
                pygame.draw.rect(screen,block_col, block[0])
                pygame.draw.rect(screen,BLACK, (block[0]), 5)

# paddle class
class Paddle():
    def __init__(self):
        self.reset()

    def move(self):
        # reset movement direction
        self.dx =0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dx = -1
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.dx = 1

    def draw(self):
        pygame.draw.rect(screen,WHITE,self.rect)
        pygame.draw.rect(screen,BLACK,self.rect,5)
    
    def reset(self):
        # define paddle variable
        self.height =20
        self.width = 120
        self.x = int ((WIDTH/2) - (self.width/2))
        self.y = HEIGHT-(self.height *2)
        self.speed = 10
        self.rect= pygame.Rect(self.x, self.y, self.width, self.height)
        self.dx = 0

# ball class
class Ball():
    def __init__(self,x,y,score):
        self.reset(x,y,score)
    def move(self):
        # collision thershold
        collision_thresh = 6
        # start off with the assumption the wall has been destroyed completely
        wall_destroyed = 1
        row_count =0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speedy >0:
                        self.speedy*= -1
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speedy < 0:
                        self.speedy *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speedx >0:
                        self.speedx*= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speedx < 0:
                        self.speedx *= -1
                    # reduce  the block's strange by doing damege to it 
                    if wall.blocks[row_count][item_count][1]> 1:
                        wall.blocks[row_count][item_count][1] -= 1
                        bounce_sound.play()
                    else:
                        wall.blocks[row_count][item_count][0] = (0,0,0,0)
                        self.score += 10
                        bounce_sound.play()
                # check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0,0,0,0):
                    wall_destroyed = 0
                    
                
                # increase item counter
                item_count += 1
            # increase row counter
            row_count +=1
        # after iterating through all thevlocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1
        # check for collision with walls
        if self.rect.left < 0 or self.rect.right >WIDTH:
            self.speedx *= -1
            bounce_sound.play()
        # check for collision with top and bottom of the screen
        if self.rect.top <0:
            self.speedy *=-1
            bounce_sound.play()
        if self.rect.bottom > HEIGHT:
            self.game_over = -1
        # look for collision with paddle
        if self.rect.colliderect(paddle):
            # check if colliding from the top
            if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speedy > 0:
                self.speedy *= -1
                bounce_sound.play()
            else:
                self.speedx *= -1
                bounce_sound.play()


        self.rect.x += self.speedx
        self.rect.y += self.speedy

        return self.game_over
    def draw(self):
        pygame.draw.rect(screen,WHITE,self.rect)
    def reset(self,x,y,score):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y 
        self.rect = pygame.Rect(self.x, self.y, self.ball_rad+5, self.ball_rad+5)
        self.speedx =5
        self.speedy = -5
        self.game_over =0
        self.score = score
        

# create a wall
wall = wall()
wall.create_wall()

# create paddle
paddle = Paddle()

# create bakk
ball = Ball(paddle.x + (paddle.width //2), paddle.y - paddle.height, score)
run = True
while run:
    clock.tick(fps)

    screen.fill(BLACK)
    score = ball.score
    # draw object
    wall.draw_wall()
    paddle.draw()
    ball.draw()
    if live:
        paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = live_ball - 1
            live = False

    if not live:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font2, WHITE, WIDTH//2 - 250, HEIGHT//2 + 150)
        if game_over == 1:
            draw_text('YOU WON!', font2, WHITE, WIDTH//2 - 100,HEIGHT//2 + 120)
            draw_text('CLICK ANYWHERE TO START', font2, WHITE, WIDTH//2 - 250, HEIGHT//2 + 170)
        if game_over == -1 and live_ball == 0:
            draw_text('YOU LOST!', font2,WHITE, WIDTH//2 - 100,HEIGHT//2 + 120)
            draw_text('CLICK ANYWHERE TO START', font2, WHITE, WIDTH//2 - 250, HEIGHT//2 + 170)
        if game_over == -1 and live_ball >0:
            draw_text(f"YOU HAVE {live_ball} LIFE!", font2,WHITE, WIDTH//2 - 120,HEIGHT//2 + 120)
            draw_text('CLICK ANYWHERE TO CONTINUE', font2, WHITE, WIDTH//2 - 250, HEIGHT//2 + 170)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and live == False:
            if live_ball == 0:
                live_ball = 3
                score = 0
                wall.create_wall()
            live = True
            ball.reset(paddle.x + (paddle.width //2), paddle.y - paddle.height,score)
            paddle.reset()
            
    draw_text(f"SCORE : {ball.score}", font1, WHITE, WIDTH//2 - 40, 5)   
    draw_text(f"LIFE : {live_ball}",font1,WHITE, 20,5)     
    
    pygame.display.update()

pygame.quit()