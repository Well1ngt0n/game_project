import pygame
import os
import sys
from PIL import Image


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
    def __init__(self, group, root_group, image):
        super().__init__(root_group)
        if group != root_group:
            self.add(group)
        self.image = image
        self.rect = self.image.get_rect()
