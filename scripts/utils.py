import pygame 
import os
BASE_IMG_PATH = 'data/imgs/'
DEFFAULT_SIZE = (50,50)

def load_img(path, size=DEFFAULT_SIZE):
  """
  Load and resize an image from the specified path, and set the colorkey to black.

  Parameters:
  ----------
  path (str): The relative path to the image file within the BASE_IMG_PATH directory.
  size (tuple, optional): The desired size of the image. Defaults to DEFFAULT_SIZE.

  Returns:
  ----------
  pygame.Surface: The loaded and resized image with the colorkey set to black.
  """
  imgs =pygame.image.load(BASE_IMG_PATH + path).convert()
  img = pygame.transform.scale(imgs, size)
  img.set_colorkey((0,0,0))
  return img


def load_imgs(path, size=DEFFAULT_SIZE):
  """
  Load and resize multiple images from the specified path, and set the colorkey to black.
  The images are sorted alphabetically before loading.

  Parameters:
  ----------
  path (str): The relative path to the directory containing the image files within the BASE_IMG_PATH directory.
  size (tuple, optional): The desired size of the images. Defaults to DEFFAULT_SIZE.

  Returns:
  ----------
  list: A list of pygame.Surface objects representing the loaded and resized images with the colorkey set to black.
  """
  imgs = []
  for imgname in sorted(os.listdir(BASE_IMG_PATH + path)):
    imgs.append(load_img(path + '/' + imgname, size))
  return imgs

class Animation:
  def __init__(self, img, duration, loop=True):
    """
    Initialize an Animation object.

    Parameters:
    ----------
    img : list
        A list of pygame.Surface objects representing the animation frames.
    duration : int
        The number of frames to display each image for.
    loop : bool, optional
        Whether the animation should loop continuously. Defaults to True.
    """
    self.imgs = img
    self.loop = loop
    self.duration = duration
    self.done = False
    self.frame = 0

  def copy(self):
    """
    Create a copy of the current Animation object.

    Returns:
    ----------
    Animation: A new Animation object with the same attributes as the current object.
    """
    return Animation(self.imgs, self.duration, self.loop)

  def update(self):
    """
    Update the animation frame based on the loop and duration settings.

    If the animation is set to loop, the frame will increment by 1 and wrap around
    to the beginning when it reaches the end. If the animation is not set to loop,
    the frame will increment by 1 and stop at the last frame when it reaches the end.

    Parameters:
    ----------
    self.frame : int
        The current frame of the animation.
    self.loop : bool
        Whether the animation should loop continuously.
    self.duration : int
        The number of frames to display each image for.
    self.imgs : list
        A list of pygame.Surface objects representing the animation frames.
    self.done : bool
        Whether the animation has completed.
    """
    if self.loop:
      self.frame  = (self.frame + 1) % (self.duration * len(self.imgs))
    else:
      maxframe = self.duration * len(self.imgs) -1
      self.frame = min(self.frame + 1, maxframe)
      if self.frame >= maxframe:
        self.done = True

  def img(self):
    """
    Get the current image of the animation based on the frame and duration.

    Parameters:
    ----------
    self.frame : int
        The current frame of the animation.
    self.duration : int
        The number of frames to display each image for.
    self.imgs : list
        A list of pygame.Surface objects representing the animation frames.

    Returns:
    ----------
    pygame.Surface: The current image of the animation.
    """
    return self.imgs[int(self.frame / self.duration)]
  

  