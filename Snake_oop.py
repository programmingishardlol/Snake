import pygame
import sys
import random


class Snake():
    def __init__(self):
        # start at center and random position
        self.length = 1
        self.positions = [((dis_width / 2), (dis_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17,24,47)
        self.score = 0
        self.speed = 30

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # cannot turn in opposite direction
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        # longer than 1, has just 3 valid movement patterns
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*gridsize)) % dis_width), (cur[1] + (y*gridsize)) % dis_height)
        # if length of snake > 2 and the new location of the head of the snake overlaps, game over
        if len(self.positions) > 2 and new in self.positions[2:]:
            game_over()
            
        # add new head position and pop the last element
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # no need for this
    # def reset(self):
    #     self.length = 1
    #     self.positions = [((dis_width / 2), (dis_height / 2))]
    #     self.direction = random.choice([up, down, left, right])
    #     self.score = 0

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223,163,49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (93,216,228), rect, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y) % 2 == 0:
                rect = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (95, 215, 228), rect)
            else:
                rect = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (85, 195, 205), rect)

def game_over():
    while True:
        font = pygame.font.SysFont("bahnschrift", 40)
        msg = font.render("press q to quit or c to continue", True, (255,255,255))
        screen = pygame.display.set_mode((dis_width,dis_height))
        screen.blit(msg, (dis_width/6, dis_height/3))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    main()

dis_width = 600
dis_height = 400

gridsize = 20
grid_width = dis_width / gridsize
grid_height = dis_height / gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init()
    pygame.display.set_caption("Snake Game~")

    # keep track of each action a given time
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((dis_width, dis_height),0, 32)

    # draw the screen and surface and update base on each action
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("monospace", 20)

    while True:
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            snake.speed += 10
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        clock.tick(snake.speed)

        screen.blit(surface, (0,0))
        text = myfont.render(f"Score {snake.score}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        pygame.display.update()

main()
