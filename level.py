import sqlite3
import sys
from settings import *
from tile import Tile
from player import Player
from pygame.locals import *
from tile_icon import TileIcon


class Level:
    def __init__(self, id_user):
        self.id = id_user
        self.player = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()
        self.life = 5
        self.reputation = 0
        # Создание таблицы и текста характеристик персонажа
        self.tablet = ImageButton(10, 10, 411, 103, "tablet.png")
        self.font = pygame.font.Font(None, 34)
        intro_text = f"Уровень вашей репутации: {self.reputation}"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = f"Количество жизней: {self.life}"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        # Подключение к БД и создание курсора
        self.connection = sqlite3.connect("bd_app")
        self.cursor = self.connection.cursor()

    def create_map(self):
        layouts = {
            'no': import_csv_layout('level_no.csv'),
            'icon': import_csv_layout('level_icons.csv')
        }
        graphics = {
            'icons': import_folder('icons')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'no':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'icon':
                            surf = graphics['icons'][int(col)]
                            TileIcon((x, y), [self.visible_sprites, self.obstacle_sprites], 'icons', surf, int(col))
        self.player = Player((900, 1015), [self.visible_sprites], self.obstacle_sprites, self.id)

    def pu_info(self, i):
        result = self.cursor.execute("SELECT * FROM user WHERE id = ?", (i,)).fetchall()[0]
        self.life = result[2]
        self.reputation = result[1]

    def info(self):
        intro_text = f"Уровень вашей репутации: {self.reputation}"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = f"Количество жизней: {self.life}"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))

    def run(self):
        pygame.init()
        pygame.display.set_caption("Duck Trip")
        pygame.display.set_icon(pygame.image.load("icon.ico"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            self.screen.fill('#92a85f')
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.tablet.draw_button(self.screen)
            self.screen.blit(self.text_1, (30, 30))
            self.screen.blit(self.text_2, (30, 70))
            self.pu_info(self.id)
            self.info()
            pygame.display.update()
            self.clock.tick(FPS)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load('background_level.png').convert()
        self.background_image_rect = self.background_image.get_rect(topleft=(0, 0))
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        background = self.background_image_rect.topleft - self.offset
        self.display_surface.blit(self.background_image, background)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
