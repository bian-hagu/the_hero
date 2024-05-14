import pygame
class Button:
  def __init__(self, surf, pos, size, text=''):
    """
    Initialize a Button object.

    Parameters:
    surf (pygame.Surface): The surface on which the button will be drawn.
    pos (tuple): The position of the top-left corner of the button on the surface.
    size (tuple): The size of the button as (width, height).
    text (str, optional): The text to be displayed on the button. Default is an empty string.

    Returns:
    None
    """
    self.surf = surf
    self.pos = pos
    self.size = size
    self.text = text

  def draw(self):
    """
    Draws the button on the surface.

    The button is drawn with a black border, a lighter shade of green, 
    a darker shade of green, and a darker shade of brown. The text on the button is rendered 
    using the 'data/font/Pixellari.ttf' font with a size of 32 and white color.
    """
    pygame.draw.rect(self.surf, 'black',         (self.pos[0], self.pos[1], self.size[0], self.size[1]))
    pygame.draw.rect(self.surf, (224, 236, 23),  (self.pos[0] + 3, self.pos[1] + 3, self.size[0]-6, self.size[1]-6))
    pygame.draw.rect(self.surf, 'black',         (self.pos[0] + 8, self.pos[1] + 8, self.size[0]-16, self.size[1]-16))
    pygame.draw.rect(self.surf, (203, 81, 16),   (self.pos[0] + 11, self.pos[1] + 11, self.size[0]-22, self.size[1]-22))
    if len(self.text) < 16:
      font = pygame.font.Font('data/font/Pixellari.ttf', 32)
    else:
      font = pygame.font.Font('data/font/Pixellari.ttf', 24)

    text = font.render(self.text, True, 'white')
    textRect = text.get_rect()
    textRect.center = (self.pos[0] + self.size[0]//2, self.pos[1] + self.size[1]//2 + 3)
    self.surf.blit(text, textRect)
    self.button_rect = self.rect()
 
  def rect(self):
    """
    Returns the rectangular coordinates of the button.

    The rectangular coordinates are represented as a tuple (x, y, width, height),
    where (x, y) is the position of the top-left corner of the button,
    and (width, height) is the size of the button.

    Returns:
    tuple: A tuple representing the rectangular coordinates of the button.
    """
    return (self.pos[0], self.pos[1], self.size[0], self.size[1])

class Menu:
  def __init__(self, surf, pos, size, labels, collumns = 1):
    """
    Initialize a Menu object.

    Parameters:
    surf (pygame.Surface): The surface on which the menu will be drawn.
    pos (tuple): The position of the top-left corner of the menu on the surface.
    size (tuple): The size of the menu as (width, height).
    labels (list): A list of strings representing the labels for the buttons in the menu.
    collumns (int, optional): The number of columns in the menu. Default is 1.
    """
    self.surf= surf
    self.pos = pos
    self.size = size
    self.labels = labels
    self.num_buttons = len(labels)
    self.buttons = []
    self.collumns = collumns

    Button(self.surf, self.pos, self.size).draw()
    pygame.draw.rect(self.surf, 'black',        (self.pos[0] + 16, self.pos[1] + 16, self.size[0]-32, self.size[1]-32))
    pygame.draw.rect(self.surf, (236, 140, 88), (self.pos[0] + 19, self.pos[1] + 19, self.size[0]-38, self.size[1]-38))
    
    blank_space = [self.size[0] - 50, self.size[1] - 50]
    button_size = [blank_space[0] if self.collumns == 1 else (blank_space[0]/2 - 5), 80]
    offset = [0 if self.num_buttons == 1 else 300, 0 if self.num_buttons == 1 else 100]

    if self.collumns == 1:
      blank_space = [blank_space[0] - button_size[0] , 
                    blank_space[1] - button_size[1] * self.num_buttons - (offset[1] - button_size[1]) * (self.num_buttons-1)]
      button_pos = [self.pos[0] + 25, self.pos[1] + 25 + blank_space[1] // 2]

      for label in self.labels:
        self.buttons.append(Button(self.surf, button_pos, button_size, label))
        button_pos = [button_pos[0], button_pos[1] + offset[1]]

    elif self.collumns == 2:
      blank_space = [blank_space[0] - button_size[0] , 
                    blank_space[1] - button_size[1] * self.num_buttons / self.collumns  - (offset[1] - button_size[1]) * (self.num_buttons-1) / self.collumns]
      button_pos = [self.pos[0] + 25, self.pos[1] + 25 + blank_space[1] // 2]
    
      for i in range(0,self.num_buttons, self.collumns):
        self.buttons.append(Button(self.surf, (button_pos[0], button_pos[1]), button_size, self.labels[i]))
    
        if i+1 < self.num_buttons:
          self.buttons.append(Button(self.surf, (button_pos[0] + offset[0], button_pos[1]), button_size, self.labels[i+1]))
        button_pos = [button_pos[0], button_pos[1] + offset[1]]
  
  def draw(self):
    """
    Draws the menu on the surface.

    The menu is drawn with a background color, and each button is drawn using the Button class.
    """
    for button in self.buttons:
      button.draw() 

  def is_click(self, x=0, y=0):
    """
    Checks if a button in the menu is clicked.

    Parameters:
    ----------
    x (int, optional): The x-coordinate offset for the mouse position. Default is 0.
    y (int, optional): The y-coordinate offset for the mouse position. Default is 0.

    Returns:
    str: The label of the clicked button, or None if no button is clicked.
    """
    mpos = pygame.mouse.get_pos()
    rect = pygame.Rect(mpos[0]-x, mpos[1]-y, 1, 1)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in self.buttons:
          if rect.colliderect(button.button_rect):
            return button.text
          

class UI(Menu):
  def __init__(self, surf):
    """
    Initialize a UI object.

    Parameters:
    ----------
    surf (pygame.Surface): The surface on which the UI will be drawn.
    """
    self.surf = surf

  def pause(self, size, labels):
    """
    Displays a pause menu on the screen.

    Parameters:
    ----------
    size : tuple
        The size of the pause menu as (width, height).
    labels : list
        A list of strings representing the labels for the buttons in the pause menu.

    Returns:
    ----------
    str
        The label of the clicked button, or None if no button is clicked.

    Note:
    This method creates an overlay surface, draws a menu surface on top of the overlay,
    and then blits the menu surface onto the main surface. It also handles mouse clicks
    to determine which button is clicked.
    """
    width, height = self.surf.get_width(), self.surf.get_height()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill('black')
    self.surf.blit(overlay, (0, 0))
 
    font = pygame.font.Font('data/font/Pixellari.ttf', 64)
    text = font.render('PAUSE', True, 'white')
    textRect = text.get_rect()
    textRect.center = (width/2, height/5)

    menu_surf = pygame.Surface(size)
    menu = Menu(menu_surf, (0,0), size, labels)
    menu.draw()
    self.surf.blit(menu_surf, (width/2 - size[0]/2, height/2 - size[1]/2 + 75))
    label = menu.is_click(width/2 - size[0]/2, height/2 - size[1]/2 + 75)
    self.surf.blit(text, textRect)

    return label
  def complete(self, size, labels):
    """
    Displays a pause menu on the screen.

    Parameters:
    ----------
    size : tuple
        The size of the pause menu as (width, height).
    labels : list
        A list of strings representing the labels for the buttons in the pause menu.

    Returns:
    ----------
    str
        The label of the clicked button, or None if no button is clicked.

    Note:
    This method creates an overlay surface, draws a menu surface on top of the overlay,
    and then blits the menu surface onto the main surface. It also handles mouse clicks
    to determine which button is clicked.
    """
    width, height = self.surf.get_width(), self.surf.get_height()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill('black')
    self.surf.blit(overlay, (0, 0))
 
    font = pygame.font.Font('data/font/Pixellari.ttf', 64)
    text = font.render('COMPLETE LEVEL', True, 'white')
    textRect = text.get_rect()
    textRect.center = (width/2, height/5)

    menu_surf = pygame.Surface(size)
    menu = Menu(menu_surf, (0,0), size, labels)
    menu.draw()
    self.surf.blit(menu_surf, (width/2 - size[0]/2, height/2 - size[1]/2 + 75))
    label = menu.is_click(width/2 - size[0]/2, height/2 - size[1]/2 + 75)
    self.surf.blit(text, textRect)

    return label
  
  def retry(self, size, labels):
    """
    Displays a retry menu on the screen.

    Parameters:
    ----------
    size : tuple
        The size of the retry menu as (width, height).
    labels : list
        A list of strings representing the labels for the buttons in the retry menu.

    Returns:
    ----------
    str
        The label of the clicked button, or None if no button is clicked.

    Note:
    This method creates an overlay surface, draws a menu surface on top of the overlay,
    and then blits the menu surface onto the main surface. It also handles mouse clicks
    to determine which button is clicked.
    """
    width, height = self.surf.get_width(), self.surf.get_height()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill('black')
    self.surf.blit(overlay, (0, 0))

    font = pygame.font.Font('data/font/Pixellari.ttf', 64)
    text = font.render('RETRY', True, 'white')
    textRect = text.get_rect()
    textRect.center = (width/2, height/5)


    menu_surf = pygame.Surface(size)
    menu = Menu(menu_surf, (0,0), size, labels)
    menu.draw()
    self.surf.blit(menu_surf, (width/2 - size[0]/2, height/2 - size[1]/2 + 75))
    label = menu.is_click(width/2 - size[0]/2, height/2 - size[1]/2 + 75)
    self.surf.blit(text, textRect)
    return label

  def main_menu(self, labels):
    """
    Displays the main menu on the screen.

    Parameters:
    ----------
    labels : list
        A list of strings representing the labels for the buttons in the main menu.

    Returns:
    ----------
    str
        The label of the clicked button, or None if no button is clicked.

    Note:
    This method creates a Menu object with the given parameters, draws the menu on the surface,
    and then handles mouse clicks to determine which button is clicked.
    """
    width, height = self.surf.get_width(), self.surf.get_height()

    menu = Menu(self.surf, (width//3, 200), (width//3, height//1.5), labels)
    menu.draw()
    return menu.is_click()

  def select_level(self, labels):
    """
    Displays a menu for selecting levels.

    Parameters:
    ----------
    labels : list
        A list of strings representing the labels for the level buttons.

    Returns:
    ----------
    str
        The label of the clicked level button, or None if no button is clicked.

    Note:
    This method creates a Menu object with the given parameters, draws the menu on the surface,
    and then handles mouse clicks to determine which level button is clicked.
    The menu is positioned at (320, 200) with a size of (640, height//1.5) and displays the labels in 2 columns.
    """
    width, height = self.surf.get_width(), self.surf.get_height()
    menu = Menu(self.surf, 
                pos=  (320, 200), 
                size= (640, height//1.5), 
                labels= labels, 
                collumns= 2)
    menu.draw()
    return menu.is_click()
  
  def shop(self, size, game):
    width, height = self.surf.get_width(), self.surf.get_height()
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(128)
    overlay.fill('black')
    self.surf.blit(overlay, (0, 0))



    menu_surf = pygame.Surface(size)
    labels = ['Buy 1 potion\n(50 Coin)', 'Buy 5 potion\n(225 Coin)', 'Back']
    menu = Menu(menu_surf, (0,0), size, labels)
    menu.draw()
    self.surf.blit(menu_surf, (width/2 - size[0]/2, height/2 - size[1]/2 + 75))
    label = menu.is_click(width/2 - size[0]/2, height/2 - size[1]/2 + 75)
    
    font64 = pygame.font.Font('data/font/Pixellari.ttf', 64)
    text = font64.render('Shop', True, 'white')
    textRect = text.get_rect()
    textRect.center = (width/2, height/5)
    self.surf.blit(text, textRect)
    
    if label == labels[0]:
      if game.coin >= 50:
        game.coin -= 50
        game.potions += 1
        game.save_game()
    if label == labels[1]:
      if game.coin >= 225:
        game.coin -= 225
        game.potions += 5
        game.save_game()
    Button(self.surf, ((150, height/2 - size[1]/2 + 75)), (size[0]*0.75, size[1]/3)).draw()
    coin_pos = [170, 240]
    potions_pos = [170, 300]
    font32 = pygame.font.Font('data/font/Pixellari.ttf', 32)
    coin_text = font32.render(str(game.coin), True, 'white')
    coin_Rect = coin_text.get_rect()
    coin_Rect.topleft = [210, coin_pos[1]]

    potions_text = font32.render(str(game.potions), True, 'white')
    potions_Rect = potions_text.get_rect()
    potions_Rect.topleft = [210, potions_pos[1]]

    self.surf.blit(potions_text, potions_Rect)
    self.surf.blit(coin_text, coin_Rect)
    self.surf.blit(game.assets['coin'], coin_pos)
    self.surf.blit(game.assets['potion'], potions_pos)
  

    return label
    
  


  def game_name(self, assets):
    """
    Draws the game name "the hero" on the surface using the provided assets.

    Parameters:
    ----------
    assets : dict
        A dictionary containing the game's character assets. The keys are the characters,
        and the values are the corresponding pygame.Surface objects.

    Returns:
    ----------
    None

    Note:
    This method iterates through each character in the game name, checks if it's not a space,
    and blits the corresponding asset onto the surface at the specified position.
    The position is updated after each character is drawn, with a fixed offset of 110 pixels.
    """
    text = 'the hero'
    pos = [200, 50]
    for char in text:
      if char != ' ':
        self.surf.blit(assets[char], pos)
      pos[0] = pos[0] + 110
