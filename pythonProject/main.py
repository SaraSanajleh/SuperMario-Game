from pygame import *
import pygame ,sys
from pygame.display import *
from pygame.locals import *
from geometry import *
import imageio
import pickle
from os import path
from pygame import mixer

pygame.mixer.pre_init(44100,16,2,512)
mixer.init()
pygame.init()
Display_screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("SUPER MARIO")
c= pygame.time.Clock()
time=60
p=pygame.image.load('player.png')
pygame.display.set_icon(p)
player=pygame.image.load('player.png')
sun_img=pygame.image.load('img/sun.png')
bg_img=pygame.image.load('icons/1000_F_246986936_4InndMgg5SEBXEDIi1vmjvbygQODccZX.jpg')
restart_img=pygame.image.load('img/restart_btn.png')
start_img=pygame.image.load('img/start_btn.png')
exit_img=pygame.image.load('img/exit_btn.png')

size=36
lose=0
main_menu = True
level= 0
max_levels=7
counter=0
font = pygame.font.SysFont('Bauhaus 93', 70)
font_counter = pygame.font.SysFont('Bauhaus 93', 30)
white = (255, 255, 255)
blue = (0, 0, 255)

pygame.mixer.music.load('sound/Stage Win (Super Mario) - QuickSounds.com.mp3')
pygame.mixer.music.play(-1,0.0,5000)
money_fx = pygame.mixer.Sound('img/coin.wav')
money_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
lose_fx = pygame.mixer.Sound('sound/mixkit-cartoon-whistle-game-over-606.wav')
lose_fx.set_volume(0.5)
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	Display_screen.blit(img, (x, y))
def reset_level(level):
    PLAYER.reset(100, height - 130)
    turtle_group.empty()
    #fire_group.empty()
    exit_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = fun(world_data)
    return world
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        Display_screen.blit(self.image, self.rect)

        return action
class gamer():
    def __init__(self,x,y):
        self.reset(x,y)

    def chang(self,lose):
        dx=0
        dy=0
        walk=5
        col=20

        if lose == 0:
            point=pygame.key.get_pressed()
            if point[pygame.K_SPACE] and self.jump == False and self.in_air==False :
                jump_fx.play()
                self.y = - 15
                self.jump = True
            if point[pygame.K_SPACE] == False:
                self.jump = False
            if point[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if point[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if point[pygame.K_LEFT] == False and point[pygame.K_RIGHT]==False:
                self.counter=0
                self.index=0
                if self.direction == 1:
                    self.image = self.p_right[self.index]
                if self.direction == -1:
                    self.image = self.p_left[self.index]

            if self.counter > walk:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.p_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.p_right[self.index]
                if self.direction == -1:
                    self.image=self.p_left[self.index]

            self.y += 1
            if self.y >10:
                self.y=10
            dy += self.y

            self.in_air = True

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx=0

                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                    if self.y < 0:
                        dy=tile[1].bottom - self.rect.top
                        self.y = 0
                    elif self.y >= 0:
                        dy=tile[1].top - self.rect.bottom
                        self.y=0
                        self.in_air = False

            if pygame.sprite.spritecollide(self,turtle_group,False):
                lose = -1
                lose_fx.play()

            if pygame.sprite.spritecollide(self,fire_group,False):
                lose = -1
                lose_fx.play()

            if pygame.sprite.spritecollide(self, exit_group, False):
                lose = 1
            elif lose == -1:
                self.image=self.dead_img
                draw_text("GAME OVER!",font,blue,(width//2)-200,height//2)
                if self.rect.y >200:
                    self.rect.y -= 5

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x , self.rect.y +dy, self.width, self.height):
                    if abs((self.rect.top+dy)-platform.rect.bottom) < col:
                        self.y=0
                        dy=platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom+dy)- platform.rect.top)<col:
                        self.rect.bottom= platform.rect.top-1
                        self.in_air=False
                        dy=0
                    if platform.move_x !=0:
                        self.rect.x += platform.move_direction
            self.rect.x += dx
            self.rect.y += dy

        Display_screen.blit(self.image,self.rect)
        #pygame.draw.rect(Display_screen,(255,255,255),self.rect,2)

        return lose

    def reset(self,x,y):
        self.p_right = []
        self.p_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            player = pygame.image.load(f'img/guy{num}.png')
            player = pygame.transform.scale(player, (28, 100))
            img_left = pygame.transform.flip(player, True, False)
            self.p_right.append(player)
            self.p_left.append(img_left)
        self.dead_img = pygame.image.load('img/ghost.png')
        self.image = self.p_right[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = 0
        self.jump = False
        self.direction = 0
        self.in_air= True
class Turtle(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y,move_x,move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image=pygame.transform.scale(img,(size, size//2 ))
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y =y
        self.move_counter=0
        self.move_direction= 1
        self.move_x=move_x
        self.move_y = move_y
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Money(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('img/coin.png')
            self.image = pygame.transform.scale(img, (size , size ))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('img/exit.png')
            self.image = pygame.transform.scale(img, (size, int(size * 2.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

turtle_group=pygame.sprite.Group()
platform_group = pygame.sprite.Group()
fire_group=pygame.sprite.Group()
money_group=pygame.sprite.Group()
exit_group = pygame.sprite.Group()
counter_money=Money(size//2,size//2)
money_group.add(counter_money)
class fun():
    def __init__(self,data):
        self.tile_list=[]
        d_img=pygame.image.load('img/dirt.png')
        grass_img=pygame.image.load('icons/grass.png')
        r_count=0
        for row in data:
            c_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(d_img,(size,size))
                    img_rect = img.get_rect()
                    img_rect.x = c_count * size
                    img_rect.y=  r_count * size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img=pygame.transform.scale(grass_img,(size,size))
                    img_rect=img.get_rect()
                    img_rect.x = c_count * size
                    img_rect.y=  r_count * size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    turtle = Turtle(c_count * size, r_count * size + 15)
                    turtle_group.add(turtle)
                if tile == 4:
                    platform=Platform(c_count * size, r_count * size,1,0)
                    platform_group.add(platform)
                if tile ==5:
                    platform = Platform(c_count * size, r_count * size,0,1)
                    platform_group.add(platform)
                if tile == 6:
                    fire = Fire(200,610)
                    fire_group.add(fire)
                    fire1=Fire(350,610)
                    fire_group.add(fire1)

                if tile == 7:
                    money = Money(c_count * size+ (size // 2), c_count * size + (size // 2))
                    money_group.add(money)
                if tile == 8:
                    exit = Exit(c_count * size, r_count * size - (size // 2))
                    exit_group.add(exit)
                c_count+=1
            r_count+=1
    def draw(self):
        for tile in self.tile_list:
            Display_screen.blit(tile[0], tile[1])
            #pygame.draw.rect(Display_screen,(255,255,255),tile[1],2)
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)

world = fun(world_data)
PLAYER=gamer(100,height - 130)
restart_button=Button(width//2 - 50 , height//2 + 100,restart_img)
star_button=Button(width//2 - 350 , height//2 ,start_img)
exit_button = Button(width // 2 + 150, height // 2, exit_img)

run=True
while run:
    c.tick(time)
    Display_screen.blit(bg_img,(0,0))
    Display_screen.blit(sun_img, (100, 100))
    if main_menu == True:
        if exit_button.draw():
            run=False
        if star_button.draw():
            main_menu=False
    else:
        world.draw()
        if lose == 0:
            turtle_group.update()
            platform_group.update()
            if pygame.sprite.spritecollide(PLAYER,money_group,True):
                counter+=1
                money_fx.play()
            draw_text('x '+str(counter),font_counter,white,size-10,10)
        turtle_group.draw(Display_screen)
        platform_group.draw(Display_screen)
        fire_group.draw(Display_screen)
        money_group.draw(Display_screen)
        exit_group.draw(Display_screen)

        lose = PLAYER.chang(lose)

        if lose == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                lose = 0
                counter = 0

        if lose == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                lose = 0
            else:
                draw_text('YOU WIN!', font, blue, (width // 2) - 140, height // 2)
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    lose = 0
                    counter = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()








