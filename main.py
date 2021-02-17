import pygame
import os
import sys
from PIL import Image
# from player import Player
from interface import Button
from other import *

pygame.init()
pygame.display.init()
size = width, height = 2560, 1440
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
monsters = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Тестовая земля, потому что денис ленивая тварь
land = pygame.sprite.Group()
for i in range(width):
    l = MySprite(land, all_sprites, load_image("1-pix-land.png"))
    l.rect.x = i
    l.rect.y = height * 2 // 3


def terminate():
    pygame.quit()
    sys.exit()


class Player:
    def __init__(self, x, y):

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
        self.track = MySprite(player_sprites, all_sprites, self.image_none)
        self.legs = MySprite(player_sprites, all_sprites, self.image_legs_move_0)
        self.move_count = 0
        self.cur_tool = "sword"
        self.tool = MySprite(player_sprites, all_sprites, self.image_sword)
        self.body = MySprite(player_sprites, all_sprites, self.image_body)

        self.head = MySprite(player_sprites, all_sprites, self.image_head)

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
        # print(self.legs.rect.y)
        if pygame.sprite.spritecollideany(self.legs, land):
            print(1)
            self.jump = False
            self.move_y = -10
        elif self.jump is False:
            self.jump = True
            self.move_y = -1

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

        if self.jump:
            self.move_y = max(self.move_y - 1, -10)
            self.y -= self.move_y
            self.legs.rect.y -= self.move_y
            self.body.rect.y -= self.move_y
            self.head.rect.y -= self.move_y
            self.tool.rect.y -= self.move_y

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


class Slime:
    def __init__(self, x, y):
        self.slime_image = load_image("slime.png")
        self.sprite = MySprite(monsters, all_sprites, self.slime_image)

        self.sprite.rect.x = x
        self.sprite.rect.y = y
        self.x = x
        self.y = y

        self.switch = False
        self.move_y = -10
        self.move_x = 0
        self.jump_fall = False

    def update(self, player):
        if pygame.sprite.spritecollideany(self.sprite, land):
            self.jump_fall = False
            self.move_y = -10
        elif self.jump_fall is False:
            self.jump_fall = True
            self.move_y = -1

        if player.x > self.x:
            self.move_x = 3
            if self.switch is True:
                self.switch = False
                self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)
        else:
            self.move_x = -3
            if self.switch is False:
                self.switch = True
                self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)

        if self.jump_fall:
            self.sprite.rect.y += self.move_y
            self.y += self.move_y
            self.sprite.rect.x += self.move_x
            self.x += self.move_x
            if self.move_y != -10:
                self.move_y -= 1
        else:
            self.jump_fall = True
            self.move_y = 10


def start_screen():
    # fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))

    button_play = Button(height // 2 - 100, "Играть", 60, screen, width)
    button_save = Button(height // 2 + 100, "Загрузить сохранение", 60, screen, width)
    upload_save = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_play.text_x - 10 <= x <= button_play.text_x - 10 + button_play.w and \
                        button_play.text_y - 10 <= y <= button_play.text_y - 10 + button_play.h:
                    return
                if button_save.text_x - 10 <= x <= button_save.text_x - 10 + button_save.w and \
                        button_save.text_y - 10 <= y <= button_save.text_y - 10 + button_save.h:
                    upload_save = True
        if upload_save:
            pass
            # Загрузка сохранений
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()

    player_group = pygame.sprite.Group()
    player = Player(150, 150)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.events(event)

        player.move()
        screen.fill(pygame.Color(255, 255, 255))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
