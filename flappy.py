import pygame
import neat
import random
import time
pygame.font.init( )

# Screen Height and Width
WIN_WIDTH = 500
WIN_HEIGHT = 700

# Images used
# The Bird Image uses a list to loop through the animation
BIRD_IMG = [pygame.transform.scale(pygame.image.load("bird1.png"), (50,40)), pygame.transform.scale(pygame.image.load("bird2.png"), (50,40)), pygame.transform.scale(pygame.image.load("bird3.png"), (50,40))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("pipe.png"))
BG_IMG = pygame.transform.scale((pygame.image.load("bg.png")), (WIN_WIDTH,WIN_HEIGHT))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))

# Font used for the color
STAT_FONT = pygame.font.SysFont("comicsans", 50)

#Settings for the window properties
icon = pygame.image.load("bird1.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Flappy Bird")
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Creating Classes
# Bird Class
class Bird:
    IMGS=BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        # X and Y positions of the bird
        self.x = x
        self.y = y
        self.tilt = 0 # The rotation of the bird on the y-axis
        self.tick_count = 0 # A clock count that aids with the animation and it's sync with the movement of the bird
        self.vel = 0 
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count+=1
        d = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
        if d >= 16:
            d = (d/abs(d)) * 16

        if d < 0:
            d -= 2
 
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count+=1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP=200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height-self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x-=self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom-round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1-=self.VEL
        self.x2-=self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2+self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1+self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win,bird, pipes, base, score):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: " + str(score), 1,(255,255,255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    bird.draw(win)
    base.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,300)
    base = Base(600)
    pipes =[Pipe(500)]

    score = 0

    run=True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        # bird.move()
        add_pipe = False
        rem= []
        for pipe in pipes:
            if pipe.collide(bird):
                score = 0

            if pipe.x + pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)
            if not pipe.passed and pipe.x<bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(500))
        
        if bird.y + bird.img.get_height() >= WIN_HEIGHT-base.IMG.get_height():
            pass

        for r in rem:
            rem.remove(r)
        base.move()
        draw_window(WIN,bird, pipes, base, score)
    
    pygame.quit()

main()