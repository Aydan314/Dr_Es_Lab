import pygame
import random
import math
pygame.init()
win=pygame.display.set_mode((800,800))
pygame.display.set_caption('Dr G`s Lab')
class player(object):
    def __init__(self,x,y,width,height,max_health,fire_rate,crit_chance,damage):
        self.x=x
        self.y=y
        self.dead=False
        self.width=width
        self.key=False
        self.height=height
        self.speed=4
        self.fire_rate=fire_rate
        self.shootcooldown=fire_rate
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.intrest_rect=pygame.Rect(self.x-200,self.y-200,self.width+400,self.height+400)
        self.upRect=pygame.Rect(self.x,self.y-4,self.width,self.height)
        self.downRect=pygame.Rect(self.x,self.y+4,self.width,self.height)
        self.rightRect=pygame.Rect(self.x,self.y,self.width+4,self.height)
        self.leftRect=pygame.Rect(self.x-4,self.y,self.width,self.height)
        self.down=False
        self.up=False
        self.left=False
        self.right=False
        self.max_health=max_health
        self.health=max_health
        self.crit_chance=crit_chance
        self.damage=damage
        if self.damage==20:
            self.gun='T1 Lazer Pistol'
        elif self.damage==25:
            self.gun='T2 Blaster Pistol'
        elif self.damage==30:
            self.gun='T3 Pulse Rifle'
        elif self.damage==35:
            self.gun='T4 Burst Repeater'
        elif self.damage >= 40:
            self.gun='T5 Plasma Minigun'
    def draw(self,win):
        if self.damage==20:
            self.gun='T1 Lazer Pistol'
        elif self.damage==25:
            self.gun='T2 Blaster Pistol'
        elif self.damage==30:
            self.gun='T3 Pulse Rifle'
        elif self.damage==35:
            self.gun='T4 Burst Repeater'
        elif self.damage >= 40:
            self.gun='T5 Plasma Minigun'
        if self.key:
            win.blit(pygame.image.load('key 1.png'),(self.x,self.y-30))
        self.intrest_rect=pygame.Rect(self.x-200,self.y-200,self.width+400,self.height+400)
        self.upRect=pygame.Rect(self.x,self.y-4,self.width,self.height+4)
        self.downRect=pygame.Rect(self.x,self.y,self.width,self.height+4)
        self.rightRect=pygame.Rect(self.x,self.y,self.width+4,self.height)
        self.leftRect=pygame.Rect(self.x-4,self.y,self.width+4,self.height)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        if self.up:
            character=pygame.image.load('character back.png')
        elif self.left:
            character=pygame.image.load('character left.png')
        elif self.right:
            character=pygame.image.load('character right.png')
        else:
            character=pygame.image.load('character forward.png')
        #pygame.draw.rect(win,(255,0,0),self.intrest_rect,1)
        #pygame.draw.rect(win,(255,255,0),self.upRect,1)
        #pygame.draw.rect(win,(255,0,255),self.downRect,1)
        #pygame.draw.rect(win,(0,255,0),self.rightRect,1)
        #pygame.draw.rect(win,(0,0,255),self.leftRect,1)
        win.blit(character,(self.x,self.y))

class lazer(object):
    def __init__(self,x,y,colour,entity):
        self.entity=entity
        self.x=x
        self.y=y
        self.point=pygame.Rect(self.x,self.y,1,1)
        self.colour=colour
        self.velocity=20
        self.time=40
        self.pos=0
        self.xpoint=player.x+round(player.width/2)
        self.ypoint=player.y+round(player.height/2)
        self.x_diff=(self.xpoint-self.x)
        self.y_diff=(self.ypoint-self.y)
        angle=math.atan2(self.y_diff, self.x_diff)
        self.x = self.xpoint - round(math.cos(angle) * self.velocity)
        self.y = self.ypoint - round(math.sin(angle) * self.velocity)
    def draw(self,win):
        self.point=pygame.Rect(self.x,self.y,1,1)
        pygame.draw.line(win,(self.colour),(self.x,self.y),(self.xpoint,self.ypoint),3)
        self.time-=1
        angle=math.atan2(self.y_diff, self.x_diff)
        self.x -= round(math.cos(angle) * self.velocity)
        self.y -= round(math.sin(angle) * self.velocity)
        self.xpoint -= round(math.cos(angle) * self.velocity)
        self.ypoint -= round(math.sin(angle) * self.velocity)

class tile(object):
    def __init__(self,x,y,width,height,varient,facing):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.open=False
        self.facing=facing
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.crate_strength=2
        self.contacted=False
        self.interact_icon=pygame.image.load('interact icon.png')
        self.interact_icon_active=pygame.image.load('interact icon active.png')
    def draw(self,win):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        key=pygame.key.get_pressed()
        if self.facing=='up':
            block=pygame.image.load(self.varient+' up.png')
        elif self.facing=='left':
            block=pygame.image.load(self.varient+' left.png')
        elif self.facing=='right':
            block=pygame.image.load(self.varient+' right.png')
        elif self.facing=='down':
            block=pygame.image.load(self.varient+' down.png')
        elif self.varient=='crate':
            if self.crate_strength==2:
                block=pygame.image.load('crate.png')
            elif self.crate_strength <= 1:
                block=pygame.image.load('crate broken.png')
        elif self.varient=='box':
            if self.crate_strength==2:
                block=pygame.image.load('box.png')
            elif self.crate_strength <= 1:
                block=pygame.image.load('box broken.png')
        else:
            block=pygame.image.load(self.varient+'.png')
        if self.varient=='wall' and self.facing=='left':
            self.rect=pygame.Rect(self.x+64,self.y,self.width,self.height)
            win.blit(block,(self.x+64,self.y))
        elif self.varient=='wall' and self.facing=='up':
            self.rect=pygame.Rect(self.x,self.y+60,self.width,self.height)
            win.blit(block,(self.x,self.y))
        elif self.varient=='door':
            self.rect=pygame.Rect(self.x,self.y+60,self.width,self.height)
            win.blit(block,(self.x,self.y))
            if self.rect.colliderect(player.downRect):
                win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y+10))
                if key[pygame.K_e]:
                    win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y+10))
                    if enemy_list!=[]:
                        if not self.contacted:
                            if not loading_room:
                                if not speaking:
                                    text('Butl3r','The door wont open')
                    else:
                        next_room()
                    self.contacted=True
                else:
                    self.contacted=False
                
        elif self.varient=='entrance':
            win.blit(block,(self.x,self.y))
            if self.rect.colliderect(player.upRect):
                win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y+20))
                if key[pygame.K_e]:
                    win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y+20))
                    if not self.contacted:
                        if not speaking:
                            text('Butl3r','This door is shut tight!')
                            self.contacted=True
            else:
                self.contacted=False

        elif self.varient=='shop':
            win.blit(block,(self.x,self.y))
            if self.rect.colliderect(player.upRect):
                win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y+20))
                if key[pygame.K_e]:
                    win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y+20))
                    if not self.contacted:
                        global in_shop
                        in_shop=True
                        self.contacted=True
            else:
                self.contacted=False
                
        elif self.varient=='chest':
            if self.open:
                block=pygame.image.load('chest open.png')
            win.blit(block,(self.x,self.y))
            if not self.open:
                if self.rect.colliderect(player.upRect):
                    win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y-40))
                    if key[pygame.K_e]:
                        win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y-40))
                        if not self.contacted:
                            if player.key:
                                if not self.open:
                                    num=random.randint(3,5)
                                    no=0
                                    for no in range(0,num):
                                        decor_list.append(decor(self.x-30+(no*5),self.y+50,20,20,'microchip'))
                                    decor_list.append(decor(self.x+self.width+30,self.y+50,20,20,'repair kit'))
                                    self.open=True
                                    player.key=False
                            else:
                                if not speaking:
                                    text('Butl3r','I need a key')
                            self.contacted=True
                else:
                    self.contacted=False
        elif self.varient=='railing':
            self.rect=pygame.Rect(self.x,self.y+40,self.width,self.height)
            win.blit(block,(self.x,self.y+40))
            
        else:
            win.blit(block,(self.x,self.y))

class decor(object):
    def __init__(self,x,y,width,height,varient):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.frame=1
        self.framecooldown=30
        self.frameup=True
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
    def draw(self,win):
        if self.varient=='lava':
            if self.framecooldown==0:
                self.frame+=1
                if self.frame==5:
                    self.frame=1
                self.framecooldown=30
            else:
                self.framecooldown-=1
            img=pygame.image.load(self.varient+' '+str(self.frame)+'.png')
            if self.y%160==0:
                img=(pygame.transform.rotate(img,180))
            if player.rect.colliderect(self.rect):
                if self.framecooldown==0:
                    damage('player',20,1)

        elif self.varient=='microchip':
            if self.frame==5:
                self.frameup=False
            elif self.frame==1:
                self.frameup=True
                     
            if self.frameup:
                if self.framecooldown==0:
                    self.frame+=1
                    self.framecooldown=3
            else:
                if self.framecooldown==0:
                    self.frame-=1
                    self.framecooldown=3
            if self.framecooldown!=0:
                self.framecooldown-=1
            img=pygame.image.load('microchip '+str(self.frame)+'.png')

        elif self.varient=='repair kit':
            if self.frame==5:
                self.frameup=False
            elif self.frame==1:
                self.frameup=True
                     
            if self.frameup:
                if self.framecooldown==0:
                    self.frame+=1
                    self.framecooldown=3
            else:
                if self.framecooldown==0:
                    self.frame-=1
                    self.framecooldown=3
            if self.framecooldown!=0:
                self.framecooldown-=1
            img=pygame.image.load('repair kit '+str(self.frame)+'.png')

        elif self.varient=='key':
            if self.frame==5:
                self.frameup=False
            elif self.frame==1:
                self.frameup=True
                     
            if self.frameup:
                if self.framecooldown==0:
                    self.frame+=1
                    self.framecooldown=4
            else:
                if self.framecooldown==0:
                    self.frame-=1
                    self.framecooldown=4
            if self.framecooldown!=0:
                self.framecooldown-=1
            img=pygame.image.load('key '+str(self.frame)+'.png')

        else:
            img=pygame.image.load(self.varient+'.png')
        win.blit(img,(self.x,self.y))

class enemy(object):
    def __init__(self,x,y,width,height,varient,max_health,identity,hit_rate):
        self.x=x
        self.y=y
        self.identity=identity
        self.height=height
        self.width=width
        self.varient=varient
        self.attack_cooldown=hit_rate
        self.hit_rate=hit_rate
        self.speed=2
        self.movecooldown=80
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.upRect=pygame.Rect(self.x,self.y-4,self.width,self.height)
        self.downRect=pygame.Rect(self.x,self.y+4,self.width,self.height)
        self.rightRect=pygame.Rect(self.x,self.y,self.width+4,self.height)
        self.leftRect=pygame.Rect(self.x-4,self.y,self.width,self.height)
        self.max_health=max_health
        self.health=max_health
        self.facing=1
        self.frame=0
        self.exploded=False
        font=pygame.font.SysFont('ocr a extended',10)
        self.name=font.render(varient,2,(255,255,255))
    def draw(self,win):
        if self.frame==20:
            self.frame=0
        else:
            self.frame+=1
        attack_player=False
        if self.rect.colliderect(player.intrest_rect):
            attack_player=True
        if self.attack_cooldown!=0:
            self.attack_cooldown-=1
        contact_player=False
        if self.rect.colliderect(player.rect):
            contact_player=True
            if self.attack_cooldown==0:
                self.attack_cooldown=self.hit_rate
                if not speaking:
                    if self.varient=='C4PO':
                        damage('player',50,2)
                        self.exploded=True
                    else:
                        damage('player',20,1)
        contact_enemy=False
        for item in enemy_list:
            if item.rect.colliderect(self.rect):
                if item.identity!=self.identity:
                    contact_enemy=True
        pygame.draw.rect(win,(230,20,20),(self.x,self.y-10,self.width,5))
        if self.health >= 0:
            pygame.draw.rect(win,(20,230,20),(self.x,self.y-10,round((self.health/self.max_health)*self.width),5))
        win.blit(self.name,(self.x,self.y-20))
        can_up=True
        can_down=True
        can_left=True
        can_right=True
        if self.movecooldown==0:
            if not attack_player:
                self.facing=random.randint(1,5)
                self.movecooldown=80
            elif contact_enemy:
                self.facing=random.randint(1,5)
                self.movecooldown=80  
            else:
                if player.y < self.y:
                    self.facing=1
                if player.x > self.x:
                    self.facing=3
                if player.x < self.x:
                    self.facing=2
                if player.y > self.y:
                    self.facing=4
                self.move_cooldown=4
        else:
            self.movecooldown-=1
        self.upRect=pygame.Rect(self.x,self.y-4,self.width,self.height+4)
        self.downRect=pygame.Rect(self.x,self.y,self.width,self.height+4)
        self.rightRect=pygame.Rect(self.x,self.y,self.width+4,self.height)
        self.leftRect=pygame.Rect(self.x-4,self.y,self.width+4,self.height)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        if self.facing==1:
            if attack_player:
                if self.frame > 10:
                    character=pygame.image.load(self.varient+' back.png')
                else:
                    character=pygame.image.load(self.varient+' back attack.png')
            else:
                character=pygame.image.load(self.varient+' back.png')
        elif self.facing==2:
            if attack_player:
                if self.frame > 10:
                    character=pygame.image.load(self.varient+' left.png')
                else:
                    character=pygame.image.load(self.varient+' left attack.png')
            else:
                character=pygame.image.load(self.varient+' left.png')
        elif self.facing==3:
            if attack_player:
                if self.frame > 10:
                    character=pygame.image.load(self.varient+' right.png')
                else:
                    character=pygame.image.load(self.varient+' right attack.png')
            else:
                character=pygame.image.load(self.varient+' right.png')
        else:
            if attack_player:
                if self.frame > 10:
                    character=pygame.image.load(self.varient+' forward.png')
                else:
                    character=pygame.image.load(self.varient+' forward attack.png')
            else:
                character=pygame.image.load(self.varient+' forward.png')
        if not speaking:       
            if self.facing!=5:
                if self.facing==1:
                    for item in level_list:
                        if self.upRect.colliderect(item.rect):
                            can_up=False
                    for item in decor_list:
                        if item.varient=='lava':
                            if self.upRect.colliderect(item.rect):
                                can_up=False
                    if can_up:
                        if not contact_player:
                            self.y-=self.speed
                            
                elif self.facing==2:
                    for item in level_list:
                        if self.leftRect.colliderect(item.rect):
                            can_left=False
                    for item in decor_list:
                        if item.varient=='lava':
                            if self.leftRect.colliderect(item.rect):
                                can_left=False
                    if can_left:
                        if not contact_player:
                            self.x-=self.speed
                            
                elif self.facing==3:
                    for item in level_list:
                        if self.rightRect.colliderect(item.rect):
                            can_right=False
                    for item in decor_list:
                        if item.varient=='lava':
                            if self.rightRect.colliderect(item.rect):
                                can_right=False
                    if can_right:
                        if not contact_player:
                            self.x+=self.speed
                            
                else:
                    for item in level_list:
                        if self.downRect.colliderect(item.rect):
                            can_down=False
                    for item in decor_list:
                        if item.varient=='lava':
                            if self.downRect.colliderect(item.rect):
                                can_down=False
                    if can_down:
                        if not contact_player:
                            self.y+=self.speed
        #pygame.draw.rect(win,(255,0,0),self.rect)
        #pygame.draw.rect(win,(255,255,0),self.upRect,1)
        #pygame.draw.rect(win,(255,0,255),self.downRect,1)
        #pygame.draw.rect(win,(0,255,0),self.rightRect,1)
        #pygame.draw.rect(win,(0,0,255),self.leftRect,1)
        win.blit(character,(self.x,self.y))

class button(object):
    def __init__(self,x,y,width,height,function):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.function=function
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.buyRect=pygame.Rect(self.x+20,self.y+500,self.width-40,60)
        self.image=pygame.image.load('shop '+function+'.png')
        self.microicon=pygame.image.load('microchip icon.png')
        self.cooldown=0
        self.price=0
        self.purchased=0
        self.limit=False
    def draw(self,win):
        global microchips
        global repair_kits
        mouse_pos=pygame.mouse.get_pos()
        pygame.draw.rect(win,(100,100,100),self.rect)
        pygame.draw.rect(win,(50,50,50),self.buyRect)
        win.blit(self.image,(self.x+25,self.y+25))
        bigfont=pygame.font.SysFont('ocr a extended',40)
        smallfont=pygame.font.SysFont('ocr a extended',30)
        qsmallfont=pygame.font.SysFont('ocr a extended',23)
        vsmallfont=pygame.font.SysFont('ocr a extended',18)
        if self.function=='health':
            if player.health < 200:
                self.price=50
            else:
                self.price=0
                self.limit=True
            win.blit(smallfont.render('Health Boost',3,(255,255,255)),(self.x+10,self.y+350))
            win.blit(vsmallfont.render('+10 Permanent Health',1,(255,255,255)),(self.x+10,self.y+400))
        elif self.function=='repair kit':
            self.price=20
            win.blit(smallfont.render('Repair Kit',3,(255,255,255)),(self.x+10,self.y+350))
            win.blit(vsmallfont.render('Heals 50 health',1,(255,255,255)),(self.x+10,self.y+400))
        elif self.function=='gun':
            if player.gun=='T1 Lazer Pistol':
                win.blit(pygame.image.load('T2 Blaster Pistol shop.png'),(self.x+25,self.y+50))
                self.price=100
                win.blit(qsmallfont.render('T2 Blaster Pistol',3,(255,255,255)),(self.x+10,self.y+350))
                win.blit(vsmallfont.render('25 Damage',1,(255,255,255)),(self.x+10,self.y+400))
                win.blit(vsmallfont.render('70 Reload Delay',1,(255,255,255)),(self.x+10,self.y+420))
                win.blit(vsmallfont.render('1/45 Crit Chance',1,(255,255,255)),(self.x+10,self.y+440))
            elif player.gun=='T2 Blaster Pistol':
                win.blit(pygame.image.load('T3 Pulse Rifle shop.png'),(self.x+25,self.y+50))
                self.price=200
                win.blit(qsmallfont.render('T3 Pulse Rifle',3,(255,255,255)),(self.x+10,self.y+350))
                win.blit(vsmallfont.render('30 Damage',1,(255,255,255)),(self.x+10,self.y+400))
                win.blit(vsmallfont.render('50 Reload Delay',1,(255,255,255)),(self.x+10,self.y+420))
                win.blit(vsmallfont.render('1/40 Crit Chance',1,(255,255,255)),(self.x+10,self.y+440))
            elif player.gun=='T3 Pulse Rifle':
                win.blit(pygame.image.load('T4 Burst Repeater shop.png'),(self.x+25,self.y+50))
                self.price=300
                win.blit(qsmallfont.render('T4 Burst Repeater',3,(255,255,255)),(self.x+10,self.y+350))
                win.blit(vsmallfont.render('35 Damage',1,(255,255,255)),(self.x+10,self.y+400))
                win.blit(vsmallfont.render('35 Reload Delay',1,(255,255,255)),(self.x+10,self.y+420))
                win.blit(vsmallfont.render('1/35 Crit Chance',1,(255,255,255)),(self.x+10,self.y+440))
            elif player.gun=='T4 Burst Repeater':
                win.blit(pygame.image.load('T5 Plasma Minigun shop.png'),(self.x+25,self.y+50))
                self.price=400
                win.blit(qsmallfont.render('T5 Plasma Minigun',3,(255,255,255)),(self.x+10,self.y+350))
                win.blit(vsmallfont.render('40 Damage',1,(255,255,255)),(self.x+10,self.y+400))
                win.blit(vsmallfont.render('20 Reload Delay',1,(255,255,255)),(self.x+10,self.y+420))
                win.blit(vsmallfont.render('1/20 Crit Chance',1,(255,255,255)),(self.x+10,self.y+440))
            else:
                self.limit=True
                win.blit(pygame.image.load('T5 Plasma Minigun shop.png'),(self.x+25,self.y+50))
                self.price=0
                win.blit(qsmallfont.render('T5 Plasma Minigun',3,(255,255,255)),(self.x+10,self.y+350))
                win.blit(vsmallfont.render('40 Damage',1,(255,255,255)),(self.x+10,self.y+400))
                win.blit(vsmallfont.render('20 Reload Delay',1,(255,255,255)),(self.x+10,self.y+420))
                win.blit(vsmallfont.render('1/20 Crit Chance',1,(255,255,255)),(self.x+10,self.y+440))


        if not self.limit:    
            if self.price > microchips:
                pricetext=bigfont.render(str(self.price),2,(220,20,20))
            else:
                pricetext=bigfont.render(str(self.price),2,(20,220,20))
            win.blit(self.microicon,(self.x+25,self.y+510))
            win.blit(pricetext,(self.x+65,self.y+510))
        else:
            win.blit(smallfont.render('Max Reached',4,(230,20,20)),(self.x+25,self.y+510))
            
        if self.cooldown!=0:
            self.cooldown-=1
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(win,(50,50,50),self.rect,4)
            if self.buyRect.collidepoint(mouse_pos):
                pygame.draw.rect(win,(250,250,250),self.buyRect,2)
                if not self.limit:
                    if pygame.mouse.get_pressed()[0]:
                        if self.price > microchips:
                            pygame.draw.rect(win,(250,0,0),self.buyRect,2)
                        else:
                            pygame.draw.rect(win,(0,0,250),self.buyRect,2)
                            if self.cooldown==0:
                                microchips-=self.price
                                self.cooldown=40
                                replace_line('Player Data.txt',4,'Microchips: '+str(microchips))
                                if self.function=='health':
                                    player.max_health+=10
                                    player.health=player.max_health
                                    replace_line('Player Data.txt',0,'Health: '+str(player.max_health))
                                if self.function=='repair kit':
                                    repair_kits+=1
                                    replace_line('Player Data.txt',5,'Repair Kits: '+str(repair_kits))
                                if self.function=='gun':
                                    if player.gun=='T1 Lazer Pistol':
                                        player.damage=25
                                        player.fire_rate=70
                                        player.crit_chance=45
                                    elif player.gun=='T2 Blaster Pistol':
                                        player.damage=30
                                        player.fire_rate=50
                                        player.crit_chance=40
                                    elif player.gun=='T3 Pulse Rifle':
                                        player.damage=35
                                        player.fire_rate=35
                                        player.crit_chance=35
                                    elif player.gun=='T4 Burst Repeater':
                                        player.damage=40
                                        player.fire_rate=20
                                        player.crit_chance=20
                                    replace_line('Player Data.txt',1,'Damage: '+str(player.damage))
                                    replace_line('Player Data.txt',2,'Firing Rate: '+str(player.fire_rate))
                                    replace_line('Player Data.txt',3,'Crit Chance: '+str(player.crit_chance))
                                self.purchased=30
        if self.purchased!=0:           
            self.purchased-=0.25
            win.blit(smallfont.render('-'+str(self.price),1,(230,20,20)),(10,70-round(self.purchased)))
            
                            
                    
                
            

def death():
    win.fill((0,0,0))
    player.dead=True
    global room_num
    grave=pygame.image.load('tombstone.png')
    win.blit(grave,(player.x,player.y))
    dead_text=pygame.image.load('dead text.png')
    win.blit(dead_text,(0,300))
    pygame.display.update()
    pygame.time.delay(1200)
    player.health=60
    load_room(start_room)
    player.dead=False
    player.health=player.max_health
    player.x=400
    player.y=100

def damage(entity,amount,ID):
    global cooldown
    if cooldown==0:
        cooldown=1
        hurt=pygame.image.load('player hurt.png')
        crit=False
        if entity=='player':
            if not player.dead:
                if player.health > 0:
                    player.health-=amount        
                num=0
                run=True
                while run:
                    if num==20:
                        run=False
                    else:
                        if player.health > 0:
                            game_window()
                            if ID==2:
                                boom=pygame.image.load('explosion.png')
                                win.blit(boom,(player.x-20,player.y-20)) 
                            win.blit(hurt,(player.x,player.y))
                            font=pygame.font.SysFont('ocr a extended',20)
                            damage_num=font.render('-'+str(amount),1,(255,255,255))
                            win.blit(damage_num,(player.x,player.y-num)) 
                            pygame.display.update()
                        else:
                            for i in range(1,30):
                                game_window()
                                if ID==2:
                                    boom=pygame.image.load('explosion.png')
                                    win.blit(boom,(player.x-20,player.y-20))
                                pygame.display.update()
                                i+=1
                            death()
                            run=False
                        num+=1
                        
        if entity=='enemy':
            for item in enemy_list:
                if item.identity==ID:
                    item.health-=amount
                    num=0
                    run=True
                    while run:
                        if num==20:
                            run=False
                        else:
                            game_window()
                            win.blit(hurt,(item.x,item.y))
                            font=pygame.font.SysFont('ocr a extended',20)
                            font2=pygame.font.SysFont('ocr a extended',30)
                            if amount > player.damage:
                                if crit:
                                    damage_num=font2.render('-'+str(amount),3,(255,195,0))
                                else:
                                    damage_num=font2.render('-'+str(amount),3,(255,0,0))
                                crit=not crit
                                    
                            else:
                                damage_num=font.render('-'+str(amount),1,(255,255,255))
                            win.blit(damage_num,(item.x,item.y-num))
                            pygame.display.update()
                            num+=1
        
        
                
        
            
    
    
def text(name,speach):
    global speaking
    speaking=True
    transparent=pygame.image.load('speach bubble.png')
    font=pygame.font.SysFont('ocr a extended',30)
    speaker=font.render(name+':',2,(0,0,255))
    pos=0
    delay=2
    while pos < len(speach)+1:
        game_window()
        win.blit(transparent,(0,700))
        win.blit(speaker,(20,700))
        line=font.render(speach[0:pos],1,(0,0,0))
        win.blit(line,(20,740))
        pygame.display.update()
        if delay==0:
            pos+=1
            delay=2
        else:
            delay-=1
    delay=60
    while delay > 0:
        game_window()
        win.blit(transparent,(0,700))
        win.blit(speaker,(20,700))
        line=font.render(speach[0:pos],1,(0,0,0))
        win.blit(line,(20,740))
        pygame.display.update()
        delay-=1
    speaking=False
        
        
        
        
        
        
def game_window():
    global microchips
    global micro_cooldown
    global repair_kits
    win.fill((155,155,155))
    index=0
    for item in decor_list:
        item.draw(win)
        if item.varient=='microchip':
            if player.rect.colliderect(item.rect):
                if micro_cooldown==0:
                    micro_cooldown=20
                    decor_list.pop(index)
                    microchips+=1
                    replace_line('Player Data.txt',4,'Microchips: '+str(microchips))
        if item.varient=='repair kit':
            if player.rect.colliderect(item.rect):
                if micro_cooldown==0:
                    micro_cooldown=20
                    decor_list.pop(index)
                    repair_kits+=1
                    replace_line('Player Data.txt',5,'Repair Kits: '+str(repair_kits))
        if item.varient=='key':
            if player.rect.colliderect(item.rect):
                decor_list.pop(index)
                player.key=True
                        
        index+=1
    if micro_cooldown!=0:
        micro_cooldown-=1

    index=0  
    for item in projectile_list:
        item.draw(win)
        if item.time==0:
            projectile_list.pop(index)
        index2=0
        for tile in level_list:
            if tile.varient=='crate':
                if item.point.colliderect(tile.rect):
                    tile.crate_strength-=1
                if tile.crate_strength==0:
                    level_list.pop(index2)
            if tile.varient=='box':
                if item.point.colliderect(tile.rect):
                    tile.crate_strength-=1
                if tile.crate_strength==0:
                    level_list.pop(index2)
            if item.point.colliderect(tile.rect):
                if projectile_list!=[]:
                    projectile_list.pop(index)
            index2+=1
        index+=1

    for item in enemy_list:
        item.draw(win)
        index=0
        for bullet in projectile_list:
            if bullet.point.colliderect(item.rect):
                projectile_list.pop(index)
                num=random.randint(1,player.crit_chance)
                if num==1:
                    dam_num=player.damage*2
                else:
                    dam_num=player.damage  
                damage('enemy',dam_num,item.identity)
            index+=1
    index=0   
    for item in enemy_list:
        if item.health <= 0:
            if enemy_list!=[]:
                enemy_list.pop(index)
                decor_list.append(decor(item.x+20,item.y+20,20,20,'microchip'))
        if item.exploded:
            enemy_list.pop(index)
        index+=1
        
    for item in level_list:
        item.draw(win)
          
    if player.shootcooldown==0:
        crosshair=pygame.image.load('crosshair active.png')
    else:
        crosshair=pygame.image.load('crosshair.png')
    win.blit(crosshair,(mouse_pos[0]-20,mouse_pos[1]-20))
    pygame.draw.rect(win,(230,20,20),(580,10,200,20))
    if player.health > 0:
        pygame.draw.rect(win,(20,230,20),(580,10,round((player.health/player.max_health)*200),20))
    pygame.draw.rect(win,(255,255,255),(580,10,200,20),1)
    font=pygame.font.SysFont('ocr a extended',20)
    bigfont=pygame.font.SysFont('ocr a extended',40)
    health_text=font.render(str(player.health)+'/'+str(player.max_health),1,(255,255,255))
    room_text=bigfont.render('Room: '+str(room_num),1,(255,255,255))
    micros_text=bigfont.render(str(microchips),2,(20,255,20))
    micro_icon=pygame.image.load('microchip icon.png')
    win.blit(micro_icon,(218,5))
    win.blit(micros_text,(260,5))
    win.blit(room_text,(5,5))
    if player.health > 0:
        win.blit(health_text,(700,35))
    player.draw(win)
    if not loading_room:
        if not speaking:
            if not inventory:
                pygame.display.update()

start_room=('@VVVE VVV#',
            '>KCC   S <',
            '>P CBbbbb<',
            '@IIICCCCC<',
            '>LLCCC G <',
            '>LL   1  <',
            '>LL g  0 <',
            '>LL   VVV#',
            '>   0   g<',
            '+^^^D ^^^=')

def replace_line(file_name,line,text):
    if '.txt' not in file_name:
        file_name=file_name+'.txt'
    file=open(file_name,'r')
    read_file=file.readlines()
    read_file[line]=text+'\n'
    open(file_name,'w').close()
    file=open(file_name,'r+')
    for item in read_file:
        file.write(item)
    file.close()

def next_room():
    room_choice=random.randint(1,6)
    chest_room2=('@VVVE VVV#',
                '>B  g   C<',
                '>  1   CC<',
                '@VVV  VVV#',
                '> B    g <',
                '>   CIIII<',
                '>LL  0  K<',
                '>LL      <',
                '>K    C 1<',
                '+^^^D ^^^=')
    chest_room=('@VV#E VVV#',
                '>K <    B<',
                '> C< 0   <',
                '>0 <   g <',
                '>CC|     <',
                '>C |   G <',
                '@VVV     <',
                '>Sg   C  <',
                '>       1<',
                '+^^^D ^^^=')
    crate_room=('@VVVE VVV#',
                '>C C  C C<',
                '>C0C  C C<',
                '>C C  C C<',
                '>       0<',
                '>C G  VVV#',
                '>   C g  <',
                '>  0     <',
                '> C  0 C <',
                '+^^^D ^^^=')
    toasthead_room=('@VV#E VVV#',
                    '> 0<     <',
                    '>  <  gC <',
                    '>C |     <',
                    '>  |  0 0<',
                    '@VVV     <',
                    '>  C     <',
                    '>   VVVVV#',
                    '> 0    C <',
                    '+^^^D ^^^=')
    c4po_room=('@VVVE VVV#',
                    '>  C   1 <',
                    '>     g  <',
                    '> 1  VVVV#',
                    '>    |   <',
                    '> CC |   <',
                    '@VVVVV   <',
                    '>   g    <',
                    '> 1    C <',
                    '+^^^D ^^^=')
    lava_room=('@VVVE VVV#',
                    '>LL C   0<',
                    '>LL    C <',
                    '>   C    <',
                    '>LLLLLLLL<',
                    '>LLLLLLLL<',
                    '>  0   g <',
                    '>  C  LLL<',
                    '>  C 1LLL<',
                    '+^^^D ^^^=')
    if room_choice==1:
        load_room(crate_room)
    elif room_choice==2:
        load_room(c4po_room)
    elif room_choice==3:
        load_room(lava_room)
    elif room_choice==4:
        load_room(chest_room)
    elif room_choice==5:
        load_room(chest_room2)
    else:
        load_room(toasthead_room)
    

def load_room(room):
    global room_num
    player.x=400
    player.y=100
    if player.dead:
        room_num=1
    else:
        room_num+=1
    global loading_room
    loading_room=True
    global enemy_list
    global projectile_list
    global level_list
    global decor_list
    num=1
    while num < 410:
        pygame.draw.rect(win,(0,0,0),(0,0,num,800))
        pygame.draw.rect(win,(0,0,0),(800-num,0,400,800))
        pygame.display.update()
        num+=1
    pygame.time.delay(200)
    projectile_list=[]
    decor_list=[]
    enemy_list=[]
    level_list=[]
    x_pos=0
    y_pos=0
    num=0
    for row in room:
        for item in row:
            if item=='V':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'wall','down'))
            elif item=='>':
                level_list.append(tile(x_pos*80,y_pos*80,16,80,'wall','right'))
            elif item=='<':
                level_list.append(tile(x_pos*80,y_pos*80,16,80,'wall','left'))
            elif item=='^':
                level_list.append(tile(x_pos*80,y_pos*80,80,16,'wall','up'))
            elif item=='#':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'wall corner','right'))
            elif item=='@':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'wall corner','left'))
            elif item=='+':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'wall corner','up'))
            elif item=='=':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'wall corner','down'))
            elif item=='C':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'crate','None'))
            elif item=='b':
                level_list.append(tile(x_pos*80+20,y_pos*80+20,40,40,'box','None'))
            elif item=='S':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'shop','None'))
            elif item=='G':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'generator','None'))
            elif item=='P':
                level_list.append(tile(x_pos*80,y_pos*80,80,40,'control panel','None'))
            elif item=='0':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Toasthead',60,num,80))
                num+=1
            elif item=='1':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'C4PO',60,num,80))
                num+=1
            elif item=='D':
                level_list.append(tile(x_pos*80,y_pos*80,160,16,'door','None'))
            elif item=='E':
                level_list.append(tile(x_pos*80,y_pos*80,160,80,'entrance','None'))
            elif item=='B':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'chest','None'))
            elif item=='I':
                level_list.append(tile(x_pos*80,y_pos*80,80,40,'railing','None'))
            elif item=='|':
                decor_list.append(decor(x_pos*80,y_pos*80,80,80,'rail'))
            elif item=='g':
                decor_list.append(decor(x_pos*80,y_pos*80,80,80,'grate'))
            elif item=='L':
                decor_list.append(decor(x_pos*80,y_pos*80,80,80,'lava'))
            elif item=='M':
                decor_list.append(decor(x_pos*80,y_pos*80,20,20,'microchip'))
            elif item=='R':
                decor_list.append(decor(x_pos*80,y_pos*80,20,20,'repair kit'))
            elif item=='K':
                decor_list.append(decor(x_pos*80,y_pos*80,40,40,'key'))
            x_pos+=1
        y_pos+=1
        x_pos=0
    num=410
    while num > 0:
        if not player.dead:
            game_window()
        pygame.draw.rect(win,(0,0,0),(0,0,num,800))
        pygame.draw.rect(win,(0,0,0),(800,0,-num,800))
        if not player.dead:
            pygame.display.update()
        num-=4
    loading_room=False

file=open('Player data.txt','r')
read_file=file.readlines()
Phealth=int(read_file[0][read_file[0].find(':')+1:-1])
Pdamage=int(read_file[1][read_file[1].find(':')+1:-1])
Prate=int(read_file[2][read_file[2].find(':')+1:-1])
Pcrit=int(read_file[3][read_file[3].find(':')+1:-1])
microchips=int(read_file[4][read_file[4].find(':')+1:-1])
repair_kits=int(read_file[5][read_file[5].find(':')+1:-1])
player=player(400,400,40,40,Phealth,Prate,Pcrit,Pdamage)
file.close()

shop_button_list=[]
shop_button_list.append(button(10,100,250,600,'health'))
shop_button_list.append(button(275,100,250,600,'gun'))
shop_button_list.append(button(540,100,250,600,'repair kit'))


micro_cooldown=0
in_shop=False
global speaking
speaking=False
global mouse_pos
mouse_pos=pygame.mouse.get_pos()
global room_num
room_num=0
load_room(start_room)
smallfont=pygame.font.SysFont('ocr a extended',15)
font=pygame.font.SysFont('ocr a extended',20)
bigfont=pygame.font.SysFont('ocr a extended',50)
run=True
global cooldown
cooldown=0
global inventory
inventory=False
inven_cooldown=0
heal_cooldown=0
while run:
    can_up=True
    can_down=True
    can_left=True
    can_right=True
    mouse_pos=pygame.mouse.get_pos()
    key=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if cooldown!=0:
        cooldown-=1
    if in_shop:
        win.fill((250,250,250))
        if key[pygame.K_ESCAPE]:
            in_shop=False
        for item in shop_button_list:
            item.draw(win)
        win.blit(pygame.image.load('microchip icon.png'),(5,12))
        win.blit(bigfont.render(str(microchips),2,(0,0,0)),(45,5))
        win.blit(pygame.image.load('shop leave.png'),(720,5))
        
        
        pygame.display.update()
    else:        
        game_window()
        if inventory:
            inven=pygame.image.load('inventory.png')
            win.blit(inven,(player.x-52,player.y-60))
            if microchips > 0:
                win.blit(pygame.image.load('microchip icon.png'),(player.x-47,player.y-56))
                micro_text=font.render(str(microchips),1,(255,255,255))
                img_rect=pygame.Rect(player.x-47,player.y-56,40,40)
                win.blit(micro_text,((player.x-micro_text.get_width())-4,player.y-32))
                if img_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(win,(255,255,255),img_rect,1)
                    info_text=font.render('Microchips',2,(255,255,255))
                    info_text2=smallfont.render('Used for upgrades',1,(220,220,220))
                    pygame.draw.rect(win,(100,100,100),(player.x-50,player.y+50,info_text.get_width()+35,45))
                    pygame.draw.rect(win,(60,60,60),(player.x-50,player.y+50,info_text.get_width()+35,45),1)
                    win.blit(info_text,(player.x-50,player.y+50))
                    win.blit(info_text2,(player.x-50,player.y+75))
            if repair_kits > 0:
                img=pygame.image.load('repair kit icon.png')
                img_rect=pygame.Rect(player.x+1,player.y-56,40,40)
                win.blit(img,(player.x+1,player.y-56))
                rep_text=font.render(str(repair_kits),1,(255,255,255))
                win.blit(rep_text,((player.x-rep_text.get_width())+40,player.y-32))
                if img_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(win,(255,255,255),img_rect,1)
                    info_text=font.render('Repair Kits',2,(255,255,255))
                    info_text2=smallfont.render('Click to use',1,(220,220,220))
                    pygame.draw.rect(win,(100,100,100),(player.x-50,player.y+50,info_text.get_width(),45))
                    pygame.draw.rect(win,(60,60,60),(player.x-50,player.y+50,info_text.get_width(),45),1)
                    win.blit(info_text,(player.x-50,player.y+50))
                    win.blit(info_text2,(player.x-50,player.y+75))
                    if pygame.mouse.get_pressed()[0]:
                        if heal_cooldown==0:
                            if player.health != player.max_health:
                                repair_kits-=1
                                replace_line('Player Data.txt',5,'Repair Kits: '+str(repair_kits))
                                player.health+=50
                                if player.health > player.max_health:
                                    player.health=player.max_health
                                heal_cooldown=30
            if heal_cooldown!=0:
                heal_cooldown-=1
            
            
            gun=pygame.image.load(player.gun+'.png')
            win.blit(gun,(player.x+50,player.y-56))
            img_rect=pygame.Rect(player.x+50,player.y-56,40,40)
            if img_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(win,(255,255,255),img_rect,1)
                    info_text=font.render(player.gun,2,(255,255,255))
                    info_text2=smallfont.render('Damage: '+str(player.damage),1,(220,220,220))
                    info_text3=smallfont.render('Reload Delay : '+str(player.fire_rate),1,(220,220,220))
                    info_text4=smallfont.render('Crit Chance : 1/'+str(player.crit_chance),1,(220,220,220))
                    pygame.draw.rect(win,(100,100,100),(player.x-50,player.y+50,info_text.get_width(),85))
                    pygame.draw.rect(win,(60,60,60),(player.x-50,player.y+50,info_text.get_width(),85),1)
                    win.blit(info_text,(player.x-50,player.y+50))
                    win.blit(info_text2,(player.x-50,player.y+75))
                    win.blit(info_text3,(player.x-50,player.y+95))
                    win.blit(info_text4,(player.x-50,player.y+115))
            
            
            
            
            pygame.display.update()
            
        if key[pygame.K_q]:
            if inven_cooldown==0:
                inventory = not inventory
                inven_cooldown=30
        if inven_cooldown!=0:
            inven_cooldown-=1
            
        if key[pygame.K_w]:
            player.up=True
            player.down=False
            player.left=False
            player.right=False
            for item in level_list:
                if item.rect.colliderect(player.upRect):
                    can_up=False
            if can_up:
                player.y-=player.speed
                
        elif key[pygame.K_s]:
            player.down=True
            player.up=False
            player.left=False
            player.right=False
            for item in level_list:
                if item.rect.colliderect(player.downRect):
                    can_down=False
            if can_down:
                player.y+=player.speed
                
        elif key[pygame.K_a]:
            player.left=True
            player.right=False
            player.up=False
            player.down=False
            for item in level_list:
                if item.rect.colliderect(player.leftRect):
                    can_left=False
            if can_left:
                player.x-=player.speed
                
        elif key[pygame.K_d]:
            player.right=True
            player.left=False
            player.down=False
            player.up=False
            for item in level_list:
                if item.rect.colliderect(player.rightRect):
                    can_right=False
            if can_right:
                player.x+=player.speed
                
        if pygame.mouse.get_pressed()[0]:
            if not inventory:
                if player.shootcooldown==0:
                    if player.gun=='T1 Lazer Pistol' or player.gun=='T2 Blaster Pistol':
                        projectile_list.append(lazer(mouse_pos[0],mouse_pos[1],(0,255,0),'player'))
                    else:
                        projectile_list.append(lazer(mouse_pos[0],mouse_pos[1],(100,100,250),'player'))
                    player.shootcooldown=player.fire_rate
        if player.shootcooldown != 0:
            player.shootcooldown-=1
        
pygame.quit()
