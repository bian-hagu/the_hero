import pygame 
import os
BASE_IMG_PATH = 'data/imgs/'
DEFFAULT_SIZE = (50,50)
def load_img(path, size=DEFFAULT_SIZE):
  imgs =pygame.image.load(BASE_IMG_PATH + path).convert()
  img = pygame.transform.scale(imgs, size)
  img.set_colorkey((0,0,0))
  return img


def load_imgs(path, size=DEFFAULT_SIZE):
  imgs = []
  for imgname in sorted(os.listdir(BASE_IMG_PATH + path)):
    imgs.append(load_img(path + '/' + imgname, size))
  return imgs

class Animation:
  def __init__(self, img, duration, loop=True):
    self.imgs = img
    self.loop = loop
    self.duration = duration
    self.done = False
    self.frame = 0

  def copy(self):
    return Animation(self.imgs, self.duration, self.loop)

  def update(self):
    if self.loop:
      self.frame  = (self.frame + 1) % (self.duration * len(self.imgs))
    else:
      maxframe = self.duration * len(self.imgs) -1
      self.frame = min(self.frame + 1, maxframe)
      if self.frame >= maxframe:
        self.done = True

  def img(self):
    return self.imgs[int(self.frame / self.duration)]
  

  