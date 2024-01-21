import sqlite3
from settings import *
from story import Story


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, id):
        super().__init__(groups)
        self.image = pygame.image.load('data/user.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.obstacle_sprites = obstacle_sprites
        self.life = 5
        self.reputation = 0
        # Подключение к БД и создание курсора
        self.connection = sqlite3.connect("bd_app")
        self.cursor = self.connection.cursor()
        result = self.cursor.execute("SELECT * FROM user WHERE id = ?",
                                     (id,)).fetchall()[0]
        self.id = result[0]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.image = pygame.image.load('data/user2.png').convert_alpha()
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.image = pygame.image.load('data/user3.png').convert_alpha()
        else:
            self.direction.y = 0
            self.image = pygame.image.load('data/user.png').convert_alpha()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.image = pygame.image.load('data/user2.png').convert_alpha()
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.image = pygame.image.load('data/user3.png').convert_alpha()
        else:
            self.direction.x = 0
            self.image = pygame.image.load('data/user.png').convert_alpha()

        if keys[pygame.K_e]:
            story = Story(0, self.id)
            story.run()

        if keys[pygame.K_r]:
            story = Story(1, self.id)
            story.run()

        if keys[pygame.K_f]:
            story = Story(2, self.id)
            story.run()

        if keys[pygame.K_g]:
            story = Story(3, self.id)
            story.run()

        if keys[pygame.K_q]:
            story = Story(4, self.id)
            story.run()

    def change_player(self, life, reputation):
        self.life = life
        self.reputation = reputation

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:  # право
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # лево
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:  # вниз
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # вверх
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
