import csv
import os
import tkinter as tk
import math
import numpy as np

root = tk.Tk()
#root.attributes("-fullscreen", True)

with open(os.getcwd() + '\\Raycasting\\map.csv', 'r') as f:
    game_map = list(csv.reader(f, delimiter=';'))

sizeY = len(game_map)
sizeX = sizeY
keys = set()

height = root.winfo_screenheight() - 100
width = height

rectSize = width/(sizeY)

posX = width/2
posY = height/2
dirX = posX
dirY = -500
mouseX = 0
angle = 0
fovAngle = 66
pixel = width/(66)
eachAngle = np.linspace(0, fovAngle, 1 * fovAngle + 1)

wallHeight = 20000

def rotate_point(x, y, cx, cy, angle):
    x = x - cx
    y = y - cy

    x1 = x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
    y1 = x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle))
    
    x1 = x1 + cx
    y1 = y1 + cy

    return x1,y1

def keyPress(e):
    keys.add(e.char)
    move(keys)

def keyRelease(e):
    keys.remove(e.char)

def rotate_angle(e):
    global angle
    if canvas.winfo_pointerx() < mouseX:
        angle -= 1
    elif canvas.winfo_pointerx() > mouseX:
        angle += 1

def move(keys):
    global posX, posY, angle, dirX, dirY
    i = int(posX/rectSize)
    j = int(posY/rectSize)
    speed = 5
    if 'a' in keys:
        moveX = speed * math.sin(math.radians(angle - 90))
        moveY = speed * math.cos(math.radians(angle - 90))
        hit = check_hit(int((posY - moveY)/rectSize), int((posX + moveX)/rectSize))
        if hit[0] == False:
            posX += moveX
            dirX += moveX
            posY -= moveY
            dirY -= moveY
    if 'd' in keys:
        moveX = speed * math.sin(math.radians(angle + 90))
        moveY = speed * math.cos(math.radians(angle + 90))
        hit = check_hit(int((posY - moveY)/rectSize), int((posX + moveX)/rectSize))
        if hit[0] == False:
            posX += moveX
            dirX += moveX
            posY -= moveY
            dirY -= moveY
    if 'w' in keys:
        moveX = speed * math.sin(math.radians(angle))
        moveY = speed * math.cos(math.radians(angle))
        hit = check_hit(int((posY - moveY)/rectSize), int((posX + moveX)/rectSize))
        if hit[0] == False:
            posX += moveX
            dirX += moveX
            posY -= moveY
            dirY -= moveY
    if 's' in keys:
        moveX = speed * math.sin(math.radians(angle))
        moveY = speed * math.cos(math.radians(angle))
        hit = check_hit(int((posY + moveY)/rectSize), int((posX - moveX)/rectSize))
        if hit[0] == False:
            posX -= moveX
            dirX -= moveX
            posY += moveY
            dirY += moveY

def calcDistance(posX, posY, dirX, dirY, angle, currAngle):   
    i = int(posX/rectSize)
    j = int(posY/rectSize)
    distance = 0
    color = 0
    dark = 0
    if math.cos(math.radians(angle)) >= 0:
        b = 0
        diff = -1
    else:
        b = sizeY
        diff = 1
    for k in range(j, b, diff):
        rectY = k + diff
        dY = posY - (rectY + (-1 + diff)//-2) * rectSize
        dX = dY * math.tan(math.radians(angle))
        rectX = int((posX + dX)/rectSize)
        if rectX >= 0 and rectX < sizeX and rectY >= 0 and rectY < sizeY:
            hit, color = check_hit(rectY, rectX)
            if hit == False:
                #canvas.create_rectangle(posX + dX - 1, posY - dY - 1, posX + dX + 2, posY - dY + 2, fill='red', tag='fov')
                pass
            else:
                #canvas.create_rectangle(posX + dX - 1, posY - dY - 1, posX + dX + 2, posY - dY + 2, fill='green', tag='fov')
                distance = math.sqrt(dX**2 + dY**2) * math.cos(math.radians(currAngle))
                break
    
    if math.tan(math.radians(angle)) != 0:
        if math.sin(math.radians(angle)) >= 0:
            b = sizeX
            diff = 1
        else:
            b = 0
            diff = -1
        for k in range(i, b, diff):
            rectX = k + diff
            dX = posX - (rectX + (-1 + diff)//-2) * rectSize
            dY = dX * 1/math.tan(math.radians(angle))
            rectY = int((posY + dY)/rectSize)
            if rectX >= 0 and rectX < sizeX and rectY >= 0 and rectY < sizeY:
                hit, colorBlue = check_hit(rectY, rectX)
                if hit == False:
                    #canvas.create_rectangle(posX - dX - 1, posY + dY - 1, posX - dX + 2, posY + dY + 2, fill='blue', tag='fov')
                    pass
                else:
                    #canvas.create_rectangle(posX - dX - 1, posY + dY - 1, posX - dX + 2, posY + dY + 2, fill='green', tag='fov')
                    distanceBlue = math.sqrt(dX**2 + dY**2) * math.cos(math.radians(currAngle))
                    if distance == 0 or distanceBlue < distance:
                        distance = distanceBlue
                        color = colorBlue
                        dark = 1
                    break
    return distance, int(color), dark          

def check_hit(i, j):
    if int(game_map[i][j]) > 0:
        return True, game_map[i][j]
    else:
        return False, game_map[i][j]

def Run():
    global dirX, dirY, posX, posY, angle, mouseX
    mouseX = canvas.winfo_pointerx()
    canvas.delete('fov')
    canvas3D.delete('wall')
    for i in eachAngle:
        dirX1, dirY1 = rotate_point(dirX, dirY, posX, posY, angle - fovAngle/2 + i)
        if i in (0, fovAngle):
            canvas.create_line(posX, posY, dirX1, dirY1, fill='red', tag='fov')
        distance, color, dark = calcDistance(posX, posY, dirX1, dirY1, angle - fovAngle/2 + i, -fovAngle/2 + i)
        fill='white'
        if color == 1:
            if dark == 0:
                fill = 'blue'
            else:
                fill = 'dark blue'
        elif color == 2:
            if dark == 0:
                fill = 'green'
            else:
                fill = 'dark green'
        elif color == 3:
            if dark == 0:
                fill = 'red'
            else:
                fill = 'dark red'
        elif color == 4:
            if dark == 0:
                fill = 'brown1'
            else:
                fill = 'brown4'
        canvas3D.create_rectangle(i * pixel, height/2, i * pixel + pixel, height/2 - wallHeight/distance, fill=fill, tag='wall', outline=fill) 
    root.after(60, Run)
    
canvas = tk.Canvas(bg='black', width=width, height=height)
canvas.grid(row = 0, column = 0)

canvas3D = tk.Canvas(bg='black', width=width, height=height)
canvas3D.grid(row = 0, column = 1)

root.bind('<w>', keyPress)
root.bind('<KeyRelease-w>', keyRelease)
root.bind('<s>', keyPress)
root.bind('<KeyRelease-s>', keyRelease)
root.bind('<a>', keyPress)
root.bind('<KeyRelease-a>', keyRelease)
root.bind('<d>', keyPress)
root.bind('<KeyRelease-d>', keyRelease)
root.bind('<Motion>', rotate_angle)

for i in range(0, sizeY):
    for j in range(0, sizeX):
        if int(game_map[i][j]) == 1:
            fill='blue'
        elif int(game_map[i][j]) == 2:
            fill = 'green'
        elif int(game_map[i][j]) == 3:
            fill = 'red'
        elif int(game_map[i][j]) == 4:
            fill = 'brown'
        else:
            fill='white'
        canvas.create_rectangle(rectSize * j, rectSize * i, rectSize * j + rectSize, rectSize * i + rectSize, fill=fill)

Run()
root.mainloop()