import pygame
from pygame.locals import *
from hero import *
pygame.init()

FPS = 60


# screen = pygame.display.set_mode((1920, 1000), pygame.RESIZABLE)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

hero = Hero(10, 500)
surface_level = 550

grass_top_block = pygame.transform.scale(pygame.image.load("asset\\block\grass_top.png"), DEFAULT_BLOCK_SIZE)

font = pygame.font.Font('freesansbold.ttf', 32)

blocks_rect = []
for i in range(30):
  blocks_rect.append(Rect(i*50, 550, DEFAULT_BLOCK_SIZE[0], DEFAULT_BLOCK_SIZE[1]))
blocks_rect.remove(blocks_rect[4])
blocks_rect.remove(blocks_rect[4])
blocks_rect.append(Rect(500, 500, DEFAULT_BLOCK_SIZE[0], DEFAULT_BLOCK_SIZE[1]))
blocks_rect.append(Rect(500, 450, DEFAULT_BLOCK_SIZE[0], DEFAULT_BLOCK_SIZE[1]))

while running:
  screen.fill("white")
  keys = pygame.key.get_pressed() 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False
  # -- Move -----------------------------------------------
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    hero.move('left')
  if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    hero.move('right')

  # Only for test ---------------------
  # if keys[pygame.K_UP]:
  #   hero.y -= hero.speed
  # if keys[pygame.K_DOWN]:
  #   hero.y += hero.speed


  # -- Jump ----------------------------------------------------------------------------
  if keys[pygame.K_SPACE] and not hero.isJump and hero.jumpCooldown <= 0:
    hero.isJump = True
  hero.jump()

  # -- Draw surface -------------------------------------------------------------------
  for block in blocks_rect:
    screen.blit(grass_top_block, block)

  hero.draw(screen)

  pygame.display.flip()
  dt = clock.tick(FPS) / 1000

pygame.quit()
