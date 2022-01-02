import pygame
import sys
import math
import random

pygame.init()
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600

# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)
BLUE  = (0,0,255)

#CREATE THE SCREEN
screen  = pygame.display.set_mode((WIDTH, HEIGHT))

# CREATE CLASS
class Paddle():
    def __init__(self):
        self.x = WIDTH/2.0
        self.y = 550
        self.dx = 0
        self.width = 120
        self.height = 20
        self.score = 0
        self.speed = 10

    def left(self):
        self.dx = -10
    def right(self):
        self.dx = 10
    def move(self):
        self.x = self.x + self.dx
        key = pygame.key.get_pressed()
        if self.x < 0 + self.width/2.0:
            self.x = 10 + self.width/2.0
            self.dx = 0
        elif self.x > WIDTH - self.width/2.0:
            self.x = WIDTH - 10 - self.width/2.0
            self.dx = 0
        
    def render(self):
        # creat rectangle
        # Rect(posisitonx,posisitiony,width,height)
        pygame.draw.rect(screen,WHITE, pygame.Rect(int(self.x-self.width/2.0),int(self.y-self.height/2.0), self.width,self.height))
    
class Ball():
    def __init__(self):
        self.x = WIDTH/2.0
        self.y = 500
        self.dx = 5
        self.dy = -5
        self.width = 15
        self.height = 15

    def left(self):
        self.dx = -5
    def right(self):
        self.dx = 5
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        # check for bodrder collision
        if self.x < 0 + self.width/2.0:
            self.x = 0 + self.width/2.0
            self.dx *= -1
        elif self.x > WIDTH - self.width/2.0:
            self.x = WIDTH - self.width/2.0
            self.dx *= -1
        if self.y < 0 + self.height/2.0:
            self.y = 0 + self.height/2.0
            self.dy *= -1
        elif self.y > HEIGHT - self.height/2.0:
            self.y = HEIGHT - self.height/2.0
            self.x = WIDTH/2.0
            self.y = 150 + HEIGHT/2.0

    def render(self):
        # creat rectangle
        # Rect(posisitonx,posisitiony,width,height)
        pygame.draw.rect(screen,WHITE, pygame.Rect(int(self.x-self.width/2.0),int(self.y-self.height/2.0), self.width,self.height))

    def is_aabb_collision(self, other):
        # Axis Aligned Bounding Box
        x_collision = (math.fabs(self.x-other.x)*2) < (self.width + other.width)
        y_collision = (math.fabs(self.y-other.y)*2) < (self.height + other.height)
        return(x_collision and y_collision)

class Brick():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 20
        self.color = random.choice([RED,BLUE,GREEN])
    def render(self):
        # creat rectangle
        # Rect(posisitonx,posisitiony,width,height)
        pygame.draw.rect(screen,self.color, pygame.Rect(int(self.x-self.width/2.0),int(self.y-self.height/2.0), self.width,self.height))
# Create font
font = pygame.font.SysFont("comicsansms", 24)
# Create Game Object
paddle = Paddle()
ball = Ball()

bricks = []
for y in range(35, 370,30):
    color = random.choice([RED, GREEN, BLUE])
    for x in range(40, 780,60):
        bricks.append(Brick(x,y))
        bricks[-1].color = color


# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # KEYBOARD EVENTS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.left()
            elif event.key == pygame.K_RIGHT:
                paddle.right()

    # Update objects
    paddle.move()
    ball.move()

    # Check for collisions
    if ball.is_aabb_collision(paddle):
        ball.dy *= -1

    dead_bricks = []
    for brick in bricks:
        if ball.is_aabb_collision(brick):
            ball.dy *= -1
            dead_bricks.append(brick)
            paddle.score += 10

    for brick in dead_bricks:
        bricks.remove(brick)

    # Render (Draw stuff)
    # fill the background color
    screen.fill(BLACK)

    # Render rectangle
    paddle.render()
    ball.render()

    for brick in bricks:
        brick.render()

    #Render the score
    score_surface = font.render(f"Score:{paddle.score}",True, WHITE)
    screen.blit(score_surface, (WIDTH/2.0 -30, 5))
    # flip the display
    pygame.display.flip()

    # set the FPS
    clock.tick(30)