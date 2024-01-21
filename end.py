from level import *
from settings import *


class End:
    def __init__(self, life, reputation):
        pygame.init()
        self.life = life
        self.reputation = reputation
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Конец!")
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("data/icon.ico"))
        self.background_image = pygame.image.load('data/background_end.png')
        self.button_exit = ImageButton(510, 560, 407, 140, "data/button_exit.png", "data/button_exit_f.png")
        self.font = pygame.font.Font(None, 34)
        intro_text = f"Уровень вашей репутации: {self.reputation}"
        self.text_1 = self.font.render(intro_text, False, (0, 0, 0))
        intro_text = f"Количество жизней: {self.life}"
        self.text_2 = self.font.render(intro_text, False, (0, 0, 0))
        if self.reputation > 50:
            self.end = "Хорошая"
            self.end_t = "Все произошедшее было сном"
        elif -1 < self.reputation < 50:
            self.end = "Нейтральная"
            self.end_t = "Вы остались жить в деревне"
        else:
            self.end = "Плохая"
            self.end_t = "Вас отправили работать в город"
        intro_text = f"Концовка: {self.end}"
        self.text_3 = self.font.render(intro_text, False, (0, 0, 0))
        self.text_4 = self.font.render(self.end_t, False, (0, 0, 0))
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

                self.button_exit.handle_event(event)

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.text_1, (520, 280))
            self.screen.blit(self.text_2, (520, 340))
            self.screen.blit(self.text_3, (520, 400))
            self.screen.blit(self.text_4, (520, 458))
            self.button_exit.draw_button(self.screen)
            self.button_exit.check_hover(pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)
