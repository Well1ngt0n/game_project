from other import *
import pygame
import os
import sys
from PIL import Image


class Player:
    def __init__(self, x, y):
        self.sprites = pygame.sprite.Group()

        switch = False
        self.image_legs_move_2 = self.image_legs_move_0 = load_image("legs.png")
        self.image_legs_move_1 = load_image("legs-move-1.png")
        self.image_legs_move_3 = load_image("legs-move-2.png")
        self.image_body = load_image("body.png")
        self.image_body_tool = load_image("body-tool.png")
        self.image_head = load_image("head.png")
        self.image_sword = load_image("sword-test.png")
        self.image_jump = load_image("legs-jump.png")
        self.track1 = load_image("sword-track-1.png")
        self.track2 = load_image("sword-track-2.png")
        self.image_none = load_image("none.png")

        self.reverse = []
        self.track = MySprite(self.sprites, self.image_none)
        self.legs = MySprite(self.sprites, self.image_legs_move_0)
        self.move_count = 0
        self.cur_tool = "sword"
        self.tool = MySprite(self.sprites, self.image_sword)
        self.body = MySprite(self.sprites, self.image_body)

        self.head = MySprite(self.sprites, self.image_head)

        self.x = self.legs.rect.x = self.body.rect.x = self.head.rect.x = x
        self.y = self.legs.rect.y = self.body.rect.y = self.head.rect.y = y
        self.tool.rect.x = self.x + 26
        self.tool.rect.y = self.y - 5

        self.delta_x = 0
        self.switch = False
        self.jump = False

        self.move_x = 0
        self.move_y = -10

        self.attack = 0

    def move(self):
        if self.cur_tool is None:
            self.tool = None
            self.body.image = self.image_body
            self.body.rect.x = self.x
            self.body.rect.y = self.y
        else:
            self.body.image = self.image_body_tool
            self.body.rect.x = self.x
            self.body.rect.y = self.y
        if self.jump:
            self.legs.image = self.image_jump


        dx = self.move_x
        if (dx < 0 and not self.switch) or (dx > 0 and self.switch):
            self.switch_lr()

        self.delta_x += dx
        self.x += dx
        self.body.rect.x += dx
        self.legs.rect.x += dx
        self.head.rect.x += dx
        if self.cur_tool is not None:
            self.tool.rect.x += dx

        if self.delta_x % 10 == 0 and self.delta_x != 0:
            self.move_count = (self.move_count + 1) % 4
            if self.move_count == 0:
                self.legs.image = self.image_legs_move_0
            elif self.move_count == 1:
                self.legs.image = self.image_legs_move_1
            elif self.move_count == 2:
                self.legs.image = self.image_legs_move_2
            elif self.move_count == 3:
                self.legs.image = self.image_legs_move_3
            self.delta_x = 0

        if self.move_y != -10:
            self.move_y -= 1
            # if не соприкасается с землей
            self.y -= self.move_y
            self.legs.rect.y -= self.move_y
            self.body.rect.y -= self.move_y
            self.head.rect.y -= self.move_y
            self.tool.rect.y -= self.move_y
            # else
            # self.legs.image = self.image_legs_move_0
            # self.jump = False
            #

        if self.attack != 0:
            if self.attack == 5:
                if self.switch:
                    self.track.image = self.track1
                    self.track.rect.x = self.x - 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(self.tool.image, 45)
                else:
                    self.track.image = self.track1
                    self.track.rect.x = self.x + 50
                    self.track.rect.y = self.y
                    self.tool.image = pygame.transform.rotate(self.tool.image, -45)
                self.tool.rect.y += 15
            if self.attack == 10:
                if self.switch:
                    self.track.image = self.track2
                    self.track.rect.x = self.x - 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(self.image_sword, 90)
                else:
                    self.track.image = self.track2
                    self.track.rect.x = self.x + 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(self.image_sword, -90)
                self.tool.rect.y += 35
            if self.attack == 15:
                self.track.image = self.image_none
                self.tool.rect.y -= 50
                self.tool.image = self.image_sword
                self.attack = -1
            self.attack += 1

    def switch_lr(self):
        self.switch = not self.switch
        self.image_legs_move_0 = pygame.transform.flip(self.image_legs_move_0, True, False)
        self.image_legs_move_1 = pygame.transform.flip(self.image_legs_move_1, True, False)
        self.image_legs_move_2 = pygame.transform.flip(self.image_legs_move_2, True, False)
        self.image_legs_move_3 = pygame.transform.flip(self.image_legs_move_3, True, False)
        self.track1 = pygame.transform.flip(self.track1, True, False)
        self.track2 = pygame.transform.flip(self.track2, True, False)
        self.track.image = pygame.transform.flip(self.track.image, True, False)
        self.image_sword = pygame.transform.flip(self.image_sword, True, False)
        self.image_jump = pygame.transform.flip(self.image_jump, True, False)
        self.body.image = pygame.transform.flip(self.body.image, True, False)
        self.image_body = pygame.transform.flip(self.image_body, True, False)
        self.image_body_tool = pygame.transform.flip(self.image_body_tool, True, False)
        self.head.image = pygame.transform.flip(self.head.image, True, False)
        self.legs.image = pygame.transform.flip(self.legs.image, True, False)
        if self.cur_tool is not None:
            self.tool.image = pygame.transform.flip(self.tool.image, True, False)
            self.tool.rect.x += 76 * self.move_x // abs(self.move_x)

    def events(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.move_x > 0:
                self.move_x = 0
            if event.key == pygame.K_a and self.move_x < 0:
                self.move_x = 0
            if event.key == pygame.K_SPACE:
                pass
                # реализовать прыжок
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move_x = 5
            if event.key == pygame.K_a:
                self.move_x = -5
            if event.key == pygame.K_SPACE and not self.jump:
                self.jump = True
                self.move_y = 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cur_tool == "sword" and self.attack == 0:
                self.attack = 1