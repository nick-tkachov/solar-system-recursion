# ---------------------------------------------------------------------------------------------------#
# Program Name: RECURSION ASSIGNMENT
# Programmer: Nick Tkachov
# Date: DECEMBER 15, 2017
# Input:    MOON PERCENTAGE: Chance of a moon occuring on a planet every time one is generated(best at 10%)
#                           - this is a recursive call which means moons can generate on top of each other
#           ASTEROID BELT OCCURENCE: Chance that a planet will have an asteroid belt
#           CHANCE OF ASTEROID FALLING: Chance that an asteroid will fall once every loop
#           AMOUNT OF PLANETS: How many planets will be in the solar system?
#           AMOUNT OF CONSTELLATIONS: How many constellations will be generated in the solar system?
#                           - constellations are recursively generated, all random
#           << NOT LISTED>>
#           BLACKHOLE CHANCE: Chance that a planet will become a blackhole
# Processing: Program takes in inputs, and utilises recursion and functions to generate solar system
# Output: A solar system consisting of chance attributes is generated
# ----------------------------------------------------------------------------------------------------#


# IMPORTS ----------------------------------------------------------------------------------------------------#
import pygame,os
import pygame.gfxdraw
from random import randint,choice,uniform,random,randrange
from math import *

# INIT SCREEN ----------------------------------------------------------------------------------------------------#
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
# COLORS ----------------------------------------------------------------------------------------------------#
WHITE = (255,255,255)
DBLUE = (12, 33, 73)
PURPLE = (70, 66, 183)
LBLUE = (99, 146, 170)
RED = (66, 7, 15)
GREEN = (6, 43, 4)
ORANGE= (112, 79, 51)
BROWN = (45, 31, 18)
DGREY = (56, 56, 56)
MOON_GREY = (102, 102, 102)
DDDGREY = (20, 20, 20)
GREY = (30, 30, 30)
BLACK = (0,0,0)
ASTEROID_GREY = (50, 50, 50)

# PERCENTAGE VALUES ----------------------------------------------------------------------------------------------------#
moon_percentage = 0.1
planet_amount = 3
asteroid_chance = 0.001
asteroidbelt_chance = 1
blackhole_chance = 0.3
constellation_amount = 4
constellation_size = 60
# CLASSES ----------------------------------------------------------------------------------------------------#
class text(): #creates a text object
    def __init__(self,x,y,size,text,bold=False):
        self.x = x
        self.y = y
        self.bold = bold
        self.text = text
        self.size = size
        self.font = pygame.font.SysFont('sans',self.size,self.bold)
        self.text_surface = self.font.render(self.text,True,WHITE)

    def draw(self,surf):
        self.bg = pygame.Surface((surf.get_width(),self.text_surface.get_rect().height))
        self.bg.fill(BLACK)
        self.bg.set_alpha(100)
        surf.blit(self.bg,(0,self.y))
        surf.blit(self.text_surface,((surf.get_width() - self.text_surface.get_rect().width)/2,self.y))#draws text in center

class display_value(): #displays the text for percentage chances (start menu)
    def __init__(self,x,y,w,h,size,total_size=0,have_bg = True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.have_bg = have_bg
        self.total_size = total_size
        self.size = size
        self.surf = pygame.Surface((self.w,self.h))
        self.surf.convert()
        self.surf.fill(RED)
        self.rect = self.surf.get_rect()
    def draw(self,surface,texts,multiply_amount = (100,'%')):
        self.rect.x,self.rect.y = ((surface.get_width() - self.surf.get_rect().width-self.total_size)/2),self.y
        if not self.have_bg and multiply_amount[0] == 1:
            self.value = str(round(texts,2) * multiply_amount[0])+ multiply_amount[1] #puts text to look properly
        elif self.have_bg:
            self.value = str(round(texts,2) * multiply_amount[0])+ multiply_amount[1] #puts text to look properly
        else:
            self.value = texts
        self.text = text(self.x,self.y,self.size,self.value,True)
        if self.have_bg: #creates a black background
            self.bg = pygame.Surface((surface.get_width(),self.h+20))
            self.bg.set_alpha(100)
            self.bg.fill(BLACK)
            surface.blit(self.bg,(self.x,self.y-10))

        self.surf.blit(self.text.text_surface,(((self.w - self.text.text_surface.get_rect().width)/2),
                       (self.h - self.text.text_surface.get_rect().height)/2)) #blits surfaces
        surface.blit(self.surf,((surface.get_width() - self.surf.get_rect().width-self.total_size)/2,self.y))
        pygame.draw.rect(surface,WHITE,pygame.Rect((surface.get_width() - self.surf.get_rect().width-self.total_size)/2,self.y,self.w,self.h),2)

    def on_mouse_click(self):
        return self.on_mouse_hover()
    def on_mouse_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

class random_stars(object): #draws stars
    def __init__(self,x,y,size,constellation = False):
        self.x = x
        self.y = y
        self.constellation = constellation
        self.size = size
        self.speed = randint(1,10)
        self.opacity = randint(1,size) * 30 + randint(0,15) #random opacity
        self.surf = pygame.Surface((size,size))
        if not self.constellation:
            self.surf.set_alpha(self.opacity)
        self.surf.fill(WHITE)

    def draw(self,surface):
        self.opacity += self.speed #creates a "glimmering" effect on stars
        if self.opacity > 255:
            self.speed = randrange(-1,-10,-1)
        elif self.opacity < 0:
            self.speed = randint(1,10)
        surface.blit(self.surf,(self.x,self.y))
        if not self.constellation:
            self.surf.set_alpha(self.opacity)

class asteroid_particles(object): #asteroid particles for the belt
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.surf = pygame.Surface((size,size))
        self.surf.fill(DGREY)
    def draw(self,surface):
        surface.blit(self.surf,(self.x,self.y))

class planet(object): #planet calss
    def __init__(self,x,y,size,parent_planet=None):
        self.x = x
        self.y = y
        self.color = choice([PURPLE,RED,GREEN,ORANGE,BROWN,LBLUE]) #random color
        self.size = randint((size*10)//planet_amount,(size*15)//planet_amount) #random size depending on the amount of planets
        self.angle = 0
        self.speed = uniform(0.1,0.5)
        self.parent_planet = parent_planet
        self.rotx,self.roty = screen.get_width()//2,screen.get_height()//2 #rotate around center
        self.blackhole = False
        self.moon_enable = False
        self.has_belt = False
        self.asteroid_amount = randint(30,50)
        self.planet_features = []
        moon_generate = random() #generates moon if it reaches the percentage
        if moon_percentage > moon_generate:
            self.generate_moon()

    def draw(self,surface): #draws planet
        self.angle += self.speed
        if self.blackhole:
            draw_blackhole(self.x,self.y,1,self.size,3)
        if self.parent_planet is not None: #if it is a moon...
            self.rotx,self.roty = self.parent_planet.x,self.parent_planet.y
            self.x,self.y = self.parent_planet.x+self.parent_planet.size+10,self.parent_planet.y

        self.x,self.y = rotate_point((self.x,self.y),(self.rotx,self.roty),self.angle)

        if self.has_belt and self.color is not MOON_GREY and not self.blackhole and not self.moon_enable:#can only have asteroid belt if it doesnt have moon (because collision)
            self.asteroid_belt()
        if len(self.planet_features) is not 0:
            for x in self.planet_features:
                x.draw(surface)

        pygame.draw.circle(surface,self.color,(int(self.x),int(self.y)),self.size)
    def get_rect(self):
        return pygame.Rect(self.x-self.size/2,self.y-self.size/2,self.size,self.size)
    def asteroid_belt(self):
        self.planet_features = create_asteroid_belt(self.size,self.x,self.y,self.asteroid_amount)
    def generate_moon(self):
        planets.append(moon(self.x,self.y,1,self))
        self.moon_enable = True
    def transform_blackhole(self):
        if self.color != MOON_GREY: #transforms into blackhole, unless moon (moons cant be blackholes)
            self.x,self.y = rotate_point((self.x,self.y),(self.rotx,self.roty),randint(0,360))
            self.rotx,self.roty = self.x+5,self.y
            self.color = (0,0,0)
            self.speed = 30
            self.size = 100//planet_amount
            self.blackhole = True

class moon(planet): #moon version of the planet except it has a parent planet so it knows what to rotate around
    def __init__(self,x,y,size,parent_planet=None):
        super().__init__(x,y,size,parent_planet)
        self.color = MOON_GREY
        self.size = randint(5,10)
        self.speed = randint(1,5)

class create_asteroid(): #asteroid creation
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.set1 = randint(15,20) #so the asteroid looks "deformed" because not all asteroids are the same
        self.set2 = randint(10,30)
        self.set3 = randint(30,50)
    def check_collision(self,surface):
        self.x -= 5
        self.y +=5
        self.rect = pygame.Rect(self.x-20,self.y-20,20,20) #creates a rect(for collision purposes)
        pygame.draw.polygon(surface,ASTEROID_GREY,[(self.x,self.y),(self.x - self.set1, self.y)
                                                   ,(self.x + self.set2, self.y - self.set3),(self.x + self.set1, self.y - self.set1)])#draws the actual polygon
        draw_fire(self.x,self.y,3,5)
        for i,v in enumerate(planets): #checks for collision with blackhole
            if v.get_rect().colliderect(self.rect):
                if not planets[i].blackhole:
                    del planets[i]
                return True
            elif self.rect.colliderect(pygame.Rect((surface.get_width()-90//planet_amount)/2,(surface.get_height()-90//planet_amount)/2,
                                                   90//planet_amount,90//planet_amount)): #checks for collison with sun (cause rocks burn in the sun)
                return True
        if self.y > surface.get_height():
            return True
        return False

# RECURSIVE FUNCTIONS ----------------------------------------------------------------------------------------------------#
def draw_blackhole (x1, y1, angle, length, n): #generates "blackhole" "effects" around the blackhole
    angle = angle + (randint(1,10)) # angle is random so it looks like it is "breaking" around it
    x2 = int(x1 + (length * cos(angle)) + n) #basic recursive function, works
    y2 = int(y1 - (length * sin(angle)) + n)
    pygame.draw.line(screen,BLACK,(x1, y1),(x2, y2),2) #draws a line
    if n > 1:
        draw_blackhole(x2, y2, angle -0.05, length, n - 1)
        draw_blackhole(x2, y2, angle + 0.3, length, n - 1)


def generate_constellation(x1, y1, angle, length, n,width = 3): #generates constellations recursively (this also creates a star at the end of every line to show that it "connects")
    max_angle = 60                #random angles between 20 and 60
    min_angle = 20
    branch_chance = .75
    branch_ran = random()           #determines if it should branch off
    angle = angle + (random() * max_angle) + min_angle
    x2 = int(x1 + (length * cos(angle)) + n)
    y2 = int(y1 - (length * sin(angle)) + n)
    if n > 1:
        if branch_chance > branch_ran:#if branch off chance is reached, will make a thinner branch
            return [[(x1,y1),(x2,y2),width-1]] + generate_constellation(x2, y2, angle -random()*2, length/1, n - 1,width)
        return [[(x1,y1),(x2,y2),width]] + generate_constellation(x2, y2, angle - random(), length/1, n - 1,width)
        return [[(x1,y1),(x2,y2),width]] + generate_constellation(x2, y2, angle + random(), length/1, n - 1,width)
    else:
        return []

def star_gaze(w,h,size): #creates stars as the background
    if h < 0:
        return []
    else:
        if w > 0:#creates stars on one line of the background, randomly
            return [random_stars(randint(w-100,w),randint(h-100,h),randint(2,8))] + star_gaze(w-100,h,size)
        else:#once one line is filled up, moves up and creates another line
            w = screen.get_width()
            return star_gaze(w,h-100,size) + [random_stars(randint(0,w),randint(h-100,h),randint(2,size))]

def create_asteroid_belt(size,x,y,amt,angle = 0):#creates asteroid belt
    if angle > 360:
        return []
    else:
        rotx,roty = x,y
        x,y = x+size,y
        x,y = rotate_point((x+10,y),(rotx,roty),angle+amt)      #uses rotate around center function to create "asteroids" around planet
        return create_asteroid_belt(size,rotx,roty,amt,angle+amt) + [asteroid_particles(x,y,size/4)] #recursive calls for more asteroids

def generate_system(w,h,size,count=1):
    if count > size:
        return []
    else:
        planets.append(planet(int(w/2) + (w/2/size*count),int(h/2),int((10*count)/planet_amount)))#generates solar system, calls planet function and giving size , puts planet in appropriate orbit
        solar_circles.append(int(((w/2)/size)*count))      #appends solar circles, to show orbit
        generate_system(w,h,size,count+1)

def recursive_fire (x1, y1, x2, y2, displace):
    if displace < 6:                            #the "quality" of the fire, more lines = more detailed
        return [(x1,y1),(x2,y2)]                #returns coordinates from recursive generation
    else:
        mid_x = (x2+x1)/2                       #uses midpoint formula to generate midpoints in between fire, generates midpoints in between in order to create a "fire" effect
        mid_y = (y2+y1)/2
        mid_x += (random()+uniform(-0.5,0.5))   #randomly gives x and y with midpoint formula
        mid_y += (random()-1)*displace
        return [(x1,y1),(x2,y2)] + recursive_fire(x1,y1,int(mid_x),int(mid_y),displace/2) + recursive_fire(x2,y2,int(mid_x),int(mid_y),displace/2)

# NON-RECURSIVE FUNCTIONS ----------------------------------------------------------------------------------------------------#
def rotate_point(point, axis, ang):
    x, y = point[0] - axis[0], point[1] - axis[1]
    radius = sqrt(x*x + y*y) # get the distance between points
    RAng = radians(ang)       # convert ang to radians.
    h = axis[0] + ( radius * cos(RAng) )
    v = axis[1] + ( radius * sin(RAng) )
    return h, v

def draw_fire(x,y,size,width):
    x = randint(x-10,x)                                         #draws the fire from recursion function
    width = randint(width - 20,width)
    f_list = []
    f_list += recursive_fire(int(x),int(y),x+width,y,randint(10*size,10*size+20)) #calls recursion function, randomly gives width so it looks like its moving
    f_list = list(set(f_list))
    f_list.sort()
    pygame.gfxdraw.filled_polygon(screen,f_list,(200,0,0))
    f_list = [(v[0]/1.3+((x-x/1.3)+width/6),v[1]/2+(y/2)) for v in f_list]        #creates a similar fire for red shade
    pygame.gfxdraw.filled_polygon(screen,f_list,(230,230,0))

def draw_constellations(surface):                               #recursive function for drawing constellations
    for z in constellation:
        for x in z:
            pygame.draw.line(surface,WHITE,x[0],x[1],round(x[2]))         #draws the line
            random_stars(x[0][0],x[0][1],5,True).draw(screen)
            random_stars(x[1][0],x[1][1],5,True).draw(screen)

def blank_overlay(surface):
    surf = pygame.Surface((surface.get_width(),surface.get_height()))
    surf.set_alpha(200)
    surf.fill(DDDGREY)
    surface.blit(surf,(0,0))

# BEGINNER VALUES ----------------------------------------------------------------------------------------------------#
planets = []
solar_circles = []
asteroids = []
constellation = []
in_menu = True
stars  = star_gaze(screen.get_width(),screen.get_height(),planet_amount) #generates stars randomly

while in_menu:
    screen.fill(DBLUE)
# CREATES MENU ----------------------------------------------------------------------------------------------------#
    moon_plus = display_value(0,166,60,50,30,-220,have_bg = False)
    moon_minus = display_value(0,166,60,50,30,220,have_bg = False)
    moon_value = display_value(0,166,140,50,30)

    asteroid_plus = display_value(0,291,60,50,30,-220,have_bg = False)
    asteroid_minus = display_value(0,291,60,50,30,220,have_bg = False)
    asteroid_value = display_value(0,291,140,50,30)

    blackhole_plus = display_value(0,414,60,50,30,-220,have_bg = False)
    blackhole_minus = display_value(0,414,60,50,30,220,have_bg = False)
    blackhole_value = display_value(0,414,140,50,30)

    asteroidplus = display_value(0,536,60,50,30,-220,have_bg = False)
    asteroidminus = display_value(0,536,60,50,30,220,have_bg = False)
    asteroidvalue = display_value(0,536,140,50,30)

    constellation_plus = display_value(0,661,60,50,30,110,have_bg = False)
    constellation_minus = display_value(0,661,60,50,30,550,have_bg = False)
    constellation_value = display_value(0,661,140,50,30,330)

    constsize_minus = display_value(0,661,60,50,30,-110,have_bg = False)
    constsize_plus = display_value(0,661,60,50,30,-550,have_bg = False)
    constsize_value = display_value(0,661,140,50,30,-330,have_bg = False)

    done_selecting  = display_value(0,741,280,50,30,have_bg = False)

    for i in stars:
        i.draw(screen)

    blank_overlay(screen)

    text(0,33,60,'SOLAR SYSTEM GENERATOR',True).draw(screen)
    text(0,120,30,'MOON OCCURENCE',True).draw(screen)
    text(0,245,30,'ASTEROID BELT OCCURENCE',True).draw(screen)
    text(0,368,30,'CHANCE OF ASTEROID FALLING (EVERY SECOND)',True).draw(screen)
    text(0,490,30,'AMOUNT OF PLANETS',True).draw(screen)
    text(0,615,30,'CONSTELLATION AMOUNT | SIZE OF CONSTELLATIONS',True).draw(screen)

# DRAWS MENU ----------------------------------------------------------------------------------------------------#
    moon_value.draw(screen,moon_percentage)
    moon_plus.draw(screen,'+')
    moon_minus.draw(screen,'-')

    asteroid_value.draw(screen,asteroidbelt_chance)
    asteroid_plus.draw(screen,'+')
    asteroid_minus.draw(screen,'-')

    blackhole_value.draw(screen,asteroid_chance)
    blackhole_plus.draw(screen,'+')
    blackhole_minus.draw(screen,'-')

    asteroidvalue.draw(screen,planet_amount,multiply_amount = (1,''))
    asteroidplus.draw(screen,'+')
    asteroidminus.draw(screen,'-')

    constellation_value.draw(screen,constellation_amount,multiply_amount = (1,''))
    constellation_plus.draw(screen,'+')
    constellation_minus.draw(screen,'-')

    constsize_value.draw(screen,constellation_size,multiply_amount = (1,''))
    constsize_plus.draw(screen,'+')
    constsize_minus.draw(screen,'-')

    done_selecting.draw(screen,'BEGIN SIMULATION')

# CHECKS FOR CLICK EVENTS ----------------------------------------------------------------------------------------------------#
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type is pygame.MOUSEBUTTONDOWN:
            if moon_plus.on_mouse_click() and moon_percentage < 0.9:  moon_percentage += 0.1
            elif moon_minus.on_mouse_click() and moon_percentage > 0.1: moon_percentage -= 0.1

            if asteroid_plus.on_mouse_click() and asteroidbelt_chance < 1:  asteroidbelt_chance += 0.1
            elif asteroid_minus.on_mouse_click() and asteroidbelt_chance > 0.1: asteroidbelt_chance -= 0.1

            if blackhole_plus.on_mouse_click() and asteroid_chance < 1:  asteroid_chance += 0.05
            elif blackhole_minus.on_mouse_click() and asteroid_chance > 0.1: asteroid_chance -= 0.05

            if asteroidplus.on_mouse_click(): planet_amount += 1
            elif asteroidminus.on_mouse_click() and planet_amount > 1: planet_amount -= 1

            if constellation_plus.on_mouse_click(): constellation_amount += 1
            elif constellation_minus.on_mouse_click() and constellation_amount > 1: constellation_amount -= 1

            if constsize_plus.on_mouse_click(): constellation_size += 10
            elif constsize_minus.on_mouse_click() and constellation_size > 10: constellation_size -= 10

            in_menu = not done_selecting.on_mouse_click()

    pygame.time.Clock().tick_busy_loop(40)
    pygame.display.flip()


# GENERATES SOLAR SYSTEM BASED ON VALUES ENTERED ----------------------------------------------------------------------------------------------------#
blackhole_generate = random()
asteroidbelt_generate = random()
generate_system(screen.get_width(),screen.get_height(),planet_amount)
if blackhole_chance > blackhole_generate:
    choice(planets).transform_blackhole()
if asteroidbelt_chance > asteroidbelt_generate:
    picked = choice(planets)
    while picked.moon_enable:
        picked = choice(planets)
    picked.has_belt = True

# APPENDS CONSTELLATIONS TO LIST, CREATES THEM RANDOMLY ----------------------------------------------------------------------------------------------------#
for x in range(constellation_amount):
    posx = randint(0,screen.get_width()-100)
    posy = randint(0,screen.get_height()-100)
    angle  = randint(0,30)
    constellation.append(generate_constellation(posx, posy, angle , constellation_size, 7))


# MAIN SOLAR SYSTEM LOOP ----------------------------------------------------------------------------------------------------#
while True:
    screen.fill(DBLUE)
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # DRAWS SOLAR SYSTEM AND STARS ----------------------------------------------------------------------------------------------------#
    for v in solar_circles:
        pygame.gfxdraw.aacircle(screen,screen.get_width()//2,screen.get_height()//2,v,(255,255,255,100))

    for i in stars:
        i.draw(screen)

    # DRAWS CONSTELLATIONS ----------------------------------------------------------------------------------------------------#
    draw_constellations(screen)

    # DRAWS PLANETS & MOVES THEM, ALSO CHECKS ASTEROID COLLISION ----------------------------------------------------------------------------------------------------#
    for x in planets:
        x.draw(screen)
        if x.blackhole:
            for o,z in enumerate(planets):
                if x.get_rect().colliderect(z.get_rect()) and not z.blackhole:
                    del planets[o]

    # CHECKS ASTEROID COLLISION ----------------------------------------------------------------------------------------------------#
    if len(asteroids) is not 0:
        for z,c in enumerate(asteroids):
            if c.check_collision(screen):
                del asteroids[z]

    # GENERATES ASTEROID ----------------------------------------------------------------------------------------------------#
    asteroid_generate = random()
    if asteroid_chance/10 > asteroid_generate:
        asteroids.append(create_asteroid(randint(100,screen.get_width()+200),0))

    pygame.draw.circle(screen,(230,230,0),(screen.get_width()//2,screen.get_height()//2),200//planet_amount)
    pygame.time.Clock().tick_busy_loop(30)
    pygame.display.update()
