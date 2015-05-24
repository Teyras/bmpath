#!/usr/bin/env python

from PIL import Image
import networkx as nx
from random import randint

image = Image.open("img.bmp")
graph = nx.Graph()

color_cross = {}
color_meter = {}

width, height = image.size

for i in range(width):
    for j in range(height):
        graph.add_node((i, j))

def neighbours (x, y):
    if (x > 0):
        if (y > 0):
            yield (x - 1, y - 1)
        if (y < height - 1):
            yield (x - 1, y + 1)
        yield (x - 1, y)
    if (x < width - 1):
        if (y > 0):
            yield (x + 1, y - 1)
        if (y < height - 1):
            yield (x + 1, y +1)
        yield (x + 1, y)
    
    if (y > 0):
        yield (x, y - 1)
    if (y < height - 1):
        yield (x, y + 1)

def dist (u, v):
    return ((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2) ** (0.5)

for v in graph.nodes():
    color = image.getpixel(v)

    for n in neighbours(v[0], v[1]):
        ncolor = image.getpixel(n)
        distance = dist(v, n)

        if color == ncolor:
            color_meter.setdefault(ncolor, randint(1, 10))
            weight = color_meter[ncolor] * distance
        else:
            color_cross.setdefault(ncolor, randint(1, 10))
            weight = color_cross[ncolor] * distance

        graph.add_edge(v, n, weight = weight)

for v in nx.astar_path(graph, (5, 5), (45, 45), dist):
    image.putpixel(v, (0, 0, 0))

image.save("img.path.bmp")

