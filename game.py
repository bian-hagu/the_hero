import sys
import json
import json
import pygame


from scripts.utils import *
from scripts.entities import *
from scripts.entities import *
from scripts.tilemap import Tilemap
from scripts.UI import *
FPS = 60

class Game:
  def __init__(self):
    """
    Initializes a NEW GAME object.
  
    """
    pygame.init()
    pygame.display.set_caption("The Hero")
    
    pygame.display.set_icon(pygame.image.load("data/imgs/hub/life.png"))
    
    pygame.display.set_icon(pygame.image.load("data/imgs/hub/life.png"))
    self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    self.clock = pygame.time.Clock()
    self.label = ''
    self.load_game()
    pygame.mixer.music.load('data/sfx/bg_music.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


  def load_level(self, map_id):
    """
    Loads a level from a file.

    Parameters
    ----------
    map_id : int or string
    """
    
    self.assets = { 
      'grass': load_imgs('tiles/grass'), 
      'grass_new': load_imgs('tiles/grass_new'),
      'spawners': load_imgs('tiles/spawners'),
      'dungeon': load_imgs('tiles/dungeon'),
      'cave': load_imgs('tiles/cave'),
      'sign': load_imgs('tiles/sign'),
      'slab': load_imgs('tiles/slab'),
      'objects': load_imgs('objects'),

      'potion': load_img('hub/potion.png', (30,30)),
      'background1': load_img('background/background.png', (1280,720)),
      'background2': load_img('background/bg.png', (1280,720)),
      'hud_health': load_img('hub/hud_health.png', (300, 100)),
      'cooldown': load_img('hub/cooldown.png', (50,15)),
      'coin': load_img('hub/coin.png', (30,30)),

      'spike/idle': Animation(load_imgs('entities/spike/spike_idle'), duration=1),
      'spike/attack': Animation(load_imgs('entities/spike/spike_attack'), duration=6),
      'spike_fall/idle': Animation(load_imgs('entities/spike_fall/spike_fall_idle'), duration=4),
      'spike_fall/attack': Animation(load_imgs('entities/spike_fall/spike_fall_attack'), duration=4),
      
      'waterfall/idle': Animation(load_imgs('entities/waterfall'), duration=8),
      'save/idle': Animation(load_imgs('entities/save/save_idle'), duration=8),
      'save/save': Animation(load_imgs('entities/save/save_saving'), duration=8),
      'coin/idle': Animation(load_imgs('entities/coin/coin_idle', (30,30)), duration=8),
      'coin/pickup': Animation(load_imgs('entities/coin/coin_pickup', (30,30)), duration=8),
      'orb/idle': Animation(load_imgs('entities/orb/orb_idle', (30,30)), duration=8),
      'orb/pickup': Animation(load_imgs('entities/orb/orb_pickup', (30,30)), duration=8),
      'vase/idle': Animation(load_imgs('entities/vase/vase_idle'), duration=4),
      'vase/break': Animation(load_imgs('entities/vase/vase_breaking'), duration=8),

      'player/idle': Animation(load_imgs('entities/hero/hero_idle'), duration=8), 
      'player/hit': Animation(load_imgs('entities/hero/hero_hit'), duration=4),
      'player/run': Animation(load_imgs('entities/hero/hero_run'), duration=6),
      'player/death': Animation(load_imgs('entities/hero/hero_death'), duration=8),
      'player/jump_up': Animation(load_imgs('entities/hero/hero_jump_up'), duration = 3),
      'player/jump_down': Animation(load_imgs('entities/hero/hero_jump_down'), duration = 3),
      'player/jump_double': Animation(load_imgs('entities/hero/hero_jump_double'), duration = 6),
      'player/flash': Animation(load_imgs('entities/hero/hero_dust'), duration=4),
      'player/spawn': Animation(load_imgs('entities/hero/hero_spawn'), duration=4),
      'player/attack': Animation(load_imgs('entities/hero/hero_attack'), duration=4),
      'sword/idle': Animation(load_imgs('entities/hero/hero_sword'), duration=4),

      'bomber/idle': Animation(load_imgs('entities/bomber/bomber_goblin_idle'), duration=8),
      'bomber/hit': Animation(load_imgs('entities/bomber/bomber_goblin_hit'), duration=4),
      'bomber/attack': Animation(load_imgs('entities/bomber/bomber_goblin_attack'), duration=8),
      'bomber/death': Animation(load_imgs('entities/bomber/bomber_goblin_death'), duration=6),
      'bomb/idle': Animation(load_imgs('entities/bomb/bomb_idle'), duration=4),
      'bomb/explode': Animation(load_imgs('entities/bomb/bomb_explode', (100,100)), duration=4),

      'goblin/idle': Animation(load_imgs('entities/goblin/goblin_idle'), duration=4),
      'goblin/run': Animation(load_imgs('entities/goblin/goblin_run'), duration=6),
      'goblin/hit': Animation(load_imgs('entities/goblin/goblin_hit'), duration=4),
      'goblin/attack': Animation(load_imgs('entities/goblin/goblin_attack'), duration=8),
      'goblin/death': Animation(load_imgs('entities/goblin/goblin_death'), duration=4),

      'slime/idle': Animation(load_imgs('entities/slime/slime_idle'), duration=4),
      'slime/run': Animation(load_imgs('entities/slime/slime_run'), duration=4),
      'slime/hit': Animation(load_imgs('entities/slime/slime_hit'), duration=4),
      'slime/death': Animation(load_imgs('entities/slime/slime_death'), duration=8),

      'minotaur/idle': Animation(load_imgs('entities/minotaur/minotaur_idle', (200,200)), duration=8),
      'minotaur/run': Animation(load_imgs('entities/minotaur/minotaur_run', (200,200)), duration=16),
      'minotaur/hit': Animation(load_imgs('entities/minotaur/minotaur_hit', (200,200)), duration=8),
      'minotaur/attack': Animation(load_imgs('entities/minotaur/minotaur_attack4', (200,200)), duration=4),
      'minotaur/death': Animation(load_imgs('entities/minotaur/minotaur_death', (200,200)), duration=62),

      
    }

    self.sfx = {
      'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
      'explosion': pygame.mixer.Sound('data/sfx/explosion.wav'),
      'sword': pygame.mixer.Sound('data/sfx/sword.wav'),
      'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
      'spawn': pygame.mixer.Sound('data/sfx/spawn.mp3'),
      'coin': pygame.mixer.Sound('data/sfx/coin.wav'),
      'end': pygame.mixer.Sound('data/sfx/end.wav'),
      'grass': pygame.mixer.Sound('data/sfx/grass_1.wav'),
    }
    
    self.sfx['jump'].set_volume(0.5)
    self.sfx['explosion'].set_volume(0.05)
    self.sfx['sword'].set_volume(0.2)
    self.sfx['hit'].set_volume(0.5) 
    self.sfx['spawn'].set_volume(0.3)
    self.sfx['coin'].set_volume(0.8)
    self.sfx['end'].set_volume(0.5)
    self.sfx['grass'].set_volume(0.1)

    self.display = pygame.Surface((1280, 720))
    self.player = Player(self, (50, 500))
    self.tilemap = Tilemap(self, size=50)
    self.scroll = [0,0]
    self.movement = [False, False]
    self.map_id = map_id
    self.is_pause = False
    self.is_retry = False
    self.complete_level = False
    self.shop = False
    self.offset = [0, 0]

    try:
      self.tilemap.load('data/maps/map' + str(map_id) + '.json')
      self.tilemap.load('data/maps/map' + str(map_id) + '.json')
    except:
      print('Error loading map')
      pass
    self.enemies = []
    spawners = [('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4), ('spawners', 5), ('spawners', 6), ('spawners', 7), ('spawners', 8)]
    for spawner in self.tilemap.extract(spawners):
      if spawner['variant'] == 0:
        self.player.pos = spawner['pos']
        self.player.air_time = 0
      elif spawner['variant'] == 1:  
        self.enemies.append(Bomber(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 2:  
        self.enemies.append(Goblin(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 3:
        self.enemies.append(Slime(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 4:
        self.enemies.append(SavePoint(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 5: 
        self.enemies.append(Waterfall(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 6:
        self.enemies.append(Spike(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 7:
        self.enemies.append(Spike_fall(self, spawner['pos'], (40,40)))
      elif spawner['variant'] == 8:
        self.enemies.append(Vase(self, spawner['pos'], (50,50)))
      else:
        pass

    for spawner in self.tilemap.extract([('boss',0)]):
      self.enemies.append(Minotaur(self, spawner['pos'], (200,200)))

  def draw_hub(self, offset = (0,0)):
    """ 
    Draw a hub 

    Parameters
    ----------

    """
    FONT36 = pygame.font.Font('data/font/Pixellari.ttf', 36)
    FONT24 = pygame.font.Font('data/font/Pixellari.ttf', 24)

    self.display.blit(self.assets['potion'], (48,35))
    potion_text = FONT24.render(str(self.potions), True, 'white')
    potion_Rect = potion_text.get_rect()
    potion_Rect.center = (62, 83)
    self.display.blit(potion_text, potion_Rect)


    hp_percent = self.player.hp/100
    hp_percent = 0 if hp_percent < 0 else hp_percent
    if hp_percent < 0.25:
      pygame.draw.rect(self.display, 'red', (110, 25, 190*hp_percent, 32), 0, 8)
      pygame.draw.rect(self.display, 'red', (0, 0, self.display.get_width(), self.display.get_height()), 10)
    else:
      pygame.draw.rect(self.display, 'green', (110, 25, 190*hp_percent, 32), 0, 8)
    self.display.blit(self.assets['hud_health'], (10,10))
    

    coin_text = FONT36.render(str(self.coin), True, 'yellow')
    coin_Rect = coin_text.get_rect()
    coin_Rect.topleft = (160, 65)
    self.display.blit(coin_text,coin_Rect)

    mana_percent = (self.player.mana)/100
    cooldown_pos = (self.player.pos[0] - offset[0], self.player.pos[1] - offset[1] - 20)
    pygame.draw.rect(self.display, (150,150,250), (cooldown_pos[0]+ 2, cooldown_pos[1] + 4, 46 * mana_percent, 7), 0, 4)
    self.display.blit(self.assets['cooldown'], cooldown_pos)

    

  def run(self, id_map):
    """ 
    Run the game
    
    Parameters
    ----------
    id_map : int or string

    """    

    self.load_level(id_map)
    self.labels1 = ['RESUME', 'RETRY', 'MAIN MENU', 'QUIT']
    self.labels2 = ['RETRY', 'MAIN MENU', 'QUIT']
    self.labels3 = ['NEXT LEVEL', 'SHOP', 'MAIN MENU', 'QUIT']
    ui = UI(self.screen)

    while True:
      self.label = ''

      if not self.is_pause:
        if self.map_id == 3:
          self.display.fill((0,0,0))
        elif self.map_id == 4:
          self.display.blit(self.assets['background2'], (0,0))
        else:
          self.display.blit(self.assets['background1'], (0,0))

        if self.player.pos[0] > self.display.get_width()/2:
          self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
        self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
        # if self.player.pos[1] < 400:
        #   self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
        # if self.player.pos[1] > 600:
        #   self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])   
        
        self.offset = ((self.scroll[0], (self.scroll[1])))
        self.tilemap.render(self.display, offset=self.offset)

        for enemy in self.enemies.copy(): 
          enemy.update(self.tilemap, (0,0))
          enemy.render(self.display, offset=self.offset)

        self.player.update(tilemap=self.tilemap, movement=(self.movement[1] - self.movement[0], 0))
        self.player.render(self.display, offset=self.offset)          
        self.draw_hub( offset=self.offset)

      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
          pygame.quit() 
          sys.exit()    
          sys.exit()    
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_1:
            pygame.quit()
            sys.exit()
          if event.key == pygame.K_ESCAPE:
            if self.is_pause:
              self.is_pause = False
            else:
              self.is_pause = True

          if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
            self.player.jump()
          if event.key == pygame.K_q or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            self.player.flash()
          if event.key == pygame.K_e or event.key == pygame.K_RETURN:
            self.player.regen()
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = True 
          

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.player.attack(self.enemies, self.display, self.offset)
      
      if self.player.dead <= 0:
        self.is_retry = True
        self.is_pause = True
      
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      if self.is_pause:
        if self.is_retry:
          self.label = ui.retry((320,400), self.labels2)
        elif self.shop:
          self.label = ui.shop((320, 460), self)
        elif self.complete_level:
          self.maps[str(self.map_id+1)] = True
          self.save_game()
          self.label = ui.complete((320, 460), self.labels3)
        else:
          self.label = ui.pause((320, 460), self.labels1)

      if self.complete_level:
        self.is_pause = True
      pygame.display.update()
      self.clock.tick(FPS)

      if self.label == 'QUIT':
        pygame.quit()
        sys.exit()
      elif self.label == 'RESUME':
        self.is_pause = False
      elif self.label == "SHOP":
        self.shop = True
      elif self.label == 'Back':
        self.shop = False
        self.complete_level = True
      elif self.label in ['MAIN MENU', 'RETRY', 'NEXT LEVEL']:
        break
    
    if self.label == 'MAIN MENU':
      self.main_menu()
    elif self.label == 'RETRY':
      self.coin -= self.player.coin
      self.run(self.map_id)
    elif self.label == 'NEXT LEVEL':
      self.run(self.map_id + 1)
     

  def main_menu(self):
    """ 
    Run the main menu
    
    Parameters
    ----------
    """
    text_size = (100, 100)
    self.assets = {
      'background': load_img('background/background.png', (1280, 720)),
      't': load_img('text/t.png', text_size),
      'h': load_img('text/h.png', text_size),
      'e': load_img('text/e.png', text_size),
      'r': load_img('text/r.png', text_size),
      'o': load_img('text/o.png', text_size),
    }
    self.display = pygame.Surface((1280, 720))

    font = pygame.font.Font('data/font/Pixellari.ttf', 128)
    gameName_text = font.render('THE HERO', True, (40,40,40))
    textRect = gameName_text.get_rect()
    textRect.centerx = 1280//2
    textRect.top = 50

    description_font = pygame.font.Font('data/font/Pixellari.ttf', 24)
    description = description_font.render('@Made by Hagu Bian', True, (200,200,200,10))
    descriptionRect = description.get_rect()
    descriptionRect.bottomright = (1250, 720)
    self.labels = ['CONTINUE', 'NEW GAME', 'SELECT LEVEL', 'QUIT']
    ui = UI(self.display)
    while True:
      self.label = ''
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

      self.display.blit(self.assets['background'], (0, 0))
      self.display.blit(description, descriptionRect)
      ui.game_name(self.assets)
      self.label = ui.main_menu(self.labels)

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)

      if self.label == 'QUIT':
        pygame.quit()
        sys.exit()
      elif self.label in self.labels:
        break 
      
    if self.label == 'SELECT LEVEL':    
      self.select_level() 
    elif self.label == 'NEW GAME':
      self.maps = {'1': True, '2': False, '3': False, '4': False, '5': False}
      self.coin = 0
      self.potions = 0
      self.save_game()
      self.run(1)
    elif self.label == 'CONTINUE':
      id = 1
      for map in self.maps:
        if not self.maps[map]:
          id = int(map) -1      
          break
      self.run(id)

  def select_level(self):
    """
    Run the select level menu.
    """
    text_size = (100, 100)
    self.assets = {
      'background': load_img('background/background.png', (1280, 720)),
      't': load_img('text/t.png', text_size),
      'h': load_img('text/h.png', text_size),
      'e': load_img('text/e.png', text_size),
      'r': load_img('text/r.png', text_size),
      'o': load_img('text/o.png', text_size),
      }
    
    self.display = pygame.Surface((1280, 720))
    description_font = pygame.font.Font('data/font/Pixellari.ttf', 24)
    description = description_font.render('@Made by Hagu Bian', False, (200,200,200,10))
    descriptionRect = description.get_rect()
    descriptionRect.bottomright = (1250, 720)
    self.labels = ['Level 1(lock)', 'Level 2(lock)', 'Level 3(lock)', 'Level 4(lock)', 'Level 5(lock)', 'Back']
    for map in self.maps:
      if self.maps[map]:
        self.labels[int(map)-1] = self.labels[int(map)-1].split('(')[0]
    
    ui = UI(self.display)
    while True:
      self.label = ''
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

      self.display.blit(self.assets['background'], (0, 0))
      self.display.blit(description, descriptionRect)
      ui.game_name(self.assets)
      self.label = ui.select_level(self.labels)

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(30)

      if self.label in ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Back']:
        break 

    if self.label == 'Back':
      self.main_menu()
    else:
      self.run(int(self.label.split(' ')[1]))

  def save_game(self):
    """
    Save the game.
    """
    f = open('data/save_game/save.json', 'w')
    save = {
      'maps': self.maps,
      "coin": self.coin,
      "potions": self.potions,
    } 
    json.dump(save, f)
    f.close()
    
  def load_game(self):
    """
    Load the save game.
    """
    try:
      f = open('data/save_game/save.json', 'r')
      save = json.load(f)
      self.maps = save['maps']
      self.coin = save['coin']
      self.potions = save['potions']
      f.close()
    except:
      self.coin = 0
      self.maps = {'1': True, '2': False, '3': False, '4': False, '5': False}
      self.potions = 0

# Game().run(0)