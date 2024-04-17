import sys
import pygame
from scripts.utils import load_imgs
from scripts.tilemap import Tilemap
RENDER_SCALE =1.0
class Editor:
  def __init__(self):
    pygame.init()

    pygame.display.set_caption("editor")
    self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    self.display = pygame.Surface((1280, 720))

    self.clock = pygame.time.Clock()


    self.assets = {
      'grass': load_imgs('tiles/grass'),
      'cave': load_imgs('tiles/cave'),
      'dungeon': load_imgs('tiles/dungeon'),
      'sign': load_imgs('tiles/sign'),
      'slab': load_imgs('tiles/slab'),
      'objects': load_imgs('objects'),
      'tiles': load_imgs('tile'),
    }
    self.movement = [False, False, False, False]

    self.tilemap = Tilemap(self, size=50)

    self.scroll = [0,0]

    self.tile_list = list(self.assets)
    self.tile_group = 0
    self.tile_variant = 0
    self.shift = False
    self.clicking = False
    self.right_clicking = False


    try:
      self.tilemap.load('map.json')
    except:

      # raise FileNotFoundError('Map file not found')
      pass




  def run(self):  
    while True:
      self.display.fill('black')
      
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      self.tilemap.render(self.display, offset=render_scroll)




      current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
      current_tile_img.set_alpha(100)
      mpos = pygame.mouse.get_pos()
      mpos = (mpos[0]/RENDER_SCALE, mpos[1]/RENDER_SCALE)
      tilepos = ((int(mpos[0] + self.scroll[0]) // self.tilemap.size), (int(mpos[1] + self.scroll[1]) // self.tilemap.size))

      self.display.blit(current_tile_img, (tilepos[0] * self.tilemap.size, tilepos[1] * self.tilemap.size))

      if self.clicking:
        self.tilemap.tilemap[str(tilepos[0]) + ';' + str(tilepos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tilepos}
      if self.right_clicking:
        tile_loc = str(tilepos[0]) + ';' + str(tilepos[1])
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]
        for tile in self.tilemap.offgrid.copy():
          tile_img = self.assets[tile['type']][tile['variant']]
          tile_r = pygame.rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
          if tile_r.collidepoint(mpos):
            self.tilemap.offgrid.remove(tile)
            





      self.display.blit(current_tile_img, (5,5))

      keys = pygame.key.get_pressed()
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
          pygame.quit() 
          sys.exit()  

        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.clicking = True
          if event.button == 3:
            self.right_clicking = True
          if self.shift:
            if event.button == 4:
              self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
            if event.button == 5:
              self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
          else:
            if event.button == 4:
              self.tile_group = (self.tile_group - 1) % len(self.tile_list)
            if event.button == 5:
              self.tile_group = (self.tile_group + 1) % len(self.tile_list)
        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.clicking = False
          if event.button == 3:
            self.right_clicking = False


        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
          if event.key == pygame.K_LSHIFT:
            self.shift = True
          if event.key == pygame.K_RETURN:  
            self.tilemap.save('map.json')
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.movement[2] = True
          if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.movement[3] = True 
          

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LSHIFT:
            self.shift = False
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = False
          if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.movement[2] = False
          if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.movement[3] = False


      if keys[pygame.K_SPACE] and self.player.collision['bottom']:
        self.player.velocity[1] = -20 #height of jump = 4 blocks

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)


Editor().run()
