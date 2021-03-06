from single import *

from time import time, localtime
import matplotlib.pyplot as plt
from os import chdir


interface = True

################################################################################
###     Fonctions :

def str_nb(n,taille = 2):
    """écrit les nombres à la bonne taille, avec des 0 devant si ils sont trops courts"""
    ch = str(n)
    while len(ch) < taille:
        ch = '0' + ch
    return ch


def affiche(ch,pos):
    if interface:
        ch = '  '+ ch + '   '
        message = police.render(ch, True, couleur, back)
        fenetre.blit(message, pos)
        pygame.display.flip()
        #Si la fenetre reçoit un signal de fermeture, on fait planter le programme :
        if QUIT in [event.type for event in pygame.event.get()]:
            this_thing_work_even_if_not_very_smart = 1/0 #Pour quitter le programme
    else:
        print(ch)


def moyenne(L):
    """permet de réaliser la moyenne d'une liste"""
    somme = 0
    for i in L:
        somme += i
    return somme / len(L)


def var_nmb_gen(parameters,min_g,max_g,pas_g):
    minimum = []
    for n_gen in range(min_g , max_g , pas_g):
        #On fait varier le nombre de générations :
        parameters[1] = n_gen
        #On affiche le nombre actuel de générations
        affiche('nmb_gen = '+ str(n_gen) + ' / ' + str(max_g),(0,60))

        #On résoud le problème et stocke la meilleure solution
        final_pop = resolve_single(problem, parameters)
        liste = [Z.fitness for Z in final_pop]
        minimum.append( round( min(liste) , 4))

        #On affiche le temps écoulé depuis le début du lancement du programme
        affiche('temps total : ' + str(int((time() - first_start) // 60)) + ' minutes',(0,140))
    return minimum[:]



################################################################################
###     Choix Utilisateur :


#On choisit le probleme pour lequel on va faire les tests :
problem = inspyred.benchmarks.Ackley()
name_problem = 'test' #(sert pour le nom des fichiers de résultats)

#On défini les paramètres par défaut :
# pop_size, nmb_gen, p_crossover, p_mutation
default_parameters = [1000, 40, 0.5, 0.5]

#On définie les caractéristiques des paramètres que l'on va faire varier :
#indice : l'indice dans la liste parameters qu'il faut passer dans resolve_problem()
#proba : si le parametre est une probabilitée ou pas (on la rentre alors en %)
parametres = [{'name' : 'pop_size' , 'indice' : 0 , 'min' : 10 , 'max' : 2000 , 'pas' : 100 , 'proba' : False},
{'name' : 'p_crossover' , 'indice' : 2 , 'min' : 0 , 'max' : 100 , 'pas' : 10 , 'proba' : True},
{'name' : 'p_mutation' , 'indice' : 3 , 'min' : 0 , 'max' : 100 , 'pas' : 10 , 'proba' : True}
]

#La façon dont le nombre de génération évolue :
min_gen = 0
max_gen = 10
pas_gen = 10

################################################################################
### Execution du programme :


#initialisation de l'interface :
if interface:
    try:
        #On initialise l'interface pour suivre l'évolution du programme
        import pygame
        from pygame.locals import QUIT
        pygame.init()
        #On choisit la police d'affichage :
        police = pygame.font.Font(pygame.font.get_default_font(),17)
        #on choisit la couleur du texte et du fond :
        couleur = (255,255,255)
        back = (0,0,0)
        #On crée la fenetre:
        fenetre = pygame.display.set_mode((450,450))
    except:
        print('Interface not supported, try install the pygame module')
        interface = False

#changement du dossier de travail, pour enregistrer les fichiers au bon endroit
chdir('data')


#On stocke dans exec times les temps d'exécution des différents problemes
exec_times = []
#On compte le nombre de fichiers générés:
nmb_files = 0
#On lance le chrono :
first_start = time()
#On affiche le nom du probleme :
affiche(name_problem,(0,0))

while True:
    #On fait varier chaque parametre les un à la suite des autres :
    for p in parametres:
        #On affiche le parametre que l'on fait varier :
        affiche('Variation de '+p['name'],(0,20))

        #On stocke la date (pour les noms de fichiers)
        date = localtime()

        #On réinitialise les paramètres :
        #(Si ce n'est pas la première boucle les paramètres peuvent avoir changé)
        parameters = default_parameters[:]

        #On initialise la liste contenant les diverses solutions :
        liste_soluces = []

        #On commence le chronomètre :
        start_time = time()

        for var_param in range(p['min'] , p['max'] + 1, p['pas']):

            if p['proba']:
                value = var_param / 100
                str_max = str(p['max'] / 100)
            else:
                value = var_param
                str_max = str(p['max'])

            #On fait évoluer le paramètre :
            parameters[p['indice']] = value

            affiche(p['name']+' = '+ str(value) + ' / '+ str_max,(0,40))

            #On récupère la liste des solutions optimales de chaque résolution
            #en faisant varier le nombre de génération à chaque fois :
            time_begin = time()
            liste_soluces.append(var_nmb_gen(parameters, min_gen, max_gen, pas_gen))
            t = time() - time_begin

            affiche('Temps intermédiaire : '+str(round(t,3))+' secondes',(0,80))

        #On arrete le chronomètre :
        time_exec = time() - start_time
        #On stocke le temps
        exec_times.append(time_exec)
        #On affiche le temps :
        affiche(p['name']+ ' done in '+str(round(time_exec,3))+' secondes.',(0,100))


        # Enregistrement du fichier csv :

        #On choisit le nom du fichier :
        name = name_problem + '_'+ p['name'] + '_' + str_nb(date[2]) + str_nb(date[3]) + str_nb(date[4]) + '.csv'

        #On écrit l'entête du fichier (date, temps d'exécutions, paramètres) :
        str_date = str(date[0]) +'/'+ str_nb(date[1]) +'/'+ str_nb(date[2]) +' '+ str_nb(date[3]) +':'+ str_nb(date[4]) +':'+ str_nb(date[5])
        entete = 'Head Debut : ' + str_date
        entete += " , Temps d'execution : " + str(int(time_exec)) + " secondes"
        entete += ' , Variation de ' + p['name'] + ' entre ' + str(p['min']) + ' et ' + str(p['max'])
        if p['proba']:
            entete += ' (en %)'
        entete += ' avec un pas de ' + str(p['pas'])
        entete += ', Variation de nmb_gens de '+ str(min_gen) + ' a ' + str(max_gen)

        #On écrit les données en elles mêmes :
        ch = entete + '\n'
        for i in liste_soluces[:]:
            for j in i:
                ch += str(j) + ','
            ch = ch[:-1] + '\n'

        #On enregistre le fichier :
        f = open(name, 'w')
        f.write(ch)
        f.close()
        affiche(name + ' saved',(0,120))
        nmb_files += 1
        affiche('csv files saved : '+ str(nmb_files) ,(0,160))
        print('---------------- CSV file saved ----------------\n\n')


    print("--- Done in",int(sum(exec_times)),'secondes ---')
