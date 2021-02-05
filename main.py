import pygame
import os
import sys
from PIL import Image

pygame.init()
pygame.display.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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


class Button:
    def __init__(self, y, text, font_size):
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        text = self.font.render(text, True, (255, 255, 255))
        self.text_x = width // 2 - text.get_width() // 2
        self.text_y = y
        self.text_w = text.get_width()
        self.text_h = text.get_height()
        screen.blit(text, (self.text_x, self.text_y))
        pygame.draw.rect(screen, (255, 255, 255), (self.text_x - 10, self.text_y - 10, self.text_w + 20, self.text_h + 20), 1)


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    # screen.blit(fon, (0, 0))
    screen.fill((0, 0, 0))

    button_play = Button(height // 2 - 100, "Играть", 60)
    button_save = Button(height // 2 + 100, "Загрузить сохранение", 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


if __name__ == "__main__":
    start_screen()

    player_group = pygame.sprite.Group()
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
