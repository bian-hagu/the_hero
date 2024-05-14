import sys
import pygame
from scripts.utils import load_imgs
from scripts.tilemap import Tilemap
class Editor:
  def __init__(self):
    """
    Initialize the Editor class.

    Parameters:
    ----------
    screen: The main display surface.
    display: The surface used for rendering.
    clock: The clock object for managing the game's frame rate.
    assets: A dictionary containing the tile images.
    movement: A list to store the movement states (left, right, up, down).
    tilemap: The Tilemap object for managing the game's tilemap.
    scroll: A list to store the scrolling position.
    tile_list: A list of tile types.
    tile_group: The index of the current tile group.
    tile_variant: The index of the current tile variant.
    shift: A boolean indicating whether the shift key is pressed.
    clicking: A boolean indicating whether the left mouse button is clicked.
    right_clicking: A boolean indicating whether the right mouse button is clicked.
    ongrid: A boolean indicating whether the tiles are placed on a grid.
    map: The current map ID.

    Methods:
    ----------
    load_level: Load a level from a JSON file.
    """
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
      'grass_new': load_imgs('tiles/grass_new'),
      'spawners': load_imgs('tiles/spawners'),   
      'boss': load_imgs('tiles/boss', (200,200)), 
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
    self.ongrid = True
    self.map = '4'

    self.load_level(self.map) # replce 0 to n map

  def load_level(self, map_id):
    """
    Load a level from a JSON wq wqfile.

    Parameters:
    ----------
    map_id: The ID of the map to load.
    """
    try:
      self.tilemap.load('data/maps/map' + str(map_id) + '.json')
    except:
      print('Error loading map')
      pass

  def run(self): 
    """
    Run the editor.
    """
    while True:
      self.tilemap.save(f'data/maps/map{self.map}.json')
      self.display.fill('black')
      self.scroll = (self.scroll[0] + (self.movement[1] - self.movement[0]), self.scroll[1] + (self.movement[3]-self.movement[2]))
      render_scroll = (int(self.scroll[0]*50), int(self.scroll[1])*50)

      self.tilemap.render(self.display, offset=render_scroll)

      current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant]
      current_tile_img.set_alpha(100)
      mpos = pygame.mouse.get_pos()
      tilepos = ((int(mpos[0]) // self.tilemap.size), (int(mpos[1]) // self.tilemap.size))
      
      # Render the current tile at mouse position
      if self.ongrid:
        self.display.blit(current_tile_img, (tilepos[0] * self.tilemap.size, tilepos[1] * self.tilemap.size))
      else: 
        self.display.blit(current_tile_img, (tilepos[0] * self.tilemap.size, tilepos[1] * self.tilemap.size))

      if self.clicking and self.ongrid:
        self.tilemap.tilemap[str(tilepos[0]+ render_scroll[0]//self.tilemap.size) + ';' + str(tilepos[1]+render_scroll[1]//self.tilemap.size)] = {
          'type': self.tile_list[self.tile_group], 
          'variant': self.tile_variant, 
          'pos': (tilepos[0] + render_scroll[0]//self.tilemap.size, tilepos[1] + render_scroll[1]//self.tilemap.size)}
        
      if self.right_clicking:
        tile_loc = str(str(tilepos[0]+ render_scroll[0]//self.tilemap.size) + ';' + str(tilepos[1]+render_scroll[1]//self.tilemap.size))
        if tile_loc in self.tilemap.tilemap:
          del self.tilemap.tilemap[tile_loc]
        for tile in self.tilemap.offgrid:
          tile_img = self.assets[tile['type']][tile['variant']]
          tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0]*self.tilemap.size, tile['pos'][1] - self.scroll[1]*self.tilemap.size, tile_img.get_width(), tile_img.get_height())
          pos = [tilepos[0]*50, tilepos[1]*50]
          if tile_r.collidepoint(pos):
            self.tilemap.offgrid.remove(tile)


      # Render current tile in left-top corner 
      self.display.blit(current_tile_img, (5,5))

      # Game events processing
      keys = pygame.key.get_pressed()
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
          pygame.quit() 
          sys.exit()  
        
        # Mouse down events processing
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.clicking = True
            if not self.ongrid:
              self.tilemap.offgrid.append({
                'type': self.tile_list[self.tile_group], 
                'variant': self.tile_variant, 
                'pos': (tilepos[0] * self.tilemap.size+render_scroll[0], tilepos[1] * self.tilemap.size + render_scroll[1])
              })
                
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

        # Mouse up events proce ssing
        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.clicking = False
          if event.button == 3:
            self.right_clicking = False

        # Keyboard down events processing
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
          if event.key == pygame.K_LSHIFT:
            self.shift = True
          if event.key == pygame.K_RETURN:  
            self.tilemap.save(f'data/maps/map{self.map}.json')
          if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.movement[2] = True
          if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.movement[3] = True 
          if event.key == pygame.K_g:
            self.ongrid = not self.ongrid
            print('ongrid:', self.ongrid)
          
        # Keyboard up events processing
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

      self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
      pygame.display.update()
      self.clock.tick(60)
      
Editor().run()