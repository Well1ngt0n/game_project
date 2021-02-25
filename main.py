import pygame
import os
import sys
from PIL import Image
# from player import Player
from interface import Button
from other import *
import level

pygame.init()
pygame.display.init()
infoObject = pygame.display.Info()
size = width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
monsters = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Тестовая земля, потому что Денис ленивая тварь
# 21.02.21 23:58 : Денис начал что-то делать (Поярков ленивая тварь)
land = pygame.sprite.Group()
_x = 0
_y = level.levels[0][0](height)
_flag = False

for i in level.levels[0][1]:
    l = MySprite(land, all_sprites, load_image("dirt_grass.png"))
    if _flag:
        l.image = load_image("dirt.png")
    l.rect.x = _x
    l.rect.y = _y

    _flag = False
    if i == 'R':
        _x += 16
    elif i == 'U':
        _y -= 16
        l.image = load_image("dirt.png")
    elif i == 'D':
        _y += 16
        _flag = True
    elif i == 'L':
        _x -= 16


def terminate():
    pygame.quit()
    sys.exit()


class Player:
    def __init__(self, x, y):

        self.image_legs_move_2 = self.image_legs_move_0 = load_image(
            "legs.png")
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

        self.track = MySprite(all_sprites, all_sprites, self.image_none)
        self.legs = MySprite(player_sprites, all_sprites,
                             self.image_legs_move_0)
        self.move_count = 0
        self.cur_tool = "sword"
        self.damage = {
            "sword": 50,
        }
        self.tool = MySprite(all_sprites, all_sprites, self.image_sword)
        self.body = MySprite(player_sprites, all_sprites, self.image_body)

        self.head = MySprite(player_sprites, all_sprites, self.image_head)

        self.x = self.legs.rect.x = self.body.rect.x = self.head.rect.x = x
        self.y = self.legs.rect.y = self.body.rect.y = self.head.rect.y = y
        self.tool.rect.x = self.x + 26
        self.tool.rect.y = self.y - 5

        self.delta_x = 0
        self.switch = False  # true - влево смотрит
        self.jump = False

        self.move_x = 0
        self.move_y = -20
        # Статы персонажа
        self.attack = 0
        self.health = 100
        self.max_health = 100
        # Константые размеры
        self.width = 52
        self.height = 0  # Не помню xD

    def move(self):
        # print(self.legs.rect.y)
        # todo: сделать, чтобы он не прыгал на 100500 блоков сам (Поярков обрежь текстуры)
        autojump = False
        _movex = self.move_x

        if len(pygame.sprite.spritecollide(self.legs, land, False)) >= 6:
            self.move_x = 0
            self.legs.rect.y -= 40

            if not pygame.sprite.spritecollideany(self.legs, land):
                autojump = True

            self.legs.rect.y += 40

            if autojump:
                auojump = False
                self.jump = True
                self.move_y = 10
                self.move_x = _movex
            else:
                if self.switch:
                    self.x += 1
                    self.body.rect.x += 1
                    self.head.rect.x += 1
                    self.tool.rect.x += 1
                    self.legs.rect.x += 1

                else:
                    self.x -= 1
                    self.body.rect.x -= 1
                    self.head.rect.x -= 1
                    self.tool.rect.x -= 1
                    self.legs.rect.x -= 1

        if pygame.sprite.spritecollideany(self.legs, land) and self.move_y <= 0:
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

        if self.delta_x % 10 == 0 and self.delta_x != 0 and not self.jump:
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
            self.move_y = max(self.move_y - 1, -20)
            for dy in range(abs(self.move_y)):
                if self.jump:
                    if pygame.sprite.spritecollideany(self.legs, land) and self.move_y <= 0:
                        self.jump = False
                    self.y -= self.move_y // abs(self.move_y) * 1
                    self.legs.rect.y -= self.move_y // abs(self.move_y) * 1
                    self.body.rect.y -= self.move_y // abs(self.move_y) * 1
                    self.head.rect.y -= self.move_y // abs(self.move_y) * 1
                    self.tool.rect.y -= self.move_y // abs(self.move_y) * 1

        if self.attack != 0:
            if self.attack == 5:
                if self.switch:
                    self.track.image = self.track1
                    self.track.rect.x = self.x - 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(
                        self.tool.image, 45)
                else:
                    self.track.image = self.track1
                    self.track.rect.x = self.x + 50
                    self.track.rect.y = self.y
                    self.tool.image = pygame.transform.rotate(
                        self.tool.image, -45)
                self.tool.rect.y += 15
            if self.attack == 10:
                if self.switch:
                    self.track.image = self.track2
                    self.track.rect.x = self.x - 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(
                        self.image_sword, 90)
                else:
                    self.track.image = self.track2
                    self.track.rect.x = self.x + 45
                    self.track.rect.y = self.y + 26
                    self.tool.image = pygame.transform.rotate(
                        self.image_sword, -90)
                self.tool.rect.y += 35
            if self.attack == 15:
                self.track.image = self.image_none
                self.tool.rect.y -= 50
                self.tool.image = self.image_sword
                self.attack = -1
            self.attack += 1

        pygame.draw.rect(screen, pygame.Color("red"), (20, 20, 100, 20))
        pygame.draw.rect(screen, pygame.Color("green"),
                         (20, 20, 100 * (self.health / self.max_health), 20))

    def switch_lr(self):
        self.switch = not self.switch
        self.image_legs_move_0 = pygame.transform.flip(
            self.image_legs_move_0, True, False)
        self.image_legs_move_1 = pygame.transform.flip(
            self.image_legs_move_1, True, False)
        self.image_legs_move_2 = pygame.transform.flip(
            self.image_legs_move_2, True, False)
        self.image_legs_move_3 = pygame.transform.flip(
            self.image_legs_move_3, True, False)
        self.track1 = pygame.transform.flip(self.track1, True, False)
        self.track2 = pygame.transform.flip(self.track2, True, False)
        self.track.image = pygame.transform.flip(self.track.image, True, False)
        self.image_sword = pygame.transform.flip(self.image_sword, True, False)
        self.image_jump = pygame.transform.flip(self.image_jump, True, False)
        self.body.image = pygame.transform.flip(self.body.image, True, False)
        self.image_body = pygame.transform.flip(self.image_body, True, False)
        self.image_body_tool = pygame.transform.flip(
            self.image_body_tool, True, False)
        self.head.image = pygame.transform.flip(self.head.image, True, False)
        self.legs.image = pygame.transform.flip(self.legs.image, True, False)
        if self.cur_tool is not None:
            self.tool.image = pygame.transform.flip(
                self.tool.image, True, False)
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
                self.move_y = 15
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cur_tool == "sword" and self.attack == 0:
                self.attack = 1


class Slime:
    def __init__(self, x, y):
        self.slime_image = load_image("slime.png")
        self.sprite = MySprite(monsters, all_sprites, self.slime_image)

        self.max_health = 150
        self.health = 150

        self.sprite.rect.x = x
        self.sprite.rect.y = y
        self.x = x
        self.y = y
        # Движение
        self.move_y = -10
        self.move_x = 0
        self.sleep = 0
        # Флаги
        self.switch = False
        self.jump_fall = False
        self.retreat = False
        # Размеры картинки, константа
        self.width = 68
        self.height = 40
        # Получив урон, должен быть щит
        self.shield = 0
        self.damage = 20
        # Чтобы игрок не получал 100500 урона за удар
        self.time_not_attack = 0
        # Жив ли еще?
        self.dead = False

    def update(self):
        if self.dead:  # Если мертв, так и обновлять нечего
            return
        if pygame.sprite.spritecollideany(self.sprite, land) and self.move_y <= 0:
            self.jump_fall = False
            self.move_y = -10
        elif self.jump_fall is False:
            self.jump_fall = True
            self.move_y = -1

        if (pygame.sprite.collide_circle(self.sprite, player.tool)
                or pygame.sprite.collide_circle(self.sprite, player.track)) and player.attack and self.shield == 0:
            self.health -= player.damage[player.cur_tool]
            self.retreat = True
            self.move_y = 0
            if player.switch:
                self.move_x = -5
            else:
                self.move_x = 5
            self.shield = 10
        elif self.shield != 0:
            self.shield -= 1

        if self.retreat:
            pass
        # Ударил игрока
        elif pygame.sprite.spritecollideany(self.sprite, player_sprites) and self.time_not_attack == 0:
            self.retreat = True
            self.move_x = 5 * self.move_x / abs(self.move_x)
            player.health -= self.damage
            self.time_not_attack = 20
        elif self.time_not_attack != 0:
            self.time_not_attack -= 1
        elif player.x >= self.x:
            self.move_x = 3
            if self.switch is True:
                self.switch = False
                self.sprite.image = pygame.transform.flip(
                    self.sprite.image, True, False)
        else:
            self.move_x = -3
            if self.switch is False:
                self.switch = True
                self.sprite.image = pygame.transform.flip(
                    self.sprite.image, True, False)

        if self.jump_fall:
            self.sprite.rect.x += self.move_x
            self.x += self.move_x
            self.move_y = max(self.move_y - 1, -20)
            for dy in range(abs(self.move_y)):
                if self.jump_fall:
                    if pygame.sprite.spritecollideany(self.sprite, land) and self.move_y <= 0:
                        self.retreat = False
                        self.jump_fall = False
                        self.sleep = 20
                    self.y -= self.move_y // abs(self.move_y) * 1
                    self.sprite.rect.y -= self.move_y // abs(self.move_y) * 1

        else:
            if self.sleep == 0:
                self.jump_fall = True
                self.move_y = 20
            else:
                self.sleep -= 1

        # Отрисовка здоровья
        pygame.draw.rect(screen, pygame.Color("red"),
                         (self.x, self.y - 20, self.width, 5))
        pygame.draw.rect(screen, pygame.Color("green"),
                         (self.x, self.y - 20, self.width * (self.health / self.max_health), 5))

        if self.health == 0:
            self.sprite.kill()
            self.dead = True


def start_screen():
    # fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))

    button_play = Button(height // 2 - 100, "Играть", 60, screen, width)
    button_save = Button(
        height // 2 + 100, "Загрузить сохранение", 60, screen, width)
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
    slime = Slime(1500, 150)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.events(event)

        screen.fill(pygame.Color(255, 255, 255))
        player.move()
        slime.update()
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
