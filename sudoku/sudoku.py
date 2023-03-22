import pygame as pg
pg.init()
import sqlite3

#speles logs
platums=660
augstums=660
balts = (255,255,255) #krasas, ar kurām var piešķirt logam tumšo/gaišo tēmu
gpeleks = (211,211,211)
font_title = pg.font.SysFont("FuturaMaxiStd-Light", 100)
font=pg.font.SysFont("FuturaMaxiStd-Light", 65)
logs = pg.display.set_mode((platums, augstums))
#mainīgie, kas noderēs tālāk kodā
grutibas_pak=""
empties=0
mydb = sqlite3.connect("rekordi.db")
cur = mydb.cursor()
pg.display.set_caption("Sudoku")

#algoritms skaitļu ģenerācijai (avots: https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
base = 3
side = base*base
squares = side*side
# pattern for a baseline valid solution
def pattern(r,c): 
    return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): 
    return sample(s,len(s)) 

rBase = range(base) 
rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
cipari = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
#print(cipari)


#klase pogām
class Poga():
    def __init__(self, x, y, bilde, izmers):
        platums = bilde.get_width()
        augstums = bilde.get_height()
        self.bilde = pg.transform.scale(bilde, (int(platums * izmers), int(augstums * izmers)))
        self.jauNospiests=False
        self.rect = self.bilde.get_rect()
        self.rect.topleft = (x,y)
                           
        
    #piešķir pogām to funkcionalitāti
    def draw(self, virsma):
        darbiba = False
        poz_poga = pg.mouse.get_pos()
        if self.rect.collidepoint(poz_poga):
            if pg.mouse.get_pressed()[0] == 1 and self.jauNospiests == False:
                self.jauNospiests = True
                darbiba = True
        if pg.mouse.get_pressed()[0] == 0:
            self.jauNospiests = False    

        virsma.blit(self.bilde, (self.rect.x, self.rect.y))  

        return darbiba  

#bilžu un poga pievienošana
spelet_bilde = pg.image.load("bildes/spelet.png").convert_alpha()
grutiba_bilde = pg.image.load("bildes/grutiba.png").convert_alpha()
rekordi_bilde = pg.image.load("bildes/rekordi.png").convert_alpha()
atpakal_bilde = pg.image.load("bildes/back.png").convert_alpha()
viegla_bilde = pg.image.load("bildes/viegla.png").convert_alpha()
videja_bilde = pg.image.load("bildes/videja.png").convert_alpha()
gruta_bilde = pg.image.load("bildes/gruta.png").convert_alpha()

spelet_poga = Poga(230,150, spelet_bilde, 1)
grutiba_poga = Poga(230,275, grutiba_bilde, 1)
rekordi_poga = Poga(230,400, rekordi_bilde, 1)
atpakal_poga = Poga(230, 560, atpakal_bilde, 1)
viegla_poga = Poga(10, 150, viegla_bilde, 1)
videja_poga = Poga(230, 150, videja_bilde, 1)
gruta_poga = Poga(450, 150, gruta_bilde, 1)

#funkcija rekordu zīmēšanai
def rekordi():
    i = 50
    kol_space = 400

    virsr1 = font.render(f'SPĒLĒTĀJS', True, (0,0,0))
    virsr2 = font.render(f'LAIKS', True, (0,0,0))
    logs.blit(virsr1, [40, 15])
    logs.blit(virsr2, [40 + kol_space, 15])
    
    cur.execute('SELECT * FROM rekordi')
    rows = cur.fetchall()
    for row in rows:
        
        kol1 = font.render(str(row[1]), True, (0,0,0))
        kol2 = font.render(str(row[2]), True, (0,0,0))
        logs.blit(kol1, [60, 50 + i])
        logs.blit(kol2, [60 + kol_space, 50 + i])

        i += 50

#funckija, kas iedarbina programmu
def strada():
    global grutibas_pak
    spele_strada = True
    tagadejais_laukums="menu"
    kluda=False
    while spele_strada == True: #cikls, kas ļauj spēles logam strādāt tik ilgi, kamēr tas netiks aizvērts
        logs.fill(gpeleks)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                spele_strada = False
            
            
                
        
        #menu pogas. ja tagadejais_laukums == kāda no vērtībām, tad laukums no mainās. if.piemers.poga.draw(logs) pārbauda, vai 
        #poga ir nospiesta un tādā gadījumā izdara piešķirto darbību
        if tagadejais_laukums == "grutiba" or tagadejais_laukums == "rekordi" or kluda==True:
            if atpakal_poga.draw(logs):
                kluda=False
                tagadejais_laukums="menu"
        if tagadejais_laukums == "menu":
            teksts("Sudoku Classic", font_title, (0,0,0), 70, 20)
            if spelet_poga.draw(logs):
                tagadejais_laukums="spele"
            elif grutiba_poga.draw(logs):
                tagadejais_laukums="grutiba"
            elif rekordi_poga.draw(logs):
                tagadejais_laukums="rekordi"
        elif tagadejais_laukums=="grutiba":
            if viegla_poga.draw(logs):
                grutibas_pak = "viegla"
                for p in sample(range(squares),40):
                    cipari[p//side][p%side] = 0
            elif videja_poga.draw(logs):
                grutibas_pak = "videja"
                for p in sample(range(squares),50):
                    cipari[p//side][p%side] = 0
            elif gruta_poga.draw(logs):
                grutibas_pak = "gruta"     
                for p in sample(range(squares),60):
                    cipari[p//side][p%side] = 0    
        elif tagadejais_laukums == "rekordi":
            rekordi() 
        elif tagadejais_laukums=="spele": 
            if grutibas_pak == "viegla" or grutibas_pak == "videja" or grutibas_pak == "gruta":
                laukuma_veidosana()      
            else:
                kluda=True
                teksts("Izvēlieties grūtību!", font_title, (0,0,0), 15, 300)  
        
                 
             
         
            
        
                
                

        

        
        
        pg.display.flip()
        
        


def laukuma_veidosana():
 
    
            

    global rinda, kolonna
    for kolonna in range(9):#zīmē ciparus
         for rinda in range(9):
            if cipari[rinda][kolonna] !=0:
                vertiba=font.render(str(cipari[rinda][kolonna]), 1, (0,0,0))
                logs.blit(vertiba, (rinda*(450/9)+122.5, kolonna*(450/9)+115.5)) 
            
    
    
    
    i=1
    while i*(450/9)<450:    #cikls, kurš zīmē līnijas
        if i%3>0:   #ik pēc katras cikla iterācijas, ja i vērtību dalot ar 3 ir atlikums, tad līnija tiek izlaista, citādi - līnija ar biezumu "10". Tādā veidā katra trešā līnija (jo tiek zīmētas vēl divas ar biezumu 0) ir biezā, kas sadala laukumus
            linijas_biezums=5 
        else:
            linijas_biezums=10
        #
        pg.draw.line(logs, (60,60,60), pg.Vector2((i*450/9)+110, 110),
        pg.Vector2((i*(450/9))+110,560), linijas_biezums)    

        pg.draw.line(logs, (60,60,60), pg.Vector2(110, (i*450/9)+110),
        pg.Vector2(560, (i*(450/9))+110), linijas_biezums)
        i+=1

    

    #vieta inputam
    for event in pg.event.get():
        nospiesta_suna=None
        izvelets = False
        if event.type == pg.MOUSEBUTTONUP:
            mouse_x, mouse_y = pg.mouse.get_pos()      
            cell_x = mouse_x//50
            cell_y = mouse_y//50
            if cell_x in range(2,11):
                if cell_y in range(2,11):
                    print( "Click in cell [%d,%d]" % ( cell_x, cell_y ) )





   

        
    pg.display.flip()
    





        

   


#f-ja, kas zīmē tekstu
def teksts(teksts, font, fonta_krasa, x, y):
    teksts = font.render(teksts, True, fonta_krasa)
    logs.blit(teksts, (x, y))
    


strada()
