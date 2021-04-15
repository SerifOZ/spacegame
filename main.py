import pygame
from pygame.locals import *
import time
import random


class Enemy:
    def __init__(self):
        self.image = pygame.image.load("enemy.png")
        self.x = random.randrange(0, 600, 40)
        self.y = 60
        self.list_of_enemies = []

    def place(self):
        self.x = random.randrange(0, 560, 40)
        self.list_of_enemies.append([self.x, self.y])

    def movement(self):
        for item in self.list_of_enemies:
            item[1] += 20


class Spaceship:
    def __init__(self, screen, ammo):
        self.ammo = ammo
        self.space_game = pygame.image.load("spaceship.png")
        self.x = 280
        self.y = 560
        self.shot_way = []
        self.shot_count = 10
        self.screen = screen

    def draw(self, enemy, font, score):
        image = font.render(f"Enemy : {len(enemy.list_of_enemies)}", True, (245, 124, 78))
        image2 = font.render(f"Shot : {self.shot_count}", True, (245, 124, 78))
        image3 = font.render(f"Score : {score}", True, (245, 124, 78))
        self.screen.fill((165, 253, 254))
        self.screen.blit(image3, (450, 0))
        self.screen.blit(image, (0, 0))
        self.screen.blit(image2, (0, 40))
        self.screen.blit(self.space_game, (self.x, self.y))
        for item in enemy.list_of_enemies:
            self.screen.blit(enemy.image, (item[0], item[1]))
        pygame.display.flip()

    def move(self, direction, enemy, font, score):
        if direction == "left" and self.x > 0:
            self.x -= 40
            self.draw(enemy, font, score)
            self.shot_move1(enemy, font, score)
        if direction == "right" and self.x < 560:
            self.x += 40
            self.draw(enemy, font, score)
            self.shot_move1(enemy, font, score)

    def shot(self, x, y):
        if self.shot_count > 0:
            self.shot_count -= 1
            temp_x = x+10
            temp_y = y-20
            shot_x_y = [temp_x, temp_y]
            self.shot_way.append(shot_x_y)
            self.screen.blit(self.ammo, (shot_x_y[0], shot_x_y[1]))
            pygame.display.flip()

    def shot_move(self, enemy, font, score):
        self.draw(enemy, font, score)
        for item in self.shot_way:
            if item[1] >= 0:
                item[1] -= 20
                self.screen.blit(self.ammo, (item[0], item[1]))
        pygame.display.flip()

    def shot_move1(self, enemy, font, score):
        self.draw(enemy, font, score)
        for item in self.shot_way:
            if item[1] >= 0:
                self.screen.blit(self.ammo, (item[0], item[1]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space")
        self.shot_image = pygame.image.load("shot.png")
        self.surface = pygame.display.set_mode((600, 600))
        self.surface.fill((165, 253, 254))
        self.spaceship = Spaceship(self.surface, self.shot_image)
        self.enemy = Enemy()
        self.score = 0
        self.font = pygame.font.SysFont(None, 40)
        self.spaceship.draw(self.enemy, self.font, self.score)
        pygame.display.flip()

    def game_win_window(self):
        image = self.font.render("You win!!", True, (147, 241, 0))
        image2 = self.font.render("Do you want play again Y/N", True, (32, 145, 174))
        self.surface.fill((165, 253, 254))
        self.surface.blit(image, (230, 280))
        self.surface.blit(image2, (120, 320))
        pygame.display.flip()

    def game_over_window(self):
        for item in self.enemy.list_of_enemies:
            if item[1] > 560:
                image = self.font.render("Game Over!!", True, (27, 74, 39))
                image2 = self.font.render("Do you want play again Y/N", True, (247, 0, 13))
                self.surface.fill((165, 253, 254))
                self.surface.blit(image, (230, 280))
                self.surface.blit(image2, (120, 320))
                pygame.display.flip()
                return True

    def game_checking(self):
        image = pygame.image.load("effect.png")
        for item in self.enemy.list_of_enemies:
            for shot in self.spaceship.shot_way:
                if item[0] <= shot[0] <= item[0]+40 and item[1] <= shot[1] <= item[1]+40:
                    temp_x = item[0]
                    temp_y = item[1]
                    self.enemy.list_of_enemies.remove(item)
                    self.spaceship.shot_way.remove(shot)
                    self.surface.blit(image, (temp_x, temp_y))
                    pygame.display.flip()
                    self.score += 10
                    self.spaceship.shot_count += 1

    def game_starting(self):
        running = True
        temp = 0
        enemy_count = 0
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.spaceship.move("left", self.enemy, self.font, self.score)
                    if event.key == K_RIGHT:
                        self.spaceship.move("right", self.enemy, self.font, self.score)
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        self.spaceship.shot(self.spaceship.x, self.spaceship.y)
                if event.type == QUIT:
                    running = False
            time.sleep(0.2)
            if temp == 8:
                if enemy_count < 20:
                    self.enemy.place()
                    temp = 0
                    enemy_count += 1
            if temp % 2 == 0:
                self.enemy.movement()
            self.spaceship.shot_move(self.enemy, self.font, self.score)
            self.game_checking()
            if self.score == 200:
                self.game_win_window()
                running = False
            if self.game_over_window():
                running = False
            temp += 1
        while not running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = True
                    if event.key == K_y:
                        new_game = Game()
                        new_game.game_starting()
                    if event.key == K_n:
                        running = True


if __name__ == "__main__":
    game = Game()
    game.game_starting()
