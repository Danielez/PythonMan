#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
import sys
import os
import pygame
from pygame.locals import *
import lib.pyganim as pyganim

def elog(e):
    elog = open("Error_log.txt", "a")
    elog.write(str(e) + "\n")
    elog.close()

def terminate():
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()    
    
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,25"  # posizione in cui verr� creata la finestra
pygame.init()
pygame.mixer.init()

FPS = 30  # Frame al secondo
clock = pygame.time.Clock()  # Contatore aggiornamento schermo
pygame.key.set_repeat(1, 20)   



################# SCHERMO ###############################
largh = 1024
altez = 710 
schermo = pygame.display.set_mode((largh, altez))  # la finestra
pygame.display.set_caption('PythonMan ver 0.1(Alpha)  --Procedural Escape from {JavaLand}  --Daniele Buffa')  # titolo

################# CARATTERE #############################
carattere = pygame.font.SysFont("comicsansms", 12)  # Carattere
carattere20 = pygame.font.SysFont("comicsansms", 20)
carattere25 = pygame.font.SysFont("comicsansms", 25)
carattere30 = pygame.font.SysFont("comicsansms", 30)
carattere40 = pygame.font.SysFont("comicsansms", 40)

################# IMMAGINI ##############################
img_path = "img"
background_path = os.path.join(img_path, "background")
end_seq_path = "end_seq"
end_seq_path = os.path.join(img_path, end_seq_path)
end_seq_files = [x for x in os.listdir(end_seq_path) if x.endswith("jpg") or x.endswith("jpeg")]
end_seq_files.sort()
end_seq_list = [pygame.image.load(os.path.join(end_seq_path, x)) for x in end_seq_files]
end_seq_list = [pygame.transform.scale(x, (1024, 710)) for x in end_seq_list]
end_seq_list = [x.convert() for x in end_seq_list]

background_files = [x for x in os.listdir(background_path) if x.endswith("jpg") or x.endswith("jpeg")]
background_list = [pygame.image.load(os.path.join(background_path, x)) for x in background_files]
background_list = [pygame.transform.scale(x, (1024, 710)) for x in background_list]
background_list = [x.convert() for x in background_list]
background_img = random.choice(background_list)

try:
    vittoria_img = pygame.image.load(os.path.join(img_path, "vittoria.jpg"))
    vittoria_img.convert()

    sconfitta_img = pygame.image.load(os.path.join(img_path, "sconfitta.jpg"))
    sconfitta_img.convert()

    pre_intro_img = pygame.image.load(os.path.join(img_path, "pre_intro.jpg"))
    pre_intro_img.convert()

    intro_img = pygame.image.load(os.path.join(img_path, "intro.jpg"))
    intro_img.convert()
    
    crediti_img = pygame.image.load(os.path.join(img_path, "crediti.jpg"))
    crediti_img.convert()
    
    nemici_img = pygame.image.load(os.path.join(img_path, "java.png"))
    nemici_img = pygame.transform.scale(nemici_img, (20, 20))
    nemici_img.convert()

    tile_img = pygame.image.load(os.path.join(img_path, "tile.jpg"))
    tile_img.convert()

    tileDanger_img = pygame.image.load(os.path.join(img_path, "tileDanger.jpg"))
    tileDanger_img.convert()

    tileDanger2_img = pygame.image.load(os.path.join(img_path, "tileDanger2.jpg"))
    tileDanger2_img.convert()
    
    
except Exception as e:
    elog(e)
    # os.startfile("Error_log.txt")
    terminate()

################# MUSICA ################################
suona_bool = True
music_path = "music"
music_files = [x for x in os.listdir(music_path) if x.endswith("mp3") or x.endswith("MP3") or x.endswith("WAV") or x.endswith("wav")]
if "bob.mp3" in music_files:  # la colonna sonora dei crediti
    del music_files[music_files.index("bob.mp3")]  # non verr� riprodotta durante il gioco normale

def suona():
    if music_files:  # ovvero se la lista music_files non � vuota... carica un brano a caso e suonalo
        pygame.mixer.music.load(os.path.join(music_path, random.choice(music_files)))
        pygame.mixer.music.play()

def nuovo_background():
    global background_img
    background_img = random.choice(background_list)
    


def lato_collisione(r, other):
    """prende due rettangoli. ritorna il lato della collisione"""
    sinistra = destra = sotto = sopra = False
    Rect = pygame.Rect
    left = Rect(r.left - 1, r.centery - 1, r.width / 2 - 1, 2)
    right = Rect(r.centerx + 2, r.centery - 1, r.width / 2 - 1, 2)
    top = Rect(r.centerx - 1, r.top - 1, 2, r.height / 2)
    bottom = Rect(r.centerx - 1, r.centery + 1, 2, r.height / 2)
    
    
    if left.colliderect(other):
        sinistra = True
    if right.colliderect(other):
        destra = True
    if bottom.colliderect(other):
        sotto = True
    if top.colliderect(other):
        sopra = True
    return sinistra, destra, sotto, sopra        

def prossimo_livello():
    global l
    global vittoria_bool
    titoli = ["Bene, andiamo avanti",
              "Lunga vita al platform",
              "La mia zita ha commentato:'ma che razza di livello �?'",
              "Sei arrivato fin qui? poi va solo a peggiorare...",
              "Che fai insisti?",
              "Speri di riuscire a vedere la schermata finale?",
              "Questo era difficile? il prossimo � un incubo",
              "E' stato molto cinematografico vero?",
              "Liberamente ispirato ad una scena di un film"]
    pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
    pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
    schermo.blit(carattere30.render(titoli[l], True, GREEN), (50, 350))
    pygame.display.update()
    pygame.time.wait(500)
    premi_continua()
    
    if l == len(livelli) - 1:  # se abbiamo completato l'ultimo livello --> vittoria
        pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
        pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
        schermo.blit(carattere40.render("MISSIONE COMPIUTA Mr. PythonMan!", True, GREEN), (50, 350))
        pygame.display.update()
        pygame.time.wait(500)
        premi_continua()
        
        schermo.blit(end_seq_list[0], (0, 0))
        pygame.display.update()
        pygame.time.wait(1000)
        premi_continua()
        
        schermo.blit(end_seq_list[1], (0, 0))
        pygame.display.update()
        pygame.time.wait(1000)
        premi_continua()
        
        schermo.blit(end_seq_list[2], (0, 0))
        pygame.display.update()
        pygame.time.wait(1000)
        premi_continua()
        
        vittoria_bool = True
    else:
        l += 1
        nuovo_background()
        genera_nemici()
        riposiziona()
        presentazione.reset()

def riposiziona():  # ricominciare il livello corrente
    global livelli
    global player
    global nemici_cor
    global vittoria_bool
    global sconfitta_bool
    vittoria_bool = sconfitta_bool = False 
    player.centerx = livelli[l][0].left + 10  # riposiziona il giocatore sul primo rettangolo del livello
    player.centery = livelli[l][0].top - 20
    genera_nemici()
    livelli = [carica_lev(os.path.join(lev_path, x)) for x in lev_files if x.startswith("lev")]
    presentazione.reset()
    
def ricomincia():  # ricominciare tutto il gioco
    global livelli
    global l
    global vittoria_bool
    global sconfitta_bool
    vittoria_bool = sconfitta_bool = False
    l = 0
    nuovo_background()
    riposiziona()
    livelli = [carica_lev(os.path.join(lev_path, x)) for x in lev_files if x.startswith("lev")]
    presentazione.reset()
    
def vittoria():
    schermo.fill(WHITE)
    schermo.blit(vittoria_img, (0, 0))
    pygame.display.update()

def sconfitta():
    temp_img = pygame.transform.flip(pygame.transform.scale(walk_list[0][0], (180, 222)), True, False)
    temp_img.set_colorkey(temp_img.get_at((0, 0)))
    schermo.fill(WHITE)
    schermo.blit(sconfitta_img, (0, 0))
    schermo.blit(temp_img, (844, 280))
    pygame.display.update()

class Piattaforma(pygame.Rect):
    def __init__(self, a, b, c, d, cade=False, timer=0):
        pygame.Rect.__init__(self, a, b, c, d)
        self.cade = cade
        self.timer = timer
        self.vy = 0
        self.unlocked = False

def carica_lev(lev_path):  # questa funzione legge i file levx.txt e restituisce una lista di rettangoli
    lista = []
    colonna = riga = 0
    file = open(lev_path).readlines()
    for line in file:
        line = line.rstrip("\n")
        for c in line:
            if c == "!":
                lista.append(Piattaforma(colonna * spaz, riga * spaz, spaz, spaz, True, 40))
                colonna += 1
            if c == "=":
                lista.append(Piattaforma(colonna * spaz, riga * spaz, spaz, spaz, True))
                colonna += 1
            if c == "#":
                lista.append(Piattaforma(colonna * spaz, riga * spaz, spaz, spaz))
                colonna += 1
            if c == " ":
                colonna += 1
            if c == "s":
                lista.insert(0, Piattaforma(colonna * spaz, riga * spaz, 20, 20))
                colonna += 1
            if c == "e":
                end_rect = (Piattaforma(colonna * spaz, riga * spaz, 40, 40))
                colonna += 1
        colonna = 0
        riga += 1
    lista.append(end_rect)
    return lista

def pausa():
    pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
    pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
    schermo.blit(carattere40.render("PAUSA", True, GREEN), (450, 350))
    pygame.display.update()
    pygame.mixer.music.pause()
    pygame.time.wait(500)
    premi_continua()
    pygame.mixer.music.unpause()
    
def premi_continua():  # premere un tasto per continuare
    
    pause_bool = True
    while pause_bool:
        
        for event in pygame.event.get():
            if event.type == QUIT:  # Chiusura finestra
                terminate()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pause_bool = False
 
def crediti():
    pygame.mixer.music.stop()
    
    i = 0
    crediti_list = ["Si ringrazia il Python, un linguaggio semplice chiaro e diretto",
                  "Si ringrazia il Java, un linguaggio astratto burocratico e criptico",
                  "Si ringrazia la mia zita per il beta testing",
                  "Si ringrazia il professore Vacanti per aver inventato il nome di battaglia 'PythonMan'",
                  "Si ringrazia la libreria Pygame",
                  "Si ringrazia il mr.x a cui ho zaffato la sprite dell'uomo che corre",
                  "Si ringraziano i colleghi del corso per il sostegno morale",
                  "Si ringrazia la marlboro",
                  "Si ringrazia il mio motorino"]
    pause_bool = True
    pygame.time.wait(500)
    while pause_bool:
        if not pygame.mixer.music.get_busy():
            if "bob.mp3" in os.listdir(music_path):
                pygame.mixer.music.load(os.path.join(music_path, "bob.mp3"))
                pygame.mixer.music.play()
        for event in pygame.event.get():
            if event.type == QUIT:  # Chiusura finestra
                terminate()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pause_bool = False
        schermo.fill(BLACK)
        schermo.blit(crediti_img, (0, 0))
        for index, item in enumerate(crediti_list):
            pygame.draw.rect(schermo, BLACK, (0, ((index * 40) - 327) + (i / 5), 1024, 25), 0)
            schermo.blit(carattere20.render(item, True, WHITE), (50, ((index * 40) - 330) + (i / 5)))
        
        
        i += 1 
        pygame.display.update()
    suona()
            
    
 
################# LIVELLI ###############################
spaz = 20  # grandezza di un "mattone" del livelli
lev_path = "level"
lev_files = os.listdir(lev_path)
lev_files.sort()
livelli = [carica_lev(os.path.join(lev_path, x)) for x in lev_files if x.startswith("lev")]
l = 0 

class Presentazione:
    def __init__(self):
        self.timer = 0
        self.titoli = ["Livello 0: Il primo livello � sempre facile.",
                       "Livello 1: Lo spirito del platform.",
                       "Livello 2: Caduta di stile.",
                       "Livello 3: Odierai la scaletta a sinistra.",
                       "Livello 4: Piattaforme cadenti.",
                       "Livello 5: Cominciamo a fare sul serio.",
                       "Livello 6: Labirintomania.",
                       "Livello 7: L'ultima fuga di PythonMan",
                       "Livello 8: Atto di fede."]
    def presenta(self):
        if self.timer < 100:
            pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
            pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
            schermo.blit(carattere40.render(self.titoli[l], True, GREEN), (50, 350))
        self.timer += 1
    def reset(self):
        self.timer = 0

presentazione = Presentazione()

     

################# SCRITTE JAVESI ########################
text = ["public", "static", "void", "main", "class", "try", "catch", "throw", "throws",
            "enum", "implements", "float", "double", "int", "byte", "string", "import", "interface", "long",
            "private", "short", "this", "while", "return", ";", "{}"]
textObj = [carattere20.render(x, True, GREEN) for x in text]
text_cor = [[random.randrange(20, largh - 50), random.randrange(altez)] for x in textObj]

################# NEMICI ################################
class Nemici(object):
    def __init__(self, a, b, direzx=random.choice(["left", "right"]), direzy=random.choice(["up", "down"])):
        self.rect = pygame.Rect(a, b, 20, 20)
        self.direzx = direzx
        self.direzy = direzy
        self.vx = random.randrange(1, 4)
        self.vy = random.randrange(1, 4)
            
def genera_nemici():
    global nemici_list
    global rand_piat
    global nemici_piattaforma
    nemici_list = [Nemici(random.randrange(largh), random.randrange(altez)) for x in range(l / 2)]
    rand_piat = [random.choice(livelli[l][1:]) for x in range((l / 2) + 1)]
    nemici_piattaforma = [Nemici(x.centerx, x.top - 20, direzx="", direzy="up") for x in rand_piat] if l != 8 else []

genera_nemici()

################# GIOCATORE #############################
pito_path = "pito"
pito_path = os.path.join(img_path, pito_path)
walk = pygame.image.load(os.path.join(pito_path, "walk.png"))
colorkey = walk.get_at((0, 0))
walk_list = []
for x in range(0, 1440, 240):
    for y in range(0, 1480, 296):
        walk_list.append((walk.subsurface(x, y, 240, 296), 0.1))



pitoright = pyganim.PygAnimation(walk_list)

pitoleft = pitoright.getCopy()
pitoleft.flip(True, False)

pitoleft.set_colorkey(colorkey)
pitoleft.scale([45, 45])
pitoleft.convert()
pitoleft.set_alpha()  # disabilita l'alpha altrimenti il colorkey non ha effetto
pitoleft.pause()

pitoright.set_colorkey(colorkey)
pitoright.scale([45, 45])
pitoright.convert()
pitoright.set_alpha()
pitoright.pause()

playeranimation = pitoright

p_v_x = 6 
p_v_y = 0    
player = pygame.Rect(0, 0, 30, 40) 
riposiziona()
aterra = False    



################# STATO DELLA PARTITA ###################
sconfitta_bool = False
vittoria_bool = False

################# PRE INTRO #############################

schermo.blit(pre_intro_img, (0, 0))
pygame.display.update()
premi_continua()
pygame.time.wait(500)

################# INTRO #################################
temp_img = pygame.transform.scale(walk_list[0][0], (180, 222))
temp_img.set_colorkey(temp_img.get_at((0, 0)))
schermo.blit(intro_img, (0, 0))
schermo.blit(temp_img, (0, 250))
pygame.display.update()
premi_continua()    
pygame.time.wait(500)
    
################# CICLO PRINCIPALE ######################

while True:
        playeranimation.pause()
        # schermo.fill(WHITE)
        
        schermo.blit(background_img, (0, 0))
        
        if suona_bool:
            if not pygame.mixer.music.get_busy():
                suona()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:  # Chiusura finestra
                terminate()
            
        key = pygame.key.get_pressed() 
        if key[K_LEFT]:
            player.centerx -= p_v_x
            playeranimation = pitoleft
            playeranimation.play()
        if key[K_RIGHT]:
            player.centerx += p_v_x
            playeranimation = pitoright
            playeranimation.play()
        if key[K_UP] and aterra:
            if l == 8:  # nel livello 8 il giocatore pu� saltare molto di pi� del normale
                p_v_y = -28
                aterra = False
            else:
                p_v_y = -10
                aterra = False
        if key[K_r]:
            ricomincia()
        if key[K_x]:
            terminate()
        if key[K_t]:
            riposiziona()
        if key[K_n]:
            suona()
        if key[K_m]:
            suona_bool = False
            pygame.mixer.music.stop()
        if key[K_b]:
            suona_bool = True
        if key[K_p]:
            pausa()
        if key[K_c]:
            crediti()
        if key[K_F1]:
            try:
                os.startfile("help.txt")
                pausa()
            except OSError as e:
                elog(e)
                
        
        if not sconfitta_bool and not vittoria_bool:
        
            aterra = False
            for i in livelli[l]:  # ogni rettangolo del livello l
                if player.colliderect(i):  # se c'� collisione
                    if i == livelli[l][-1]:  # collisione con l'ultimo rettangolo
                        prossimo_livello()  # prossimo livello, se siamo nell'ultimo livello vittoria
                    
                    lato_coll = lato_collisione(player, i)  # da che lato � stata la collisione?
                                        
                    if lato_coll[2]:  # collisione sotto
                        player.bottom = i.top + 1
                        # pygame.draw.rect(schermo,RED,(player.centerx-1, player.centery+1, 2, player.height/2),1)
                        aterra = True
                        if p_v_y > 0:  # distinguere fra un salto e la caduta
                            p_v_y = 0
                    
                    elif lato_coll[3]:  # collisione sopra
                        # pygame.draw.rect(schermo,RED,(player.centerx-1, player.top-1, 2, player.height/2),1)
                        player.top = i.bottom
                        p_v_y = 0
                    
                    elif lato_coll[0]:  # collisione a sinistra
                        player.left = i.right - 1
                        # pygame.draw.rect(schermo,RED,(player.left-1, player.centery-1, player.width/2-1, 2),1) 
                        
                
                    elif lato_coll[1]:  # collisione a destra
                        player.right = i.left + 1
                        # pygame.draw.rect(schermo,RED,(player.centerx+2, player.centery-1, player.width/2-1, 2),1)
                    
                    if i.cade:  # Piattaforme cadenti, il giocatore toccandole innesca il timer
                        i.unlocked = True
                     
                
                if i.unlocked:  # la piattaforma cade
                    i.timer += 1
                    if i.timer > 50:  # quando il timer raggiunge 50 "cicli"
                        if i.y < altez + 50:
                            i.vy += 1
                            i.centery += i.vy
        
            if not aterra:  # caduta libera
                if p_v_y < 10:  # velocit� massima di caduta
                    p_v_y += 1
    
            player.centery += p_v_y  # modifica posizione verticale
            p_v_x = 14 if l == 8 else 6  # nel livello 8 il giocatore pu� spostarsi pi� velocemente
    
            if player.centery > altez:  # condizione sconfitta: caduto fuori dallo schermo
                pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
                pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
                schermo.blit(carattere40.render("Sei caduto nel GarbageCollector, che fine orrenda!", True, GREEN), (50, 350))
                pygame.display.update()
                pygame.time.wait(500)
                premi_continua()
                sconfitta_bool = True
    
            
    
    
               
    
            for x in range(len(textObj)):
                schermo.blit(textObj[x], text_cor[x])  # le scritte javesi
                
                if text_cor[x][1] > altez:  # le scritte scese troppo in basso vengono riposizionate in alto
                    text_cor[x][1] = random.randrange(-20, 20)
                else:
                    text_cor[x][1] += 1  # le scritte scendono
            
            # disegna le piattaforme contenute in livelli[l]
            for x in livelli[l]:
                                
                if x == livelli[l][-1]:  # ultimo rettangolo
                    pygame.draw.rect(schermo, BLUE, x, 0)  # l'ultimo rettangolo � blu
                elif x == livelli[l][0]:
                    pygame.draw.rect(schermo, ORANGE, x, 0)  # l'ultimo rettangolo � blu
                elif x.cade:  # piattafrome che cadono
                    if x.timer <= 25:
                        schermo.blit(tileDanger_img, (x.x, x.y))
                    if x.timer > 25:
                        schermo.blit(tileDanger2_img, (x.x, x.y))
                else:
                    schermo.blit(tile_img, (x.x, x.y))
                    pygame.draw.rect(schermo, GREEN, x, 1)
                    
                    
                    
                        
    
            
            
            for x in nemici_list:  # nemici che si muovono per tutto lo schermo
                
                pygame.draw.rect(schermo, RED, x.rect, 3)
                schermo.blit(nemici_img, (x.rect.x, x.rect.y))                
                if player.colliderect(x.rect):
                    pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
                    pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
                    schermo.blit(carattere40.render("Game Over Mr. PythonMan!", True, GREEN), (50, 350))
                    pygame.display.update()
                    pygame.time.wait(500)
                    premi_continua()
                    sconfitta_bool = True
                
                if x.rect.left < 0:
                    x.direzx = "right"
                if x.rect.right > largh:
                    x.direzx = "left"
                if x.rect.top < 0:
                    x.direzy = "down"
                if x.rect.bottom > altez:
                    x.direzy = "up"
                
                if x.direzx == "left":
                    x.rect.centerx -= x.vx
                if x.direzx == "right":
                    x.rect.centerx += x.vx
                if x.direzy == "up":
                    x.rect.centery -= x.vy
                if x.direzy == "down":
                    x.rect.centery += x.vy
            
            for x in range(len(nemici_piattaforma)):  # nemici su piattaforme
                pygame.draw.rect(schermo, RED, nemici_piattaforma[x].rect, 3)
                schermo.blit(nemici_img, (nemici_piattaforma[x].rect.x, nemici_piattaforma[x].rect.y)) 
                if player.colliderect(nemici_piattaforma[x].rect):
                    pygame.draw.rect(schermo, BLACK, (0, 340, 1024, 100), 0)
                    pygame.draw.rect(schermo, RED, (0, 340, 1024, 100), 5)
                    schermo.blit(carattere40.render("Game Over Mr. PythonMan!", True, GREEN), (50, 350))
                    pygame.display.update()
                    pygame.time.wait(500)
                    premi_continua()
                    sconfitta_bool = True
                if nemici_piattaforma[x].rect.top < rand_piat[x].top - 200:
                    nemici_piattaforma[x].direzy = "down"
                if nemici_piattaforma[x].rect.bottom == rand_piat[x].top:
                    nemici_piattaforma[x].direzy = "up"           
            
                if nemici_piattaforma[x].direzy == "up":
                    nemici_piattaforma[x].rect.centery -= nemici_piattaforma[x].vy
                if nemici_piattaforma[x].direzy == "down":
                    nemici_piattaforma[x].rect.centery += nemici_piattaforma[x].vy
                        
            playeranimation.blit(schermo, (player.left - 7, player.top - 5))  # animazione di Pythonman
            # pygame.draw.rect(schermo, GREEN,player,1) #rettangolo del giocatore
            
        
        presentazione.presenta()
        
        
        
            
        
        
        if vittoria_bool:
            vittoria()
        elif sconfitta_bool:
            sconfitta()
        
        pygame.display.update()
        clock.tick(FPS)
