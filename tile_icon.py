from settings import *
from story import Story


class TileIcon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), id=-1):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.id = id
        self.rect = self.image.get_rect(topleft=pos)

    def level(self):
        return self.id

    def input(self):
        keys = pygame.key.get_pressed()

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