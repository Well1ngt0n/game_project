import pygame
import os
import sys
from PIL import Image

pygame.init()
pygame.display.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None, reflection=False):
    fullname = os.path.join('data', name)
    if reflection:
        image = Image.open(fullname)
        image.transpose(Image.FLIP_LEFT_RIGHT)
        image.save(fullname)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class MySprite(pygame.sprite.Sprite):
    def __init__(self, all, image):
        super().__init__(all)
        self.image = image
        self.rect = self.image.get_rect()


class Player:
    def __init__(self, x, y):
        switch = False
        self.image_legs_move_2 = self.image_legs_move_0 = load_image("legs.png")
        self.image_legs_move_1 = load_image("legs-move-1.png")
        self.image_legs_move_3 = load_image("legs-move-2.png")
        self.image_body = load_image("body.png")
        self.image_body_tool = load_image("body-tool.png")
        self.image_head = load_image("head.png")

        self.reverse = []

        self.legs = MySprite(player_group, self.image_legs_move_0)
        self.move_count = 0
        self.body = MySprite(player_group, self.image_body)
        self.tool = False
        self.head = MySprite(player_group, self.image_head)

        self.x = self.legs.rect.x = self.body.rect.x = self.head.rect.x
        self.y = self.legs.rect.y = self.body.rect.y = self.head.rect.y

        self.delta_x = 0
        self.switch = False

        self.move_x = 0

    def move(self):
        dx = self.move_x
        if (dx < 0 and not self.switch) or (dx > 0 and self.switch):
            self.switch_lr()

        self.delta_x += dx
        self.x += dx
        self.body.rect.x += dx
        self.legs.rect.x += dx
        self.head.rect.x += dx

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

    def switch_lr(self):
        self.switch = not self.switch
        self.image_legs_move_0 = pygame.transform.flip(self.image_legs_move_0, True, False)
        self.image_legs_move_1 = pygame.transform.flip(self.image_legs_move_1, True, False)
        self.image_legs_move_2 = pygame.transform.flip(self.image_legs_move_2, True, False)
        self.image_legs_move_3 = pygame.transform.flip(self.image_legs_move_3, True, False)
        self.body.image = pygame.transform.flip(self.body.image, True, False)
        self.image_body = pygame.transform.flip(self.image_body, True, False)
        self.image_body_tool = pygame.transform.flip(self.image_body_tool, True, False)
        self.head.image = pygame.transform.flip(self.head.image, True, False)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move_x = 2
            if event.key == pygame.K_a:
                self.move_x = -2
            if event.key == pygame.K_SPACE:
                pass
                # реализовать прыжок
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.move_x = 0
            if event.key == pygame.K_a:
                self.move_x = 0
            if event.key == pygame.K_SPACE:
                pass
                # реализовать прыжок
        self.move()


if __name__ == "__main__":
    player_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    player = Player(30, 30)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.events(event)
        screen.fill(pygame.Color(255, 255, 255))
        player_group.update()
        player_group.draw(screen)
        clock.tick()
        pygame.display.flip()
    pygame.quit()
