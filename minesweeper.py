import pygame
from pygame.locals import *
pygame.init()

import random

size=(640, 480)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Minesweeper")



class Tile(pygame.sprite.Sprite):
    id_num=0
    tiles_unclicked=0
    def __init__(self, total_tiles):
        '''
        T.__init__(int)
        Initializes Tile
        
        A tile that can be clicked on. It may hide a bomb. If it does contain a 
        bomb, and is clicked on, the player will lose. If it does not contain a
        bomb and is clicked on, it will display how many bombs within a 1 tile
        raduis of it. As an argument, it takes an integer of how many Tiles will
        be created in total.
        '''
        pygame.sprite.Sprite.__init__(self)
        self.sqrt=int(total_tiles**.5)
        self.image=pygame.image.load("tile_unclicked.bmp").convert()
        self.image=pygame.transform.scale(self.image, (int(400/self.sqrt), int(380/self.sqrt)))
        self.rect=self.image.get_rect()
        self.flagged=False
        self.clicked=False
        self.bomb=False
        self.bombs_around=0
        self.above=None
        self.below=None
        self.left=None
        self.right=None
        self.x=Tile.id_num-(int((Tile.id_num)/self.sqrt)*self.sqrt)
        self.y=int(Tile.id_num/self.sqrt)
        Tile.id_num+=1
        Tile.tiles_unclicked+=1
        
        #Finds where the Tile will be placed on-screen
        if self.x<=(self.sqrt/2)-1:
            temp_num=(self.x-((self.sqrt/2)-1))*-1
            self.rect.right=320-(temp_num*(int(400/self.sqrt)))
        if self.x>=(self.sqrt/2):
            temp_num=(self.x-(self.sqrt/2))
            self.rect.left=320+(temp_num*(int(400/self.sqrt)))
            
        self.rect.top=(self.y*int(380/self.sqrt))+77
        
        
              
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        '''
        M.__init__()
        Initializes Mouse
        '''
        pygame.sprite.Sprite.__init__(self)
        self.x=0
        self.y=0
        self.image=pygame.Surface((1,1)).convert()
        self.image.fill((0,0,0))
        self.image.set_alpha(0)        
        self.rect=self.image.get_rect()
        
    def update(self):
        '''
        M.update() --> None
        This method is used to move this sprite around on screen, and track the
        mouse.
        '''
        self.rect.left=self.x
        self.rect.top=self.y

mouse=Mouse()



def clear_bombs(tile):
    '''
    clear_bombs(Tile) --> None
    Called when the player clicks on a safe tile. This will clear the Tile it 
    takes as an agrument. If the given Tile dosnt have an adjacent bombs, this 
    funstion will call itself recjursivly to clear out those adjacent tiles.
    '''
    
    #Clears the Tile
    tile.clicked=True
    Tile.tiles_unclicked-=1
    tile.image=pygame.image.load("empty_tile.bmp").convert()
    tile.image=pygame.transform.scale(tile.image, ((int(400/tile.sqrt)), int(380/tile.sqrt)))
    
    #If a number should be displayed on the Tile
    if tile.bombs_around!=0:
        temp_text=numbers_font_tiles.render(str(tile.bombs_around), True, (0,0,0))
        temp_rect=temp_text.get_rect()
        temp_rect.center=(int(int(400/tile.sqrt)/2),int(int(400/tile.sqrt)/2))
        tile.image.blit(temp_text, temp_rect)
    
    
    #If the adjacent Tiles can also be cleared.
    if tile.bombs_around==0 and tile.bomb==False:
        if tile.above!=None:
            if tile.above.clicked==False and tile.above.flagged==False:
                clear_bombs(tile.above)
            if tile.above.left!=None:
                if tile.above.left.clicked==False and tile.above.left.flagged==False:
                    clear_bombs(tile.above.left)
        if tile.below!=None:
            if tile.below.clicked==False and tile.below.flagged==False:
                clear_bombs(tile.below)
            if tile.below.right!=None:
                if tile.below.right.clicked==False and tile.below.right.flagged==False:
                    clear_bombs(tile.below.right)
        if tile.left!=None:
            if tile.left.clicked==False and tile.left.flagged==False:
                clear_bombs(tile.left)
            if tile.left.below!=None:
                if tile.left.below.clicked==False and tile.left.below.flagged==False:
                    clear_bombs(tile.left.below)
        if tile.right!=None:
            if tile.right.clicked==False and tile.right.flagged==False:
                clear_bombs(tile.right)
            if tile.right.above!=None:
                if tile.right.above.clicked==False and tile.right.above.flagged==False:
                    clear_bombs(tile.right.above)
                    
    return



background=pygame.Surface(size)
background=background.convert()

#Loads the images for the game
frame=pygame.image.load("outer_frame.bmp").convert()
frame=pygame.transform.scale(frame, ((10*40)+50, size[1]))
frame_rect=frame.get_rect()
frame_rect.centerx=size[0]/2

face_spot=pygame.image.load("face_spot.bmp").convert()
face_spot=pygame.transform.scale(face_spot, ((35,35)))
face_spot_rect=face_spot.get_rect()
face_spot_rect.centerx=size[0]/2
face_spot_rect.centery=42

smile_face=pygame.image.load("smile.bmp").convert()
smile_face=pygame.transform.scale(smile_face, ((28,28)))
smile_face.set_colorkey((255,255,255))
smile_face_rect=smile_face.get_rect()
smile_face_rect.centerx=size[0]/2
smile_face_rect.centery=42

smug_face=pygame.image.load("smug.bmp").convert()
smug_face=pygame.transform.scale(smug_face, ((28,28)))
smug_face.set_colorkey((255,255,255))
smug_face_rect=smug_face.get_rect()
smug_face_rect.centerx=size[0]/2
smug_face_rect.centery=42

dead_face=pygame.image.load("dead.bmp").convert()
dead_face=pygame.transform.scale(dead_face, ((28,28)))
dead_face.set_colorkey((255,255,255))
dead_face_rect=dead_face.get_rect()
dead_face_rect.centerx=size[0]/2
dead_face_rect.centery=42

scared_face=pygame.image.load("scared_face.bmp").convert()
scared_face=pygame.transform.scale(scared_face, ((28,28)))
scared_face.set_colorkey((255,255,255))
scared_face_rect=scared_face.get_rect()
scared_face_rect.centerx=size[0]/2
scared_face_rect.centery=42

black_box=pygame.Surface((80,39)).convert()
black_box.fill((0,0,0))



#Creates the Tiles for the game
total_tiles=100

helvet=pygame.font.match_font("Helvetica", True, False)
numbers_font_tiles=pygame.font.Font(helvet, int((400/(total_tiles**.5))-4))

numbers_font_red=pygame.font.Font(helvet, 38)
tiles=[]
for i in range(0,total_tiles):
    tile=Tile(total_tiles)
    tiles+=[tile]

c=0
for i in tiles:
    if i.y!=0:
        i.above=tiles[c-i.sqrt]
    if i.y!=i.sqrt-1:
        i.below=tiles[c+i.sqrt]
    if i.x!=0:
        i.left=tiles[c-1]
    if i.x!=i.sqrt-1:
        i.right=tiles[c+1]
    c+=1
    
#Fills the Tiles with bombs
bombs=10
bomb_list=[]

for i in range(0,bombs):
    bomb_pos=random.randint(0,total_tiles-1)
    while tiles[bomb_pos].bomb==True:
        bomb_pos=random.randint(0,total_tiles-1)
    tiles[bomb_pos].bomb=True
    if tiles[bomb_pos].above!=None:
        tiles[bomb_pos].above.bombs_around+=1
        if tiles[bomb_pos].above.left!=None:
            tiles[bomb_pos].above.left.bombs_around+=1
    if tiles[bomb_pos].below!=None:
        tiles[bomb_pos].below.bombs_around+=1
        if tiles[bomb_pos].below.right!=None:
            tiles[bomb_pos].below.right.bombs_around+=1
    if tiles[bomb_pos].left!=None:
        tiles[bomb_pos].left.bombs_around+=1
        if tiles[bomb_pos].left.below!=None:
            tiles[bomb_pos].left.below.bombs_around+=1
    if tiles[bomb_pos].right!=None:
        tiles[bomb_pos].right.bombs_around+=1
        if tiles[bomb_pos].right.above!=None:
            tiles[bomb_pos].right.above.bombs_around+=1
    bomb_list+=[tiles[bomb_pos]]



tile_group=pygame.sprite.Group(tiles)

background.fill((192, 192, 192))

clock=pygame.time.Clock()
keep_going=True

bombs_flagged=0
tiles_flagged=0
Tile.tiles_unclicked-=bombs

game_over=False
game_won=False
last_time_r_clicked=False
l_clicking=False
time_spent=0

while keep_going:
    
    clock.tick(30)
            
    if bombs_flagged==bombs and tiles_flagged==bombs and Tile.tiles_unclicked==0:
        game_won=True
        
    if game_over!=True and game_won!=True:
        time_spent+=1
    
    
    for ev in pygame.event.get():
        
        if ev.type==QUIT:
            keep_going=False
            
        if ev.type==MOUSEMOTION:
            mouse.x=ev.pos[0]
            mouse.y=ev.pos[1]
            
        if ev.type==KEYDOWN:
            #Restarts the game
            if ev.key==114:
                
                game_over=False
                game_won=False
                l_clicked=False
                l_clicking=False
                r_clicked=False
                r_clicking=False
                time_spent=0
                tiles_flagged=0
                bombs_flagged=0
                
                #Creates the Tiles for the game
                
                Tile.id_num=0
                Tile.tiles_unclicked=0-bombs
                
                
                tiles=[]
                for i in range(0,total_tiles):
                    tile=Tile(total_tiles)
                    tiles+=[tile]
                
                c=0
                for i in tiles:
                    if i.y!=0:
                        i.above=tiles[c-i.sqrt]
                    if i.y!=i.sqrt-1:
                        i.below=tiles[c+i.sqrt]
                    if i.x!=0:
                        i.left=tiles[c-1]
                    if i.x!=i.sqrt-1:
                        i.right=tiles[c+1]
                    c+=1
                    
                #Fills the Tiles with bombs
                bomb_list=[]
                
                for i in range(0,bombs):
                    bomb_pos=random.randint(0,total_tiles-1)
                    while tiles[bomb_pos].bomb==True:
                        bomb_pos=random.randint(0,total_tiles-1)
                    tiles[bomb_pos].bomb=True
                    if tiles[bomb_pos].above!=None:
                        tiles[bomb_pos].above.bombs_around+=1
                        if tiles[bomb_pos].above.left!=None:
                            tiles[bomb_pos].above.left.bombs_around+=1
                    if tiles[bomb_pos].below!=None:
                        tiles[bomb_pos].below.bombs_around+=1
                        if tiles[bomb_pos].below.right!=None:
                            tiles[bomb_pos].below.right.bombs_around+=1
                    if tiles[bomb_pos].left!=None:
                        tiles[bomb_pos].left.bombs_around+=1
                        if tiles[bomb_pos].left.below!=None:
                            tiles[bomb_pos].left.below.bombs_around+=1
                    if tiles[bomb_pos].right!=None:
                        tiles[bomb_pos].right.bombs_around+=1
                        if tiles[bomb_pos].right.above!=None:
                            tiles[bomb_pos].right.above.bombs_around+=1
                    bomb_list+=[tiles[bomb_pos]]
                
                tile_group=pygame.sprite.Group(tiles)
                     
                     
    #Tracks if the mouse has been clicked
    m_buttons=pygame.mouse.get_pressed()
    if m_buttons[0]==0:
        l_clicked=False
    if m_buttons[0]==1:
        l_clicked=True
        l_clicking=True
    if m_buttons[2]==0:
        last_time_r_clicked=False
        r_clicked=False
    if m_buttons[2]==1:
        r_clicked=True
        
    if game_over==False and game_won==False:     
        collisions=pygame.sprite.spritecollide(mouse, tile_group, False)
        
        #If the player tries to clear a Tile
        if l_clicked==False and l_clicking==True:
            l_clicking=False
            for i in collisions:
                if i.clicked==False and i.flagged==False:
                    i.clicked=True
                    
                    #If the player clicks on a bomb
                    if i.bomb==True:
                        game_over=True
                        for ii in bomb_list:
                            i.image=pygame.image.load("bomb_red.bmp").convert()
                            i.image=pygame.transform.scale(i.image, ((int(400/i.sqrt)), int(380/i.sqrt)))
                            if ii!=i:
                                ii.image=pygame.image.load("bomb_clicked.bmp").convert()
                                ii.image=pygame.transform.scale(ii.image, ((int(400/i.sqrt)), int(380/i.sqrt)))
                    
                    #If the player clicks on a Tile with no bomb
                    if i.bomb==False:
                        i.image=pygame.image.load("empty_tile.bmp").convert()
                        i.image=pygame.transform.scale(i.image, ((int(400/i.sqrt)), int(380/i.sqrt)))
                        if i.bombs_around!=0:
                            Tile.tiles_unclicked-=1
                            temp_text=numbers_font_tiles.render(str(i.bombs_around), True, (0,0,0))
                            temp_rect=temp_text.get_rect()
                            temp_rect.center=(int(int(400/i.sqrt)/2),int(int(400/i.sqrt)/2))
                            i.image.blit(temp_text, temp_rect)
                        if i.bombs_around==0:
                            clear_bombs(i)      
        
        #If the player places or removes a flag from a Tile
        if r_clicked==True and last_time_r_clicked==False:
            last_time_r_clicked=True
            for i in collisions:
                if i.clicked==False:
                    if i.flagged==False:
                        i.flagged=True
                        i.image=pygame.image.load("flag.bmp").convert()
                        i.image=pygame.transform.scale(i.image, ((int(400/i.sqrt)), int(380/i.sqrt)))
                        tiles_flagged+=1
                        if i.bomb==True:
                            bombs_flagged+=1
                    elif i.flagged==True:
                        i.flagged=False
                        i.image=pygame.image.load("tile_unclicked.bmp").convert()
                        i.image=pygame.transform.scale(i.image, ((int(400/i.sqrt)), int(380/i.sqrt)))
                        tiles_flagged-=1
                        if i.bomb==True:
                            bombs_flagged-=1
        
    #Updates what will be shown on the UI
    bombs_counter=bombs-tiles_flagged
    bombs_counter_text=numbers_font_red.render(str(bombs_counter), True, (255,0,0))
    
    time_spent_text=numbers_font_red.render(str(min(int(time_spent/30),99999)), True, (255,0,0))
    
    #Displays the UI        
    mouse.update()
    background.blit(frame, frame_rect)
    background.blit(face_spot, face_spot_rect)
    background.blit(black_box, (120, 23))#mines
    background.blit(bombs_counter_text, (120,23))
    background.blit(black_box, (440, 23))#time
    background.blit(time_spent_text, (440, 23))
    if game_over==True:
        background.blit(dead_face, dead_face_rect)
    elif game_won==True:
        background.blit(smug_face, smug_face_rect)
    elif l_clicking==True:
        background.blit(scared_face, scared_face_rect)
    else:
        background.blit(smile_face, smile_face_rect)
    tile_group.draw(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()