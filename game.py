import sys
import pygame
from scripts.utils import load_img
from scripts.entities import Entity
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
      'player': load_img('herochar.png', (50, 50)),
      'grass_top': load_img('grass_top.png', (50, 50)), 
      'stone': load_img('stone.png', (50, 50)),
      'background': load_img('background.png', (1280,720))
    }

    self.player = Entity(self, 'player', (50, 450), (50, 50), 5)
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
      self.player.render(self.display,  self.movement, offset=render_scroll)    

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
        self.player.velocity[1] = -20

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)

Game().run()
