from tkinter import *
from tkinter import messagebox as mb
from threading import Timer
import random
import pygame

pygame.init()
sndFile = 'snd/Sound08078.wav'
soundWall = pygame.mixer.Sound(sndFile)
sndFile1 = 'snd/Sound08428.wav'
soundLose = pygame.mixer.Sound(sndFile1)
sndFile2 = 'snd/Sound19349.wav'
soundHit = pygame.mixer.Sound(sndFile2)
ballr = 5

#Load level
def LoadLvl(lvl):
    cells = {}
    f = open('levels/lvl' + str(lvl) + '.txt')
    for line in f:
        line1 = line[:-1]
        line2 = line1.split()
        line2 = int(line2[0]) * 20, int(line2[1]) * 20
        cells[line2] = "blue"
    f.close()
    return cells

#Make level
def DrawLevel(colrec):
    for i in colrec.keys():
        c.create_rectangle(int(i[0]) - 20, int(i[1]) - 20, int(i[0]), int(i[1]), fill='blue')

#Win or lose
def IsWin(colrec, ball):
    if(ball[1] + ballr >= 400):
        end = False
        DoWinOrLose(end)
        return True
    for i in colrec.keys():
            if(colrec[i] == "blue"):
                return False
    else:
        end = True
        if DoWinOrLose(end) == False:
            return True
        else:
            return False

#Win or lose dialog
def DoWinOrLose(end):
    global lvl
    global colrec
    if(end == True):
        if(lvl < 5):
            answer = mb.showinfo(title="Game Over!", message="Level " + str(lvl) + "passed!")
            lvl += 1
            colrec = LoadLvl(lvl)
            DrawLevel(colrec)
        else:
            answer = mb.showinfo(title="Game Over!", message="You win!")
            return True
    elif(end == False):
        soundLose.play()
        answer = mb.showinfo(title="Game Over!", message="You lose! Your Store: " + str(score))

#Platform move
def DrawPlatform(platform):
    c.create_rectangle(platform[0], platform[1], platform[2], platform[3], fill = 'red', outline = 'white')

def DeletePlatform(platform):
    c.create_rectangle(platform[0], platform[1], platform[2], platform[3], fill = 'white', outline = 'white')

#Ball move
def DrawBall(ball):
    My_create_circle(ball[0], ball[1], 'red')

def DeleteBall(ball):
    My_create_circle(ball[0], ball[1], 'white')

def My_create_circle(x, y, color):
    return c.create_oval(x-ballr, y-ballr, x+ballr, y+ballr, fill = color, outline = 'white')

#Draw store
def DrawScore(count):
    l.configure(text = "Store: " + str(count))

#Platform move for A or D click
def keypress(event):
    global platform
    global halfplatform
    if(platform[2] != 600):
        if(event.keycode == 68):
            DeletePlatform(platform)
            platform[0] += 10
            platform[2] += 10
            halfplatform += 10
            DrawPlatform(platform)
    if(platform[0] != 0):
        if(event.keycode == 65):
            DeletePlatform(platform)
            platform[0] -= 10
            platform[2] -= 10
            halfplatform -= 10
            DrawPlatform(platform)

#Recolor blue cells
def recolorCells(colrec):
    for i in colrec.keys():
        if (colrec[i] == "blue"):
            c.create_rectangle(i[0] - 20, i[1] - 20, i[0], i[1], fill='blue')

#Ball flying
def BallFlying():
    global ball
    global platform
    global halfplatform
    global colrec
    global score
    sign = ["-", "+"]
    value = [0.5, 1, 2,]
    change = False
    if(ball[1] + ballr >= platform[1] and ball[0] - ballr <= platform[2] and ball[0] + ballr >= platform[0]):
        soundWall.play()
        v[1] = -v[1]
        flysign = random.choice(sign)
        flyvalue = random.choice(value)
        if(ball[0] - ballr >= halfplatform):
            if(v[0] <= 3):
                if(flysign == "-"):
                    v[0] -= flyvalue
                else:
                    v[0] += flyvalue
        elif(ball[0] + ballr <= halfplatform):
            if(v[0] >= -3):
                if(flysign == "-"):
                    v[0] -= flyvalue
                else:
                    v[0] += flyvalue
    elif(ball[0] - ballr <= 0 or ball[0] + ballr >= 600):
        v[0] = -v[0]
        soundWall.play()
    elif(ball[1] - ballr <= 0 and change == False):
        v[1] = -v[1]
        soundWall.play()
    recolorcells = False
    for i in colrec.keys():
        x = i[0]
        y = i[1]
        if(recolorcells == False):
            if(abs(ball[0] - x) < ballr + 5 and abs(ball[1] - y) < ballr + 5 and v[1] > 0):
                recolorcells = True
        isHit = False
        if(colrec[i] == "blue"):
            if(ball[1] - ballr <= y and ball[1] - ballr > y - 20 and ball[0] - ballr >= x - 20 and ball[0] + ballr <= x):
                v[1] = -v[1]
                isHit = True
            elif(ball[1] - ballr >= y - 20 and ball[1] + ballr <= y and ball[0] + ballr >= x - 20 and ball[0] + ballr < x):
                v[0] = -v[0]
                isHit = True
            elif(ball[1] - ballr >= y - 20 and ball[1] + ballr <= y and ball[0] - ballr <= x and ball[0] - ballr > x - 20):
                v[0] = -v[0]
                isHit = True
            elif(ball[1] + ballr >= y - 20 and ball[1] + ballr < y and ball[0] + ballr <= x and ball[0] - ballr >= x - 20):
                v[1] = -v[1]
                isHit = True
        if(isHit):
            soundHit.play()
            c.create_rectangle(x - 20, y - 20, x, y, fill='white', outline = 'white')
            colrec[i] = "white"
            score += 1
            DrawScore(score)
            break

    DeleteBall(ball)
    if(recolorcells == True):
        recolorCells(colrec)
    ball[0] += v[0]
    ball[1] += v[1]
    DrawBall(ball)

#Ball moving timer
def OnTimer():
    if(IsWin(colrec, ball) != True):
        BallFlying()
        t = Timer(0.000025, OnTimer)
        t.start()

root = Tk()
root.title('Tennis')
c = Canvas(root, width = 600, height = 400, bg='white')


#Make level dictonary
lvl = 1
colrec = LoadLvl(lvl)
#Draw level
DrawLevel(colrec)

#Make platform
platform = [260, 390, 340, 400]
halfplatform = (platform[0] + platform[2]) / 2
DrawPlatform(platform)

#Make ball
ball = [290, 300]
DrawBall(ball)

#Make score
score = 0
l = Label(root, text='Store: ' + str(score), width=25, height=3, bg='#ff0000', fg='#000000',font=("Comic Sans MS", 30, "bold"))
l.pack()
c.pack()

#Start speed flying
v = [0, 1.8]

#Make click A or D
root.bind('<Key>',keypress)

#Make timer
t = Timer(0.000025, OnTimer)
t.start()

root.mainloop()
