import sqlite3
import sys
from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Duck Trip")
        pygame.display.set_icon(pygame.image.load("icon.ico"))
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('background.png')
        # Создание фона
        self.button_play = ImageButton(478, 320, 407, 140, "button_play.png", "button_play_f.png", "click.mp3")
        self.button_exit = ImageButton(478, 460, 407, 140, "button_exit.png", "button_exit_f.png", "click.mp3")
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

            self.screen.blit(self.background_image, (0, 0))
            self.button_play.draw_button(self.screen)
            self.button_play.check_hover(pygame.mouse.get_pos())
            self.button_exit.draw_button(self.screen)
            self.button_exit.check_hover(pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
