import pygame
from csv import reader
from os import walk

WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 32


class ImageButton:
    def __init__(self, x, y, width, height, image, image_hover=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image_hover = self.image

        if image_hover:
            self.image_hover = pygame.image.load(image_hover)
            self.image_hover = pygame.transform.scale(self.image_hover, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None

        if sound:
            self.sound = pygame.mixer.Sound(sound)

        self.is_hovered = False

    def draw_button(self, screen):
        current_image = self.image_hover if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
