"""
My flappy bird game made in python and pygame (for pixel collision used mask)
"""
import pygame
import os
import random
pygame.font.init() #init font

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")


# loads imgs and make them bigger
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    """
    Class representing the bird
    """
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5


    def __init__(self, x, y):
        """
        initialize the object
        :param x: starting x position(int)
        :param y: starting y position(int)
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.img_count = 0
        self.height = self.y
        self.img = self.IMGS[0]

    def jump(self):
        """
        make bird jumps
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make bird moves
        :return: None
        """
        self.tick_count += 1 # how many times moved since last jump

        # how many pixels moves up/down in frame  -10.5 + 1.5 = -9
        # for downward acceleration
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        # terminal velocity
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        # if bird goes up it doesnt goes down
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL


    def draw(self, window):
        """
        draw the bird
        :param window: pygame window
        :return: None
        """
        self.img_count += 1

        # changing bird img, loop through three images
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # when bird nose is down it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotate img around center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """
        gets the mask for image of bird
        :return:
        """
        return pygame.mask.from_surface(self.img)



class Pipe:
    """
    reoresents a pipe object
    """
    GAP = 200
    VEL = 5

    def __init__(self, x):
        """
        initialize pipe object
        :param x: int
        """
        self.x = x
        self.heigth = 0
        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.heigth = random.randrange(50,450)
        self.top = self.heigth - self.PIPE_TOP.get_height()
        self.bottom = self.heigth + self.GAP

    def move(self):
        """
        move pipe with velocity
        :return: None
        """
        self.x -= self.VEL

    def draw(self, window):
        """
        draw both the top and bottom pipe
        :param window:
        :return: None
        """
        # Top
        window.blit(self.PIPE_TOP, (self.x, self.top))
        # Bottom
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """
        returns if a point is colliding with the pipe
        :param bird:
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        return False

class Base:
    """
    reptesents the moving floor of the game
    """
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """
        initialize the object
        :param y: int
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor
        :return:
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, window):
        """
        Draw the floor (2 images following each other)
        :param window: pygame window
        :return: None
        """
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))



def draw_window(win, bird, pipes, base, score):
    """
    draws the window for the main game loop
    :param win: pygame window
    :param bird: Bird object
    :param pipes: List of pipes
    :param base: Base object
    :param score: score of the game
    :return:
    """
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)
    # Score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
    # Base
    base.draw(win)
    # Bird
    bird.draw(win)
    pygame.display.update()


def main():
    """
    main loop of game
    :return: None
    """
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    #win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    score = 0


    run = True
    while run:
        clock.tick(30)
        # If player hits close button it turn off the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Getting player input UP arrow key
        event = pygame.key.get_pressed()
        if event[pygame.K_UP]:
            bird.jump()
        bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            # controls the collision if bird collide it creates new bird and pipes and set game score to 0
            if pipe.collide(bird):
                bird = Bird(230, 350)
                pipes = [Pipe(600)]
                score = 0
            # Remove pipes if the are out of screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            # If bird pass the pipe it sets variable for new pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            # Moves the pipes
            pipe.move()

        # if add_pipe == True it update the score and add pipe to list
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        #remove pipes from list
        for r in rem:
            pipes.remove(r)

        # it starts game again if bird reachs the top or ground
        if bird.y + bird.img.get_height() >= 730 or WINDOW_HEIGHT - bird.y >= WINDOW_HEIGHT:
            bird = Bird(230, 350)
            pipes = [Pipe(600)]
            score = 0

        # Moves the base
        base.move()

        # Drawing window
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()

main()






