import pygame 

BASE_IMG_PATH = 'asset/img/'

def load_img(path, size):
  return pygame.transform.scale(pygame.image.load(BASE_IMG_PATH + path), size)
