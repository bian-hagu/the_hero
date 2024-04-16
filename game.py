import sys
import pygame
from scripts.utils import *
from scripts.entities import Entity, Player
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
      'grass_top': load_img('tiles/grass_top.png'), 
      'stone': load_img('tiles/stone.png'),
      'background': load_img('background/background.png', (1280,720)),
      'player/idle': Animation(load_imgs('entities/hero/hero_idle'), duration=4), 
      'player/jump_up': Animation(load_imgs('entities/hero/hero_jump_up'), duration = 3),
      'player/jump_down': Animation(load_imgs('entities/hero/hero_jump_down'), duration = 3),
      'player/run' : Animation(load_imgs('entities/hero/hero_run'), duration= 6)
    }

    self.player = Player(self, (50, 450), (50, 50))
    self.tilemap = Tilemap(self, size=50)
    self.scroll = [0,0]

  def run(self):  
    while True:
      self.display.blit(self.assets['background'], (0,0))
      if self.player.pos[0] > self.display.get_width()/2:
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
      self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
      
      render_scroll = ((self.scroll[0], (self.scroll[1])))    
      self.tilemap.render(self.display, offset=render_scroll)
      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, offset=render_scroll)    
      if self.player.pos[1] > 1000:
        print("Game over")
        pygame.quit()
        sys.exit()
      keys = pygame.key.get_pressed()
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
          pygame.quit() 
          sys.exit()  
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = True 
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = False
      if keys[pygame.K_SPACE] and self.player.collision['bottom']:
        self.player.velocity[1] = -20 #height of jump = 4 blocks

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)


Game().run()
