import sys, pygame
from random import *

# CLASSES -----------------------
class Catcher(object):
    """
    The Catcher is the player's character who moves left and right to catch
    coconuts falling from the top of the screen.
    """
    def __init__(self):
        self.x = 0.45 * width
        self.y = height - 180
        self.speed = 5
        self.img = pygame.image.load('catcher.png')
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getSpeed(self):
        return self.speed
        
    def setX(self, x):
        self.x = x
        
    def setSpeed(self, speedChange):
        self.speed += speedChange
        
    def getWidth(self):
        return self.img.get_rect().width
    
    def getHeight(self):
        return self.img.get_rect().height
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        
class Coconut(object):
    """
    Coconuts fall from the top of the screen and the player has to catch them
    using the catcher.
    """
    def __init__(self, speed):
        self.x = random() * (width - 50)
        self.y = -50
        self.speed = speed
        self.img = pygame.image.load('coconut.png')
        self.width = self.img.get_rect().width
        self.height = self.img.get_rect().height
    
    def getY(self):
        return self.y
    
    def getX(self):
        return self.x
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getSpeed(self):
        return self.speed
    
    def isCaught(self, x, y, width, height):
        if (self.x > x + width or
            self.x + self.width < x or
            self.y + self.height < y or
            self.y > y + height * .20):
            return False
        else:
            return True
        
    def fall(self):
        self.y += self.speed
        
    def draw(self):
        screen.blit(self.img, (self.x, self.y))

class Pineapple(Coconut):
    def __init__(self, speed):
        Coconut.__init__(self, speed)
        self.img = pygame.image.load('pineapple.png')
        
        
        
# GLOBAL FUNCTIONS -------------------------------
def renderTxt(text, fontSize, font = 'freesansbold.ttf', color = (255, 255, 255), x = 0, y = 0):
     """
     function: displays text on screen
     @params: string text
            : int fontSize
            : string font file (.ttf)
            : tuple color (val, val, val)
            : int x
            : int y
     """   
     fontSpec = pygame.font.Font(font, fontSize)
     textSurf = fontSpec.render(text, True, color)
     textRect = textSurf.get_rect()
     textRect.topleft = (x, y)
     screen.blit(textSurf, textRect)
    

# COLORS -------------------------
white = (255, 255, 255)
black = (0, 0, 0)

# SETUP ---------------------------
pygame.init()
size = width, height = 900, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Coconut Catch')
backgroundImg = pygame.image.load('background.jpeg')
introBG = pygame.image.load('introBG.jpeg')
score = 0

clock = pygame.time.Clock()

# START SCREEN ---------------------
def startScreen():
    
    intro = True
    
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    
        screen.blit(introBG, (0, 0))        
        renderTxt("Press Space to Play", 90, 'freesansbold.ttf', white, 12, 360)        
        pygame.display.update()


# GAME LOOP ------------------------
def gameLoop():
    
    catcher = Catcher()
    coconuts = []
    
    global score
    timer = 0
    dx = 0
    cocoSpeed = 1
    lives = 5
    level = 1
    
    levelingUp = False
    haveBoost = False
    gameOver = False
    
    while not gameOver:
        # EVENT HANDLING -----------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx -= catcher.getSpeed()
                elif event.key == pygame.K_RIGHT:
                    dx += catcher.getSpeed()
                elif event.key == pygame.K_SPACE:
                    if haveBoost:
                        catcher.setSpeed(5)
                        haveBoost = False
                elif event.key == pygame.K_ESCAPE:
                    gameOver = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    dx += catcher.getSpeed()
                elif event.key == pygame.K_RIGHT:
                    dx -= catcher.getSpeed()
                    
        # LOGIC -----------------------------------            
        if (not catcher.getX() + dx > width - catcher.getWidth() 
                and not catcher.getX() + dx < 0):            
            catcher.setX(catcher.getX() + dx)
        
        if timer % 60 == 0 and not levelingUp:
            randNum = random()
            if (randNum > 0 and randNum < 0.06):
                coconuts.append(Pineapple(cocoSpeed))
            else:
                coconuts.append(Coconut(cocoSpeed))
        timer += 1

        # DRAW ELEMENTS------------------------------
        screen.blit(backgroundImg, (0, 0))
        catcher.draw()
        for coconut in coconuts:
            if coconut.isCaught(catcher.getX(), catcher.getY(), catcher.getWidth(), catcher.getHeight()):
                if type(coconut) is Pineapple:
                    haveBoost = True
                score += 10
                if score % 100 == 0:
                    levelingUp = True
                    level += 1
                    cocoSpeed += 0.5
                coconuts.remove(coconut)
                
            if coconut.getY() + coconut.getHeight() > height:
                if type(coconut) is not Pineapple:
                    lives -= 1
                coconuts.remove(coconut)
                
            coconut.draw()
            coconut.fall()
        renderTxt('score = ' + str(score), 20, 'freesansbold.ttf', white, 12, 12)
  
        ### DRAW LIVES ####
        for i in range(1, lives):
            if i == 1:
                x = 860
            lifeImg = pygame.transform.smoothscale(pygame.image.load('catcher.png'), (30, 60))
            screen.blit(lifeImg, (x, 10))
            x -= 40
        ###################
        
        ### DRAW BOOST SYMBOL ###
        if haveBoost:
            boostImg = pygame.transform.smoothscale(pygame.image.load('pineapple.png'), (30, 50))
            screen.blit(boostImg, (12, 730))
        
        #########################
      
        if lives < 0:
            gameOver = True
        
        pygame.display.update()
        clock.tick(60)
        
# GAME OVER --------------------------
def endGame():
    global score
    close = False
    
    while not close:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                    
        screen.fill(black)        
        renderTxt("Game Over", 90, 'freesansbold.ttf', white, 200 , 360)
        renderTxt("Your score was " + str(score), 50, 'freesansbold.ttf', white, 220 , 500)
        pygame.display.update()        
        

# MAIN CODE --------------------------
startScreen()
gameLoop()
endGame()
pygame.quit()
sys.exit()
quit()