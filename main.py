import sqlite3
import sys
from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Duck Trip")
        pygame.display.set_icon(pygame.image.load("data/icon.ico"))
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        # Создание фона
        self.background_image = pygame.image.load('data/background.png')
        self.button_play = ImageButton(478, 320, 407, 140, "data/button_play.png", "data/button_play_f.png",
                                       "data/click.mp3")
        self.button_exit = ImageButton(478, 460, 407, 140, "data/button_exit.png", "data/button_exit_f.png",
                                       "data/click.mp3")
        # Подключение к БД и создание курсора
        self.connection = sqlite3.connect("bd_app")
        self.cursor = self.connection.cursor()
        # Выполнение запроса и создание записи в БД
        self.cursor.execute("INSERT INTO user(count, life) VALUES(?, ?)", (0, 5))
        self.connection.commit()
        # Выполнение запроса и поиск записи в БД
        result = self.cursor.execute("SELECT id FROM user WHERE count = ? AND life = ?",
                                     (0, 5)).fetchall()[0]
        id_user = result[0]
        self.level = Level(id_user)
        # Музыка
        pygame.mixer.init()
        pygame.mixer.music.load("data/muz.mp3")
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == self.button_exit:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == self.button_play:
                    self.level.run()

                self.button_play.handle_event(event)
                self.button_exit.handle_event(event)

            # Отрисовка фона
            self.screen.blit(self.background_image, (0, 0))
            # Отрисовка кнопок и проверка для реакции на мышь
            self.button_play.draw_button(self.screen)
            self.button_play.check_hover(pygame.mouse.get_pos())
            self.button_exit.draw_button(self.screen)
            self.button_exit.check_hover(pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
