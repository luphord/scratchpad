from turtle import *
screen = Screen()
screen.setup(width = 1.0, height = 1.0)
clearscreen()

N = 11
m = 40

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
bezier((0, N * m), (0, 0), (N * m, 0), N)

color("green")
bezier((0, -N * m), (0, 0), (N * m, 0), N)

color("blue")
bezier((0, -N * m), (0, 0), (-N * m, 0), N)

color("brown")
bezier((0, N * m), (0, 0), (-N * m, 0), N)

done()