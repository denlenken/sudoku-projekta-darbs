import pygame as pg
pg.init()
import sqlite3
import copy
import getpass

#speles logs u.c. mainīgie
platums=660
augstums=660
gpeleks = (211,211,211)
font_title = pg.font.SysFont("FuturaMaxiStd-Light", 100)
font=pg.font.SysFont("FuturaMaxiStd-Light", 65)
logs = pg.display.set_mode((platums, augstums))
grutibas_pak=""
sakuma_laiks=0
zimetas_vertibas=[]
empties=0
mydb = sqlite3.connect("rekordi.db")
cur = mydb.cursor()
pg.display.set_caption("Sudoku")
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
cipari_kopija = copy.deepcopy(cipari)
#print(cipari_kopija)

class Poga():
    def __init__(self, x, y, bilde, izmers):
        platums = bilde.get_width()
        augstums = bilde.get_height()
        self.bilde = pg.transform.scale(bilde, (int(platums * izmers), int(augstums * izmers)))
        self.jauNospiests=False
        self.rect = self.bilde.get_rect()
        self.rect.topleft = (x,y)          
        
    #piešķir pogām funkcionalitāti
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

#rekordu attēlošana datu bāzē (augošā secībā pēc laika)
def rekordi():
    i = 50
    kol_space = 400

    virsr1 = font.render(f'SPĒLĒTĀJS', True, (0,0,0))
    virsr2 = font.render(f'LAIKS (s)', True, (0,0,0))
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

        #menu pogas
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
                laukuma_veidosana(zimetas_vertibas)      
            else:
                kluda=True
                teksts("Izvēlieties grūtību!", font_title, (0,0,0), 15, 300)  
         
        pg.display.flip()
        
def upd_db(lietotajvards, pagajusais_laiks): #pievieno datu bāzei datus
    cur.execute("INSERT INTO rekordi (name, time) VALUES (?,?)", (lietotajvards, pagajusais_laiks))
    mydb.commit()
    cur.close()
    mydb.close()

def gameover():#spēles beigu f-ja
    global sakuma_laiks
    sakuma_laiks = 0
    pagajusais_laiks = (pg.time.get_ticks() - sakuma_laiks) // 1000
    lietotajvards = getpass.getuser()
    upd_db(lietotajvards, pagajusais_laiks)
    teksts("Spēle beigusies!", font_title, (0,0,0), 50, 200)


def laukuma_veidosana(zimetas_vertibas): #spēles zīmēšana
    global rinda, kolonna, sakuma_laiks
    if cipari == cipari_kopija: #pārbauda, vai spēle beidzās. !!SVARĪGI!! galvenā while cikla dēļ, spēles beigu gadījumā logs uz mazu brīdi parāda beigu ekrānu un uzreiz izslēdz programmu. 
        #tas ir tāpēc, ka while cikls vairāk par vienu reizi mēģina atkārtot gameover() f-ju, tātad arī upd_db() jeb datu bāzes datu atjaunināšanas f-ju un tā cur.close(), kuru nevar izpildīt,
        #kad cur.close() jau tika izpildīts vienu reizi, tāpēc programma nocrasho, bet laiku rekordu sadaļā saglabā.
        #print("Spēle beigusies!")
        gameover()
        return

    if sakuma_laiks == 0: #pulkstenis
        sakuma_laiks = pg.time.get_ticks()
    pagajusais_laiks = (pg.time.get_ticks() - sakuma_laiks) // 1000
    laika_teksts = "Laiks: {} s".format(pagajusais_laiks)    
    laika_virsotne = font.render(laika_teksts, True, (0,0,0))
    laika_laukums= laika_virsotne.get_rect()
    laika_laukums.center = (335, 50)
    logs.blit(laika_virsotne, laika_laukums)

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
        pg.Vector2((i*(450/9))+110,560), linijas_biezums)    #TODO: cipari atkartojas. japaskatas ari tas, pec kada principa tiek genereti cipari

        pg.draw.line(logs, (60,60,60), pg.Vector2(110, (i*450/9)+110),
        pg.Vector2(560, (i*(450/9))+110), linijas_biezums)
        i+=1

    set_value=0
    #inputs
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            mouse_x, mouse_y = pg.mouse.get_pos() #kursora koord. nolasīšana
            global cell_x, cell_y      
            cell_x = mouse_x//50 #dalīts ar 50, jo tāds ir vienas šūnas izmērs (x un y)
            cell_y = mouse_y//50
            if cell_x in range(2, 11) and cell_y in range(2, 11) and cipari[cell_x-2][cell_y-2] ==0: #ifs skatās, vai klikšķis notiek sudoku laukumā un nospiestās šūnas vērtība ir 0. Citādi programma klikšķi nereģistrē
                #print("klikšķis [%d,%d]" % (cell_x, cell_y))
                for zimeta_vertiba in zimetas_vertibas:
                    if zimeta_vertiba[0] == (cell_x, cell_y):
                        zimetas_vertibas.remove(zimeta_vertiba)
                zimetas_vertibas.append(((cell_x, cell_y), "_"))
        if event.type == pg.KEYDOWN: #tiek nolasits lietotāja inputs
            if event.key == pg.K_1:
                set_value=1
                #print("1")
            elif event.key == pg.K_2:
                set_value=2
                #print("2")
            elif event.key == pg.K_3:
                set_value=3
                #print("3")
            elif event.key == pg.K_4:
                set_value=4
                #print("4")
            elif event.key == pg.K_5:
                set_value=5
                #print("5")
            elif event.key == pg.K_6:
                set_value=6
                #print("6")
            elif event.key == pg.K_7:
                set_value=7
                #print("7")
            elif event.key == pg.K_8:
                set_value=8
                #print("8")
            elif event.key == pg.K_9:
                set_value=9
                #print("9")
            if event.key == pg.K_BACKSPACE or event.key == pg.K_0:
                if zimetas_vertibas:
                    cell_x, cell_y = zimetas_vertibas[-1][0]
                    cipari[cell_x - 2][cell_y - 2] = 0
                    zimetas_vertibas.pop()
                set_value = None
                zimetas_vertibas = [(cell, value) for (cell, value) in zimetas_vertibas if value is not None]
            #uzzīmētā cipara vērtības piešķiršana sarakstam cipari, ņemot vērā uzzīmētā cipara pozīciju. pēc vērtības piešķiršanas, set_value atkal ir 0, lai varētu zīmēt vērtību citai šūnai
            if set_value is not None and zimetas_vertibas:
                zimetas_vertibas[-1] = (zimetas_vertibas[-1][0], set_value)
                cell_x, cell_y = zimetas_vertibas[-1][0]
                cipari[cell_x - 2][cell_y - 2] = set_value
                set_value = None
            #ja set_value ir 0, tātad šūnai atkal vērtība ir tukša, tāpēc sarakstā tajā vietā atkal ir 0
            if set_value == 0:  
                cipari[cell_x - 2][cell_y - 2] = set_value
                set_value = None

    for cell, value in zimetas_vertibas: #vērtību zīmēšana (tiek zimētas sarkanā krāsā, bet to var izmainīt)
        if value is not None:
            cell_x, cell_y = cell
            number_text = str(value)
            text_surface = font.render(number_text, True, (255,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = ((cell_x+0.6) * 50, (cell_y+0.7) * 50)
            logs.blit(text_surface, text_rect)
    
    pg.display.flip()

#teksta zīmēšanas f-ja
def teksts(teksts, font, fonta_krasa, x, y):
    teksts = font.render(teksts, True, fonta_krasa)
    logs.blit(teksts, (x, y))
    
strada()
