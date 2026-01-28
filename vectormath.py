import pygame
import math

def dot_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2

def lerp (a, b, t):
    return a + t * (b - a)

# 6 a^5 - 15 a^4 + 10 a^3
def smoothstep (a):
    return round(6 * pow(a, 5) - 15 * pow(a, 4) + 10 * pow(a, 3), 3)

def entropy_calc (a, e):
    a *= e
    if a>1:
        a = 1
    if a<-1:
        a = -1
    return a