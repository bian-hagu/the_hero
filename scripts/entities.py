import pygame
import random

GRAVITY = 10

class Entity:
  def __init__(self, game, type, pos, size, hp = 100, dmg = 25, speed=1,attack_speed = 60):
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
    self.hp = hp
    self.dmg = dmg
    self.speed = speed
    self.attack_speed = attack_speed
    self.collision = {'top': False, 'bottom': False, 'left': False, 'right': False}
    self.animation_offset = (-3,-3)
    self.flip = False
    self.action = ''
    self.set_action('idle')
    self.hitting = 0  
    self.attacking = 0
    self.attack_cd = 0




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
    self.hitting += -1 if self.hitting > 0 else 0

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

  def hit(self, dmg):
    self.pos[0] += -30 if not self.flip else 30
    self.hp -= dmg
    self.hitting = 10

class Player(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, 'player', pos, size, 100, 25, 5)
    self.air_time = 0
    self.jumps = 1
    self.doublejumps_cd = 0
    self.flashing = 0
    self.spawn = 30

  def update(self, tilemap, enemies, movement=(0, 0)):
    super().update(tilemap=tilemap, movement=movement)
    self.air_time += 1
    self.attacking -= 1
    self.attack_cd -= 1
    
    c_rect = self.rect()
    for enemy in enemies:
      if enemy.type == 'slime':
        e_rect= enemy.rect()
        if c_rect.colliderect(e_rect):
          self.hitting = 10
          self.hit(enemy.dmg)

    if self.collision['bottom']:
      if self.jumps <2:
        self.jumps += 1
      self.air_time = 0
      self.doublejumps_cd  -= 1 if self.doublejumps_cd > 0 else 0

    if self.spawn > 0:
      self.spawn -= 1
      self.set_action('spawn')
    # elif self.hp <= 0:
    #   self.set_action('death')
    #   self.game.over -= 1
    elif self.air_time > 1 and self.jumps == 0 and self.velocity[1] < 5:
      self.set_action('jump_double')
    elif self.air_time > 1 and self.velocity[1] < 0:
      self.set_action('jump_up')
    elif self.air_time > 10 and self.velocity[1] > 0:
      self.set_action('jump_down')
    elif self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    elif self.flashing != 0 and self.velocity[0] != 0:
      self.set_action('flash')
    elif self.attacking >= 0:
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
    if self.attack_cd < 0:
      self.attack_cd = self.attack_speed
      if self.attacking <= -1:
        self.attacking = 10

        if self.flip:
          sw = Sword(self.game, (self.pos[0] - self.size[0], self.pos[1]), self.size)
          sw.flip = True
        else:
          sw = Sword(self.game, (self.pos[0] + self.size[0], self.pos[1]), self.size)

        sw_rect = pygame.Rect(sw.pos[0], sw.pos[1], sw.size[0], sw.size[1])
        sw.render(surf, offset)

        for enemy in enemies:
          e_rect=enemy.rect()
          if sw_rect.colliderect(e_rect):
            enemy.hit(self.dmg)

class Sword(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game,'sword', pos, size, 0)

class Bomber(Entity):
  def __init__(self, game, pos, size, speed = 5):
    super().__init__(game, 'bomber', pos, size, 50, speed, attack_speed=120)  
    self.walking = 0

  def update(self, tilemap, movement=(0, 0)):
    player = self.game.player
    self.attack(player)
    self.attack_cd -= 1
    self.attacking -= 1

    if self.pos[0] < player.pos[0]:
      self.flip = False
    elif self.pos[0] > player.pos[0]:
      self.flip = True

    if self.attacking < 0:
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

    if self.hitting > 0:
      self.set_action('hit')
    elif self.attacking >= 0:
      self.set_action('attack')
    else: 
      self.set_action('idle')

  def attack(self, player):
    if self.attack_cd < 0:
      bomb = Bomb(self.game, self.pos, player.pos)
      self.game.enemies.append(bomb)
      self.attack_cd = self.attack_speed
      if self.attacking <= -1:
        self.attacking = 10

class Bomb(Entity):
  def __init__(self, game, pos, d_pos):
    super().__init__(game, 'bomb', pos, (50,50), 1, 30)  
    self.des_pos = d_pos
    self.flying = False
    self.exploding = 30

  def update(self, tilemap, movement = (0,0)):
    if not self.flying:
      self.velocity = [(self.des_pos[0] - self.pos[0])/self.size[0],-15]
      self.flying = True

    if self.collision['bottom']:
      self.explode()

    super().update(tilemap, movement)

    if self.exploding <= 0:
      self.set_action('explode')
    else:
      self.set_action('idle')

  def explode(self):
    pos = self.pos
    self.velocity = [0, 0]
    self.exploding -=1
    if self.exploding == 0:
      self.size = (100,100)
      self.pos[0] = pos[0] + self.size[0]
    elif self.exploding  == -5:
      rect = self.rect()
      player = self.game.player
      if rect.colliderect(player.rect()):
        player.velocity[1] = -10
        player.hit(self.dmg)
    elif self.exploding <= -10:
      self.game.enemies.remove(self)

class Goblin(Entity):
  def __init__(self, game, pos, size, speed = 3):
    super().__init__(game, 'goblin', pos, size, 150, 20, speed)  

    self.walking = 0

  def update(self, tilemap, movement=(0, 0)):
    player = self.game.player
    self.attack(player)
    self.attack_cd -= 1
    self.attacking -= 1

    if self.pos[1] == player.pos[1]:
      if self.pos[0]+ self.size[0] < player.pos[0] :
        self.flipped = True
        movement = (movement[0] - 0.5 if movement[0] > 0 else 0.5, movement[1])
      elif self.pos[0] - self.size[0] > player.pos[0]:
        self.flipped = False
        movement = (movement[0] + 0.5 if movement[0] < 0 else -0.5, movement[1])
      else:
        movement = (0,0)

      
    if self.attacking < 0:
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

    if self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    elif self.attacking >= 0:
      self.set_action('attack')
    else: 
      self.set_action('idle')
    
  def attack(self, player):
    if self.attack_cd < 0:
      self.attack_cd = self.attack_speed
      self.velocity = [0,0]

      rect = pygame.Rect(self.pos[0] - self.size[0]/2, self.pos[1] , self.size[0] * 2, self.size[1])
      p_rect = player.rect()
      if rect.colliderect(p_rect):
        self.velocity = [0,0]
        self.attacking = 10
        player.hit(self.dmg)

class Slime(Entity):
  def __init__(self, game, pos, size, speed = 3):
    super().__init__(game, 'slime', pos, size, 100, 10, speed)  ,

    self.walking = 0
    self.flip = True

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
      self.velocity[1] = 20

    elif random.random() < 0.01:
      self.walking = random.randint(30, 120)
    super().update(tilemap, movement)


    if self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    else: 
      self.set_action('idle')