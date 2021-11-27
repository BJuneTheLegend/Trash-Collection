import pygame, sys, random, copy
from pygame.math import Vector2

pygame.init()
pygame.font.init()

class Player:
    def __init__(self):
        self.PlayerTexture = pygame.image.load('Boat.png').convert_alpha()
        self.HookTexture = pygame.image.load('Hook.png').convert_alpha()

        self.PlayerW = self.PlayerTexture.get_width()*2 #double width and hight based on size of image.
        self.PlayerH = self.PlayerTexture.get_height()*2
        self.PlayerTexture = pygame.transform.scale(self.PlayerTexture, (self.PlayerW, self.PlayerH))

        self.t = Trash()

        self.pos = Vector2(ScreenW/2-self.PlayerW/2, 50) #Center player on screen no matter the var

        self.LineEnd = Vector2(self.PlayerRectUpdate().center).y+300 #Assign bottem of line when code is first run.
        self.HookPos = Vector2(self.PlayerRectUpdate().center[0]-10, self.LineEnd)

        self.Points = 0

    def PlayerRectUpdate(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.PlayerW, self.PlayerH) #Return a rect for other functions.

    def LineUpdate(self):
        PlayerVector = Vector2(self.PlayerRectUpdate().center) #get center of player.
        return (PlayerVector, (PlayerVector.x, self.LineEnd)) #Give custom line object for Hook.

    def HookUpdate(self):
        return pygame.Rect(self.HookPos.x, self.HookPos.y, 12, 15)

    def DrawPlayer(self):
        Screen.blit(self.PlayerTexture, self.PlayerRectUpdate())

    def MovePlayer(self):
        key = pygame.key.get_pressed()
        speed = 5

        if key[pygame.K_d] or key[pygame.K_RIGHT]: #Check if D or RightArrow is pressed.
            if not self.pos.x + self.PlayerW >= ScreenW: #Make sure player does not go off screan .
                self.pos.x += speed
                self.HookPos.x += speed
        if key[pygame.K_a] or key[pygame.K_LEFT]: #Same comments from above apply here.
            if not self.pos.x <= 0:
                self.pos.x -= speed
                self.HookPos.x -= speed

    def Line(self):
        key = pygame.key.get_pressed()
        speed = 4
        margin = 40 #Right a margin of how close it can get to a pos

        if key[pygame.K_w] or key[pygame.K_UP]: #Change the pos of the bottom of the line
            if not self.LineEnd <= self.LineUpdate()[0].y+margin: #get PlayerVector from lineupdate (Scuffed way, ik)
                self.LineEnd -= speed
                self.HookPos.y -= speed
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            if not self.LineEnd >= ScreenH-margin: #make sure bottom of the line does not go off screen.
                self.LineEnd += speed
                self.HookPos.y += speed

        pygame.draw.line(Screen, (0,0,0), self.LineUpdate()[0], self.LineUpdate()[1], 3)

    def DrawHook(self):
        Screen.blit(self.HookTexture, self.HookUpdate())

    def Update(self):
        self.PlayerRectUpdate()
        self.LineUpdate()
        self.HookUpdate()
        self.MovePlayer()
        self.Line()
        self.DrawPlayer()
        self.DrawHook()

class Trash:
    def __init__(self):
        self.SixPack = pygame.image.load('6Ppack.png').convert_alpha()
        self.Box = pygame.image.load('Box.png').convert_alpha()
        self.WaterBottle = pygame.image.load('Water Bottle.png').convert_alpha()

        self.ItemChoices = {
            'SixPack': {'Type': 'SixPack', 'Rect': [0, 0, 32, 24]},
            'Box': {'Type': 'Box', 'Rect':  [0, 0, 25, 29]},
            'WaterBottle': {'Type': 'WaterBottle', 'Rect': [0, 0, 12, 38]}
        }

        self.Objects = []
        self.GameStart = True

    def RandomPos(self, cond=True):
        if cond:
            return random.randint(60, ScreenW - 60)
        else:
            return random.randint(120, ScreenH - 120)

    def MakeObjects(self):
        ObjCap = 40

        if len(self.Objects) == 0:
            for i in range(0, random.randint(10, ObjCap)):
                choice = copy.deepcopy(random.choice((self.ItemChoices['SixPack'], self.ItemChoices['Box'], self.ItemChoices['WaterBottle'])))
                choice['Rect'][0], choice['Rect'][1] = self.RandomPos(), self.RandomPos(False)

                self.Objects.append(choice)

    def DrawObjects(self):
        for o in self.Objects:
            if o['Type'] == 'SixPack':
                Screen.blit(self.SixPack, o['Rect'])
            elif o['Type'] == 'Box':
                Screen.blit(self.Box, o['Rect'])
            elif o['Type'] == 'WaterBottle':
                Screen.blit(self.WaterBottle, o['Rect'])

    def Update(self):
        self.MakeObjects()
        self.DrawObjects()

class Main:
    def __init__(self):
        self.p = Player()
        self.t = Trash()

        self.WaterOverlay = pygame.image.load('WaterOverlay.png').convert_alpha()
        self.Font = pygame.font.Font('Chelsea_Market/ChelseaMarket-Regular.ttf', 32)

        self.WaterOverlayRect = pygame.Rect(0, 0, self.WaterOverlay.get_width(), self.WaterOverlay.get_height())

        self.TicksPerSecond = copy.copy(TickTime)
        self.Time = [0, 0]

    def FontSurface(self):
        return self.Font.render(f'Points: {self.p.Points}', True, pygame.Color('white'))

    def FontDraw(self):
        Screen.blit(self.FontSurface(), (0, 0))

    def TimeCounter(self):
        if self.TicksPerSecond != 60:
            self.TicksPerSecond += 1

        elif self.TicksPerSecond == 60:
            self.Time[1] += 1
            self.TicksPerSecond = 0
            return True

        if self.Time[1] == 60:
            self.Time[1] = 0
            self.Time[0] += 1

    def DrawWaterOverlay(self):
        Screen.blit(self.WaterOverlay, self.WaterOverlayRect)

    def Update(self):
        self.DrawWaterOverlay()
        self.t.Update()
        self.p.Update()
        self.FontSurface()
        self.FontDraw()



ScreenW = 600
ScreenH = int(ScreenW * 0.8)
Screen = pygame.display.set_mode((ScreenW, ScreenH))
pygame.display.set_caption('Picky Upy')

TickTime = 60

m = Main()
Clock = pygame.time.Clock() #Set frame cap.
while True:
    Clock.tick(TickTime) #call frame cap (60 being in frames per second)
    m.TimeCounter()
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                for i, o in enumerate(m.t.Objects):
                    if pygame.Rect.colliderect(m.p.HookUpdate(), o['Rect']):
                        m.t.Objects.remove(o)
                        m.p.Points += 1


    print(m.Time)
    Screen.fill((130, 228, 255))
    m.Update()
    pygame.display.update()
