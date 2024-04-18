import pygame
import json

NEIGHBOR_OFFSET = [ (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2),
                    (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                    (0, -2), (0, -1), (0, 0), (0, 1), (0, 2),
                    (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                    (2, -2), (2, -1), (2, 0),  (2, 1), (2, 2),
                    (3, -2), (3, -1), (3, 0), (3, 1), (3, 2)]
PHYSICS_TILES = {'grass', 'stone'}


class Tilemap:
  def __init__(self, game, size=50):
    """
    Initializes a new Tilemap object.

    Parameters
    ----------
      game (Game): The game instance this tilemap belongs to.
      size (int, optional): The size of each tile in pixels. Defaults to 50.
    """
    self.game = game
    self.size = size
    self.tilemap = {}
    self.offgrid = []

    # for i in range(50):
    #   self.tilemap[str(i+1) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (1 + i, 10)}

  def save(self, path):
    f = open(path, 'w')
    json.dump({'tilemap': self.tilemap, 'size': self.size, 'offgrid': self.offgrid}, f)
    f.close()

  def load(self, path):
    f = open(path, 'r')
    map_data = json.load(f)
    f.close()
    self.tilemap = map_data['tilemap']
    self.size = map_data['size']
    self.offgrid = map_data['offgrid']



  def tiles_around(self, pos):
    tiles = []
    tile_loc = (int(pos[0] // self.size), int(pos[1] // self.size))
    for offset in NEIGHBOR_OFFSET:
      check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap:
        tiles.append(self.tilemap[check_loc])
    return tiles

  def physics_rects_around(self, pos):
    rects = []
    for tile in self.tiles_around(pos):
      if tile['type'] in PHYSICS_TILES:
        rects.append(pygame.Rect(tile['pos'][0] * self.size, tile['pos'][1] * self.size, self.size, self.size))
    return rects

  def render(self, surf, offset = (0, 0)):
    for x in range(int(offset[0]//self.size), int((offset[0] + surf.get_width())//self.size +1)):
      for y in range(int(offset[1]//self.size), int((offset[1] + surf.get_height())//self.size +1)):
        loc = str(x) + ';' + str(y)
        if loc in self.tilemap:
          tile = self.tilemap[loc] 
          surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.size - offset[0], tile['pos'][1]*self.size - offset[1]))

