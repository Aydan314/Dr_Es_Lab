import pygame
import random
import math
pygame.init()
clock=pygame.time.Clock()
win=pygame.display.set_mode((800,800))
pygame.display.set_caption('Dr E`s Lab')
class character(object):
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
    def __init__(self,x,y,colour,entity,ID,damage):
        self.entity=entity
        self.damage=damage
        self.x=x
        self.y=y
        self.point=pygame.Rect(self.x,self.y,1,1)
        self.colour=colour
        self.velocity=20
        self.time=40
        self.collide=False
        if self.entity=='player':
            self.xpoint=player.x+round(player.width/2)
            self.ypoint=player.y+round(player.height/2)
            self.x_diff=(self.xpoint-self.x)
            self.y_diff=(self.ypoint-self.y)
        elif self.entity=='turret':
            for item in level_list:
                if item.varient=='turret':
                    if item.x+item.y==ID:
                        self.xpoint=item.x+round(item.width/2)
                        self.ypoint=item.y+10
                        self.x_diff=(self.xpoint-self.x)
                        self.y_diff=(self.ypoint-self.y)
        else:
            for item in enemy_list:
                if item.identity==ID:
                    self.xpoint=item.x+round(item.width/2)
                    self.ypoint=item.y+round(item.height/2)
                    self.x_diff=(self.xpoint-self.x)
                    self.y_diff=(self.ypoint-self.y)
        angle=math.atan2(self.y_diff, self.x_diff)
        self.x = self.xpoint - round(math.cos(angle) * self.velocity)
        self.y = self.ypoint - round(math.sin(angle) * self.velocity)
    def draw(self,win):
        if not self.collide:
            self.point=pygame.Rect(self.x,self.y,1,1)
            pygame.draw.line(win,(self.colour),(self.x,self.y),(self.xpoint,self.ypoint),3)
            self.time-=1
            angle=math.atan2(self.y_diff, self.x_diff)
            self.x -= round(math.cos(angle) * self.velocity)
            self.y -= round(math.sin(angle) * self.velocity)
            self.xpoint -= round(math.cos(angle) * self.velocity)
            self.ypoint -= round(math.sin(angle) * self.velocity)
        else:
            for item in level_list:
                if item.varient != 'crate' or item.varient != 'box' or item.varient != 'barrel':
                    if item.varient=='wall corner':
                        if self.point.colliderect(item.rect) or self.point.colliderect(item.rect2):
                            self.collide=True
                    else:
                        if self.point.colliderect(item.rect):
                            self.collide=True
            index=0
            for item in projectile_list:
                if item.collide:
                    projectile_list.pop(index)
                index+=1

class tile(object):
    def __init__(self,x,y,width,height,varient,facing):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.varient=varient
        self.open=False
        self.powered=False
        self.facing=facing
        self.cooldown=0
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.rect2=pygame.Rect(self.x,self.y,10,self.height)
        self.crate_strength=2
        if facing=='None':
            if self.varient!='entrance':
                if self.varient!='airlock':
                    self.image=pygame.image.load(self.varient+'.png')
        if self.varient=='barrel':
            self.crate_strength=3
        self.contacted=False
        self.interact_icon=pygame.image.load('interact icon.png')
        self.interact_icon_active=pygame.image.load('interact icon active.png')
    def draw(self,win):
        global checkpoint
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        key=pygame.key.get_pressed()
        if self.facing=='up':
            if 'wall' in self.varient:
                if checkpoint < 4:
                    block=pygame.image.load(self.varient+' up '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load(self.varient+' up 3.png')
            else:    
                block=pygame.image.load(self.varient+' up.png')
        elif self.facing=='left':
            if self.varient=='wall':
                if checkpoint < 4:
                    block=pygame.image.load('wall right '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load('wall right 3.png')
            elif self.varient=='wall corner':
                if checkpoint < 4:
                    block=pygame.image.load(self.varient+' left '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load(self.varient+' left 3.png')
            else:
                block=pygame.image.load(self.varient+' left.png')
        elif self.facing=='right':
            if 'wall' in self.varient:
                if checkpoint < 4:
                    block=pygame.image.load(self.varient+' right '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load(self.varient+' right 3.png')
            else:    
                block=pygame.image.load(self.varient+' right.png')
        elif self.facing=='down':
            if 'wall' in self.varient:
                if checkpoint < 4:
                    block=pygame.image.load(self.varient+' down '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load(self.varient+' down 3.png')
            else:    
                block=pygame.image.load(self.varient+' down.png')
        elif self.varient=='crate':
            if self.crate_strength==2:
                block=self.image
            elif self.crate_strength <= 1:
                block=pygame.image.load('crate broken.png')
        elif self.varient=='box':
            if self.crate_strength==2:
                block=self.image
            elif self.crate_strength <= 1:
                block=pygame.image.load('box broken.png')
        elif self.varient=='barrel':
            if self.crate_strength==3:
                block=self.image
            if self.crate_strength==2:
                block=pygame.image.load('barrel damaged.png')
            elif self.crate_strength <= 1:
                block=pygame.image.load('barrel broken.png')
        else:
            if 'wall' not in self.varient:
                if self.varient!='entrance':
                    if self.varient!='airlock':
                        block=self.image
        if self.varient=='wall' and self.facing=='left':
            self.rect=pygame.Rect(self.x+64,self.y,self.width,self.height)
            win.blit(block,(self.x+64,self.y))
        elif self.varient=='wall' and self.facing=='up':
            self.rect=pygame.Rect(self.x,self.y+60,self.width,self.height)
            win.blit(block,(self.x,self.y))
        elif self.varient=='wall corner' and self.facing=='up':
            self.rect=pygame.Rect(self.x,self.y+60,self.width,16)
            self.rect2=pygame.Rect(self.x,self.y,16,self.height)
            win.blit(block,(self.x,self.y))
            #pygame.draw.rect(win,(250,0,0),self.rect,1)
            #pygame.draw.rect(win,(250,0,0),self.rect2,1)
        elif self.varient=='wall corner' and self.facing=='down':
            self.rect=pygame.Rect(self.x,self.y+60,self.width,16)
            self.rect2=pygame.Rect(self.x+64,self.y,16,self.height)
            win.blit(block,(self.x,self.y))
            #pygame.draw.rect(win,(250,0,0),self.rect,1)
            #pygame.draw.rect(win,(250,0,0),self.rect2,1)
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
                        for item in level_list:
                            if item.varient!='door':
                                item.draw(win)
                        next_room()
                    self.contacted=True
                else:
                    self.contacted=False
                
        elif self.varient=='entrance':
            if checkpoint < 4:
                win.blit(pygame.image.load('entrance '+str(checkpoint)+'.png'),(self.x,self.y))
            else:
                win.blit(pygame.image.load('entrance 3.png'),(self.x,self.y))    
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
                                    for i in range(0,checkpoint+1):
                                        decor_list.append(decor(self.x+self.width+30+(i*5),self.y+50,20,20,'repair kit'))
                                    self.open=True
                                    player.key=False
                            else:
                                if not speaking:
                                    text('Butl3r','I need a key')
                            self.contacted=True
                else:
                    self.contacted=False
                    
        elif self.varient=='switch':
            if self.powered:
                block=pygame.image.load('switch on.png')
            win.blit(block,(self.x,self.y))
            if self.rect.colliderect(player.upRect):
                win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y-40))
                if key[pygame.K_e]:
                    win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y-40))
                    if not self.contacted:
                        self.powered=not self.powered
                        self.contacted=True
            else:
                self.contacted=False

        elif self.varient=='turret':
            if self.cooldown!=0:
                self.cooldown-=1
            if self.powered:
                block=pygame.image.load('turret.png')
                self.rect2=pygame.Rect(self.x,self.y,200,self.height)
                if player.rect.colliderect(self.rect2):
                    if self.cooldown==0:
                        projectile_list.append(lazer(player.x+20,player.y+20,(255,255,0),'turret',self.x+self.y,0))
                        self.cooldown=10
                pygame.draw.line(win,(255,0,0),(self.x+20,self.y+13),(self.x+200,self.y+13),1)
            else:
                block=pygame.image.load('turret inactive.png')
            for item in level_list:
                if item.varient=='switch':
                    if item.powered:
                        self.powered=False
                    else:
                        self.powered=True
            win.blit(block,(self.x,self.y))

        elif self.varient=='airlock':
            if self.powered:
                if checkpoint < 4:
                    block=pygame.image.load('airlock '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load('airlock 3.png')
                if self.rect.colliderect(player.upRect) or self.rect.colliderect(player.downRect):
                    win.blit(self.interact_icon,(self.x+round(self.width/2)-20,self.y-40))
                    if key[pygame.K_e]:
                        win.blit(self.interact_icon_active,(self.x+round(self.width/2)-20,self.y-40))
                        if not self.contacted:
                            if not speaking:
                                text('Butl3r','The door requires power')
                                self.contacted=True
                else:
                    self.contacted=False
            else:
                if checkpoint < 4:
                    block=pygame.image.load('airlock open '+str(checkpoint)+'.png')
                else:
                    block=pygame.image.load('airlock open 3.png')
                self.rect=pygame.Rect(self.x,self.y,2,self.height)
            for item in level_list:
                if item.varient=='switch':
                    if item.powered:
                        self.powered=False
                    else:
                        self.powered=True
                        
            win.blit(block,(self.x,self.y))
                
        elif self.varient=='railing' or self.varient=='table' or self.varient=='control panel':
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
        if self.varient=='lava':
            self.img_list=(pygame.image.load(self.varient+' 1.png'),
                      pygame.image.load(self.varient+' 2.png'),
                      pygame.image.load(self.varient+' 3.png'),
                      pygame.image.load(self.varient+' 4.png'))
    def draw(self,win):
        if self.varient=='lava':
            if self.framecooldown==0:
                self.frame+=1
                if self.frame==5:
                    self.frame=1
                self.framecooldown=30
            else:
                self.framecooldown-=1
            img=self.img_list[self.frame-1]
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
        if self.varient=='Speed-E':
            self.speed=4
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
        self.spawn_id=1
        self.exploded=False
        self.said_text=False
        self.attack_cooldown2=10
        font=pygame.font.SysFont('ocr a extended',10)
        self.name=font.render(varient,2,(255,255,255))
    def draw(self,win):
        if self.varient!='Mechsuit':
            if self.frame==20:
                self.frame=0
            else:
                self.frame+=1
        else:
            if self.frame==100:
                self.frame=0
            else:
                self.frame+=1
        attack_player=False
        if self.rect.colliderect(player.intrest_rect):
            attack_player=True
            if not speaking:
                if self.varient=='Turretbot':
                    if self.attack_cooldown==0:
                        projectile_list.append(lazer(player.x+20,player.y+20,(255,0,0),'enemy',self.identity,20))
                        self.attack_cooldown=self.hit_rate
                elif self.varient=='Tee-Vee':
                    if self.attack_cooldown==0:
                        projectile_list.append(lazer(player.x+20,player.y+20,(255,0,0),'enemy',self.identity,10))
                        self.attack_cooldown=self.hit_rate
                elif self.varient=='MiKrowave':
                    if self.attack_cooldown==0:
                        projectile_list.append(lazer(player.x+20,player.y+20,(255,0,0),'enemy',self.identity,50))
                        self.attack_cooldown=self.hit_rate
                elif self.varient=='Mechsuit':
                    if self.attack_cooldown==0:
                        projectile_list.append(lazer(player.x+20,player.y+20,(255,50,50),'enemy',self.identity,30))
                        self.attack_cooldown=self.hit_rate
                        
        if self.varient=='Mechsuit':
            if self.health < self.max_health/2:
                    if self.attack_cooldown2==0:
                            if not self.said_text:
                                if not speaking:
                                    text('Dr E','Ouch that really hurt!')
                                    text('Dr E','I wasn`t even trying though')
                                    text('Dr E','For I can get my minions to beat you up')
                                    text('Dr E','Here they come!')
                                    self.said_text=True
                            if not speaking:
                                self.attack_cooldown2=300
                                if len(enemy_list) < 5:
                                    num=random.randint(0,8)
                                    if num==0:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Toasthead',60,self.spawn_id,80))
                                    elif num==1:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'C4PO',60,self.spawn_id,80))
                                    elif num==2:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Turretbot',60,self.spawn_id,80))
                                    elif num==3:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Binbot',100,self.spawn_id,80))
                                    elif num==4:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Tee-Vee',80,self.spawn_id,40))
                                    elif num==5:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Speed-E',80,self.spawn_id,60))
                                    elif num==6:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'MiKrowave',150,self.spawn_id,80))
                                    elif num==7:
                                        enemy_list.append(enemy(self.x,self.y,40,40,'Nukehead',120,self.spawn_id,40))
                                    elif num==8:
                                        enemy_list.append(enemy(self.x,self.y,60,60,'Safecracker',200,self.spawn_id,80))
                                    self.spawn_id+=1
                    else:
                        self.attack_cooldown2-=1
                
                    
                             
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
                    elif self.varient=='Toasthead':
                        damage('player',20,1)
                    elif self.varient=='Binbot':
                        damage('player',25,1)
                    elif self.varient=='Speed-E':
                        damage('player',30,1)
                    elif self.varient=='Nukehead':
                        damage('player',100,2)
                        self.exploded=True
                    elif self.varient=='Safecracker':
                        damage('player',50,1)
                    elif self.varient=='Mechsuit':
                        damage('player',50,1)
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
            if not loading_room:
                if self.facing!=5:
                    if self.facing==1:
                        for item in level_list:
                            if item.varient=='wall corner':
                                if self.upRect.colliderect(item.rect) or self.upRect.colliderect(item.rect2):
                                    can_up=False
                            if self.upRect.colliderect(item.rect):
                                can_up=False
                        for item in decor_list:
                            if item.varient=='lava':
                                if self.upRect.colliderect(item.rect):
                                    can_up=False
                        if can_up:
                            if not contact_player:
                                if self.varient!='Turretbot' and self.varient!='Tee-Vee' and self.varient!='MiKrowave':
                                    self.y-=self.speed
                                else:
                                    if not attack_player:
                                        self.y-=self.speed
                                    
                                
                    elif self.facing==2:
                        for item in level_list:
                            if item.varient=='wall corner':
                                if self.leftRect.colliderect(item.rect) or self.leftRect.colliderect(item.rect2):
                                    can_left=False
                            if self.leftRect.colliderect(item.rect):
                                can_left=False
                        for item in decor_list:
                            if item.varient=='lava':
                                if self.leftRect.colliderect(item.rect):
                                    can_left=False
                        if can_left:
                            if not contact_player:
                                if self.varient!='Turretbot' and self.varient!='Tee-Vee' and self.varient!='MiKrowave':
                                    self.x-=self.speed
                                else:
                                    if not attack_player:
                                        self.x-=self.speed
                                
                    elif self.facing==3:
                        for item in level_list:
                            if item.varient=='wall corner':
                                if self.rightRect.colliderect(item.rect) or self.rightRect.colliderect(item.rect2):
                                    can_right=False
                            if self.rightRect.colliderect(item.rect):
                                can_right=False
                        for item in decor_list:
                            if item.varient=='lava':
                                if self.rightRect.colliderect(item.rect):
                                    can_right=False
                        if can_right:
                            if not contact_player:
                                if self.varient!='Turretbot' and self.varient!='Tee-Vee' and self.varient!='MiKrowave':
                                    self.x+=self.speed
                                else:
                                    if not attack_player:
                                        self.x+=self.speed
                                
                    else:
                        for item in level_list:
                            if item.varient=='wall corner':
                                if self.downRect.colliderect(item.rect) or self.downRect.colliderect(item.rect2):
                                    can_down=False
                            if self.downRect.colliderect(item.rect):
                                can_down=False
                        for item in decor_list:
                            if item.varient=='lava':
                                if self.downRect.colliderect(item.rect):
                                    can_down=False
                        if can_down:
                            if not contact_player:
                                if self.varient!='Turretbot' and self.varient!='Tee-Vee' and self.varient!='MiKrowave':
                                    self.y+=self.speed
                                else:
                                    if not attack_player:
                                        self.y+=self.speed
        #pygame.draw.rect(win,(255,0,0),self.rect)
        #pygame.draw.rect(win,(255,255,0),self.upRect,1)
        #pygame.draw.rect(win,(255,0,255),self.downRect,1)
        #pygame.draw.rect(win,(0,255,0),self.rightRect,1)
        #pygame.draw.rect(win,(0,0,255),self.leftRect,1)
        win.blit(character,(self.x,self.y))
        if self.varient=='Mechsuit':
            if self.health<=0:
                    if not speaking:
                        text('Dr E','So you have defeated me')
                        text('Dr E','I have to say i`m impressed')
                        text('Dr E','Goodbye world!')
                        global game_complete
                        game_complete=True

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
    global said_text
    said_text=False
    for item in enemy_list:
        item.said_text=False
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
    global room_list
    room_list=[]

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

        close_damage=True                
        if entity=='enemy':
            for item in enemy_list:
                if item.identity==ID:
                    if item.varient=='Safecracker':
                        hurt=pygame.image.load('safecracker hurt.png')
                    if item.varient=='Mechsuit':
                        hurt=pygame.image.load('mechsuit hurt.png')
                    if item.varient=='C4PO' or item.varient=='Nukehead':
                        if item.rect.colliderect(player.rect):
                            close_damage=False
                    if close_damage:
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
    global run_tutor
    global run
    skip=False
    speaking=True
    allow_skip=False
    transparent=pygame.image.load('speach bubble.png')
    font=pygame.font.SysFont('ocr a extended',30)
    speaker=font.render(name+':',2,(0,0,255))
    pos=0
    delay=2
    key=pygame.key.get_pressed()
    run_text=True
    while run_text:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        if pos > len(speach)+round(0.25*len(speach)):
            run_text=False
            
        key=pygame.key.get_pressed()
        if not key[pygame.K_e]:
            allow_skip=True
        if allow_skip:
            if key[pygame.K_e]:
                run_text=False
                skip=True
        if not run_tutor:
            game_window()
        else:
            pygame.time.delay(20)
        win.blit(transparent,(0,700))
        win.blit(speaker,(20,700))
        if not skip:
            win.blit(pygame.image.load('interact icon.png'),(750,750))
        else:
            win.blit(pygame.image.load('interact icon active.png'),(750,750))
        if pos > len(speach)+1:
            line=font.render(speach,1,(0,0,0))
        else:
            line=font.render(speach[0:pos],1,(0,0,0))
        win.blit(line,(20,740))
        pygame.display.update()
        if delay==0:
            pos+=1
            delay=2
        else:
            delay-=1
    delay=10
    while delay > 0:
        if not run_tutor:
            game_window()
        else:
            pygame.time.delay(20)
        win.blit(transparent,(0,700))
        win.blit(speaker,(20,700))
        line=font.render(speach,1,(0,0,0))
        win.blit(line,(20,740))
        if not skip:
            win.blit(pygame.image.load('interact icon.png'),(750,750))
        else:
            win.blit(pygame.image.load('interact icon active.png'),(750,750))
        pygame.display.update()
        delay-=1
    speaking=False
        
        
        
        
global game_complete
game_complete=False
        
def game_window():
    global microchips
    global micro_cooldown
    global repair_kits
    global game_complete
    global enemy_list
    global endless_mode
    global Pscore
    if not endless_mode:
        if game_complete:
            enemy_list=[]
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
                if not player.key:
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
        if item.entity=='enemy':
                if item.point.colliderect(player.rect):
                    projectile_list.pop(index)
                    damage('player',item.damage,1)
        if item.entity=='turret':
                if item.point.colliderect(player.rect):
                    if projectile_list!=[]:
                        projectile_list.pop(index)
                        damage('player',40,1)
        index2=0
        for tile in level_list:
            if tile.varient=='crate' or tile.varient=='box' or tile.varient=='barrel':
                if item.point.colliderect(tile.rect):
                    tile.crate_strength-=1
                if tile.crate_strength==0:
                    level_list.pop(index2)
                if item.point.colliderect(tile.rect) or item.point.colliderect(tile.rect2):
                    if projectile_list!=[]:
                        projectile_list.pop(index)
            else:
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
                if bullet.entity=='player':
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
            if item.varient!='Mechsuit':
                if enemy_list!=[]:
                    enemy_list.pop(index)
                    if item.varient=='Toasthead' or item.varient=='C4PO' or item.varient=='Turretbot':
                        decor_list.append(decor(item.x+20,item.y+20,20,20,'microchip'))
                    if item.varient=='Binbot' or item.varient=='Tee-Vee' or item.varient=='Speed-E':
                        rno=random.randint(3,4)
                        for i in range(1,rno):
                            decor_list.append(decor(item.x+i*10,item.y+i*10,20,20,'microchip'))
                    if item.varient=='MiKrowave' or item.varient=='Nukehead' or item.varient=='Safecracker':
                        rno=random.randint(4,5)
                        for i in range(1,rno):
                            decor_list.append(decor(item.x+i*10,item.y+i*10,20,20,'microchip'))
        if item.exploded:
            enemy_list.pop(index)
        index+=1

    player.draw(win)
    
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
    if endless_mode:
        score_text=font.render('High Score: '+str(Pscore),3,(255,255,50))
        win.blit(score_text,(5,45))
    micros_text=bigfont.render(str(microchips),2,(20,255,20))
    micro_icon=pygame.image.load('microchip icon.png')
    win.blit(micro_icon,(218,5))
    win.blit(micros_text,(260,5))
    win.blit(room_text,(5,5))
    if player.health > 0:
        win.blit(health_text,(700,35))

    global said_text
    global speak_delay
    if not endless_mode:
        if room_num==101:
            if not said_text:
                if not speaking:
                    if speak_delay==0:
                        text('Dr E','So you have made it')
                        text('Dr E','Through all 100 of my rooms')
                        text('Dr E','You have destroyed all my creations')
                        text('Dr E','But i am afraid you venture no further')
                        text('Dr E','Prepare to Die!')
                        said_text=True
                        speak_delay=150
                    else:
                        speak_delay-=1
        
    if not loading_room:
        if not speaking:
            if not inventory:
                pygame.display.update()
                clock.tick(60)

global start_room
start_room=('@VVVE VVV#',
            '>  p  S p<',
            '>OO bbbb <',
            '@IIIPP   <',
            '>LLC>c   <',
            '>LL +__^^=',
            '>LL g    <',
            '>T    sss<',
            '>cc    g <',
            '+^^^D ^^^=')
global boss_room
boss_room=('@VVVE VVV#',
            '>        <',
            '>OOOOO g <',
            '>bbbb    <',
            '> g   bbb<',
            '>   9  OO<',
            '>        <',
            '>bb  CCCC<',
            '> OOg  CC<',
            '+^^^^^^^^=')

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
    global room_list
    global room_num
    global checkpoint
    global endless_mode
    if not endless_mode:
        if room_num==24:
            checkpoint=1
            load_room(start_room)
            replace_line('Player Data.txt',6,'Checkpoint: 1')
            room_choice=0
            room_list=[]
        elif room_num==49:
            checkpoint=2
            load_room(start_room)
            replace_line('Player Data.txt',6,'Checkpoint: 2')
            room_choice=0
            room_list=[]
        elif room_num==74:
            checkpoint=3
            load_room(start_room)
            replace_line('Player Data.txt',6,'Checkpoint: 3')
            room_choice=0
            room_list=[]
        elif room_num==99:
            checkpoint=4
            load_room(start_room)
            replace_line('Player Data.txt',6,'Checkpoint: 4')
            room_choice=0
            room_list=[]
        elif room_num==100:
            room_choice=0
            room_list=[]
            load_room(boss_room)
        else:
            if room_list==[]:
                for i in range(1,17):
                    room_list.append(i)
            room_choice=random.choice(room_list)
            index=0
            for item in room_list:
                if item==room_choice:
                    room_list.pop(index)
                index+=1
    else:
        if room_list==[]:
            for i in range(1,17):
                room_list.append(i)
        room_choice=random.choice(room_list)
        index=0
        for item in room_list:
            if item==room_choice:
                room_list.pop(index)
            index+=1
        checkpoint=random.randint(0,3)
        

    binbot_room=('@VVVE VVV#',
                '>3 g    O<',
                '@VVVVVVCC<',
                '>O   | CC<',
                '>    |  3<',
                '>bb VVVVV#',
                '>bb  CCC3<',
                '>  g O   <',
                '>3     G <',
                '+^^^D ^^^=')
    teevee_room=('@VVVE VVV#',
                '>sss   g <',
                '>CCCC III#',
                '@IIIII 4 <',
                '>Gbbb    <',
                '>bb4 IIII#',
                '>b   ssss<',
                '>C g  4T <',
                '>CCC4  cc<',
                '+^^^D ^^^=')
    turret_room2=('@VVVE VVV#',
                '>i O     <',
                '>4C C  t <',
                '@VVVVVVt <',
                '>2     tg<',
                '>  bbbb  <',
                '>g CCCC  <',
                '>PP    3 <',
                '>cc1     <',
                '+^^^D ^^^=')
    airlock_room2=('@VVVE VVV#',
                '>i     bb<',
                '>  C    0<',
                '@VVVAAVVV#',
                '>4 CCCC 2<',
                '>bbbb    <',
                '>   4   C<',
                '> 2 bbbbC<',
                '>     bbC<',
                '+^^^D ^^^=')
    lava_room2=('@VVVE VVV#',
                '>CC3   T <',
                '>CC    cc<',
                '>CC   bbb<',
                '@LLLLLLL <',
                '>  g     <',
                '>O  LLLLL#',
                '>GO4   3g<',
                '>bbO     <',
                '+^^^D ^^^=')
    chest_room3=('@VVVE VVV#',
                '>B p   LL<',
                '>3 p   LK<',
                '> OOOO3  <',
                '> OOOO bb<',
                '>  4   bb<',
                '> II  VVV#',
                '>4LL  bBb<',
                '>KLL     <',
                '+^^^D ^^^=')
    chest_room4=('@VVVE VVV#',
                '>1     OO<',
                '>   OOOOO<',
                '>G P     <',
                '>4 c    3<',
                '>    CiCC<',
                '@VA#   CC<',
                '>B <    3<',
                '>  <    K<',
                '+^^=D ^^^=')
    cafeteria=('@VVVE VVV#',
                '>pvp  pvp<',
                '>2 b  b 4<',
                '>T     T <',
                '>cc    cc<',
                '@VVV  VVV#',
                '>v  3 g v<',
                '>bb    OO<',
                '>OOg 3 CC<',
                '+^^^D ^^^=')
    room2=('@VVVE VVV#',
                '>T     T <',
                '>cc    cc<',
                '>iv    T <',
                '>4     3c<',
                '@VVVAAVVV#',
                '>Ovp  pvO<',
                '>T     T <',
                '>c1 1 1cc<',
                '+^^^D ^^^=')
    storage_room2=('@VVVE VVV#',
                '>0      p<',
                '>  VVVVVV#',
                '>OO   bbi<',
                '>OOO  bbb<',
                '>4    2 2<',
                '>CC     C<',
                '@VVAVV# b<',
                '>p g  <4G<',
                '+^^^D =^^=')
    magma_room=('@VVVE VVV#',
                '>bbb   CC<',
                '>LLLLL CC<',
                '>LLLL    <',
                '>3   3 3 <',
                '>  LLLLLL<',
                '>     LLL<',
                '>OOO     <',
                '>OO   4  <',
                '+^^^D ^^^=')
    boom_room=('@VVVE VVV#',
                '>OO g  CC<',
                '>OOOO   C<',
                '>1  1   1<',
                '+^^^__^^^=',
                '> g    bb<',
                '>1  1 III#',
                '>OOO     <',
                '>bb   1 G<',
                '+^^^D ^^^=')
    melee_room=('@VVVE VVV#',
                '>p  g   p<',
                '+^_^^^^_^=',
                '>   0bb  <',
                '>0CC 0 0 <',
                '+^^^__^^^=',
                '>vG    Pv<',
                '>OO    c <',
                '>3 3   3 <',
                '+^^^D ^^^=')
    ranged_room=('@VVVE VVV#',
                '>bb     i<',
                '@IIIIII  <',
                '>PPp ss2 <',
                '>cc 2   2<',
                '>G   ss  <',
                '+^^__^^_^=',
                '>4    4 4<',
                '>  @AA#  <',
                '+^^+D =^^=')
    split_room=('@VVVE VVV#',
                '>p     i <',
                '> OOO bb <',
                '@t VVVVt #',
                '>  PLLP  <',
                '>3  LL 4 <',
                '>O  LL  O<',
                '>4  LL   <',
                '>G    3 G<',
                '+^^^D ^^^=')



    speede_room=('@VVVE VVV#',
                '>OOO   CC<',
                '>OOg  CCC<',
                '+__^^^^__=',
                '>   PP   <',
                '>5  cc  5<',
                '>pG    Gp<',
                '+^^^__^^^=',
                '>bbb  g 5<',
                '+^^^D ^^^=')
    server_room2=('@VVVE VVV#',
                '+^^^__^^^=',
                '>sss  sss<',
                '>G4     G<',
                '>sss  sss<',
                '>g     5g<',
                '>sss  sss<',
                '>T5    T <',
                '>cc4   cc<',
                '+^^^D ^^^=')
    cafeteria2=('@VVVE VVV#',
                '>pvp  pvp<',
                '>T T    g<',
                '>c4cc  bb<',
                '>g   T T <',
                '>5   cccc<',
                '>T T    5<',
                '>c c    g<',
                '>4    OOO<',
                '+^^^D ^^^=')
    mikrowave_room=('@VVVE VVV#',
                '>CC  g   <',
                '>CCC    G<',
                '@III  III#',
                '>6 OOO   <',
                '>   OOOO <',
                '@IIIII  6<',
                '>P 6  bbb<',
                '>6 gbbbb <',
                '+^^^D ^^^=')
    lava_room3=('@VVVE VVV#',
                '>bbb   bb<',
                '>LLLOOO 5<',
                '>  LLLLLL<',
                '> g 6   g<',
                '>  CCCCC <',
                '>LLL OOOO<',
                '> LLLLLLg<',
                '>G 6   5 <',
                '+^^^D ^^^=')
    chest_room5=('@VVVE VVV#',
                '>K5O  CCC<',
                '@III  bbb<',
                '>i6G     <',
                '> OOOOOO <',
                '>4     6K<',
                '@VA#  @VA#',
                '>B <  >B <',
                '> g<  >  <',
                '+^^=D +^^=')
    chest_room6=('@VVVE VVV#',
                '>1     bb<',
                '>i P CCCC<',
                '>  c  OOO<',
                '>5  6    <',
                '@VVVVVVt <',
                '> B      <',
                '>OOO   CC<',
                '>0 bbb  K<',
                '+^^^D ^^^=')
    workshop=('@VVVE VVV#',
                '>ORO  ORO<',
                '>T     T <',
                '>cc5    c<',
                '+^^^__^^^=',
                '>RbR  RbR<',
                '>g6    6g<',
                '>T G   T <',
                '>cc4   cc<',
                '+^^^D ^^^=')
    magma_room2=('@VVVE VVV#',
                '>RRR  RRR<',
                '@III  III#',
                '>Gg6  3 G<',
                '>bbb   OO<',
                '>OOOO5  b<',
                '>CCCCC   <',
                '>LLLLLL 5<',
                '>LLL     <',
                '+^^^D ^^^=')
    airlock_room3=('@VVVE VVV#',
                '>OOO  bbb<',
                '>4iCC g 4<',
                '>   CC CC<',
                '@VVAVVAVV#',
                '> G  bbb <',
                '>OOOOOO  <',
                '>6  6   6<',
                '>CCC     <',
                '+^^^D ^^^=')
    turret_room3=('@VVVE VVV#',
                '>Rp    pR<',
                '>4 bbb   <',
                '@VVVVVV  <',
                '>  5   CC<',
                '>i OO <t <',
                '>6  C <t <',
                '@VVVVV#t <',
                '>pg6   t <',
                '+^^^D ^^^=')
    ranged_room2=('@VVVE VVV#',
                '>Rpp  ppR<',
                '>2  g   2<',
                '>OOOCC   <',
                '>bbR  bb <',
                '>6  6    <',
                '>ROOOO CC<',
                '>  bbb  G<',
                '>4 g   4 <',
                '+^^^D ^^^=')
    melee_room2=('@VVVE VVV#',
                '>RpR  RpR<',
                '>bbbb  OO<',
                '>0  0  C0<',
                '>G  CCCC <',
                '>3sss3  3<',
                '> OOO    <',
                '+^__^^__^=',
                '>5g     5<',
                '+^^^D ^^^=')
    boom_room2=('@VVVE VVV#',
                '>OOO  OOO<',
                '>1  1  1 <',
                '>OO    bb<',
                '> 1  1CCC<',
                '>bbssss  <',
                '> 1  1  1<',
                '>P    G P<',
                '>c 1  1 c<',
                '+^^^D ^^^=')
    toasthead_room2=('@VVVE VVV#',
                '>p     0p<',
                '>sss     <',
                '>0  OOOO <',
                '>bb    0 <',
                '>    RRR <',
                '>FFF0 CCC<',
                '>0   bbbb<',
                '>      0 <',
                '+^^^D ^^^=')
    storage_room3=('@VVVE VVV#',
                '>R R   GR<',
                '>CCCCC  3<',
                '>bbb  g  <',
                '>OOOOO   <',
                '>R 6  bb <',
                '>3   CCCC<',
                '> OOOOOG <',
                '> g   3 6<',
                '+^^^D ^^^=')


    nukehead_room=('@VVVE VVV#',
                '>vpR  Rpv<',
                '>7   g   <',
                '@VVV  VVV#',
                '>T p  pT <',
                '>cc    cc<',
                '>OOOOO   <',
                '>7 bbbb7 <',
                '> CCCC  7<',
                '+^^^D ^^^=')
    storage_room4=('@VVVE VVV#',
                '>ROR     <',
                '>bbbbb   <',
                '>ROR  OOO<',
                '>6 7  5bb<',
                '>LLLL   O<',
                '> LLLL   <',
                '>6    sss<',
                '>CCC   7 <',
                '+^^^D ^^^=')
    safecracker_room=('@VVVE VVV#',
                '>CRC  CRC<',
                '>8  g   8<',
                '@III  III#',
                '>OOO   CC<',
                '>bbbbb   <',
                '>bb     G<',
                '>8 g   OO<',
                '>p     8p<',
                '+^^^D ^^^=')
    chest_room7=('@VV#E VVV#',
                '>B <   OO<',
                '>  < g  b<',
                '>8      b<',
                '@IIIII   <',
                '>G  P LLL<',
                '> 7 c CCC<',
                '>bbbb  6 <',
                '>6 K   g <',
                '+^^^D ^^^=')
    chest_room8=('@VVVE VVV#',
                '>OOO    B<',
                '>6    bbb<',
                '@VVV  VVV#',
                '>B8   6OO<',
                '>OO   Gbb<',
                '@VVV  VVV#',
                '>Kv7  vK8<',
                '>CC    bb<',
                '+^^^D ^^^=')
    melee_room3=('@VVVE VVV#',
                '>0P g bbb<',
                '> c    0 <',
                '@^^^G3   <',
                '>LLL+^__^#',
                '>LLL     <',
                '> LL  CCC<',
                '>OO  8 CC<',
                '>8    OO5<',
                '+^^^D ^^^=')
    ranged_room3=('@VVVE VVV#',
                '>pR    Rp<',
                '>4      2<',
                '@^^^__^^^#',
                '> p    p <',
                '>OOOO 6  <',
                '>6    CCb<',
                '> bbbbb 6<',
                '> 2   CCC<',
                '+^^^D ^^^=')
    boom_room3=('@VVVE VVV#',
                '>1 p    1<',
                '>    bbb <',
                '@IIIII g <',
                '> OOOOO  <',
                '>7     7 <',
                '@^^^__^^^#',
                '>CC   OOO<',
                '> 1 g   7<',
                '+^^^D ^^^=')
    server_room3=('@VVVE VVV#',
                '>7CC    6<',
                '>ssssss  <',
                '> 8  g  G<',
                '>C ssssss<',
                '>C       <',
                '>sssss bb<',
                '>T 8  OOO<',
                '>cc   g 8<',
                '+^^^D ^^^=')
    lava_room4=('@VVVE VVV#',
                '>LLL  bbb<',
                '> LLL 8  <',
                '>  LLL OO<',
                '>6O LLL  <',
                '> OO LLL <',
                '> 8OO LLL<',
                '>  7 G LL<',
                '>6CC    L<',
                '+^^^D ^^^=')
    turret_room4=('@VVVE VVV#',
                '>CC    bb<',
                '>OOO    2<',
                '>8 t  < 1<',
                '>  t g<  <',
                '>b t  <6G<',
                '>8 t  <  <',
                '> Ct g< i<',
                '>  t  <7 <',
                '+^^+D =^^=')
    airlock_room4=('@VVVE VVV#',
                '>p      p<',
                '>   g   6<',
                '@VAV# i G<',
                '>   <  7 <',
                '> 8 <IIII#',
                '>OO   bbb<',
                '>PP  g 8 <',
                '> c   7  <',
                '+^^^D ^^^=')
    workshop2=('@VVVE VVV#',
                '@^^^__^^^#',
                '>RpR  RpR<',
                '>6g  G7g <',
                '>RRR  RRR<',
                '>T 8  5T <',
                '>ccCCC  c<',
                '>T  8 5T <',
                '> c G  cc<',
                '+^^^D ^^^=')
    control_room=('@VVVE VVV#',
                '>sss  sss<',
                '>G4     G<',
                '>PPP  PPP<',
                '>c c3 3cc<',
                '>sss  sss<',
                '>G8 7  8G<',
                '>PPP  PPP<',
                '>ccc  7c4<',
                '+^^^D ^^^=')
    power_room=('@VVVE VVV#',
                '>G s  s G<',
                '> 6G  G6 <',
                '>G G  G G<',
                '> 8    7 <',
                '>G G  G G<',
                '>   5    <',
                '@IIII 4ss<',
                '>PPP    8<',
                '+^^^D ^^^=')
    



    
    airlock_room=('@VVVE VVV#',
                '>G    bbO<',
                '>0     CC<',
                '>O   VVVV#',
                '>bb   | i<',
                '>C    |0g<',
                '@VAVVVVAV#',
                '>  p  p  <',
                '>G2    O2<',
                '+^^^D ^^^=')
    storage_room=('@VVVE VVV#',
                '>bb g  CC<',
                '>COC  bbb<',
                '>b1   GOC<',
                '>gbb     <',
                '@IIIIPCC1<',
                '>2LLLc bb<',
                '>LLLL  bb<',
                '>LLg   CC<',
                '+^^^D ^^^=')
    new_room=('@VVVE VVV#',
                '>        <',
                '>        <',
                '>        <',
                '>        <',
                '>        <',
                '>        <',
                '>        <',
                '>        <',
                '+^^^D ^^^=')
    barrel_room=('@VVVE VVV#',
                '>bbbg  bb<',
                '>OOOOOO  <',
                '>1       <',
                '>  OOOOOO<',
                '+___^^^^^=',
                '> 1   P 0<',
                '>OO    g <',
                '>OOg   1G<',
                '+^^^D ^^^=')
    room=('@VVVE VVV#',
                '>Gbb   CG<',
                '>bbbg  CC<',
                '>1 PPGi b<',
                '>C 2c2  b<',
                '+__^^^^__=',
                '>C     gb<',
                '@III  III#',
                '>LLt 1LLL<',
                '+^^^D ^^^=')
    plant_room=('@VVVE VVV#',
                '>pCC  CCp<',
                '>p0gO   p<',
                '>p 0    p<',
                '@IIIII  I#',
                '>p 2    p<',
                '>p bb g p<',
                '>p bbb  p<',
                '>p  g  2p<',
                '+^^^D ^^^=')
    shop_room=('@VVVE VVV#',
                '>pSp  pSp<',
                '>g      g<',
                '>ccc  ccc<',
                '+^^^__^^^=',
                '>CO  1 bb<',
                '>CCC    2<',
                '>CC    Ob<',
                '>2    bbb<',
                '+^^^D ^^^=')
    turret_room=('@VVVE VVV#',
                '>C bb  CC<',
                '>t p IIII#',
                '>1   LLLL<',
                '>       i<',
                '>bLL LL  <',
                '>1>t  <  <',
                '> >t  <  <',
                '>b>t  <G2<',
                '+^+^D =^^=')
    office_room=('@VVVE VVV#',
                '>FFF  FFF<',
                '>T b  bT <',
                '>c 0    c<',
                '@VVV  VVV#',
                '>FPb  bPF<',
                '>T  2  T <',
                '>cc2    c<',
                '>bbb  bbb<',
                '+^^^D ^^^=')
    server_room=('@VVVE VVV#',
                '>G      G<',
                '>sss  sss<',
                '>Pb   0bP<',
                '@III  III#',
                '>bb1   bb<',
                '>sss  sss<',
                '>b2    bb<',
                '>sss  sss<',
                '+^^^D ^^^=')
    turretbot_room=('@VVVE VVV#',
                '>p     bb<',
                '>bCCIII G<',
                '> bb  2 C<',
                '@IIIII   <',
                '>2 p ssss<',
                '>Pb      <',
                '>c   ssss<',
                '>bb2   bb<',
                '+^^^D ^^^=')
    chest_room2=('@VVVE VVV#',
                '>B  g   C<',
                '>  1   CC<',
                '@VVV  VVV#',
                '> B    g <',
                '>   CIIII<',
                '>LL  0  K<',
                '>LL OO   <',
                '>K    C 1<',
                '+^^^D ^^^=')
    chest_room=('@VV#E VVV#',
                '>K <   pB<',
                '> C< 0   <',
                '>0 <   g <',
                '>CC|    G<',
                '>C |   T <',
                '@VVV   cc<',
                '>Sgp  C  <',
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
                    '>p0<     <',
                    '> C<  gC <',
                    '>C |     <',
                    '>G |  0 0<',
                    '@VVV     <',
                    '>  C   G <',
                    '>C  VVVVV#',
                    '>G0    C <',
                    '+^^^D ^^^=')
    c4po_room=('@VVVE VVV#',
                    '>  C   1 <',
                    '>ss   g  <',
                    '> 1  VVVV#',
                    '>    | p <',
                    '> CC |   <',
                    '@VVVVV   <',
                    '>P  g  ss<',
                    '>c1    b <',
                    '+^^^D ^^^=')
    lava_room=('@VVVE VVV#',
                    '>LL C   0<',
                    '>LL    C <',
                    '>   C    <',
                    '>LLLLLLLL<',
                    '>LLLLLLLL<',
                    '>  0   g <',
                    '>bbC  LLL<',
                    '>bbC 1LLL<',
                    '+^^^D ^^^=')
    if room_choice==1:
        if checkpoint==0:
            load_room(crate_room)
        elif checkpoint==1:
            load_room(binbot_room)
        elif checkpoint==2:
            load_room(shop_room)
        elif checkpoint==3:
            load_room(nukehead_room)
            
    elif room_choice==2:
        if checkpoint==0:
            load_room(c4po_room)
        elif checkpoint==1:
            load_room(teevee_room)
        elif checkpoint==2:
            load_room(speede_room)
        elif checkpoint==3:
            load_room(shop_room)
            
    elif room_choice==3:
        if checkpoint==0:
            load_room(lava_room)
        elif checkpoint==1:
            load_room(turret_room2)
        elif checkpoint==2:
            load_room(server_room2)
        elif checkpoint==3:
            load_room(storage_room4)
            
    elif room_choice==4:
        if checkpoint==0:
            load_room(chest_room)
        elif checkpoint==1:
            load_room(airlock_room2)
        elif checkpoint==2:
            load_room(cafeteria2)
        elif checkpoint==3:
            load_room(safecracker_room)
            
    elif room_choice==5:
        if checkpoint==0:
            load_room(chest_room2)
        elif checkpoint==1:
            load_room(lava_room2)
        elif checkpoint==2:
            load_room(mikrowave_room)
        elif checkpoint==3:
            load_room(chest_room7)
            
    elif room_choice==6:
        if checkpoint==0:
            load_room(turretbot_room)
        elif checkpoint==1:
            load_room(shop_room)
        elif checkpoint==2:
            load_room(lava_room3)
        elif checkpoint==3:
            load_room(chest_room8)
            
    elif room_choice==7:
        if checkpoint==0:
            load_room(server_room)
        elif checkpoint==1:
            load_room(chest_room3)
        elif checkpoint==2:
            load_room(chest_room5)
        elif checkpoint==3:
            load_room(melee_room3)
            
    elif room_choice==8:
        if checkpoint==0:
            load_room(office_room)
        elif checkpoint==1:
            load_room(chest_room4)
        elif checkpoint==2:
            load_room(chest_room6)
        elif checkpoint==3:
            load_room(ranged_room3)
            
    elif room_choice==9:
        if checkpoint==0:
            load_room(storage_room)
        elif checkpoint==1:
            load_room(cafeteria)
        elif checkpoint==2:
            load_room(workshop)
        elif checkpoint==3:
            load_room(boom_room3)

    elif room_choice==10:
        if checkpoint==0:
            load_room(airlock_room)
        elif checkpoint==1:
            load_room(room2)
        elif checkpoint==2:
            load_room(magma_room2)
        elif checkpoint==3:
            load_room(server_room3)
            
    elif room_choice==11:
        if checkpoint==0:
            load_room(turret_room)
        elif checkpoint==1:
            load_room(storage_room2)
        elif checkpoint==2:
            load_room(airlock_room3)
        elif checkpoint==3:
            load_room(lava_room4)
            
    elif room_choice==12:
        if checkpoint==0:
            load_room(shop_room)
        elif checkpoint==1:
            load_room(magma_room)
        elif checkpoint==2:
            load_room(turret_room3)
        elif checkpoint==3:
            load_room(airlock_room4)
            
    elif room_choice==13:
        if checkpoint==0:
            load_room(toasthead_room)
        elif checkpoint==1:
            load_room(boom_room)
        elif checkpoint==2:
            load_room(ranged_room2)
        elif checkpoint==3:
            load_room(turret_room4)
            
    elif room_choice==14:
        if checkpoint==0:
            load_room(plant_room)
        elif checkpoint==1:
            load_room(melee_room)
        elif checkpoint==2:
            load_room(boom_room2)
        elif checkpoint==3:
            load_room(workshop2)
            
    elif room_choice==15:
        if checkpoint==0:
            load_room(room)
        elif checkpoint==1:
            load_room(ranged_room)
        elif checkpoint==2:
            load_room(toasthead_room2)
        elif checkpoint==3:
            load_room(control_room)
            
    elif room_choice==16:
        if checkpoint==0:
            load_room(barrel_room)
        elif checkpoint==1:
            load_room(split_room)
        elif checkpoint==2:
            load_room(storage_room3)
        elif checkpoint==3:
            load_room(power_room)
        

def load_room(room):
    global room_num
    global checkpoint
    global endless_mode
    global Pscore
    player.key=False
    player.x=400
    player.y=100
    if player.dead:
        if not endless_mode:
            if checkpoint==0:
                room_num=1
            elif checkpoint==1:
                room_num=25
            elif checkpoint==2:
                room_num=50
            elif checkpoint==3:
                room_num=75
            else:
                room_num=100
        else:
            if room_num > Pscore:
                    replace_line('Player Data.txt',8,'Endless Score: '+str(room_num))
                    Pscore=room_num
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
            elif item=='_':
                decor_list.append(decor(x_pos*80,y_pos*80,80,80,'stairs'))
            elif item=='C':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'crate','None'))
            elif item=='c':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'chair','None'))
            elif item=='b':
                level_list.append(tile(x_pos*80+20,y_pos*80+20,40,40,'box','None'))
            elif item=='S':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'shop','None'))
            elif item=='T':
                level_list.append(tile(x_pos*80,y_pos*80,160,40,'table','None'))
            elif item=='F':
                level_list.append(tile(x_pos*80,y_pos*80,40,80,'filing cabinet','None'))
            elif item=='G':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'generator','None'))
            elif item=='P':
                level_list.append(tile(x_pos*80,y_pos*80,80,40,'control panel','None'))
            elif item=='p':
                level_list.append(tile(x_pos*80,y_pos*80,40,80,'plant','None'))
            elif item=='s':
                level_list.append(tile(x_pos*80,y_pos*80,40,80,'server','None'))
            elif item=='R':
                level_list.append(tile(x_pos*80,y_pos*80,40,80,'toolrack','None'))
            elif item=='v':
                level_list.append(tile(x_pos*80,y_pos*80,60,80,'vending machine','None'))
            elif item=='i':
                level_list.append(tile(x_pos*80+20,y_pos*80+20,40,40,'switch','None'))
            elif item=='t':
                level_list.append(tile(x_pos*80+20,y_pos*80+20,40,40,'turret','None'))
            elif item=='0':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Toasthead',60,num,80))
                num+=1
            elif item=='1':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'C4PO',60,num,80))
                num+=1
            elif item=='2':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Turretbot',60,num,80))
                num+=1
            elif item=='3':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Binbot',100,num,80))
                num+=1
            elif item=='4':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Tee-Vee',80,num,40))
                num+=1
            elif item=='5':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Speed-E',80,num,60))
                num+=1
            elif item=='6':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'MiKrowave',150,num,80))
                num+=1
            elif item=='7':
                enemy_list.append(enemy(x_pos*80,y_pos*80,40,40,'Nukehead',120,num,40))
                num+=1
            elif item=='8':
                enemy_list.append(enemy(x_pos*80,y_pos*80,60,60,'Safecracker',200,num,80))
                num+=1
            elif item=='9':
                enemy_list.append(enemy(x_pos*80,y_pos*80,80,80,'Mechsuit',5000,num,100))
                num+=1
            elif item=='D':
                level_list.append(tile(x_pos*80,y_pos*80,160,16,'door','None'))
            elif item=='A':
                level_list.append(tile(x_pos*80,y_pos*80,80,80,'airlock','None'))
            elif item=='E':
                level_list.append(tile(x_pos*80,y_pos*80,160,80,'entrance','None'))
            elif item=='B':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'chest','None'))
            elif item=='O':
                level_list.append(tile(x_pos*80,y_pos*80,40,40,'barrel','None'))
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
            elif item=='r':
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

shop_button_list=[]
shop_button_list.append(button(10,100,250,600,'health'))
shop_button_list.append(button(275,100,250,600,'gun'))
shop_button_list.append(button(540,100,250,600,'repair kit'))

file=open('Player data.txt','r')
read_file=file.readlines()
Phealth=int(read_file[0][read_file[0].find(':')+1:-1])
Pdamage=int(read_file[1][read_file[1].find(':')+1:-1])
Prate=int(read_file[2][read_file[2].find(':')+1:-1])
Pcrit=int(read_file[3][read_file[3].find(':')+1:-1])
microchips=int(read_file[4][read_file[4].find(':')+1:-1])
repair_kits=int(read_file[5][read_file[5].find(':')+1:-1])
checkpoint=int(read_file[6][read_file[6].find(':')+1:-1])
Pgame=(read_file[7][read_file[7].find(':')+1:-1])
Pscore=int(read_file[8][read_file[8].find(':')+1:])
Ptutor=(read_file[9][read_file[9].find(':')+1:-1])
if Pgame==' True':
    endless_mode=True
    game_complete=True
else:
    game_complete=False
    endless_mode=False
global run_tutor
if Ptutor==' True':
    do_tutorial=False
    run_tutor=False
else:
    do_tutorial=True
    run_tutor=True
player=character(400,400,40,40,Phealth,Prate,Pcrit,Pdamage)
file.close()

micro_cooldown=0
global speak_delay
speak_delay=150
global said_text
said_text=False
in_shop=False
global speaking
speaking=False
global mouse_pos
mouse_pos=pygame.mouse.get_pos()
global room_num
global room_list
room_list=[]
smallfont=pygame.font.SysFont('ocr a extended',15)
font=pygame.font.SysFont('ocr a extended',20)
midfont=pygame.font.SysFont('ocr a extended',37)
bigfont=pygame.font.SysFont('ocr a extended',50)
global run
run=True
global cooldown
cooldown=0
global inventory
inventory=False
menu=True
inven_cooldown=0
heal_cooldown=0
finish_cooldown=200
menu_frame=0
menu_ind=1
choice=False
choice_delay=1
first_run=True
allow_esc=False
down=False
while run:
    can_up=True
    can_down=True
    can_left=True
    can_right=True
    mouse_pos=pygame.mouse.get_pos()
    mouse_point=pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)
    key=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if cooldown!=0:
        cooldown-=1

    if menu:
        button1=pygame.Rect(20,600,400,80)
        button2=pygame.Rect(20,700,400,80)
        if menu_frame==0:
            if menu_ind==5:
                down=True
            elif menu_ind==1:
                down=False
            if not down:
                menu_ind+=1
            else:
                menu_ind-=1  
            menu_frame=60
        else:
            menu_frame-=1
        win.blit(pygame.image.load('menu background '+str(menu_ind)+'.png'),(0,0))
        pygame.draw.rect(win,(100,100,100),button1)
        pygame.draw.rect(win,(70,70,70),button1,2)
        pygame.draw.rect(win,(100,100,100),button2)
        pygame.draw.rect(win,(70,70,70),button2,2)
        if mouse_point.colliderect(button1):
            if not choice:
                pygame.draw.rect(win,(255,255,255),button1,3)
                if not game_complete:
                    play=bigfont.render('> PLAY GAME <',10,(255,255,255))
                    win.blit(play,(23,610))
                else:
                    play=midfont.render('> PLAY ENDLESS <',10,(255,255,255))
                    win.blit(play,(23,615))
                if pygame.mouse.get_pressed()[0]:
                    menu=False
        else:
            if not game_complete:
                play=bigfont.render('PLAY GAME',10,(255,255,255))
                win.blit(play,(60,610))
            else:
                play=midfont.render('PLAY ENDLESS',10,(255,255,255))
                win.blit(play,(60,615))
            
        if mouse_point.colliderect(button2):
            if not choice:
                play=midfont.render('> RESET PROGRESS <',10,(255,255,255))
                win.blit(play,(23,716))
                pygame.draw.rect(win,(255,255,255),button2,3)
                if pygame.mouse.get_pressed()[0]:
                    choice=True
                    choice_delay=1
        else:
            play=midfont.render('RESET PROGRESS',10,(255,255,255))
            win.blit(play,(60,716))

        if choice:
            pygame.draw.rect(win,(70,70,70),(480,660,300,120))
            pygame.draw.rect(win,(50,50,50),(480,660,300,120),2)
            if choice_delay==1:
                yes=bigfont.render('YES',4,(150,255,150))
                no=bigfont.render('NO',4,(255,150,150))
                are_sure=midfont.render('ARE YOU SURE?',4,(255,255,255))
                win.blit(are_sure,(485,665))
                button3=pygame.Rect(485,715,yes.get_width(),yes.get_height())
                button4=pygame.Rect(650,715,no.get_width(),no.get_height())
                if mouse_point.colliderect(button3):
                    yes=bigfont.render('>YES<',4,(100,255,100))
                    if pygame.mouse.get_pressed()[0]:
                        choice_delay=60
                        replace_line('Player Data.txt',0,'Health: 50')
                        replace_line('Player Data.txt',1,'Damage: 20')
                        replace_line('Player Data.txt',2,'Firing Rate: 80')
                        replace_line('Player Data.txt',3,'Crit Chance: 50')
                        replace_line('Player Data.txt',4,'Microchips: 0')
                        replace_line('Player Data.txt',5,'Repair Kits: 0')
                        replace_line('Player Data.txt',6,'Checkpoint: 0')
                        replace_line('Player Data.txt',7,'Game Complete: False')
                        replace_line('Player Data.txt',8,'Endless Score: 0')
                        replace_line('Player Data.txt',9,'Done Tutorial: False')
                        game_complete=False
                        run_tutor=True
                win.blit(yes,(485,715))
                if mouse_point.colliderect(button4):
                    no=bigfont.render('>NO<',4,(255,100,100))
                    if pygame.mouse.get_pressed()[0]:
                        choice=False
                win.blit(no,(650,715))
            else:
                choice_delay-=1
                reset=midfont.render('PROGRESS',4,(255,255,255))
                reset2=midfont.render('RESET',4,(255,255,255))
                win.blit(reset,(485,680))
                win.blit(reset2,(485,720))
                if choice_delay==2:
                    choice=False
                    choice_delay=1
                
        pygame.display.update()
        
    elif run_tutor:
        for i in range(1,300):
            win.blit(pygame.image.load('menu background '+str(menu_ind)+'.png'),(0,0))
            pygame.draw.rect(win,(100,100,100),button1)
            pygame.draw.rect(win,(70,70,70),button1,2)
            pygame.draw.rect(win,(100,100,100),button2)
            pygame.draw.rect(win,(70,70,70),button2,2)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                    run_tutor=False
            pygame.draw.rect(win,(0,0,0),(0,0,(i*2),800))
            pygame.draw.rect(win,(0,0,0),(800-(i*2),0,800,800))
            pygame.display.update()
        win.fill((0,0,0))
        win.blit(pygame.image.load('table.png'),(400,300))
        win.blit(pygame.image.load('chair.png'),(420,340))
        win.blit(pygame.image.load('chair.png'),(500,340))
        win.blit(pygame.image.load('Character forward.png'),(250,380))
        win.blit(pygame.image.load('Dr E forward.png'),(300,380))
        if not speaking:
            text('Dr E','Yes!')
            text('Dr E','It is finally complete!')
            text('Dr E','My greatest creation yet')
            text('Toasthead','You mean me!')
            for i in range(1,60):
                win.fill((0,0,0))
                win.blit(pygame.image.load('table.png'),(400,300))
                win.blit(pygame.image.load('chair.png'),(420,340))
                win.blit(pygame.image.load('chair.png'),(500,340))
                win.blit(pygame.image.load('Character forward.png'),(250,380))
                win.blit(pygame.image.load('Dr E left.png'),(300,380))
                win.blit(pygame.image.load('Toasthead forward.png'),(i*2,400))
                pygame.time.delay(20)
                pygame.display.update()
            text('Dr E','No not you!')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character forward.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(300,380))
            win.blit(pygame.image.load('Toasthead forward attack.png'),(120,400))
            text('Toasthead','Oh you mean him')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character forward.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(300,380))
            win.blit(pygame.image.load('Toasthead forward.png'),(120,400))
            text('Dr E','Yes i mean him!')
            text('Toasthead','I shall just leave then :(')
            for i in range(1,82):
                win.fill((0,0,0))
                win.blit(pygame.image.load('table.png'),(400,300))
                win.blit(pygame.image.load('chair.png'),(420,340))
                win.blit(pygame.image.load('chair.png'),(500,340))
                win.blit(pygame.image.load('Character forward.png'),(250,380))
                win.blit(pygame.image.load('Dr E left.png'),(300,380))
                win.blit(pygame.image.load('Toasthead forward.png'),(120-(i*2),400))
                pygame.time.delay(20)
                pygame.display.update()
            text('Dr E','As i was saying...')
            text('Dr E','This is my greatest creation yet')
            text('Dr E','A robot butler')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character forward.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(300,380))
            text('Dr E','I call it the Butl3r')
            text('Dr E','It shall be way better')
            text('Dr E','Than my other creations')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character right.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(300,380))
            text('Butl3r','Hello world')
            text('Dr E','It works!')
            text('Butl3r','Hello creator')
            text('Dr E','Okay time for the real test')
            text('Dr E','Butl3r make me a cup of tea')
            text('Butl3r','No')
            for i in range(1,40):
                win.fill((0,0,0))
                win.blit(pygame.image.load('table.png'),(400,300))
                win.blit(pygame.image.load('chair.png'),(420,340))
                win.blit(pygame.image.load('chair.png'),(500,340))
                win.blit(pygame.image.load('Character right.png'),(250,380))
                win.blit(pygame.image.load('Dr E left.png'),(300+i,380))
                pygame.time.delay(20)
                pygame.display.update()
            text('Dr E','What do you mean no!')
            text('Butl3r','I don`t want to')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character right.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(340,380))
            text('Dr E','Huh, shouldn`t have given')
            text('Dr E','This thing emotions')
            text('Dr E','Didn`t think that through')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character forward.png'),(250,380))
            win.blit(pygame.image.load('Dr E forward.png'),(340,380))
            text('Dr E','Welp, i shall put you in the lab')
            text('Dr E','With all my other failed creations')
            win.fill((0,0,0))
            win.blit(pygame.image.load('table.png'),(400,300))
            win.blit(pygame.image.load('chair.png'),(420,340))
            win.blit(pygame.image.load('chair.png'),(500,340))
            win.blit(pygame.image.load('Character right.png'),(250,380))
            win.blit(pygame.image.load('Dr E left.png'),(340,380))
            text('Butl3r','No you can`t do that!')
            text('Dr E','Oh yes i can muhahaha!')
            run_tutor=False
            pygame.display.update()

    elif in_shop:
        win.fill((250,250,250))
        if key[pygame.K_ESCAPE]:
            in_shop=False
        for item in shop_button_list:
            item.draw(win)
        win.blit(pygame.image.load('microchip icon.png'),(5,12))
        win.blit(bigfont.render(str(microchips),2,(0,0,0)),(45,5))
        win.blit(pygame.image.load('shop leave.png'),(720,5))
        allow_esc=False
        pygame.display.update()
    else:
        if first_run:
            file=open('Player data.txt','r')
            read_file=file.readlines()
            Phealth=int(read_file[0][read_file[0].find(':')+1:-1])
            Pdamage=int(read_file[1][read_file[1].find(':')+1:-1])
            Prate=int(read_file[2][read_file[2].find(':')+1:-1])
            Pcrit=int(read_file[3][read_file[3].find(':')+1:-1])
            microchips=int(read_file[4][read_file[4].find(':')+1:-1])
            repair_kits=int(read_file[5][read_file[5].find(':')+1:-1])
            checkpoint=int(read_file[6][read_file[6].find(':')+1:-1])
            Pgame=(read_file[7][read_file[7].find(':')+1:-1])
            Pscore=int(read_file[8][read_file[8].find(':')+1:])
            Ptutor=(read_file[9][read_file[9].find(':')+1:-1])
            if Pgame==' True':
                endless_mode=True
                game_complete=True
            else:
                game_complete=False
                endless_mode=False
            if Ptutor==' True':
                do_tutorial=False
            else:
                do_tutorial=True
            player=character(400,400,40,40,Phealth,Prate,Pcrit,Pdamage)
            file.close()
            if not endless_mode:
                if checkpoint==0:
                    room_num=0
                elif checkpoint==1:
                    room_num=24
                elif checkpoint==2:
                    room_num=49
                elif checkpoint==3:
                    room_num=74
                else:
                    room_num=99
            else:
                room_num=0
            load_room(start_room)
            first_run=False
            if do_tutorial:
                do_tutorial=False
                text('Dr E','Welcome to my basement lab')
                text('Dr E','Where you shall spend the rest of your life')
                text('Dr E','Unless you somehow manage')
                text('Dr E','To get through all 100 of my rooms')
                text('Dr E','By the way you see that shop over there')
                text('Dr E','It does nothing ignore it')
                text('Dr E','It definately doesn`t make you stronger')
                text('Dr E','There are also checkpoints')
                text('Dr E','Every 25 rooms')
                text('Dr E','Reaching them will set your respawn point')
                text('Dr E','But you don`t need to know that')
                text('Dr E','One last thing...')
                text('Dr E','Use WASD to move')
                text('Dr E','And click to shoot')
                text('Dr E','To toggle your inventory press Q')
                text('Dr E','Okay that is all')
                text('Dr E','Goodbye Muhahaha!')
                replace_line('Player Data.txt',9,'Done Tutorial: True')
                
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
        if not endless_mode:
            if game_complete:
                if finish_cooldown==0:
                    if not speaking:
                        text('@','Well done you have finished the game')
                        text('@','Thanks for playing!')
                        text('@','Endless mode is now unlocked')
                        text('@','Return to main menu to access')
                        replace_line('Player Data.txt',7,'Completed Game: True')
                        endless_mode=True

                else:
                    finish_cooldown-=1
            
            
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
                if item.varient=='wall corner':
                    if player.upRect.colliderect(item.rect) or player.upRect.colliderect(item.rect2):
                            can_up=False
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
                if item.varient=='wall corner':
                    if player.downRect.colliderect(item.rect) or player.downRect.colliderect(item.rect2):
                            can_down=False
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
                if item.varient=='wall corner':
                    if player.leftRect.colliderect(item.rect) or player.leftRect.colliderect(item.rect2):
                            can_left=False
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
                if item.varient=='wall corner':
                    if player.rightRect.colliderect(item.rect) or player.rightRect.colliderect(item.rect2):
                            can_right=False
                if item.rect.colliderect(player.rightRect):
                    can_right=False
            if can_right:
                player.x+=player.speed
                
        if pygame.mouse.get_pressed()[0]:
            if not inventory:
                if player.shootcooldown==0:
                    if player.gun=='T1 Lazer Pistol' or player.gun=='T2 Blaster Pistol':
                        projectile_list.append(lazer(mouse_pos[0],mouse_pos[1],(0,255,0),'player',0,0))
                    else:
                        projectile_list.append(lazer(mouse_pos[0],mouse_pos[1],(100,100,250),'player',0,0))
                    player.shootcooldown=player.fire_rate
        if player.shootcooldown != 0:
            player.shootcooldown-=1

        if not key[pygame.K_ESCAPE]:
            allow_esc=True
        if allow_esc:
            if key[pygame.K_ESCAPE]:
                menu=True
                first_run=True
        
        
pygame.quit()
