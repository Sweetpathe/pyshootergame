#coding : utf-8
"""
Redwood's space
@autor : Redwood Soleil, the magnificent
"""


#importement
import pygame 
import sys
import time
import random
import os

pygame.init()                            #initialisation de pygame


print("A game made ny Pybhate SOLEIL, please support him on 'www.pybhate_soleil.com'")
time.sleep(3)

#constantes
w = 70               # (1)
h = 80               # (2)



#variables

	#booleans
ecran_name = False
ecran_param = True
ecran_titre = False
jouer = False
fin_jeu = False
quitter = False

victoire = bool()
defaite = bool()                                             #bools qui determinerons 

playing_musique = bool()                                     #bool qui dit si la musique est jouee

	#couleurs
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255,165,0)
yellow = (255,255,0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)


	#valeurs
stage = 1                                #niveau de jeu

a = 0                                   #variable d'affichage d'etoiles

joueur = None                                 #variable du joueur (vide pour l'instant)
joueur_rect = None                            #rect associe au joueur

ennemi_rect = None

ennemi_2_rect = None
ennemi_3_rect = None

ecran_hauteur = None
ecran_largeur = None

delais = 0                                 #temps entre chaque tir

tirage = 0                                 #variable de tir ennemi

hor = 0
hor2 = 0
valeurs = [-1, 0, 1]                        #valeurs de mouvement
bougeage = 0                               

mov = 0                                 #variable qui determinera qui bougera

tira = 0                                #variable qui determinera qui tirera

now = int()                           #variable de time qui se repete

nom = ""                                 #nom du joueur

 
	#composantes
ecran = pygame.display.set_mode([1000, 800])               #ecran de jeu

icone = pygame.image.load("ressources/logo.png")
icone = pygame.transform.scale(icone, (64, 64))
pygame.display.set_icon(icone)                                  #l'icone de l'app  

pygame.display.set_caption("redwood's space")                                             #nom de l'ecran

police_petite = pygame.font.SysFont("ressources/starcruiser.ttf", 30)
police_grande = pygame.font.SysFont("ressources/starcruiser.ttf", 65)
police_normale = pygame.font.SysFont("Arial", 40)

sprite_joueur = "ressources/sprites/normal.png"                   #sprite du joueur
sprite_ennemi_1 = "ressources/sprites/carrier.png"

bruit_joueur = "ressources/sounds/tir_gentil.wav"                     #son de tir du joueur

clock = pygame.time.Clock()



#classes
class vaisseau:
	def __init__(self, x, y, pv, m, t, etat, image, bruit):
		self.x = x
		self.y = y
		self.pv = pv
		self.etat = etat
		self.m = m
		self.t = t 
		
		self.image = pygame.image.load(image)                               #inserer une var image
		if self.etat % 2 == 0:
			self.image = pygame.transform.rotate(self.image, 90)
		else:
			self.image = pygame.transform.rotate(self.image, 270)	
		self.image = pygame.transform.scale(self.image, (w, h))

		self.bruit = pygame.mixer.Sound(bruit)                               #inserer une var son
		self.bruit.set_volume(5)

		self.list_tirs = []

	def tirer(self):
		self.bruit.play()
		self.list_tirs.append([self.x + 35, self.y])


#programme

	#ecran de parametres
while ecran_param:
	for event in pygame.event.get():                   #si le joueur quitte
		if event.type == pygame.QUIT:
			quitter = True
			ecran_param = False

		else:                                          #pour la selection de la taille de l'ecran
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				ecran_hauteur = 640
				ecran_largeur = 400
				ecran = pygame.display.set_mode([ecran_hauteur, ecran_largeur])  
				ecran_name = True
				ecran_param = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
				ecran_hauteur = 800
				ecran_largeur = 640
				ecran = pygame.display.set_mode([ecran_hauteur, ecran_largeur])  
				ecran_name = True
				ecran_param = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
				ecran_hauteur = 1000
				ecran_largeur = 800
				ecran = pygame.display.set_mode([ecran_hauteur, ecran_largeur])
				ecran_name = True
				ecran_param = False

	#affichage du texte de parametrage de l'ecran
	text_param = police_petite.render("[press a] : 640x500[press z] : 800x640[press e] : 1000x800", True, white)
	text_param_rect = text_param.get_rect()
	ecran.blit(text_param, (500 - text_param_rect[2]/2, 400 - text_param_rect[3]/2))
	pygame.display.update()

ecran.fill(black)

	#ecran de demande de nom
while ecran_name:


	#affichage du nom
	text_ask = police_petite.render("Write your name", True, white)
	text_ask_rect = text_ask.get_rect()
	ecran.blit(text_ask, (ecran_hauteur/2 - text_ask_rect[2]/2, ecran_largeur/2 - text_ask_rect[3]/2))

	name_text = police_petite.render("{}".format(nom), True, red)
	name_text_rect = name_text.get_rect()
	ecran.blit(name_text, [ecran_hauteur/2 - name_text_rect[3]/2, 200])

	pygame.display.update()
	ecran.fill(black)


	
	for event in pygame.event.get():                   #si le joueur quitte
		if event.type == pygame.QUIT:
			quitter = True
			ecran_name = False

		#inputs de l'utlisateur
		if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			nom = nom[:-1]

		if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
			nom += "a"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
			nom += "b"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
			nom += "c"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
			nom += "d"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
			nom += "e"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
			nom += "f"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
			nom += "g"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
			nom += "h"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
			nom += "i"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
			nom += "j"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
			nom += "k"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
			nom += "l"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
			nom += "m"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
			nom += "n"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
			nom += "o"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
			nom += "p"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			nom += "q"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
			nom += "r"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			nom += "s"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
			nom += "t"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
			nom += "u"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
			nom += "v"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
			nom += "w"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
			nom += "x"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
			nom += "y"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
			nom += "z"

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			nom += " "

		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and nom != " ":
			ecran_titre = True
			ecran_name = False



	#ecran titre
while ecran_titre:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quitter = True
			ecran_titre = False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
			jouer = True         
			ecran_titre = False

	text_titre = police_petite.render("Redwood's space [press R to start playing]", True, red)
	text_titre_rect = text_titre.get_rect()
	ecran.blit(text_titre, (ecran_hauteur/2 - text_titre_rect[2]/2, ecran_largeur/2 - text_titre_rect[3]/2))
	pygame.display.update()



#vaisseaux     (x, y, pv, m, t, etat, image, bruit)                           (etat pair = gentil)
joueur = vaisseau(ecran_hauteur/2 - 35, ecran_largeur -100, 3, 3, 5, 2, sprite_joueur, bruit_joueur)                                                            #variable du joueur
ennemi_1 = vaisseau(ecran_hauteur/2 - 35, 20, 10, 3, 5, 1, sprite_ennemi_1 , bruit_joueur)
ennemi_2 = vaisseau(ecran_hauteur/2 - 35, 20, 10, 3, 5, 1, sprite_ennemi_1 , bruit_joueur)
ennemi_3 = vaisseau(ecran_hauteur/2 - 35, 120, 10, 3, 5, 1, sprite_ennemi_1 , bruit_joueur)
      
##########################################################################################################################################################################

#fonctions (2)
	#collision de tirs
def collision_tirs(vaisseau, rect):

	for tir in joueur.list_tirs:

		tir_rect = pygame.Rect(tir[0], tir[1], 3, 6)

		if rect.colliderect(tir_rect):
			vaisseau.pv -= 1
			joueur.list_tirs.remove(tir)

def collision_tirs_2(v1, r1, v2, r2):

	for tir in joueur.list_tirs:

		tir_rect = pygame.Rect(tir[0], tir[1], 3, 6)

		if r1.colliderect(tir_rect):
			v1.pv -= 1
			joueur.list_tirs.remove(tir)

		if r2.colliderect(tir_rect):
			v2.pv -= 1
			joueur.list_tirs.remove(tir)


###########################################################################################################################################################################
	#jeu 

debut = time.time()                                    #quand le joueur commence la partie

while jouer:
	if not fin_jeu:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quitter = True
				jouer = False

				


		joueur_rect = pygame.Rect(joueur.x, joueur.y, w, h)                      #Rect associe a chaque tir

		#mouvement du joueur
		pressed = pygame.key.get_pressed()                                        #catch the moving key

		if pressed[pygame.K_LEFT] and joueur.x > 0:                               #le and c'est pour pas sortir de l'ecran
			joueur.x -= joueur.m
        
		if pressed[pygame.K_RIGHT] and joueur.x < ecran_hauteur - h :                                 #pareil            
			joueur.x += joueur.m

		if pressed[pygame.K_SPACE] and delais >= 10:
			joueur.tirer()
			delais = 0

		#conditions des levels
		if stage == 1:

			#affichage 
			ecran.blit(ennemi_1.image, (ennemi_1.x, ennemi_1.y))            #le vaisseau ennemi
			
			text_pv_ennemi_1 = police_petite.render("PV : {}/10".format(ennemi_1.pv), True, green)
			ecran.blit(text_pv_ennemi_1, [0, 0])                                  #pv de l'ennemi 1

			#mouvement du vaisseau ennemi
			if bougeage == 30:
				hor = random.choice(valeurs)
				bougeage = 0

			if ennemi_1.x + hor*ennemi_1.m >= 0 and ennemi_1.x + w + hor*ennemi_1.m <= ecran_hauteur:
				ennemi_1.x += hor*ennemi_1.m

			
			ennemi_1_rect = pygame.Rect(ennemi_1.x, ennemi_1.y, w, h)                         #rect associe a chaque ennemi

			#tir du vaisseau ennemi
			if tirage == 80:
				ennemi_1.tirer()
				tirage = 0

			for tir in ennemi_1.list_tirs:
				tir_ennemi_rect = pygame.Rect(tir[0], tir[1] + w, 3, 6)

				if joueur_rect.colliderect(tir_ennemi_rect):
					joueur.pv -= 1
					ennemi_1.list_tirs.remove(tir)

				elif tir[1] > ecran_largeur:
					ennemi_1.list_tirs.remove(tir)

				else:
					tir[1] += ennemi_1.t
					pygame.draw.rect(ecran, yellow, tir_ennemi_rect)

			collision_tirs(ennemi_1, ennemi_1_rect)
			
			if ennemi_1.pv <= 0 or joueur.pv <= 0 :
				if ennemi_1.pv <= 0:
					joueur.pv = 3
					del ennemi_1_rect
					stage += 1

				if joueur.pv <= 0:
					defaite = True
					fin_jeu = True


		if stage == 2:

			#victoire du joueur
			if ennemi_2.pv <= 0 and ennemi_3.pv <= 0:
				victoire = True
				fin_jeu = True

			#aleat
			mov = random.randint(1, 10)                    
			tira = random.randint(1, 10)


			#collision de bullets
			if ennemi_2.pv > 0:
				ennemi_2_rect = pygame.Rect(ennemi_2.x, ennemi_2.y, w, h) 
			
			if ennemi_3.pv > 0:
				ennemi_3_rect = pygame.Rect(ennemi_3.x, ennemi_3.y, w, h)                  #rect associe a chaque vaisseau

			collision_tirs_2(ennemi_2, ennemi_2_rect, ennemi_3, ennemi_3_rect)                         #collision

			#affichage
			text_pv_ennemi_2 = police_petite.render("PV : {}/10".format(ennemi_2.pv), True, green)
			text_pv_ennemi_2_rect = text_pv_ennemi_2.get_rect()
			text_pv_ennemi_3 = police_petite.render("PV : {}/10".format(ennemi_3.pv), True, green)                    

			if ennemi_2.pv > 0:
				ecran.blit(ennemi_2.image, (ennemi_2.x, ennemi_2.y))
				ecran.blit(text_pv_ennemi_2, [0, 0])                                      #pv ennemi 2

			if ennemi_3.pv > 0:
				ecran.blit(ennemi_3.image, (ennemi_3.x, ennemi_3.y))
				ecran.blit(text_pv_ennemi_3, [0, text_pv_ennemi_2_rect[3]])                                      #pv ennemi 3

			#mouvement
				#mouvement ennemi 2
			
			if bougeage == 20    and   (mov % 2) == 0 :
				hor = random.choice(valeurs)
				bougeage = 0

			if ennemi_2.x + hor*ennemi_2.m >= 0 and ennemi_2.x + w + hor*ennemi_2.m <= ecran_hauteur:
				ennemi_2.x += hor*ennemi_2.m

	
				#mouvement ennemi 3

			if bougeage == 20  and   (mov%2) != 0:
				hor2 = random.choice(valeurs)
				bougeage = 0

			if ennemi_3.x + hor2*ennemi_3.m >= 0 and ennemi_3.x + w + hor2*ennemi_3.m <= ecran_hauteur:
				ennemi_3.x += hor2*ennemi_3.m

			#tir des ennemis
				#tir de l'ennemi 2

			if tirage == 80 and tira % 2 == 0:
				ennemi_2.tirer()
				tirage = 0

			for tir in ennemi_2.list_tirs:
				tir_ennemi_rect_2 = pygame.Rect(tir[0], tir[1] + w, 3, 6)

				if joueur_rect.colliderect(tir_ennemi_rect_2):
					joueur.pv -= 1
					ennemi_2.list_tirs.remove(tir)

				elif tir[1] > ecran_largeur:
					ennemi_2.list_tirs.remove(tir)

				else:
					tir[1] += ennemi_2.t
					pygame.draw.rect(ecran, yellow, tir_ennemi_rect_2)

				#tir de l'ennemi 3

			if tirage == 80 and tira % 2 != 0:
				ennemi_3.tirer()
				tirage = 0

			for tir in ennemi_3.list_tirs:
				tir_ennemi_rect_3 = pygame.Rect(tir[0], tir[1] + w, 3, 6)

				if joueur_rect.colliderect(tir_ennemi_rect_3):
					joueur.pv -= 1
					ennemi_3.list_tirs.remove(tir)

				elif tir[1] > ecran_largeur:
					ennemi_3.list_tirs.remove(tir)

				else:
					tir[1] += ennemi_3.t
					pygame.draw.rect(ecran, yellow, tir_ennemi_rect_3)

		#si le joueur meurt
		if joueur.pv <= 0:
			defaite = True
			fin_jeu = True




        #affichage des elements recurrents

		for tir in joueur.list_tirs :                        #affichage des bullets

			if tir[1] < 0:
				joueur.list_tirs.remove(tir)

			else:
				tir[1] -= joueur.t
				pygame.draw.rect(ecran, red, (tir[0], tir[1], 3, 6))

		ecran.blit(joueur.image, [joueur.x, joueur.y])                                  #affichage du joueur
		
		text_pv = police_petite.render("PV : {}/3".format(joueur.pv), True, red)
		text_pv_rect = text_pv.get_rect()
		ecran.blit(text_pv, [ecran_hauteur - text_pv_rect[2], 0])                                 #affichage des pvs

		text_stage = police_petite.render("stage : {}/10".format(stage), True, yellow)
		text_stage_rect = text_stage.get_rect()
		ecran.blit(text_stage, [ecran_hauteur - text_stage_rect[2], ecran_largeur - text_stage_rect[3]])                       #affichage du stage

		while a <= 2:                                                                  #etoiles aleatoires
			pygame.draw.circle(ecran, white, [random.randint(0, ecran_hauteur), random.randint(0, ecran_largeur)], 1)
			a += 1 

		pygame.display.update()    
		ecran.fill(black)


		clock.tick(60)                        #fps de jeu

    	#var increasing
		delais += 1
		bougeage += 1
		tirage += 1

		#var reinitialization
		a = 0
		now = time.time()
		duration = int(now - debut)
		timer_text = police_grande.render("{}".format(duration), True, orange)

		#affichage (2)
		ecran.blit(timer_text, [0, 150])



	else:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitter = True
				jouer = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				os.system("python3 game.py")

		if defaite:            #si le joueur perd
			text_defaite = police_petite.render("{} failed, he sucks, [r] to replay".format(nom), True, white)
			text_defaite_rect = text_defaite.get_rect()

			ecran.blit(text_defaite, [ecran_hauteur/2 - text_defaite_rect[2]/2, ecran_largeur/2 - text_defaite_rect[3]/2])
						

		if victoire:          #si le joueur gagne
			text_victoire = police_petite.render("Congratulations, {} is our hero, time {}".format(nom, duration), True, white)
			text_victoire_rect = text_victoire.get_rect()

			ecran.blit(text_victoire, [ecran_hauteur/2 - text_victoire_rect[2]/2, ecran_largeur/2 - text_victoire_rect[3]/2])
			
			
		pygame.display.update()
		ecran.fill(black)
		clock.tick(60)

			
if quitter:                              #quand le joueur quitte
    pygame.quit()
    sys.exit()	