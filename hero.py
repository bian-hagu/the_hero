import pygame
from pygame.locals import *
DEFAULT_JUMPFORCE = 20
DEFAULT_BLOCK_SIZE = (50, 50)
DEFAULT_HERO_SIZE = (50, 50)
class Hero:
  def __init__(self, x, y):
    """
    Initialize the hero object with the given position.
    Args:
      x (int): X coordinate of the hero.
      y (int): Y coordinate of the hero.
    """
    self.x, self.y = pygame.Vector2(x, y)
    self.y = y
    self.speed = 5
    self.Health = 100
    self.jumpForce = 20
    self.isJump = False
    self.jumpCooldown = 0
    self.direction = 'right'
    self.img = pygame.transform.scale(\
      pygame.image.load("asset\\block\herochar.png"), DEFAULT_HERO_SIZE)
    

  def move(self, direction):
    if self.direction != direction:
      self.img = pygame.transform.flip(self.img, True, False)
      self.direction = direction
    if self.direction == "left":
      self.x -=self.speed
    elif self.direction == "right":
      self.x += self.speed

  def jump(self):
    if self.isJump:
      self.y -= self.jumpForce
      self.jumpForce -= 1.5
      if self.y >= 500:
        self.y = 500
        self.isJump = False
        self.jumpForce = DEFAULT_JUMPFORCE
        self.jumpCooldown = 30
    else:
      self.jumpCooldown -= 1

  def draw(self, screen):
    hitbox = (self.x+5, self.y, 50, 50)
    screen.blit(self.img, (self.x, self.y))
    pygame.draw.rect(screen, 'red', hitbox, 1)

