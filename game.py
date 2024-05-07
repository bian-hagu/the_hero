import sys
import pygame
from scripts.utils import *
from scripts.entities import *
from scripts.tilemap import Tilemap
class Game:
  def __init__(self):
    pygame.init()

    pygame.display.set_caption("The Hero")
    self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    self.display = pygame.Surface((1280, 720))

    self.clock = pygame.time.Clock()
    self.movement = [False, False]
    self.assets = {
      'grass': load_imgs('tiles/grass'), 
      'grass_new': load_imgs('tiles/grass_new'),
      'spawners': load_imgs('tiles/spawners'),
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
    self.player = Player(self, (50, 500), (50, 50))
    self.over = 4
    self.tilemap = Tilemap(self, size=50)
    self.load_level(0)

  def load_level(self, map_id):
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
      elif spawner['variant'] == 1:  
        self.enemies.append(Enemy(self, 'blue_fly', spawner['pos'], (50,50)))
      elif spawner['variant'] == 2:  
        self.enemies.append(Bomber(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 3:  
        self.enemies.append(Goblin(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 4:  
        self.enemies.append(Enemy(self, 'mushroom', spawner['pos'], (50,50)))
      elif spawner['variant'] == 5:  
        self.enemies.append(Enemy(self, 'orange_fly', spawner['pos'], (50,50)))
      elif spawner['variant'] == 6:  
        self.enemies.append(Enemy(self, 'rabit',spawner['pos'], (50,50)))
      elif spawner['variant'] == 7:  
        self.enemies.append(Slime(self, spawner['pos'], (50,50)))
      elif spawner['variant'] == 8:  
        self.enemies.append(Enemy(self, 'worm',spawner['pos'], (50,50)))
      else: 
        print('unkown enemy')
    self.scroll = [0,0]
    self.particles = []

  def draw_hub(self, surf, offset = (0,0)):
    hp_percent = self.player.hp/100
    dj_precent = (60 - self.player.doublejumps_cd)/60

    if hp_percent < 0.25:
      pygame.draw.rect(surf, 'red', (110, 25, 190*hp_percent, 32), 0, 8)
    else:
      pygame.draw.rect(surf, 'green', (110, 25, 190*hp_percent, 32), 0, 8)
    surf.blit(self.assets['hud_health'], (10,10))
    
    cooldown_pos = (self.player.pos[0] - offset[0], self.player.pos[1] - offset[1] - 20)
    pygame.draw.rect(surf, 'white', (cooldown_pos[0]+ 2, cooldown_pos[1] + 4, 46 * dj_precent, 7), 0, 4)
    surf.blit(self.assets['cooldown'], cooldown_pos)


  def run(self):    
    while True:
      # if self.over <= 0 or self.player.pos[1] > 1000:
      #   print('Game over')
      #   pygame.quit()
      #   sys.exit() 
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
      

      for particle in self.particles.copy():
        kill = particle.update()
        particle.render(self.display, offset=render_scroll)
        if kill:
          self.particles.remove(particle)

      keys = pygame.key.get_pressed()
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
          pygame.quit() 
          sys.exit()    
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
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

      self.draw_hub(self.display, offset=render_scroll)
      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)


Game().run()