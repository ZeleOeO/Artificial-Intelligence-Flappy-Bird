import pygame
import neat
import random
import time

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load("bird1.png")), pygame.transform.scale2x(pygame.image.load("bird2.png")), pygame.transform.scale2x(pygame.image.load("bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("pipe.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("bg.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))

class Bird:
    IMGS=BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel =0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count+=1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 
        if (d>=16):
            d=16 
        if d<0:
            d=-2
        self.y += d
        
