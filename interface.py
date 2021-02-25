import pygame
import os
import sys
from PIL import Image
from other import *


class Button:
    def __init__(self, y, text, font_size, screen, width):
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        text = self.font.render(text, True, (255, 255, 255))
        self.text_x = width // 2 - text.get_width() // 2
        self.text_y = y
        self.text_w = text.get_width()
        self.text_h = text.get_height()
        screen.blit(text, (self.text_x, self.text_y))
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.text_x - 10, self.text_y - 10, self.text_w + 20, self.text_h + 20), 1)
        self.w = self.text_w + 20
        self.h = self.text_h + 20