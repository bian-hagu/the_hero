import pygame





class Button:
  def __init__(self, surf, pos, size, text=''):
    self.surf = surf
    self.pos = pos
    self.size = size
    self.text = text

  def draw(self):
    pygame.draw.rect(self.surf, 'black',         (self.pos[0], self.pos[1], self.size[0], self.size[1]))
    pygame.draw.rect(self.surf, (224, 236, 23),  (self.pos[0] + 3, self.pos[1] + 3, self.size[0]-6, self.size[1]-6))
    pygame.draw.rect(self.surf, 'black',         (self.pos[0] + 8, self.pos[1] + 8, self.size[0]-16, self.size[1]-16))
    pygame.draw.rect(self.surf, (203, 81, 16),   (self.pos[0] + 11, self.pos[1] + 11, self.size[0]-22, self.size[1]-22))

    font = pygame.font.Font('data/font/Pixellari.ttf', 32)
    text = font.render(self.text, True, 'white')
    textRect = text.get_rect()
    textRect.center = (self.pos[0] + self.size[0]//2, self.pos[1] + self.size[1]//2 + 3)
    self.surf.blit(text, textRect)
 
  def rect(self):
    return (self.pos[0], self.pos[1], self.size[0], self.size[1])

class Menu:
  def __init__(self, surf, pos, size, labels):
    self.surf= surf
    self.pos = pos
    self.size = size
    self.labels = labels
    self.num_buttons = len(labels)
    self.buttons = []

  def draw(self):
    Button(self.surf, self.pos, self.size).draw()
    pygame.draw.rect(self.surf, 'black',        (self.pos[0] + 16, self.pos[1] + 16, self.size[0]-32, self.size[1]-32))
    pygame.draw.rect(self.surf, (236, 140, 88), (self.pos[0] + 19, self.pos[1] + 19, self.size[0]-38, self.size[1]-38))
    
    blank_space = [self.size[0] - 50, self.size[1] - 50]
    button_size = [self.size[0] - 50 , 80]
    blank = 0 if self.num_buttons == 1 else 100
    blank_space = [blank_space[0] - button_size[0] , 
                   blank_space[1] - button_size[1] * self.num_buttons - (blank - button_size[1]) * (self.num_buttons-1)]
    button_pos = [self.pos[0] + 25, self.pos[1] + 25 + blank_space[1] // 2]

    for label in self.labels:
      self.buttons.append(Button(self.surf, button_pos, button_size, label))
      button_pos = [button_pos[0], button_pos[1] + blank]
    for button in self.buttons:
      button.draw()

  def is_click(self, x, y):
    mpos = pygame.mouse.get_pos()
    rect = pygame.Rect(mpos[0]-x, mpos[1]-y, 1, 1)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          for button in self.buttons:
            if rect.colliderect(button.rect()):
              return button.text

class UI(Menu):
  def __init__(self, surf):
    self.surf = surf

  def pause(self, size):
    width, height = self.surf.get_width(), self.surf.get_height()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill('black')
    self.surf.blit(overlay, (0, 0))
 
    menu_surf = pygame.Surface(size)
    menu = Menu(menu_surf, (0,0), size, ['RESUME', 'MAIN MENU', 'QUIT'])
    menu.draw()
    self.surf.blit(menu_surf, (width/2 - size[0]/2, height/2 - size[1]/2))
    label = menu.is_click(width/2 - size[0]/2, height/2 - size[1]/2)
    return label

