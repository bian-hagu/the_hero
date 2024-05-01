import pygame
import random

GRAVITY = 10
class Entity:
  def __init__(self, game, type, pos, size, hp = 100, speed=5):
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
    self.animation_offset = (-3,-3)
    self.flip = False
    self.action = ''
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
  
  def update(self, tilemap, movement = (0, 0),):
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
    movement = [self.velocity[0] + movement[0], self.velocity[1] + movement[1]]
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
    self.doublejumps_cd = 0
    self.flashing = 0
    self.spawn = 30
    self.attack_cd = 0

  def update(self, tilemap, movement=(0, 0)):
    super().update(tilemap=tilemap, movement=movement)

    self.air_time += 1
    self.attack_cd -= 1

    if self.collision['bottom']:
      if self.jumps <2:
        self.jumps += 1
      self.air_time = 0
      self.doublejumps_cd -=1
    if self.spawn > 0:
      self.spawn -= 1
      self.set_action('spawn')
    elif self.air_time > 1 and self.jumps == 0 and self.velocity[1] < 5:
      self.set_action('jump_double')
    elif self.air_time > 1 and self.velocity[1] < 0:
      self.set_action('jump_up')
    elif self.air_time > 10 and self.velocity[1] > 0:
      self.set_action('jump_down')
    elif movement[0] != 0:
      self.set_action('run')
    elif self.flashing != 0 and self.velocity[0] != 0:
      self.set_action('flash')
    elif self.attack_cd >= 0:
      self.set_action('attack')
    else:
      self.set_action('idle')

    if self.flashing > 0:
      self.flashing = max(0, self.flashing - 1)
    if self.flashing < 0:
      self.flashing = min(0, self.flashing + 1)
    if abs(self.flashing) > 50:
      self.velocity[0] = abs(self.flashing) / self.flashing * 8
      if abs(self.flashing) == 51:
        self.velocity[0] *= 0.1
      
    if self.velocity[0] > 0:
      self.velocity[0] = max(self.velocity[0] - 0.1, 0)
    else:
      self.velocity[0] = min(self.velocity[0] + 0.1, 0)

      
        

  def jump(self):
    if self.jumps == 2:
      self.velocity[1] -= 15
      self.jumps -= 1
    elif self.jumps == 1 and self.doublejumps_cd <= 0:   
      self.velocity[1] -= 15
      self.jumps -= 1
      self.doublejumps_cd = 60

  def flash(self):
    if not self.flashing:
      if self.flip:
        self.flashing = -60
      else:
        self.flashing = 60

  def attack(self, enemies, surf, offset):
    if self.attack_cd <= -1:
      self.attack_cd = 10
      e_rects = []
      for enemy in enemies:
        e_rects.append(enemy.rect())

      if self.flip:
        sw = Sword(self.game, (self.pos[0] - self.size[0], self.pos[1]), self.size)
        sw.flip = True
      else:
        sw = Sword(self.game, (self.pos[0] + self.size[0], self.pos[1]), self.size)
      sw_rect = pygame.Rect(sw.pos[0], sw.pos[1], sw.size[0], sw.size[1])
      for rect in e_rects:
        if sw_rect.colliderect(rect):
          print('hit')

      sw.render(surf, offset)



class Sword(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game,'sword', pos, size, 0)

class Enemy(Entity):
  def __init__(self, game, enemy_type, pos, size, speed = 5):
    super().__init__(game, enemy_type, pos, size, speed)  

    self.walking = 0

  def update(self, tilemap, movement=(0, 0)):
    if self.walking:
      if tilemap.solid_check((self.rect().centerx + (-24 if self.flip else 24), self.pos[1] + 50)):
        if (self.collision['right'] or self.collision['left']):
          self.flip = not self.flip
        else:
          movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
      else:
        self.flip = not self.flip
      self.walking = max(0, self.walking -1)
    elif random.random() < 0.01:
      self.walking = random.randint(30, 120)

    super().update(tilemap, movement)
    
    if movement[0] != 0:
      self.set_action('run')
    else: 
      self.set_action('idle')

  def render(self, surf, offset = (0,0)):
    super().render(surf, offset=offset)
