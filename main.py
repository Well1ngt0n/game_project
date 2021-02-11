import pygame
import os
import sys
from PIL import Image
from player import Player
from interface import Button

pygame.init()
pygame.display.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


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
        player.sprites.update()
        player.sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
