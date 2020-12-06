import svgwrite
from random import random, seed
from math import sqrt

sqrt2 = sqrt(2)
seed(1234)

width, height = 1920, 1080
square_width = 200

drawing = svgwrite.Drawing(
    filename="rotating_squares.svg", debug=True, size=(width, height)
)

# color1 = (80, 140, 200) # light blue
color1 = (82, 119, 46) # desaturated green
color2 = (190, 190, 190)

for i in range(2000):
    alpha_x, alpha_y = random(), random()
    x, y = (
        alpha_x * (width + square_width) - square_width,
        alpha_y * (height + square_width) - square_width,
    )
    alpha = random()
    r = color1[0] + alpha * (color2[0] - color1[0])
    g = color1[1] + alpha * (color2[1] - color1[1])
    b = color1[2] + alpha * (color2[2] - color1[2])
    angle = (random() - 0.5) * 90 * sqrt(alpha_x ** 2 + alpha_y ** 2) / sqrt2
    rect = drawing.rect(
        insert=(x, y),
        size=(square_width, square_width),
        fill=svgwrite.rgb(r, g, b),
        stroke="none",
        opacity=0.6 * random(),
        transform=f"rotate({angle}, {x}, {y})",
    )
    drawing.add(rect)

drawing.save()
