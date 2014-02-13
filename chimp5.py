#/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation, 
follow along in the tutorial.
"""


#Import Modules
import os, pygame, sys,math
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound


#classes for our game objects
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.punching = 0
        self.move = 10
        self.moveup = 10
        self.rect.move_ip(5, 50)

    def update(self):
        # "move the fist based on the mouse position"
        # pos = pygame.mouse.get_pos()
        # self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)
            self.rect.move_ip(-5, -10)

    def translate(self,vert,horz):
        newpos = self.rect.move((horz*self.move, vert*self.moveup))
        #Code to keep the fist in the display
        if newpos.left >= self.area.left and \
           newpos.right <= self.area.right and \
           newpos.top >= self.area.top and \
           newpos.bottom <= self.area.bottom:
           self.rect=newpos     
  
    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 30
        self.moveup = 1.2
        self.move = 3.2
        self.dizzy = 0
        self.gravity = -.05
        self.maxmove = 5.
        self.hitbottom=0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        self.moveup=self.moveup-self.gravity
        if abs(self.moveup) > self.maxmove:
            self.moveup= self.maxmove*self.moveup/abs(self.moveup)
        newpos = self.rect.move((self.move, self.moveup))
        if newpos.left < self.area.left or \
           newpos.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, self.moveup))
            self.image = pygame.transform.flip(self.image, 1, 0)
        if newpos.bottom > self.area.bottom: self.hitbottom=1
        if newpos.top < self.area.top or \
           newpos.bottom > self.area.bottom:
            self.moveup = -self.moveup
            newpos = self.rect.move((self.move, self.moveup))
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            #self.dizzy = 1
            self.original = self.image
            self.move = self.move
            self.moveup = -self.moveup

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        if self.score < 0:
            self.text = "Game Over, score: %d" % (self.score)
            self.image = self.font.render(self.text, 1, 
            (255, 255, 0))
        self.text = "Lives: %d, score: %d" % (self.lives,
        self.score)
        self.image = self.font.render(self.text, 1, 
        (255, 255, 0))
        self.rect = self.image.get_rect()
        

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 460))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(50,50)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        #text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        #textpos = text.get_rect(centerx=background.get_width()/2)
        #background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp()
    fist = Fist()
    scoreboard = Scoreboard()
    scoreSprite = pygame.sprite.Group(scoreboard)
    allsprites = pygame.sprite.RenderPlain((fist, chimp))

#Main Loop
    while 1:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            #Check spacebar to punch
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                    scoreboard.score += 1
                else:
                    whiff_sound.play() #miss
            elif event.type == KEYUP and event.key == K_SPACE:
                fist.unpunch()

        #Check arrow keys to move fist
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_UP]:
            fist.translate(-1,0)
        if keys_pressed[K_DOWN]:
            fist.translate(1,0)    
        if keys_pressed[K_RIGHT]:
            fist.translate(0,1)    
        if keys_pressed[K_LEFT]:
            fist.translate(0,-1) 
 
        #Check to make sure that chimp hasn't fallen,
        #if it has lose a life
        if chimp.hitbottom:
            scoreboard.lives -=1
            chimp.hitbottom=0
                   
        allsprites.update()
        scoreSprite.update()
        if scoreboard.lives < 0:
            break
    #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        scoreSprite.draw(screen)
        pygame.display.flip()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
