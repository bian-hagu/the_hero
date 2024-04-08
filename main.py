import pygame
from pygame.locals import *
pygame.init()


FPS = 60
GRAVITY = 20
DEFAULT_BLOCK_SIZE = (50,50)

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0


p1_pos = pygame.Vector2(screen.get_width() / 2, 540 )
p2_pos = pygame.Vector2(screen.get_width() / 2 + 10, 540 )

move_speed = 5
jumpForce = GRAVITY
isJump = False
jump_cooldown = 0
surface_level = 550

grass_top_block = pygame.transform.scale(pygame.image.load("asset\\block\grass_top.png"), DEFAULT_BLOCK_SIZE)

font = pygame.font.Font('freesansbold.ttf', 32)

def load_map():
  for i in range(40):
    if i != 5 and i != 6:
      screen.blit(grass_top_block, (50*i, surface_level))

  screen.blit(grass_top_block, (550, surface_level-50))
  screen.blit(grass_top_block, (550, surface_level-100))
  return ()
def drawJD():
  if jump_cooldown < 0:
    text = font.render('100', True, "white" )
  else: 
    text = font.render(f'{100-int(jump_cooldown/0.6)}', True, "white" )
  textRect = text.get_rect()
  textRect.center = (50, 50)
  screen.blit(text, textRect)

tick = 0
# player_hitbox = Rect(250, 100,100)
while running:

  jump_cooldown -= 1
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False


  screen.fill("lightskyblue")

  x,y = p1_pos
  keys = pygame.key.get_pressed() 

  if keys[pygame.K_a]:
    p1_pos.x -= move_speed
  if keys[pygame.K_d]:
    p1_pos.x += move_speed
    
  if keys[pygame.K_LEFT]:
    p2_pos.x -= move_speed
  if keys[pygame.K_RIGHT]:
    p2_pos.x += move_speed

  # #-- Jump ----------------------------------------------------------------------------
  if isJump == False and keys[pygame.K_SPACE] and jump_cooldown <= 0:
    isJump = True
    jump_cooldown = FPS   

  if isJump:
    p1_pos.y -= jumpForce
    if jumpForce >= -GRAVITY:
      jumpForce -= 1.5

    if p1_pos.y > surface_level:
      p1_pos.y = surface_level -10 
      isJump = False
      jumpForce = GRAVITY
  
  # -- Draw surface -------------------------------------------------------------------
  drawJD()
  player_rect = load_map()

  # collide = pygame.Rect.colliderect(player_rect, block_rect)

  pygame.draw.rect(screen, 'orange', (p1_pos.x - 10, p1_pos.y - 30, 20, 40))
  pygame.draw.rect(screen, 'lime', (p2_pos.x - 10, p2_pos.y - 30, 20, 40))
  # a = (x - p1_pos.x)**2 + (y-p1_pos.y)**2
  # if a != 0:
  #   print(a)
  pygame.display.flip()
  dt = clock.tick(FPS) / 1000

pygame.quit()
