import turtle
import os
import time

window = turtle.Screen()
window.title("Game Pong")
window.bgcolor("black")
window.setup(width=800, height=400)
window.tracer(0)

delay = 0

#score 
score_a = 0
score_b = 0

#Paddle A
paddle_a  = turtle.Turtle()
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=4.5, stretch_len=1)
paddle_a.speed(0)
paddle_a.penup()
paddle_a.goto(-375, 0)

#Paddle B
paddle_b  = turtle.Turtle()
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=4.5, stretch_len=1)
paddle_b.speed(0)
paddle_b.penup()
paddle_b.goto(375, 0)

#ball
ball  = turtle.Turtle()
ball.shape("square")
ball.color("white")
ball.shapesize(stretch_wid=0.7, stretch_len=0.7)
ball.speed(delay)
ball.penup()
ball.goto(0, 0)
ball.dx = 0.1
ball.dy = 0.1

#pen 
pen  = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.goto(0,170)
pen.shapesize(stretch_wid=1, stretch_len=1)
pen.hideturtle()
pen.write("Player 1: 0   Player 2: 0", align="center", font=("Courier", 15, "normal"))
#speed 
speed = 20

#fungtion
def paddle_a_up():
    y = paddle_a.ycor()
    y += speed
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= speed
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += speed
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= speed
    paddle_b.sety(y)


#keyboard binding
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

#main game loop

while True:
    window.update()
    ball.speed(delay)
    #pause
    if ball.xcor() == 0 and ball.ycor()==0:
        time.sleep(0.8)

    #move the ball
    ball.setx(ball.xcor() + ball.dx) 
    ball.sety(ball.ycor() + ball.dy)

    #border checking
    if ball.ycor() > 190:
        ball.sety(190)
        ball.dy *= -1
        os.system("aplay sound_game_pong_2.wav&")

    if ball.ycor() < -190:
        ball.sety(-190)
        ball.dy *= -1
        os.system("aplay sound_game_pong_2.wav&")

    if ball.xcor() > 390:
        ball.goto(0,0)
        #reset delay
        delay = 0.1
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player 1: {}   Player 2: {}".format(score_a,score_b), align="center", font=("Courier", 15, "normal"))
        
    if ball.xcor() < -390:
        ball.goto(0,0)
        #reset delay
        delay = 0.1
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player 1: {}   Player 2: {}".format(score_a,score_b), align="center", font=("Courier", 15, "normal"))


    if (ball.xcor() > 365 and ball.xcor() < 382) and (ball.ycor() < paddle_b.ycor() + 47 and ball.ycor() > paddle_b.ycor() - 47):
        ball.setx(360)
        #shorten the delay
        delay -= 1
        ball.dx *= -1 
        os.system("aplay sound_game_pong_1.wav&")

        if (ball.ycor() < paddle_b.ycor() - 42 and ball.ycor() > paddle_b.ycor() - 47) and ball.dy > 0:
            ball.dy *= -1
            if (ball.xcor() > 380 and ball.xcor() < 382):
                ball.setx(382)

        if (ball.ycor() < paddle_b.ycor() + 47 and ball.ycor() > paddle_b.ycor() + 42) and ball.dy < 0:
            ball.dy *= -1
            if (ball.xcor() > 380 and ball.xcor() < 382):
                ball.setx(382)
    
    if (ball.xcor() < -365 and ball.xcor() > -383) and (ball.ycor() < paddle_a.ycor() + 47 and ball.ycor() > paddle_a.ycor() - 47):
        ball.setx(-360)
        #shorten the delay
        delay -= 1
        ball.dx *= -1 
        os.system("aplay sound_game_pong_1.wav&")

        if (ball.ycor() < paddle_a.ycor() - 42 and ball.ycor() > paddle_a.ycor() - 47) and ball.dy > 0:
            ball.dy *= -1
            if (ball.xcor() < -380 and ball.xcor() > -383):
                ball.setx(-383)

        if (ball.ycor() < paddle_a.ycor() + 47 and ball.ycor() > paddle_a.ycor() + 42) and ball.dy < 0:
            ball.dy *= -1
            if (ball.xcor() < -380 and ball.xcor() > -383):
                ball.setx(-383)

    # AI player
    # if paddle_b.ycor() < ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 20 :
    #     paddle_b_up()
    # elif paddle_b.ycor() > ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 20 :
    #     paddle_b_down()
    
    # if paddle_a.ycor() < ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 50 :
    #     paddle_a_up()
    # elif paddle_a.ycor() > ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 50 :
    #     paddle_a_down()
    
    