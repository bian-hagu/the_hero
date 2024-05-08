import sys
import pygame
from scripts.utils import *
from scripts.entities import *
from scripts.tilemap import Tilemap
from scripts.UI import *
class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("The Hero")
    
    pygame.display.set_icon(pygame.image.load("data/imgs/hub/life.png"))
    self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    self.clock = pygame.time.Clock()
    self.label = ''

  def load_level(self, map_id):
    self.assets = {
      'grass': load_imgs('tiles/grass'), 
      'grass_new': load_imgs('tiles/grass_new'),
      'spawners': load_imgs('tiles/spawners'),
      'life': load_img('hub/life.png'),
      'background': load_img('background/background.png', (1280,720)),
      'background1': load_img('background/bg.png', (1280,720)),
      'hud_health': load_img('hub/hud_health.png', (300, 100)),
      'cooldown': load_img('hub/cooldown.png', (50,15)),

      'player/idle': Animation(load_imgs('entities/hero/hero_idle'), duration=8), 
      'player/hit': Animation(load_imgs('entities/hero/hero_hit'), duration=4),
      'player/run': Animation(load_imgs('entities/hero/hero_run'), duration= 6),
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
      'slime/death': Animation(load_imgs('entities/slime/slime_death'), duration=4),

    }
    
    self.display = pygame.Surface((1280, 720))
    self.player = Player(self, (50, 500), (50, 50))
    self.tilemap = Tilemap(self, size=50)
    self.scroll = [0,0]
    self.movement = [False, False]
    
    self.is_pause = False

    try:
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
      elif spawner['variant'] == 2:  
        self.enemies.append(Bomber(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 3:  
        self.enemies.append(Goblin(self, spawner['pos'], (50,50)))
        self.enemies.append(Slime(self, spawner['pos'], (50,50)))
      else: 
        print('unkown enemy')
  
  def draw_hub(self, offset = (0,0)):
    self.display.blit(self.assets['life'], (37,35))
    hp_percent = self.player.hp/100
    hp_percent = 0 if hp_percent < 0 else hp_percent
    if hp_percent < 0.25:
      pygame.draw.rect(self.display, 'red', (110, 25, 190*hp_percent, 32), 0, 8)
    else:
      pygame.draw.rect(self.display, 'green', (110, 25, 190*hp_percent, 32), 0, 8)
    self.display.blit(self.assets['hud_health'], (10,10))
   
    dj_percent = (60 - self.player.doublejumps_cd)/60
    cooldown_pos = (self.player.pos[0] - offset[0], self.player.pos[1] - offset[1] - 20)
    pygame.draw.rect(self.display, 'white', (cooldown_pos[0]+ 2, cooldown_pos[1] + 4, 46 * dj_percent, 7), 0, 4)
    self.display.blit(self.assets['cooldown'], cooldown_pos)

  def run(self, id_map):    
    self.load_level(id_map)
    self.labels = ['RESUME', 'MAIN MENU', 'QUIT']
    ui = UI(self.screen)

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
          if event.key == pygame.K_1:
            if self.is_pause:
              self.is_pause = False
            else:
              self.is_pause = True

          if event.key == pygame.K_SPACE:
            self.player.jump()
          if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            self.player.flash()
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
            self.player.attack(self.enemies, self.display, render_scroll)
      
      if not self.is_pause:
        self.display.blit(self.assets['background'], (0,0))

        if self.player.pos[0] > self.display.get_width()/2:
          self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
        if self.player.pos[1] < 300:
          self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
        if self.player.pos[1] > 600:
          self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])   
        
        render_scroll = ((self.scroll[0], (self.scroll[1])))
        self.tilemap.render(self.display, offset=render_scroll)

        for enemy in self.enemies.copy(): 
          if enemy.hp <= 0:
            self.enemies.remove(enemy)
          enemy.update(self.tilemap, (0,0))
          enemy.render(self.display, offset=render_scroll)

        self.player.update(tilemap=self.tilemap, enemies=self.enemies, movement=(self.movement[1] - self.movement[0], 0))
        self.player.render(self.display, offset=render_scroll)          
        self.draw_hub( offset=render_scroll)
      
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      if self.is_pause:
        self.label = ui.pause((300, 400), self.labels)

      pygame.display.update()
      self.clock.tick(60)

      if self.label == 'QUIT':
        pygame.quit()
        sys.exit()
      elif self.label == 'RESUME':
        self.is_pause = False
      elif self.label == 'MAIN MENU':
        break

    self.main_menu()

  def main_menu(self):
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
      self.run(0)

  def select_level(self):
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
    self.labels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Back']
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

      if self.label in self.labels:
        break 

    if self.label == 'Back':
      self.main_menu()
    elif self.label == 'Level 1':
      self.run(0)
    elif self.label == 'Level 2':
      self.run(0)
    elif self.label == 'Level 3':
      self.run(0)
    elif self.label == 'Level 4':
      self.run(0)
    elif self.label == 'Level 5':
      self.run(0)

if __name__ == '__main__':
  game = Game()
  # game.run(0)
  game.select_level()
