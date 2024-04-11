import pygame

NEIGHBOR_OFFSET = [(-50, -50), (-50, 0), (-50, 50),
                   (0, -50), (0, 0), (0, 50),
                   (50, -50), (50, 0), (50, 50)]
PHYSICS_TILES = {'grass_top', 'stone'}


class Tilemap:
  def __init__(self, game, size=50):
    self.game = game
    self.size = size
    self.tilemap = {}
    self.offgrid = []

    for i in range(10):
      self.tilemap[str(i+1) + ';10'] = {'type': 'grass_top', 'pos': (1 + i, 10)}
      self.tilemap['5;' + str(i+1)] = {'type': 'stone', 'pos': (5, 1 + i)}

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

  def render(self, surf):
    for tile in self.offgrid:
      surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

    for loc in self.tilemap:
      tile = self.tilemap[loc]
      surf.blit(self.game.assets[tile['type']], (tile['pos'][0]*self.size, tile['pos'][1]*self.size))
