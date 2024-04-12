import pygame

class Entity:
  def __init__(self, game, type, pos, size, speed=5):
    self.game = game
    self.type = type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0,0]
    self.speed = speed

  def rect(self):
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def update(self, tilemap, movement = (0, 0)):
    collision = {'top': False, 'bottom': False, 'left': False, 'right': False}
    
    movement = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
    
    # Update entity position x ----------------------------------------------------------------
    self.pos[0] += movement[0] * self.speed
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if movement[0] >= 0:
          entity_rect.right = rect.left
          collision['right'] = True
        if movement[0] < 0:
          entity_rect.left = rect.right
          collision['left'] = True
        self.pos[0] = entity_rect.x


    # Update entity position y ----------------------------------------------------------------
    self.pos[1] += movement[1]
    entity_rect = self.rect()
    for rect in tilemap.physics_rects_around(self.pos):
      if entity_rect.colliderect(rect):
        if movement[1] >= 0:
          entity_rect.bottom = rect.top
          collision['bottom'] = True
        else:
          entity_rect.top = rect.bottom
          collision['top'] = True      
      self.pos[1] = entity_rect.y

    # Update velocity -------------------------------------------------------------------------
    self.velocity[1] = min(5, self.velocity[1] +1)
    if collision['bottom'] or collision['top']:
      self.velocity[1] = 0



  def render(self, surf):
    surf.blit(self.game.assets['player'], self.pos)
    pygame.draw.rect(surf, (255, 0, 0), self.rect(), 1)
