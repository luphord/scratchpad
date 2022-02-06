from turtle import *
screen = Screen()
screen.setup(width = 1.0, height = 1.0)
clearscreen()

speed(0)

def linear_interpolate(p1, p2, alpha):
    x1, y1 = p1
    x2, y2 = p2
    return x1 + alpha * (x2 - x1), y1 + alpha * (y2 - y1)

def bezier(p1, p2, p3, n):
    for i in range(n):
        penup()
        a = linear_interpolate(p1, p2, i / n)
        b = linear_interpolate(p2, p3, (i + 1) / n)
        goto(*a)
        pendown()
        goto(*b)

color("red")
bezier((-600, 500), (-400, -400), (600, -500), 20)
color("green")
bezier((-600, 500), (400, 400), (600, -500), 20)

done()