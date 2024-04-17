from scripts.entities import Entity

class Goblin(Entity):
    def __init__(self, game, pos, size, speed=5):
        super().__init__(game, 'goblin', pos, size, speed)
        self.health = 100
        self.defense = 50
        self.attack_damage = 10
        self.is_facing_right = True

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)


        if self.is_facing_right:
            if self.rect.right + self.speed > tilemap.width:
                self.is_facing_right = False
        else:
            if self.rect.left - self.speed < 0:
                self.is_facing_right = True


        if self.collision['bottom'] and self.game.player.rect.colliderect(self.rect):
            self.game.player.take_damage(self.attack_damage - self.game.player.defense)

    def render(self, surf, direct, offset=(0, 0)):
        asset = self.game.assets['goblin']
        if not self.is_facing_right:
            asset = pygame.transform.flip(asset, True, False)
        surf.blit(asset, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

goblin = Goblin(game, (300, 450), (50, 50))
game.add_entity(goblin)

