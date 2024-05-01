import sys
import pygame
from scripts.utils import *
from scripts.entities import Entity, Player, Enemy
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
      'player/idle': Animation(load_imgs('entities/hero/hero_idle'), duration=4), 
      'player/jump_up': Animation(load_imgs('entities/hero/hero_jump_up'), duration = 3),
      'player/jump_down': Animation(load_imgs('entities/hero/hero_jump_down'), duration = 3),
      'player/run' : Animation(load_imgs('entities/hero/hero_run'), duration= 6),
      'player/jump_double': Animation(load_imgs('entities/hero/hero_jump_double'), duration = 6),
      'player/flash': Animation(load_imgs('entities/hero/hero_dust'), duration=4),
      'player/spawn': Animation(load_imgs('entities/hero/hero_spawn'), duration=8),
      'player/attack': Animation(load_imgs('entities/hero/hero_attack'), duration=4),
      'sword/idle': Animation(load_imgs('entities/hero/hero_sword'), duration=4),
      'rabit/idle': Animation(load_imgs('entities/rabit/rabit_idle'), duration=4),
      'rabit/run': Animation(load_imgs('entities/rabit/rabit_walk'), duration=6),
    }

    self.player = Player(self, (50, 500), (50, 50))
    self.tilemap = Tilemap(self, size=50)
    self.load_level(0)

  def load_level(self, map_id):
    try:
      self.tilemap.load('data/maps/map' + str(map_id) + '.json')
    except:
      print('Error loading map')
      pass

    self.enemies = []
    for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 6)]):
      if spawner['variant'] == 0:
        self.player.pos = spawner['pos']
        self.player.air_time = 0
      elif spawner['variant'] == 6: 
        self.enemies.append(Enemy(self, 'rabit',spawner['pos'], (50,50), 10))
      else:
        print('unkown enemy')
    
    self.scroll = [0,0]
    self.particles = []

    
  def run(self):    
    while True:
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
        enemy.update(self.tilemap, (0,0))
        enemy.render(self.display, offset=render_scroll)

      self.player.update(tilemap=self.tilemap, movement=(self.movement[1] - self.movement[0], 0))
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

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)


Game().run()