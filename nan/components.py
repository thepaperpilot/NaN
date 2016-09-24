import os
import interpolation
import pygame

class Player:
    pass

class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Size:
    def __init__(self, width=0.0, height=0.0, scale=1.0):
        self.width = width
        self.height = height
        self.scale = scale

class Text:
    def __init__(self, text="", font=None, color=(0, 128, 0)):
        self.text = text
        self.font = font
        self.color = color

class Image:
    def __init__(self, file=None, image=None, blend=0):
        if file:
            self.image = pygame.image.load(os.path.join('images', file))
        else:
            self.image = image
        self.blend = blend

class Click:
    def __init__(self, run=None):
        self.run = run

class Over:
    active = False

    def __init__(self, enterf=None, exitf=None):
        self.enterf = enterf
        self.exitf = exitf

class Circle:
    def __init__(self, color=(0,128,0), radius=0.0, width=0):
        self.color = color
        self.radius = radius
        self.width = width

class Rect:
    def __init__(self, color=(0,128,0), rect=pygame.Rect(0, 0, 0, 0), width=0):
        self.color = color
        self.rect = rect
        self.width = width

class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class ChangePosition:
    current = None

    def __init__(self, target=(0,0), time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = target
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args

class ChangeSize:
    current = None

    def __init__(self, target=1, time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = target
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args

class ChangeVelocity:
    current = None

    def __init__(self, target=(0,0), time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = target
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args

class ChangeAlpha:
    current = None

    def __init__(self, start=0, end=0, time=0, interp=interpolation.InterpolationBase(), chain=None, *args):
        self.target = end
        self.start = start
        self.time = time
        self.interp = interp
        self.chain = chain
        self.args = args

class CircleAnimation:
    current = 0

    def __init__(self, radius=0, time=0, stopangle=0, loop=False, chain=None, *args):
        self.radius = radius
        self.time = time
        self.stopangle = stopangle
        self.loop = loop
        self.chain = chain
        self.args = args

class Delay:
    def __init__(self, time=0, chain=None, *args):
        self.time = time
        self.chain = chain
        self.args = args
