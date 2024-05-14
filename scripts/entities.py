import pygame
import random

GRAVITY = 20
ENEMIES = ['slime', 'goblin', 'bomber', 'vase', 'minotaur']
class Entity:
  """
  A base class for all entities in the game.
  
  Parameters
  ----------
  game (Game): The game instance.
  type (str): The type of the entity.
  pos (tuple): The position of the entity.
  size (tuple): The size of the entity.
  coin (int): The amount of coin the entity gives.
  action (str): The current action of the entity.
  animation (Animation): The current animation of the entity.

  Methods
  ----------
  update(self, tilemap, movement): Updates the entity's state.
  hit(self, dmg): Handles the entity being hit.
  set_action(self, action): Sets the current action of the entity.
  rect(self): Sets the rectangle
  """

  def __init__(self, game, type, pos, size, hp = 100, dmg = 25, speed=1, attack_speed = 60, coin = 0):
    self.game = game
    self.type = type
    self.pos = list(pos)
    self.size = size
    self.velocity = [0,0]
    self.hp = hp
    self.dmg = dmg
    self.speed = speed
    self.coin = coin
    self.attack_speed = attack_speed
    self.collision = {'top': False, 'bottom': False, 'left': False, 'right': False}
    self.animation_offset = (-3,-3)
    self.flip = False
    self.action = ''
    self.set_action('idle')
    self.hitting = 0  
    self.attacking = 0
    self.attack_cd = 0
    self.dead = 30

  def rect(self):
    """
    Returns the rectangular bounding box of the entity.

    Returns:
    ---------
        The rectangular bounding box of the entity as a pygame.Rect object.
    """
    return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

  def set_action(self, action):
    """
    Sets the action of the entity and updates the animation.

    Parameters:
    ----------
    action (str): The new action of the entity.
    """
    if action != self.action:
      self.action = action
      self.animation = self.game.assets[self.type + '/' + self.action].copy()
  
  def update(self, tilemap, movement = (0, 0),):
    """
    Update the position and state of the entity.

    Parameters:
    ----------
    tilemap : Tilemap instance
        The tilemap instance that the entity is moving on.
    movement : tuple of int, optional
        The (x, y) movement vector of the entity, default to (0, 0).
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
    
    if self.hitting > 0:
      self.velocity[0] = 0
    else:
      if movement[0] > 0:
        self.flip = False
      if movement[0] < 0:
        self.flip = True

    # Update velocity -------------------------------------------------------------------------
    self.velocity[1] = min(GRAVITY, self.velocity[1] + 1)
    if self.collision['bottom'] or self.collision['top']:
      self.velocity[1] = 0
    if self.collision['left'] or self.collision['right']:
      self.velocity[0] = 0
    self.animation.update()

  def render(self, surf, offset = (0, 0)):
    """
    Renders the entity to the given surface.

    Parameters:
    -----------
    surf (pygame.Surface): The surface to render the entity to.
    offset (tuple): The offset to apply to the position of the entity when rendering.
    """
    asset = pygame.transform.flip(self.animation.img(), self.flip, False)
    surf.blit(asset, (self.pos[0] - offset[0] + self.animation_offset[0], self.pos[1] - offset[1] + self.animation_offset[1]))
 
  def hit(self, dmg, nock = 0):
    """
    Base class for all entities in the game.

    Parameters:
    ----------
    game : Game
        The game instance.
    type : str
        The type of the entity.
    pos : tuple
        The position of the entity.
    size : tuple
        The size of the entity.
    coin : int
        The amount of coin the entity gives.
    """
    self.game.sfx['hit'].play()
    self.velocity[0] += nock
    self.velocity[1] -= abs(nock/2)
    self.hp -= dmg
    self.hitting = 10

class Player(Entity):
  """
  The player character class.

  Parameters:
  ----------
  game (Game): The game instance.
  pos (tuple): The position of the player.
  size (tuple): The size of the player.
  air_time (int): The time the player has been in the air.
  jumps (int): The number of jumps the player has made.
  doublejumps_cd (int): The cooldown for double jumps.
  flashing (int): The time the player is flashing.
  spawn (int): The time the player is spawning.
  dead (int): The time the player is dead.

  Methods:
  ----------
    update(self, tilemap, enemies, movement): Updates the player.
    jump(self): Makes the player jump.
    flash(self): Makes the player flash.
    attack(self, enemies, surf, offset): Makes the player attack.
  """
  def __init__(self, game, pos):
    super().__init__(game, 'player', pos, (45, 45), 
                     hp=100, dmg=25, speed=5, attack_speed=30)
    self.air_time = 0
    self.jumps = 1
    self.mana = 100
    self.flashing = 0
    self.spawn = 30
    self.dead = 60
    self.potions = 0

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the player entity.

    Parameters:
    tilemap (Tilemap): The tilemap on which the player moves.
    enemies (list): A list of enemy instances.
    movement (tuple): The movement vector of the player.
    """
    self.air_time += 1
    self.attacking -= 1
    self.attack_cd -= 1
    
    if self.collision['bottom']:
      if self.jumps != 2:
        self.jumps += 1
      self.air_time = 0
      self.mana += 1 if self.mana < 100 else 0

    if self.hp <= 0 or self.pos[1] >= 800:
      self.dead -= 1

    if self.spawn > 0:
      self.game.sfx['spawn'].play()
      self.spawn -= 1
      self.set_action('spawn')
    elif self.hp <= 0:
      self.game.sfx['end'].play(0)
      self.set_action('death')
    elif self.air_time > 1 and self.jumps == 0 and self.velocity[1] < 5:
      self.set_action('jump_double')
    elif self.air_time > 1 and self.velocity[1] < 0:
      self.set_action('jump_up')
    elif self.air_time > 10 and self.velocity[1] > 0:
      self.set_action('jump_down')
    elif self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.game.sfx['grass'].play()
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
    if abs(self.flashing) > 0:
      self.velocity[0] = abs(self.flashing) / self.flashing * self.speed + 1 
      if abs(self.flashing) == 1:
        self.velocity[0] *= 0.05
      
    if self.velocity[0] > 0:
      self.velocity[0] = max(self.velocity[0] - 0.1, 0)
    else:
      self.velocity[0] = min(self.velocity[0] + 0.1, 0)    
    super().update(tilemap=tilemap, movement=movement)
  def jump(self):
    if self.jumps == 2:
      self.jumps -= 1
      self.game.sfx['jump'].play()
      self.velocity[1] -= 18
    elif self.jumps == 1 and self.mana >= 75:   
      self.jumps -= 1
      self.velocity[1] -= 15
      self.mana -= 75

  def flash(self):
    """
    Makes the player jump.

    If the player has two jumps left and the double jump cooldown is over,
    the player jumps and reduces the number of jumps by one.
    If the player has one jump left and the double jump cooldown is over,
    the player jumps and reduces the number of jumps by one.
    """
    if not self.flashing and self.mana >= 60:
      self.mana -= 60
      if self.flip:
        self.flashing = -10
      else:
        self.flashing = 10

  def regen(self):
    if self.game.potions > 0:
      self.game.sfx['coin'].play()
      self.game.potions -= 1
      self.hp += 30
      if self.hp < 100:
        self.hp = self.hp
      else:
        self.hp = 100

  def attack(self, enemies, surf, offset):
    """
    Makes the player attack enemies.

    Parameters
    ----------
    enemies : list
        A list of enemy instances.
    surf : pygame.Surface
        The surface on which the player attacks.
    offset : tuple
        The offset of the surface.
    """
    if self.attack_cd < 0:
      self.attack_cd = self.attack_speed
      if self.attacking <= -1:
        self.attacking = 10
        self.game.sfx['sword'].play()

        if self.flip:
          sw = Sword(self.game, (self.pos[0] - self.size[0], self.pos[1]), self.size)
          sw.flip = True
        else:
          sw = Sword(self.game, (self.pos[0] + self.size[0], self.pos[1]), self.size)

        sw_rect = pygame.Rect(sw.pos[0], sw.pos[1], sw.size[0], sw.size[1])
        sw.render(surf, offset)

        for enemy in enemies:
          if enemy.type in ENEMIES:
            e_rect=enemy.rect()
            if sw_rect.colliderect(e_rect):
              enemy.hit(self.dmg, 10 if self.pos[0] < enemy.pos[0] else -10)

class Sword(Entity):
  """
  A class representing a sword entity.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the sword.
  size : tuple
      The size of the sword.
  coin : int
      The coin value of the sword. Default is 0.

  Methods:
  --------
  __init__(self, game, pos, size, coin=0)
      Initializes the sword entity.
  """

  def __init__(self, game, pos, size):
    super().__init__(game,'sword', pos, size, 0)

class Bomber(Entity):
  """
  A class representing a bomber enemy.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the bomber.
  size : tuple
      The size of the bomber.
  speed : int
      The speed of the bomber. Default is 5.

  Methods:
  --------
  __init__(self, game, pos, size, speed=5)
      Initializes the bomber enemy.
  update(self, tilemap, movement=(0, 0))
      Updates the bomber enemy.
  attack(self, player)
      Makes the bomber enemy attack the player.
  """
  def __init__(self, game, pos, size, speed = 5):
    super().__init__(game, 'bomber', pos, size, 50, speed, attack_speed=120, coin = 100)  
    self.walking = 0
    self.attack_cd = self.attack_speed

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the bomber enemy.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the bomber enemy moves.
    movement : tuple
        The movement vector of the bomber enemy.
    """
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
        if tilemap.solid_check((self.rect().centerx + (-24 if self.flip else 24), self.pos[1] + self.size[1])):
          if (self.collision['right'] or self.collision['left']):
            self.flip = not self.flip
          else:
            movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
        else:
          self.flip = not self.flip
        self.walking = max(0, self.walking -1)
      elif random.random() < 0.01:
        self.walking = random.randint(30, 120)
      
    if self.hp <= 0:
      if self.dead == 30:
        self.game.enemies.append(Coin(self.game, self.pos, (30, 30), self.coin))
      self.dead -= 1
      if self.dead <= 0:
        self.game.enemies.remove(self)

    super().update(tilemap, movement)

    if self.hp <= 0:
      self.set_action('death')
    elif self.hitting > 0:
      self.set_action('hit')
    else: 
      self.set_action('idle')

  def attack(self, player):
    """
    Makes the bomber enemy attack the player.

    Parameters:
    -----------
    player : Player
        The player instance to attack.

    Side Effects:
    -------------
    - Appends a Bomb instance to the game's enemies list.
    - Resets the attack cooldown and attacking Parameters.
    """
    if self.attack_cd < 0:
      bomb = Bomb(self.game, self.pos, player.pos)
      self.game.enemies.append(bomb)
      self.attack_cd = self.attack_speed
      if self.attacking <= -1:
        self.attacking = 10

class Bomb(Entity):
  """
  A class representing a bomb entity.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the bomb.
  size : tuple
      The size of the bomb.
  d_pos : tuple
      The destination position of the bomb.
  coin : int
      The coin value of the bomb. Default is 1.

  Methods:
  --------
  __init__(self, game, pos, d_pos)
      Initializes the bomb entity.
  update(self, tilemap, movement)
      Updates the bomb entity.
  """
  def __init__(self, game, pos, d_pos):
    """
    Initializes the bomb entity.

    Parameters:
    -----------
    game : Game
        The game instance.
    pos : tuple
        The position of the bomb.
    d_pos : tuple
        The destination position of the bomb.
    """
    super().__init__(game, 'bomb', pos, (50,50), 1, 30)  
    self.des_pos = d_pos
    self.flying = False
    self.exploding = 10

  def update(self, tilemap, movement = (0,0)):
    """
    Updates the bomb entity.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the bomb entity moves.
    movement : tuple
        The movement vector of the bomb entity.
    """
    if not self.flying:
      self.velocity = [(self.des_pos[0] - self.pos[0])/self.size[0], -15]
      self.flying = True

    if self.collision['bottom']:
      self.explode()

    super().update(tilemap, movement)

    if self.exploding <= 0:
      self.set_action('explode')
    else:
      self.set_action('idle')

  def explode(self):
    """
    Explodes the bomb entity.
    """
    pos = self.pos
    self.velocity = [0, 0]
    self.exploding -=1
    if self.exploding == 0:
      self.size = (100,100)
      self.pos[0] = pos[0] + self.size[0]
    elif self.exploding  == -5:
      self.game.sfx['explosion'].play()
      rect = self.rect()
      player = self.game.player
      if rect.colliderect(player.rect()):
        player.velocity[1] = -10
        player.hit(self.dmg)
    elif self.exploding <= -10:

      self.game.enemies.remove(self)

class Goblin(Entity):
  """
  A class representing a goblin enemy.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the goblin.
  size : tuple
      The size of the goblin.
  speed : int
      The speed of the goblin. Default is 3.
  coin : int
      The coin value of the goblin. Default is 75.

  Methods:
  --------
  __init__(self, game, pos, size, speed=3)
      Initializes the goblin enemy.
  update(self, tilemap, movement=(0, 0))
      Updates the goblin enemy.
  attack(self, player)
      Makes the goblin enemy attack the player.
  """

  def __init__(self, game, pos, size):
    super().__init__(game, 'goblin', pos, size, 150, dmg=15, speed=3, coin = 75)  
    self.walking = 0

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the goblin enemy.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the goblin enemy moves.
    movement : tuple
        The movement vector of the goblin enemy.
    """
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
        if tilemap.solid_check((self.rect().centerx + (-24 if self.flip else 24), self.pos[1] + self.size[1])):
          if (self.collision['right'] or self.collision['left']):
            self.flip = not self.flip
          else:
            movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
        else:
          self.flip = not self.flip
        self.walking = max(0, self.walking -1)
      elif random.random() < 0.01:
        self.walking = random.randint(30, 120)
        
    if self.hp <= 0:
      if self.dead == 30:
        self.game.enemies.append(Coin(self.game, self.pos, (30, 30), self.coin))
      self.dead -= 1
      if self.dead <= 0:
        self.game.enemies.remove(self)

    super().update(tilemap, movement)

    if self.hp <= 0:
      self.set_action('death')
    elif self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    elif self.attacking > 0:
      self.set_action('attack')
    else: 
      self.set_action('idle')
    
  def attack(self, player):
    """
    Makes the goblin enemy attack the player.

    Parameters:
    -----------
    player : Player
        The player instance to attack.
    """
    if self.attack_cd < 0:
      self.attack_cd = self.attack_speed
      self.velocity = [0,0]

      rect = pygame.Rect(self.pos[0] - self.size[0]/2, self.pos[1] , self.size[0] * 2, self.size[1])
      p_rect = player.rect()
      if rect.colliderect(p_rect):
        self.velocity = [0,0]
        self.attacking = 10
        player.hit(self.dmg, 2 if self.pos[0] < player.pos[0] else -2)

class Slime(Entity):
  """
  A class representing a slime enemy.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the slime.
  size : tuple
      The size of the slime.
  speed : int
      The speed of the slime. Default is 3.
  coin : int
      The coin value of the slime. Default is 20.

  Methods:
  --------
  __init__(self, game, pos, size, speed=3)
      Initializes the slime enemy.
  update(self, tilemap, movement=(0, 0))
      Updates the slime enemy.
  """
  def __init__(self, game, pos, size):
    """
    Initializes the slime enemy.

    Parameters:
    -----------
    game : Game
        The game instance.
    pos : tuple
        The position of the slime.
    size : tuple
        The size of the slime.
    speed : int
        The speed of the slime. Default is 3.
    """
    
    super().__init__(game=game,
                     type='slime', 
                     pos=pos, 
                     size=size, 
                     hp = 100, 
                     dmg = 3, 
                     speed=8,
                     attack_speed=0,
                     coin = 20)

    self.walking = 0
    self.flip = True
    self.e_coin = None

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the slime enemy.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the slime enemy moves.
    movement : tuple
        The movement vector of the slime enemy.
    """
    self.attack_cd -= 1
    player = self.game.player
    self.attack(player)
    if self.rect().colliderect(player.rect()):
      self.walking = 0

    if self.walking:
      if tilemap.solid_check((self.rect().centerx + (-24 if self.flip else 24), self.pos[1] + self.size[1])):
        if (self.collision['right'] or self.collision['left']):
          self.flip = not self.flip
        else:
          movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
      else:
        self.flip = not self.flip
      self.walking = max(0, self.walking -1)
    elif random.random() < 0.01:
      self.walking = random.randint(20, 60)
        
    if self.hp <= 0:
      if self.dead == 30:
        self.game.enemies.append(Coin(self.game, self.pos, (30, 30), self.coin))
      self.dead -= 1
      if self.dead <= 0:
        self.game.enemies.remove(self)

    super().update(tilemap, movement)

    if self.hp <= 0:
      self.set_action('death')
    elif self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    else: 
      self.set_action('idle')

  def attack(self, player):
    if self.attack_cd <= 0:
      p_rect = player.rect() 
      if p_rect.colliderect(self.rect()):
        self.attack_cd = 15
        self.velocity = [0,0]
        player.hit(self.dmg, 8 if self.pos[0] < player.pos[0] else -8)

class SavePoint(Entity):
  """
  A class representing a save point entity.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the save point.
  size : tuple
      The size of the save point.
  time : int
      The time counter for the save point animation.

  Methods:
  --------
  __init__(self, game, pos, size)
      Initializes the save point entity.
  update(self, tilemap, movement)
      Updates the save point entity.
  """
  def __init__(self, game, pos, size):
    """
    Initializes the save point entity.

    Parameters:
    -----------
    game : Game
        The game instance.
    pos : tuple
        The position of the save point.
    size : tuple
        The size of the save point.
    """
    super().__init__(game, 'save', pos, size, 1)
    self.time = 0

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the save point entity.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the save point entity moves.
    movement : tuple
        The movement vector of the save point entity.

    Side Effects:
    -------------
    - Changes the save point's animation state.
    - Adds the save point's coin value to the player's coin count when the player collides with it.
    """
    if self.time <= 0:
      self.time += 1
    elif self.time >= 10:
      self.time -= 1
    p_rect = self.game.player.rect()
    if p_rect.colliderect(self.rect()):
      self.set_action('save')
      self.game.coin += 100
      self.game.sfx['spawn'].play()
      self.game.complete_level = True
    
    super().update(tilemap, movement)
  
class Coin(Entity):
  """
  A class representing a coin entity.

  Parameters:
  -----------
  game : Game
      The game instance.
  pos : tuple
      The position of the coin.
  size : tuple
      The size of the coin.
  coin : int
      The coin value of the coin.

  Methods:
  --------
  __init__(self, game, pos, size, coin)
      Initializes the coin entity.
  update(self, tilemap, movement)
      Updates the coin entity.
  """
  def __init__(self, game, pos, size, coin):

    super().__init__(game, 'coin', pos, size, coin=coin)
    self.pickup = 10
    if random.randint(1, 10) <= 4: # 40% change of spawning Orb
      self.game.enemies.append(Orb(game=self.game, 
                               pos=(self.pos[0] + 10, self.pos[1]),
                               size=self.size,
                               hp=random.randint(1, 30)))
    if random.randint(1, 100) <= 10: # 10% chance add potion
      self.game.potions += 1

  def update(self, tilemap, movement=(0, 0)):
    p_rect = self.game.player.rect()
    if p_rect.colliderect(self.rect()):
      self.pickup -= 1
      self.set_action('pickup')
      if self.pickup <= 0:
        self.game.coin += self.coin
        self.game.player.coin += self.coin
        self.game.sfx['coin'].play()
        self.game.enemies.remove(self)
    super().update(tilemap, movement=movement)

class Orb(Entity):
  def __init__(self, game, pos, size, hp):
    super().__init__(game, type='orb', pos=pos, size=size, hp=hp)
    self.pickup = 10

  def update(self, tilemap, movement=(0, 0)):
    p_rect = self.game.player.rect()
    if p_rect.colliderect(self.rect()):
      self.pickup -= 1
      self.set_action('pickup')
      if self.pickup <= 0:
        hp_loss = 100 - self.game.player.hp
        self.game.player.hp += self.hp if hp_loss > self.hp else hp_loss 
        self.game.sfx['coin'].play()
        self.game.enemies.remove(self)
    super().update(tilemap, movement=movement)

class Waterfall(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game=game, type='waterfall', pos=pos, size=size)

  def update(self, tilemap, movement=(0, 0)):
    self.animation.update()

class Spike(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, type='spike', pos=pos, size=size, dmg=20, attack_speed=120)

  def update(self, tilemap, movement=(0, 0)):
    """
    Updates the spike trap entity.

    Parameters:
    -----------
    tilemap : Tilemap
        The tilemap on which the spike trap entity moves.
    movement : tuple, optional
        The movement vector of the spike trap entity. Default is (0, 0).

    Side Effects:
    -------------
    - Updates the attack cooldown and attacking counters.
    - Checks if the player is within the spike trap's range.
    - Calls the attack method if the player is within range.
    - Updates the animation of the spike trap.
    - Sets the action of the spike trap based on the attacking counter.
    """
    self.attack_cd -= 1
    self.attacking -= 1
    player = self.game.player
    if self.pos[0] + self.size[0] >= player.pos[0]\
      and self.pos[0] - self.size[0] <= player.pos[0]:
      self.attack(player)
    self.animation.update()
    if self.attacking > 0:
      self.set_action('attack')
    else:
      self.set_action('idle')

  def attack(self, player):
    """
    Makes the spike trap attack the player.

    Parameters:
    -----------
    player : Player
        The player instance to attack.
    """
    if self.attack_cd <= 0:
      self.attacking = 60
      rect = self.rect()
      p_rect = player.rect()
      if rect.colliderect(p_rect):
        self.attack_cd = self.attack_speed
        player.hit(self.dmg)

class Spike_fall(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, type='spike_fall', pos=pos, size=size, dmg=15, attack_speed=120)
    self.falling = False

  def update(self, tilemap, movement=(0, 0)):

    self.attack_cd -= 1
    self.attacking -= 1
    player = self.game.player
    self.fall(player)

    if self.pos[0] + 75 >= player.pos[0]\
      and self.pos[0] - 75 <= player.pos[0]:
      self.falling = True
      self.set_action('attack')
    if self.falling:
      super().update(tilemap, movement)


  def fall(self, player):
    if self.falling:
      # rect = pygame.Rect(self.pos[0] - self.size[0]/2, self.pos[1] , self.size[0] * 2, self.size[1])
      rect = self.rect()
      p_rect = player.rect()
      if rect.colliderect(p_rect):
        self.velocity = [0,0]
        player.hit(self.dmg, 0)
        self.game.enemies.remove(self)
      elif self.collision['bottom']:
        self.game.enemies.remove(self)

class Minotaur(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, type='minotaur', pos=pos, size=size, 
                     hp=1000, dmg=20, attack_speed=180, speed=3,
                     coin=100)
    self.walking = 0
    
  def update(self, tilemap, movement=(0, 0)):
    player = self.game.player
    self.attack(player)
    self.attack_cd -= 1
    self.attacking -= 1

    if self.pos[1] + (self.size[1] - player.size[1]== player.pos[1] ):
      if self.pos[0] < player.pos[0] :
        self.flipped = True
        movement = (movement[0] - 0.5 if movement[0] > 0 else 0.5, movement[1])
      elif self.pos[0] - self.size[0] > player.pos[0]:
        self.flipped = False
        movement = (movement[0] + 0.5 if movement[0] < 0 else -0.5, movement[1])
      else:
        movement = (0,0)
      
    if self.attacking < 0:
      if self.walking:
        if tilemap.solid_check((self.rect().centerx + (-24 if self.flip else 24), self.pos[1] + self.size[1])):
          if (self.collision['right'] or self.collision['left']):
            self.flip = not self.flip
          else:
            movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
        else:
          self.flip = not self.flip
        self.walking = max(0, self.walking -1)
      elif random.random() < 0.01:
        self.walking = random.randint(30, 120)
        
    if self.hp <= 0:
      if self.dead == 120:
        self.game.enemies.append(Coin(self.game, self.pos, (30, 30), self.coin))
      self.dead -= 1
      if self.dead <= 0:
        self.game.enemies.remove(self)

    super().update(tilemap, movement)

    if self.hp <= 0:
      self.set_action('death')
    elif self.hitting > 0:
      self.set_action('hit')
    elif movement[0] != 0:
      self.set_action('run')
    elif self.attacking > 0:
      self.set_action('attack')
    else: 
      self.set_action('idle')

  def attack(self, player):
    """
    Makes the goblin enemy attack the player.

    Parameters:
    -----------
    player : Player
        The player instance to attack.
    """
    if self.attack_cd < 0:
      self.attack_cd = self.attack_speed
      self.velocity = [0,0]

      rect = pygame.Rect(self.pos[0] - self.size[0]/2, self.pos[1] , self.size[0] * 2, self.size[1])
      p_rect = player.rect()
      if rect.colliderect(p_rect):
        self.attacking = 30
    if self.attacking == 10:
      player.hit(self.dmg, 20 if self.pos[0] < player.pos[0] else -20)

  def render(self, surf, offset):
    super().render(surf, offset)
    hp_percent = (self.hp)/1000
    hp_size = (500, 20)
    hp_pos = ((surf.get_width() - hp_size[0])/2, 30)
    pygame.draw.rect(surf, (40,40,40), (hp_pos[0]-2, hp_pos[1]-2, hp_size[0]+4, hp_size[1]+4), 0, 10)
    pygame.draw.rect(surf, 'red', (hp_pos[0], hp_pos[1], hp_size[0]*hp_percent, hp_size[1]), 0, 10)

class Vase(Entity):
  def __init__(self, game, pos, size):
    super().__init__(game, type='vase', pos=pos, size=size)
    self.breaking = 0

  def update(self, tilemap, movement=(0, 0)):
    self.breaking += -1 if self.breaking > 0 else 0
    if self.hitting == 10:
      self.breaking = 30

    if self.breaking  ==  20:
      if random.randint(1,10) <= 4: # 40% chance get poision
        self.game.potions += 2 if random.randint(1,10) <= 2 else 1
      if random.randint(1,10) <= 6: # 40% chance of spawning coin
        self.game.enemies.append(Coin(self.game, self.pos, (30,30), random.randint(10, 50)))
    
    if self.breaking == 1:
      self.game.enemies.remove(self)
  
    super().update(tilemap, movement)
    
    if self.breaking > 0:
      self.set_action('break')
    else:
      self.set_action('idle')
