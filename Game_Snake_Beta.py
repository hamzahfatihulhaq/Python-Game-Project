import turtle
"""
    module turtle adalah module yang lebih sederhana dari tkinter
    yang dimana dapat merepresentasikan grafik dan vektor
"""
import random
import time


delay = 0.1

#score
score = 0
hight_score = 0

#setup window screen 
window = turtle.Screen()
window.title("Game Snake Beta")
window.bgcolor("gray")
window.setup(width =1000, height=1000)
window.tracer(0) #set delay and turn off/on for update drawing

#head sneak
head = turtle.Turtle()
head.color("black")
head.speed(0)
head.shape("square")
head.shapesize(0.8,0.8)
head.penup()
head.goto(0,0) #move with vactor(x,y)
head.direction = "stop"
#make speed
speed = 10

#food
food = turtle.Turtle()
food.color("black","black")
food.speed(0)
food.shape("circle")
food.shapesize(0.6,0.6)
food.penup()
food.goto(330,330) #move with vactor(x,y)

#pen
pen =  turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,300)
pen.write("score : 0 Hight Score : 0", align="center", font=("Courier", 24, "normal"))

#segments body
segments = [] 

#START
start = turtle.Turtle()
start.speed(0)
start.shape("square")
start.color("white")
start.penup()
start.hideturtle()
start.goto(0,0)
start.write("START", align="center", font=("Courier", 24, "normal"))

#Trap
traps = []

#fungtion
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + speed)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - speed)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - speed)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + speed)

#keyboard bindings
window.listen() #untuk mengumpulkan argument dummy agar bisa diteruskan ke methode onclick
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")


#main game loop
while True:
    window.update()
    #Clear Start
    if head.direction == "up" or head.direction == "down" or head.direction == "left" or head.direction == "right":
        start.clear() 

    #if check for a collision with the boarder
    if head.ycor() > 340 or head.ycor() <-340 or head.xcor() > 480 or head.xcor() < -480:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"
        #hide the segments
        for segment in segments:
            segment.goto(1000,1000)
        
        #clear the segment list
        segments.clear()
        
        #hide the trap
        for trap in traps:
            trap.goto(1000,1000)
            trap.clear()
    
        #clear the trap list
        traps.clear()
        
        #Reset the score
        score = 0

        #Reset the delay
        delay = 0.1

        #Update the score display
        pen.clear()
        pen.write("score : {}   hight score : {}".format(score, hight_score), align="center", font=("Courier", 24, "normal"))
        
        #write start
        start.write("START", align="center", font=("Courier", 24, "normal"))

    # check for a collision with the food
    if head.distance(food) < 18:
        #move the rondom soot
        x = random.randint(-470,470)
        y = random.randint(-330,330)
        food.goto(x,y) 
        #add a sagment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.shapesize(0.8,0.8)
        new_segment.color("black","gray")
        new_segment.penup()
        segments.append(new_segment)

        #shorten the delay
        delay -= 0.001

        #incerease the score
        score += 10
        if score > hight_score:
            hight_score = score 

        pen.clear()
        pen.write("score : {}   hight score : {}".format(score,hight_score), align="center", font=("Courier", 24, "normal"))

        #add trap
        if score > 50 :
            new_trap = turtle.Turtle()
            new_trap.color("black","black")
            new_trap.speed(0)
            new_trap.shape("turtle")
            new_trap.shapesize(0.8,0.8)
            #new_trap.hideturtle()
            new_trap.penup()
            new_trap.goto(x*-1,y*-1) #move with vactor(x,y)
            new_trap.pendown()
            traps.append(new_trap)
        
    #move the end segments first in reverse order
    #range(start,end,step)
    for index in range(len(segments)-1, 0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
    #move segment 0 to where the head is 
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()
    
    #check for head collision with the body segments 
    for segment in segments:
        if segment.distance(head) < 10:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            #hide the segments
            for segment in segments:
                segment.goto(1000,1000)
        
            #clear the segment list
            segments.clear()
            
            #hide the trap
            for trap in traps:
                trap.goto(1000,1000)
                trap.clear()
    
            #clear the trap list
            traps.clear()

            #Reset the score
            score = 0
            #Reset the delay
            delay = 0.1
            #Update the score display
            pen.clear()
            pen.write("score : {}   hight score : {}".format(score,hight_score), align="center", font=("Courier", 24, "normal"))
            
            #wirte start
            start.write("START", align="center", font=("Courier", 24, "normal"))

    for trap in traps :
        if trap.distance(head) < 13:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
            
            #hide the trap
            for trap in traps:
                trap.goto(1000,1000)
                trap.clear()
    
            #clear the trap list
            traps.clear()
            #hide the segments
            for segment in segments:
                segment.goto(1000,1000)
        
            #clear the segment list
            segments.clear()
            
            #Reset the score
            score = 0
            #Reset the delay
            delay = 0.1
            #Update the score display
            pen.clear()
            pen.write("score : {}   hight score : {}".format(score,hight_score), align="center", font=("Courier", 24, "normal"))
            
            #wirte start
            start.write("START", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

window.mainloop()