from settings import *


class TileIcon(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), id=-1):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.id = id
        self.rect = self.image.get_rect(topleft=pos)

    def level(self):
        return self.id
