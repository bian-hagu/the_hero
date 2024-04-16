import pygame
GRAVITY = 10
class Entity:
  def __init__(self, game, type, pos, size, speed=5):
    self.game = game
    self.type = type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0,0]
    self.speed = speed
    self.collision = {'top': False, 'bottom': False, 'left': False, 'right': False}

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def update(self, tilemap, movement = (0, 0)):
    self.collision = {'top': False, 'bottom': False, 'left': False, 'right': False}
    movement = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
    
    # Update entity position x ----------------------------------------------------------------
    self.pos[0] += movement[0] * self.speed
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if movement[0] >= 0:
          entity_rect.right = rect.left
          self.collision['right'] = True
        if movement[0] < 0:
          entity_rect.left = rect.right
          self.collision['left'] = True
        self.pos[0] = entity_rect.x


    # Update entity position y ----------------------------------------------------------------
    self.pos[1] += movement[1]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if movement[1] >= 0:
          entity_rect.bottom = rect.top
          self.collision['bottom'] = True
        else:
          entity_rect.top = rect.bottom
          self.collision['top'] = True      
      self.pos[1] = entity_rect.y

    # Update velocity -------------------------------------------------------------------------
    self.velocity[1] = min(GRAVITY, self.velocity[1] +1)
    if self.collision['bottom'] or self.collision['top']:
      self.velocity[1] = 0



  def render(self, surf, direct, offset = (0, 0)):
    asset = self.game.assets['player']
    if direct[0] :
       asset = pygame.transform.flip(asset, True, False)
    surf.blit(asset, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    # pygame.draw.rect(surf, (255, 0, 0), self.rect(), 1)
