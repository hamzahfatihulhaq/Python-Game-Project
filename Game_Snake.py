import curses
from random import randint
#setup window
curses.initscr() #initscr sama dengan stdscr di c
win = curses.newwin(20,60,0,0) #y,x
win.keypad(1)
curses.noecho()
"""
Biasanya aplikasi curses mematikan noecho otomatis 
tombol ke layar, berfungsi agar bisa membaca tombol 
dan hanya menampilkannya dalam keadaan tertentu.
"""
curses.curs_set(0)
win.border(0)
win.nodelay(1) #-1

#snake and food
snake = [(2,10),(2,9),(2,8)]#tuple in list, because tuple is imutable
food = (15,35)

win.addch(food[0],food[1],"o") 

#game logic
score = 0

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0,2, "SCORE : " + str(score)+ ' ')
    win.timeout(150 - (len(snake)//20 + len(snake)//10 % 140)) #increase speed
    
    prev_key = key
    event = win.getch()#untuk mendapatakan next character
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_RIGHT,curses.KEY_LEFT,curses.KEY_UP,curses.KEY_DOWN,ESC]:
        key = prev_key
    
    #calculate  the coordinat our snake
    #current coordinat of the head
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1
    
    #insert new head
    snake.insert(0, (y,x)) #akan sama dengan append 0(n)

    #check if we hit the border
    if y == 0: break
    if y == 19: break
    if x == 0 : break
    if x == 59: break

    #if snake runs over it self
    if snake[0] in snake[1:]: break

    #snake eat food
    if snake[0] == food:
        #eat the food
        score += 1
        food = ()
        #make new food
        while food == ():
            food = (randint(1,18),randint(1,58)) # 0,19 and 59 is  border
            if food in snake:
                food = ()
        win.addch(food[0],food[1],"o")

    else:
        #move snake
        last = snake.pop() #remove last item
        win.addch(last[0], last[1], " ")

    win.addch(snake[0][0],snake[0][1],"*")
curses.endwin() #destroy windows
print(f"Final score = {score}") #f-string

