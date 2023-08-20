import pygame
from pygame import *
import math


class Object:

    def __init__(self, x, y, width, height, program):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.program = program
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self):

        pygame.draw.rect(self.program.window, (70, 70, 70), self.rect)


class LightPoint:

    def __init__(self, x, y, angle, program, light_points):

        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

        self.angle = angle
        self.precision = 2

        self.program = program
        self.light_points = light_points

        self.update()

    def update(self):

        self.x = self.start_x
        self.y = self.start_y

        run = True

        while run:

            self.x += math.cos(self.angle) * self.precision
            self.y += math.sin(self.angle) * self.precision

            for i in self.program.objects:
                if i.rect.colliderect(Rect(self.x, self.y, 1, 1)):
                    run = False
                    break

            if -10 <= self.x < self.program.width + 10 and -10 <= self.y < self.program.height + 10:
                continue

            break

    def draw(self):

        if not self.light_points.index(self) == len(self.light_points) - 1:

            points = [(self.x, self.y), (self.start_x, self.start_y), (self.light_points[self.light_points.index(self)
                      + 1].x, self.light_points[self.light_points.index(self) + 1].y)]

            pygame.draw.polygon(self.program.window, (255, 255, 255, 5), points)


class Light:

    def __init__(self, x, y, angle, program):

        self.x = x
        self.y = y

        self.angle = angle

        self.program = program

        self.light_points = []
        self.add_light_points()

        self.rect = Rect(self.x - 10, self.y - 10, 20, 20)

    def add_light_points(self):

        self.light_points = []

        angle = self.angle - 0.6

        number = 1

        while True:

            angle += 0.015

            self.light_points.append(LightPoint(self.x, self.y, angle, self.program, self.light_points))

            number += 1

            if angle > self.angle + 0.6:
                break

    def draw(self):

        for i in self.light_points:
            i.draw()


class Program:

    def __init__(self, width, height):

        pygame.init()

        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()
        self.level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                      [0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.objects = []
        self.create_level()

        self.light = Light(250, 100, 0, self)

        self.run = True

        self.FPS = 30

    def create_level(self):

        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                new_x = x * 50
                new_y = y * 50
                size = 50

                if self.level[y][x] == 1:
                    self.objects.append(Object(new_x, new_y, size, size, self))

        self.objects.append(Object(100, 100, 5, 5, self))

    def main(self):

        while self.run:
            self.check_if_close_game()
            self.update()

            self.draw()

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()

    def check_if_close_game(self):

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                self.run = False
                break

    def draw(self):

        self.window.fill((0, 0, 0))

        self.light.draw()

        pygame.draw.circle(self.window, (150, 150, 150), [self.light.x, self.light.y], 10)

        for i in self.objects:
            i.draw()

        pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")

    def update(self):

        keys = pygame.key.get_pressed()

        update = False

        if keys[K_a] or keys[K_LEFT]:

            self.light.angle -= 0.06
            update = True

        elif keys[K_d] or keys[K_RIGHT]:

            self.light.angle += 0.06
            update = True

        if keys[K_w] or keys[K_UP]:

            self.light.x += math.cos(self.light.angle) * 4
            self.light.y += math.sin(self.light.angle) * 4
            update = True

        if update:
            self.light.add_light_points()


if __name__ == "__main__":
    my_program = Program(500, 400)
    my_program.main()
