import sqlite3
import pygame
import sys
from pygame.locals import *
from end import End
from level import *
from settings import *


class Story:
    def __init__(self, id_s, id_u):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Duck Trip")
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("data/icon.ico"))
        self.background_image = pygame.image.load('data/background_story.png')
        self.text_2 = None
        self.text_1 = None
        self.text_surface = None
        self.id_u = id_u
        self.id_s = id_s
        self.x = 390
        self.y = 380
        self.x2 = 810
        self.y2 = 380
        # Подключение к БД и создание курсора
        self.connection = sqlite3.connect("bd_app")
        self.cursor = self.connection.cursor()
        result = self.cursor.execute("SELECT * FROM user WHERE id = ?", (self.id_u,)).fetchall()[0]
        self.life = result[2]
        self.reputation = result[1]
        # Создание карточек и текста к ним
        self.font = pygame.font.Font(None, 34)
        self.button_1 = ImageButton(253, 222, 365, 485, "data/button_story.png", "data/button_story2.png",
                                    "data/click.mp3")
        self.button_2 = ImageButton(668, 222, 365, 485, "data/button_story.png", "data/button_story2.png",
                                    "data/click.mp3")
        # Музыка
        pygame.mixer.init()
        pygame.mixer.music.load("data/muz.mp3")
        pygame.mixer.music.play(-1)

        if self.id_s == 0:
            self.story_0()
        elif self.id_s == 1:
            self.story_1()
        elif self.id_s == 2:
            self.story_2()
        elif self.id_s == 3:
            self.story_3()
        elif self.id_s == 4:
            self.story_4()

    def story_0(self):
        intro_text = "Вы повстречали крестьянина, который катит тяжелую тележку в горку..."
        self.text_surface = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Помочь крестьянину"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Пнуть по тележке"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        self.x = 320
        self.y = 380
        self.x2 = 750
        self.y2 = 380

    def story_1(self):
        intro_text = "Вы заплутали и наткнулись лагерь разбойников..."
        self.text_surface = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Сообщить жителям деревни"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Вступить в их лагерь"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        self.x = 270
        self.y = 380
        self.x2 = 726
        self.y2 = 380

    def story_2(self):
        intro_text = "Проходя мимо кузницы вас окликнул незнакомый человек..."
        self.text_surface = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Подойти"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Убежать"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))

    def story_3(self):
        intro_text = "Вы встретили попрошайку..."
        self.text_surface = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Дать мелочи"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Проигнорировать"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        self.x = 360
        self.y = 380
        self.x2 = 770
        self.y2 = 380

    def story_4(self):
        intro_text = "Вы постучали и дверь открыл дедушка..."
        self.text_surface = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Вежливо поздороваться"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = "Пригрозить"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        self.x = 290
        self.y = 380
        self.x2 = 785
        self.y2 = 380

    def bd(self):
        self.cursor.execute("UPDATE user SET count = ?, life = ? WHERE id = ?",
                            (self.reputation, self.life, self.id_u))
        self.connection.commit()
        return False

    def run(self):
        pygame.init()
        pygame.display.set_caption("Duck Trip")
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("data/icon.ico"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                if event.type == pygame.USEREVENT and event.button == self.button_1:
                    if self.id_s == 0:
                        self.reputation += 20
                        running = self.bd()
                    elif self.id_s == 1:
                        self.reputation += 20
                        running = self.bd()
                    elif self.id_s == 2:
                        self.reputation += 20
                        running = self.bd()
                    elif self.id_s == 3:
                        self.reputation += 20
                        running = self.bd()
                    elif self.id_s == 4:
                        self.reputation += 20
                        end = End(self.life, self.reputation)
                        end.run()

                if event.type == pygame.USEREVENT and event.button == self.button_2:
                    if self.id_s == 0:
                        self.life -= 2
                        self.reputation -= 20
                        running = self.bd()
                    elif self.id_s == 1:
                        self.life -= 2
                        self.reputation -= 20
                        running = self.bd()
                    elif self.id_s == 2:
                        self.life -= 1
                        self.reputation -= 20
                        running = self.bd()
                    elif self.id_s == 3:
                        self.reputation -= 20
                        running = self.bd()
                    elif self.id_s == 4:
                        self.reputation -= 20
                        end = End(self.life, self.reputation)
                        end.run()
                        running = False

                self.button_1.handle_event(event)
                self.button_2.handle_event(event)

            self.screen.blit(self.background_image, (0, 0))
            self.button_1.draw_button(self.screen)
            self.button_1.check_hover(pygame.mouse.get_pos())
            self.button_2.draw_button(self.screen)
            self.button_2.check_hover(pygame.mouse.get_pos())
            self.screen.blit(self.text_surface, (204, 110))
            self.screen.blit(self.text_1, (self.x, self.y))
            self.screen.blit(self.text_2, (self.x2, self.y2))
            if self.life == 0:
                end = End(self.life, self.reputation)
                end.run()
                running = False
            pygame.display.update()
            self.clock.tick(FPS)
