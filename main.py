import pygame
import os
import sys
from PIL import Image
# from player import Player
from random import randint
from interface import *
from other import *
import level
from random import randint

pygame.init()
pygame.display.init()
infoObject = pygame.display.Info()
size = width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
monsters = pygame.sprite.Group()
monsters_objects = []
player_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
land = pygame.sprite.Group()
land_underground = pygame.sprite.Group()
unmovable = pygame.sprite.Group()
edges = pygame.sprite.Group()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


# Тестовая земля, потому что Денис ленивая тварь
# 21.02.21 23:58 : Денис начал что-то делать (Поярков ленивая тварь)
_x = 0
_y = height // 2
_flag = False

for i in range(0, width + 199, 200):
    l = MySprite(unmovable, unmovable, load_image("sky.png"))
    l.rect.x = i
    l.rect.y = 0

l = MySprite(edges, all_sprites, load_image("edge.png"))
l.rect.x = -16
l.rect.y = _y - 160

for i in range(len(level.levels[0][0])):
    if level.levels[0][0][i] == "T":
        l = MySprite(all_sprites, all_sprites, load_image("tree.png"))
        l.rect.x = _x
        l.rect.y = _y - 196
        continue

    l = MySprite(land, all_sprites, load_image("dirt_grass.png"))

    if _flag:
        if i > 1 and level.levels[0][0][i - 2] == 'U':
            l.image = load_image("dirt_both.png")
        else:
            l.image = load_image("dirt_right.png")
    l.rect.x = _x
    l.rect.y = _y
    _y = int(_y)

    for j in range(_y + 16, _y + randint(200, 300), 16):
        if i != 0 and level.levels[0][0][i - 1] == 'U':
            continue

        t = MySprite(all_sprites, all_sprites, load_image("dirt.png"))
        _rand = randint(0, 80)
        if 5 >= _rand >= 0:
            t.image = load_image("stone.png")
        elif _rand == 50:
            t.image = load_image("copper.png")
        t.rect.x = _x
        t.rect.y = j

    _flag = False
    if level.levels[0][0][i] == 'R':
        if i != 0 and level.levels[0][0][i - 1] == 'U':
            l.image = load_image("dirt_grass_left_up.png")
        _x += 16

    elif level.levels[0][0][i] == 'U':
        if i != 0 and level.levels[0][0][i - 1] == 'U':
            l.image = load_image("dirt_grass_left.png")
        else:
            l.image = load_image("dirt_left.png")
        _y -= 16

    elif level.levels[0][0][i] == 'D':
        if i != 0 and level.levels[0][0][i - 1] == 'R':
            l.image = load_image("dirt_grass_right_up.png")
        elif i - 1 != 0 and level.levels[0][0][i - 1] == 'U':
            l.image = load_image("dirt_grass_both.png")
        else:
            l.image = load_image("dirt_grass_right.png")
        _y += 16
        _flag = True
    # elif level.levels[0][0][i] == 'L':
    #     _x -= 16
l = MySprite(edges, all_sprites, load_image("edge.png"))
l.rect.x = _x
l.rect.y = _y - 160


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
        self.image_spear = pygame.transform.rotate(load_image("spear.png"), -45)
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
            "spear": 70,
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
        # А может мы уже умерли?
        self.dead = False  # АХАХАХ ДЕД
        # Константые размеры
        self.width = 52
        self.height = 0  # Не помню xD
        # смотрю, нажата ли кнопка
        self.key_a = False
        self.key_d = False
        self.key_space = False

    def move(self):
        # print(self.legs.rect.y)
        # todo: сделать, чтобы он не прыгал на 100500 блоков сам (Поярков обрежь текстуры)
        # Костыль для камеры
        self.x = self.legs.rect.x
        self.y = self.legs.rect.y

        if self.health <= 0:
            self.dead = True

        if len(pygame.sprite.spritecollide(self.legs, land, False)) >= 6:
            self.legs.rect.y -= 40
            _flag = pygame.sprite.spritecollideany(self.legs, land)
            self.legs.rect.y += 40

            if not _flag:
                self.jump = True
                self.move_y = 10
            else:
                self.legs.rect.x += 5
                rcount = len(pygame.sprite.spritecollide(
                    self.legs, land, False))
                self.legs.rect.x -= 10
                lcount = len(pygame.sprite.spritecollide(
                    self.legs, land, False))
                self.legs.rect.x += 5

                if rcount > lcount and self.move_x > 0 or rcount < lcount and self.move_x < 0:
                    self.move_x = 0

        if pygame.sprite.spritecollideany(self.legs, edges):
            self.legs.rect.x += 5
            rcount = pygame.sprite.spritecollideany(self.legs, edges)
            self.legs.rect.x -= 10
            lcount = pygame.sprite.spritecollideany(self.legs, edges)
            self.legs.rect.x += 5

            if lcount and self.move_x < 0 or rcount and self.move_x > 0:
                self.move_x = 0

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
            if self.cur_tool == "sword":
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
                self.attack = (self.attack + 1) % 16
            else:
                if self.switch:
                    k = -1
                else:
                    k = 1
                if self.attack <= 5:
                    self.tool.rect.x += k * 10
                elif self.attack < 10:
                    self.tool.rect.x -= k * 10
                elif self.attack == 10:
                    if self.switch:
                        self.tool.rect.x = self.x - 65
                    else:
                        self.tool.rect.x = self.x - 15
                self.attack = (self.attack + 1) % 11

        pygame.draw.rect(screen, pygame.Color("red"), (20, 20, 100, 20))
        pygame.draw.rect(screen, pygame.Color("green"),
                         (20, 20, 100 * (self.health / self.max_health), 20))

    def switch_lr(self):
        self.attack = 0
        if self.cur_tool == "sword":
            if self.switch:
                self.tool.rect.x = self.x - 50
            else:
                self.tool.rect.x = self.x + 26
        elif self.cur_tool == "spear":
            if self.switch:
                self.tool.rect.x = self.x - 65
            else:
                self.tool.rect.x = self.x - 15
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
        self.image_spear = pygame.transform.flip(self.image_spear, True, False)
        if self.cur_tool is not None:
            self.tool.image = pygame.transform.flip(
                self.tool.image, True, False)
            if self.cur_tool == "sword":
                self.tool.rect.x += 76 * self.move_x // abs(self.move_x)
            else:
                self.tool.rect.x += 50 * self.move_x // abs(self.move_x)

    def events(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.move_x > 0:
                if self.key_d == False:
                    self.key_a = False
                self.key_d = False
            if event.key == pygame.K_a and self.move_x < 0:
                if self.key_a == False:
                    self.key_d = False
                self.key_a = False
            if event.key == pygame.K_SPACE:
                self.key_space = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.key_d = True
                self.key_a = False
            if event.key == pygame.K_a:
                self.key_a = True
                self.key_d = False
            if event.key == pygame.K_SPACE and not self.jump:
                self.key_space = True
            if event.key == pygame.K_1:
                self.cur_tool = "sword"
                self.tool.image = self.image_sword
                if self.switch:
                    self.tool.rect.x = self.x - 50
                else:
                    self.tool.rect.x = self.x + 26
            if event.key == pygame.K_2:
                self.cur_tool = "spear"
                self.tool.image = self.image_spear
                if self.switch:
                    self.tool.rect.x = self.x - 65
                else:
                    self.tool.rect.x = self.x - 15

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cur_tool and self.attack == 0:
                self.attack = 1

        if self.key_a:
            self.move_x = -5
        elif self.key_d:
            self.move_x = 5
        else:
            self.move_x = 0

        if self.key_space and not self.jump:
            self.jump = True
            self.move_y = 15


class Harpy:  # Летающий юнит(((
    def __init__(self, x, y):
        self.move = [load_image(f"harpy_move_{k}.png") for k in range(3)]
        self.cur_move = 0

        self.sprite = MySprite(monsters, all_sprites, self.move[0])
        self.sprite.rect.x = self.x = x
        self.sprite.rect.y = self.y = y

        self.switch = True
        self.fall = False
        self.dead = False
        self.attack = False

        self.step = 0

        self.retreat = 0

        self.move_x = 5
        self.move_y = 10

        self.time_not_attack = 0

        self.shield = 0
        self.damage = 40
        self.max_health = 100
        self.health = 100

        self.width = 120

    def update(self):
        self.x = self.sprite.rect.x
        self.y = self.sprite.rect.y

        if self.dead:
            return

        fl = False
        count = 0
        if not self.attack:
            for i in range(0, 300):
                self.sprite.rect.y += 1
                count += 1
                if pygame.sprite.spritecollideany(self.sprite, land):
                    fl = True
                    break
            if not fl:
                self.fall = True
                self.move_y = 0
            else:
                self.move_y = 10
                self.fall = False
            self.sprite.rect.y -= count

        if abs(player.x - self.x) < 300 and player.y > self.y and not self.attack:
            self.move_y = 0
            self.attack = True

        if (pygame.sprite.collide_circle(self.sprite, player.tool)
                or pygame.sprite.collide_circle(self.sprite, player.track)) and player.attack and self.shield == 0:
            self.retreat = 1
            self.shield = 1
            self.health -= player.damage[player.cur_tool]
            if self.health <= 0:
                self.sprite.kill()
                self.dead = True

        if self.shield != 0:
            self.shield = (self.shield + 1) % 15

        if player.x - 10 <= self.x <= player.x + 10 and self.retreat == 0:
            self.move_x = 0
            self.move_y = -10

        if self.retreat > 0:
            if self.switch:
                self.move_x = -5
            else:
                self.move_x = 5
            self.move_y = 10
            self.retreat = (self.retreat + 1) % 40

        elif pygame.sprite.spritecollideany(self.sprite, player_sprites):
            player.health -= self.damage
            self.retreat = True

        elif (player.x + 10 < self.x and self.move_x > 0) or (player.x - 10 > self.x and self.move_x < 0):
            self.move_x *= -1

        if pygame.sprite.spritecollideany(self.sprite, land):
            self.move_y = 10
            for i in range(-1, 2, 2):
                self.sprite.rect.x += 10 * i
                if not pygame.sprite.spritecollideany(self.sprite, land):
                    break
                self.sprite.rect.x -= 10 * i
            self.x = self.sprite.rect.x

        self.step = (self.step + 1) % 15
        self.sprite.image = self.move[self.step // 5 - 1]

        self.x += self.move_x
        self.sprite.rect.x += self.move_x
        if self.fall:
            self.move_y = max(self.move_y - 1, -10)
        self.y -= self.move_y
        self.sprite.rect.y -= self.move_y

        if self.move_x == 0:
            if player.x < self.x:
                self.move_x = -5

            else:
                self.move_x = 5
        if (self.move_x > 0 and self.switch) or (self.move_x < 0 and not self.switch):
            self.sprite.image = pygame.transform.flip(
                self.sprite.image, True, False)
            self.switch = not self.switch
            for i in range(len(self.move)):
                self.move[i] = pygame.transform.flip(self.move[i], True, False)

        pygame.draw.rect(screen, pygame.Color("red"),
                         (self.x, self.y - 20, self.width, 5))
        pygame.draw.rect(screen, pygame.Color("green"),
                         (self.x, self.y - 20, self.width * (self.health / self.max_health), 5))


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
        # УРААА КОСТЫЛЬ!!
        self.x = self.sprite.rect.x
        self.y = self.sprite.rect.y
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

        if self.health <= 0:
            self.sprite.kill()
            self.dead = True


def start_screen(death=False):
    # fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))

    if death:
        text("Вы умерли", screen, height // 2 - 300, 100, width)

    button_play = Button(height // 2 - 100, "Играть", 60, screen, width)
    button_save = Button(
        height // 2 + 100, "Уровни", 60, screen, width)
    upload_level = False
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
                    upload_level = True
        if upload_level:
            levels_screen()
            upload_level = False

            screen.fill((0, 0, 0))

            button_play = Button(
                height // 2 - 100, "Играть", 60, screen, width)
            button_save = Button(
                height // 2 + 100, "Уровни", 60, screen, width)
        pygame.display.flip()


def levels_screen():
    screen.fill((0, 0, 0))
    levels = []
    for i in range(4):
        levels.append(Button(height // 5 + i * 100,
                             f"Уровень {i + 1}", 60, screen, width))
    exit_btn = Button(height // 5 + 400, f"Назад", 60, screen, width)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if exit_btn.text_x - 10 <= x <= exit_btn.text_x - 10 + exit_btn.w and \
                        exit_btn.text_y - 10 <= y <= exit_btn.text_y - 10 + exit_btn.h:
                    print(1)
                    return
        pygame.display.flip()


if __name__ == "__main__":
    play = True
    dead = False
    while play:
        start_screen(dead)
        dead = False
        camera = Camera()
        player_sprites = pygame.sprite.Group()
        player = Player(150, 150)
        monsters_objects.append(Slime(1500, 150))
        monsters_objects.append(Harpy(1000, 150))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                player.events(event)
            # изменяем ракурс камеры
            camera.update(player.legs)
            # camera.update(monsters_objects[1].sprite)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)

            if player.dead is True:
                running = False
                dead = True
            unmovable.update()
            unmovable.draw(screen)
            all_sprites.update()
            all_sprites.draw(screen)
            for monster in monsters_objects:
                monster.update()
            player.move()
            clock.tick(60)
            pygame.display.flip()

        all_sprites = pygame.sprite.Group()
        monsters = pygame.sprite.Group()
        player_sprites = pygame.sprite.Group()
        monsters_objects = []
    pygame.quit()
