import pygame
import json

NEIGHBOR_OFFSET = [ (-4, -4), (-4, -3), (-4, -2), (-4, -1), (-4, 0), (-4, 1), (-4, 2), (-4, 3), (-4, 4),
                    (-3, -4), (-3, -3), (-3, -2), (-3, -1), (-3, 0), (-3, 1), (-3, 2), (-3, 3), (-3, 4),
                    (-2, -4), (-2, -3), (-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3), (-2, 4),
                    (-1, -4), (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4),
                    (0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                    (1, -4), (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                    (2, -4), (2, -3), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                    (3, -4), (3, -3), (3, -2), (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                    (4, -4), (4, -3), (4, -2), (4, -1), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
PHYSICS_TILES = {'grass', 'stone', 'grass_new', 'dungeon', 'slab'}

class Tilemap:
  def __init__(self, game, size=50):
    """
    Initialize a new instance of the Tilemap class.

    Parameters:
    ----------
    game (Game): The game instance that the tilemap belongs to.
    size (int): The size of each tile in the tilemap.
    tilemap (dict): A dictionary to store the tile data for the tilemap.
    offgrid (dict): A dictionary to store the offgrid tile data.
    """
    
    self.game = game
    self.size = size
    self.tilemap = {}
    self.offgrid = {}
  
  def extract(self, id_pairs, keep=False):
    """
    Extracts tiles from the tilemap and offgrid based on given id pairs.

    Parameters:
    ----------
    id_pairs : list of tuples
        A list of tuples, where each tuple contains the type and variant of a tile.
    keep : bool, optional
        If True, the extracted tiles will be kept in the tilemap and offgrid.
        If False, the extracted tiles will be removed from the tilemap and offgrid.
        Default is False.

    Returns:
    -------
    list of dict
        A list of dictionaries, where each dictionary represents a tile.
        The dictionaries contain the type, variant, and position of the tile.
        If the tile is from the offgrid, the position is in absolute coordinates.
        If the tile is from the tilemap, the position is in tile coordinates.

    """
    matches = []
    for tile in self.offgrid.copy():
      if (tile['type'], tile['variant']) in id_pairs:
        matches.append(tile.copy())
        if not keep:
          self.offgrid.remove(tile)
                  
    for loc in self.tilemap:
      tile = self.tilemap[loc]
      if (tile['type'], tile['variant']) in id_pairs:
        matches.append(tile.copy())
        matches[-1]['pos'] = matches[-1]['pos'].copy()
        matches[-1]['pos'][0] *= self.size
        matches[-1]['pos'][1] *= self.size
        if not keep:
          del self.tilemap[loc]
    return matches

  def save(self, path):
    f = open(path, 'w')
    json.dump({'tilemap': self.tilemap, 'size': self.size, 'offgrid': self.offgrid}, f)
    f.close()

  def load(self, path):
    """
    Save the current state of the tilemap to a JSON file.

    Parameters:
    ----------
    path : str
        The path to the JSON file where the tilemap data will be saved.
    """

    f = open(path, 'r')
    map_data = json.load(f)
    f.close()

    self.tilemap = map_data['tilemap']
    self.size = map_data['size']
    self.offgrid = map_data['offgrid']

  def tiles_around(self, pos):
    """
    Get a list of tiles around a given position.

    Parameters:
    ----------
    pos : tuple of int
        The position (x, y) of the center tile.

    Returns:
    -------
    list of dict
        A list of dictionaries, where each dictionary represents a tile.
        The dictionaries contain the type, variant, and position of the tile.
        The position is in tile coordinates.
    """
    tiles = []
    tile_loc = (int(pos[0] // self.size), int(pos[1] // self.size))
    for offset in NEIGHBOR_OFFSET:
      check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap:
        tiles.append(self.tilemap[check_loc])
    return tiles

  def physics_rects_around(self, pos):
    """
    Get a list of rectangles representing physics tiles around a given position.

    Parameters:
    ----------
    pos : tuple of int
        The position (x, y) of the center tile. The position is in pixel coordinates.

    Returns:
    -------
    list of pygame.Rect
        A list of pygame Rect objects. Each Rect represents a physics tile.
        The Rect's position and size are in pixel coordinates.

    Note:
    -----
    This function uses the `tiles_around` method to get the tiles around the given position.
    It then checks if the tile's type is in the `PHYSICS_TILES` set.
    If the tile is a physics tile, it creates a new pygame Rect object with the tile's position and size.
    The Rect object's position is in pixel coordinates.
    The function returns a list of all the physics tile Rect objects.
    """
    rects = []
    for tile in self.tiles_around(pos):
      if tile['type'] in PHYSICS_TILES:
        rects.append(pygame.Rect(tile['pos'][0] * self.size, tile['pos'][1] * self.size, self.size, self.size))
    return rects

  def solid_check(self, pos):
    """
    Check if a tile at a given position is a solid physics tile.

    Parameters:
    ----------
    pos : tuple of int
        The position (x, y) of the tile to check. The position is in pixel coordinates.

    Returns:
    -------
    dict or None
        If a solid physics tile is found at the given position, the function returns a dictionary
        representing the tile. The dictionary contains the type, variant, and position of the tile.
        If no solid physics tile is found, the function returns None.

    Note:
    -----
    This function uses the tilemap to check if a tile at the given position is a solid physics tile.
    It calculates the tile location based on the given position and the tile size.
    It then checks if the tile location exists in the tilemap and if the tile's type is in the
    PHYSICS_TILES set. If both conditions are met, the function returns the tile dictionary.
    Otherwise, it returns None.
    """
    tile_loc = str(int(pos[0] // self.size)) + ';' + str(int(pos[1] // self.size))
    if tile_loc in self.tilemap:
      if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
        return self.tilemap[tile_loc]

  def render(self, surf, offset = (0, 0)):
    """
    Renders the tilemap onto a surface.

    Parameters:
    ----------
    surf : pygame.Surface
        The surface where the tilemap will be rendered.
    offset : tuple of int, optional
        The offset of the tilemap in pixel coordinates.
        Default is (0, 0).

    Returns:
    -------
    None

    Note:
    -----
    This method renders both offgrid and ongrid tiles onto the given surface.
    Offgrid tiles are rendered first, followed by ongrid tiles.
    The rendering is optimized by only rendering the tiles that are within the visible area.
    The offset parameter is used to adjust the position of the tilemap on the surface.
    """
    # Render offgrid tiles
    for tile in self.offgrid:
        surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
    
    # Render ongrid tiles within the visible range
    for x in range(int(offset[0]//self.size), int((offset[0] + surf.get_width())//self.size +1)):
      for y in range(int(offset[1]//self.size), int((offset[1] + surf.get_height())//self.size +1)):
        loc = str(x) + ';' + str(y)
        if loc in self.tilemap:
          tile = self.tilemap[loc] 
          surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.size - offset[0], tile['pos'][1]*self.size - offset[1]))
