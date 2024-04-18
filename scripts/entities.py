import pygame
GRAVITY = 10
class Entity:
  def __init__(self, game, type, pos, size, speed=5):
    """
    Initialize a new Entity instance.

    Parameters
    ----------
    game : Game instance
      The game instance that the entity belongs to.
    type : str
      The type of the entity, used to look up its assets.
    pos : tuple of int
      The (x, y) position of the entity.
    size : tuple of int
      The (width, height) size of the entity.
    speed : int, optional
      The movement speed of the entity, default to 5.

    Returns
    -------
    None

    """
    self.game = game
    self.type = type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0,0]
    self.speed = speed
    self.collision = {'top': False, 'bottom': False, 'left': False, 'right': False}
    
    self.action = ''
    self.animation_offset = (-3,-3)
    self.flip = False
    self.set_action('idle')



  def rect(self):
    """
    Returns the rectangular bounding box of the entity.

    Returns
    -------
    pygame.Rect
      The rectangular bounding box of the entity.
    """
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def set_action(self, action):
    """Set the current action of the entity.

    Parameters
    ----------
    action (str): The name of the action to set.

    Returns
    -------
      None
    """
    if action != self.action:
      self.action = action
      self.animation = self.game.assets[self.type + '/' + self.action].copy()
  
  def update(self, tilemap, movement = (0, 0)):
    """
    Update the position and state of the entity.

    Parameters
    ----------
    tilemap : Tilemap instance
        The tilemap instance that the entity is moving on.
    movement : tuple of int, optional
        The (x, y) movement vector of the entity, default to (0, 0).

    Returns
    -------
    None
    """
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
    
    # Update animation ---------------------------------------------------------------------
    if movement[0] > 0:
      self.flip = False
    if movement[0] < 0:
      self.flip = True

    # Update velocity -------------------------------------------------------------------------
    self.velocity[1] = min(GRAVITY, self.velocity[1] +1)
    if self.collision['bottom'] or self.collision['top']:
      self.velocity[1] = 0
    self.animation.update()



  def render(self, surf, offset = (0, 0)):
    asset = pygame.transform.flip(self.animation.img(), self.flip, False)
    surf.blit(asset, (self.pos[0] - offset[0] + self.animation_offset[0], self.pos[1] - offset[1] + self.animation_offset[1] ))












class Player(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, 'player', pos, size, 5)
    self.air_time = 0
    self.jumps = 1
    self.doublejumps_cooldown = 0

  def update(self, tilemap, movement=(0, 0)):
    super().update(tilemap, movement)
    
    self.air_time += 1

    if self.collision['bottom']:
      if self.jumps <2:
        self.jumps += 1
      self.air_time = 0
      self.doublejumps_cooldown -=1

    if self.air_time > 1 and self.jumps == 0 and self.velocity[1] < 5:
      self.set_action('jump_double')
    elif self.air_time > 1 and self.velocity[1] < 0:
      self.set_action('jump_up')
    elif self.air_time > 10 and self.velocity[1] > 0:
      self.set_action('jump_down')
    elif movement[0] != 0:
      self.set_action('run')
    else:
      self.set_action('idle')
  def jump(self):
    if self.jumps == 2:
      self.velocity[1] -= 15
      self.jumps -= 1
    elif self.jumps == 1 and self.doublejumps_cooldown <= 0:   
      self.velocity[1] -= 15
      self.jumps -= 1
      self.doublejumps_cooldown = 60



