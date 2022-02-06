from turtle import *
screen = Screen()
screen.setup(width = 1.0, height = 1.0)
clearscreen()

N = 11
m = 40

speed(0)

color("red")
for i in range(N):
    penup()
    goto(0, (N - i) * m)
    pendown()
    goto((i + 1) * m, 0)

color("green")
for i in range(N):
    penup()
    goto(0, -(N - i) * m)
    pendown()
    goto((i + 1) * m, 0)

color("blue")
for i in range(N):
    penup()
    goto(0, -(N - i) * m)
    pendown()
    goto(-(i + 1) * m, 0)

color("brown")
for i in range(N):
    penup()
    goto(0, (N - i) * m)
    pendown()
    goto(-(i + 1) * m, 0)

done()