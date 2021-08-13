import pygame, sys
import random
import neat
import os

pygame.init()
pygame.font.init()

GEN = 0
background = pygame.image.load("Images\Background.jpg")
background = pygame.transform.scale(background, (576, 1024))

floor1 = pygame.image.load("Images\Background_Floor.png")
floor1 = pygame.transform.scale(floor1, (576, 200))
floor2 = pygame.image.load("Images\Background_Floor.png")
floor2 = pygame.transform.scale(floor2, (576, 200))
FLOORS = [floor1, floor2]

bird1 = pygame.image.load("Images\Flappy_Bird(1).png")
bird1 = pygame.transform.scale(bird1, (70,50))
bird2 = pygame.image.load("Images\Flappy_Bird(2).png")
bird2 = pygame.transform.scale(bird2, (70,50))
bird3 = pygame.image.load("Images\Flappy_Bird(3).png")
bird3 = pygame.transform.scale(bird3, (70,50))
Bird_Images = [bird1, bird2, bird3]

Pipe_Up1 = pygame.image.load("Images\Pipe_Up.png")
Pipe_Up1 = pygame.transform.scale(Pipe_Up1, (100, 700))
Pipe_Up2 = pygame.transform.scale(Pipe_Up1, (100, 700))
Pipe_Up3 = pygame.transform.scale(Pipe_Up1, (100, 700))
Pipe_Down1 = pygame.image.load("Images\Pipe_Down.png")
Pipe_Down1 = pygame.transform.scale(Pipe_Down1, (100, 700))
Pipe_Down2 = pygame.transform.scale(Pipe_Down1, (100, 700))
Pipe_Down3 = pygame.transform.scale(Pipe_Down1, (100, 700))

Pipe_Up = [Pipe_Up1, Pipe_Up2, Pipe_Up3]
Pipe_Down = [Pipe_Down1, Pipe_Down2, Pipe_Down3]
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
class Bird:
    IMGs = Bird_Images
    MAX_ROTATION =  25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0 #Physics of bird
        self.vel = 0
        self.height = self.y
        self.image_count = 0
        self.img = self.IMGs[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        #insert velocity equation for y-position of the bird
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

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
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.img = self.IMGs[0]
        elif self.image_count < self.ANIMATION_TIME*2:
            self.img = self.IMGs[1]
        elif self.image_count < self.ANIMATION_TIME*3:
            self.img = self.IMGs[2]
        elif self.image_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGs[1]
            self.image_count = 0

        if self.tilt <= -80:
            self.img = self.IMGs[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Floor:
    ANIMATION_REPITION = 576
    FLOOR = FLOORS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x2 = x + self.ANIMATION_REPITION
        self.y2 = y
        self.tick_count = 0

    def move(self):
        self.x -= 5
        self.x2 -= 5
        if self.x <= -576:
            self.x = 0
            self.x2 = 576

    def draw(self, win):
        win.blit(self.FLOOR[0], (self.x, self.y))
        win.blit(self.FLOOR[1], (self.x2, self.y))


class Pipes:
    UP_PIPES = Pipe_Up
    DOWN_PIPES = Pipe_Down
    PIPE_WIDTH = 100
    PIPE_LENGTH = 700
    BLANK_SPACE_Y = 940
    BLANK_SPACE_X = 400
    FIRST_GENERATION = random.randint(500,1000)

    def __init__(self):
        self.x1 = self.FIRST_GENERATION
        self.x2 = self.FIRST_GENERATION + self.BLANK_SPACE_X
        self.x3 = self.FIRST_GENERATION + 2*self.BLANK_SPACE_X
        self.y_Down1 = random.randint(-600, -50)
        self.y_Down2 = random.randint(-600, -50)
        self.y_Down3 = random.randint(-600, -50)
        self.top1 = self.y_Down1 + self.PIPE_LENGTH
        self.top2 = self.y_Down2 + self.PIPE_LENGTH
        self.top3 = self.y_Down3 + self.PIPE_LENGTH
        self.y_Up1 = self.y_Down1 + self.BLANK_SPACE_Y
        self.y_Up2 = self.y_Down2 + self.BLANK_SPACE_Y
        self.y_Up3 = self.y_Down3 + self.BLANK_SPACE_Y
        self.Pipe_Counter = 0

    def move(self):
        self.x1 -= 5
        self.x2 -= 5
        self.x3 -= 5

        if self.x1 < -150:
            self.x1 = 1000
            self.y_Down1 = random.randint(-600, -50)
            self.y_Up1 = self.y_Down1 + self.BLANK_SPACE_Y
            self.top1 = self.y_Down1 + self.PIPE_LENGTH
            self.Pipe_Counter += 1

        if self.x2 < -150:
            self.x2 = self.x1 + self.BLANK_SPACE_X
            self.y_Down2 = random.randint(-600, -50)
            self.y_Up2 = self.y_Down2 + self.BLANK_SPACE_Y
            self.top2 = self.y_Down2 + self.PIPE_LENGTH
            self.Pipe_Counter += 1

        if self.x3 < -150:
            self.x3 = self.x2 + self.BLANK_SPACE_X
            self.y_Down3 = random.randint(-600, -50)
            self.y_Up3 = self.y_Down3 + self.BLANK_SPACE_Y
            self.top3 = self.y_Down3 + self.PIPE_LENGTH
            self.Pipe_Counter += 1

    def draw(self, win):
        win.blit(self.UP_PIPES[0], (self.x1, self.y_Up1))
        win.blit(self.DOWN_PIPES[0], (self.x1, self.y_Down1))
        win.blit(self.UP_PIPES[1], (self.x2, self.y_Up2))
        win.blit(self.DOWN_PIPES[1], (self.x2, self.y_Down2))
        win.blit(self.UP_PIPES[2], (self.x3, self.y_Up3))
        win.blit(self.DOWN_PIPES[2], (self.x3, self.y_Down3))

    def get_mask_Up_Pipes(self):
        Up_pipe1 = self.UP_PIPES[0].convert_alpha()
        Up_pipe2 = self.UP_PIPES[1].convert_alpha()
        Up_pipe3 = self.UP_PIPES[2].convert_alpha()
        return  pygame.mask.from_surface(Up_pipe1), pygame.mask.from_surface(Up_pipe1), pygame.mask.from_surface(Up_pipe2)

    def get_mask_Down_Pipes(self):
        Down_pipe1 = self.DOWN_PIPES[0].convert_alpha()
        Down_pipe2 = self.DOWN_PIPES[1].convert_alpha()
        Down_pipe3 = self.DOWN_PIPES[2].convert_alpha()
        return  pygame.mask.from_surface(Down_pipe1), pygame.mask.from_surface(Down_pipe2), pygame.mask.from_surface(Down_pipe3)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        up_mask1, up_mask2, up_mask3 = self.get_mask_Up_Pipes()
        bottom_mask1, bottom_mask2, bottom_mask3 = self.get_mask_Down_Pipes()

        top_offset1 = (self.x1 - bird.x, self.y_Down1 - round(bird.y))
        bottom_offset1 = (self.x1 - bird.x, self.y_Up1 - round(bird.y))

        top_offset2 = (self.x2 - bird.x, self.y_Down2 - round(bird.y))
        bottom_offset2 = (self.x2 - bird.x, self.y_Up2 - round(bird.y))

        top_offset3 = (self.x3 - bird.x, self.y_Down3 - round(bird.y))
        bottom_offset3 = (self.x3 - bird.x, self.y_Up3 - round(bird.y))

        b_point1 = bird_mask.overlap(bottom_mask1, bottom_offset1)
        t_point1 = bird_mask.overlap(up_mask1, top_offset1)

        b_point2 = bird_mask.overlap(bottom_mask2, bottom_offset2)
        t_point2 = bird_mask.overlap(up_mask2, top_offset2)

        b_point3 = bird_mask.overlap(bottom_mask3, bottom_offset3)
        t_point3 = bird_mask.overlap(up_mask3, top_offset3)

        if t_point1:
            return True
        if t_point2:
            return True
        if t_point3:
            return True
        if b_point1:
            return True
        if b_point2:
            return True
        if b_point3:
            return True

        return False

    def passed_pipes(self, current):
        if self.Pipe_Counter != current:
            return self.Pipe_Counter, True
        return self.Pipe_Counter, False

    def get_y(self, bird):
        ### Must choose which of pipe 1, pipe 2, or pipe 3 is the closest pipe
        distances = [self.x1 + self.PIPE_WIDTH - bird.x, self.x2 + self.PIPE_WIDTH - bird.x, self.x3 + self.PIPE_WIDTH - bird.x]
        positive_distances = []
        for distance in distances:
            if distance >= 0:
                positive_distances.append(distance)
            else:
                pass
        index = distances.index(min(positive_distances))
        top_heights = [self.top1, self.top2, self.top3]
        bottom_heights = [self.y_Up1, self.y_Up2, self.y_Up3]
        return top_heights[index], bottom_heights[index]

def draw_window(win, birds, floor, pipe, score, GEN):
    win.blit(background, (0,0))
    pipe.draw(win)
    floor.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (576 - score_label.get_width() - 15, 10))

    score_label = STAT_FONT.render("Gen: " + str(GEN),1,(255,255,255))
    win.blit(score_label, (10, 10))
    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()



def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200,200))
        g.fitness = 0
        ge.append(g)

    floor = Floor(0, 900)
    pipe = Pipes()
    passed_pipes, counter = pipe.passed_pipes(0)
    run = True
    win = pygame.display.set_mode((576, 1024))
    clock = pygame.time.Clock()
    score = 0

    while run:
        clock.tick(30)
        passed_pipes, counter = pipe.passed_pipes(passed_pipes)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        if len(birds) > 0:
            pass
        else:
            run = False
            break

        ### NEED TO CREATE FUNCTION TO FIND CLOSEST PIPES
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate((bird.y, abs(bird.y - pipe.get_y(bird)[0]), abs(bird.y - pipe.get_y(bird)[1])))

            if output[0] > 0.5:
                bird.jump()

        for x, bird in enumerate(birds):
            if pipe.collide(bird):
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        for x, bird in enumerate(birds):
            if bird.y + 50 > 900 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if counter:
            score += 1
            for g in ge:
                g.fitness += 5

        pipe.move()
        floor.move()
        draw_window(win, birds, floor, pipe, score, GEN)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
