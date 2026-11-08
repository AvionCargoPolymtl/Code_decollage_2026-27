import numpy as np
from math import *

def reynolds_calc (vitesse, corde):
    nu = 1.4207e-5 
    return (vitesse * corde) / nu


def dynamic_thrust(pitch, diameter, RPM, Vx, Theoretical):

    parenthese = 4.23333*(10**-4)*RPM*pitch

    correction = Theoretical/(4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)/9.81)

    parenthese = 4.23333*(10**-4)*RPM*pitch-Vx
    return (4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)*correction)

#FONCTION drag_flying_pig
#son numero d'article est le 1
def drag_flying_pig(v):
    equation_1 = 0.0215*v**2 + 0.0135*v - 0.0625
    return equation_1

#FONCTION drag_dumpster_dire
#son numero d'article est le 2
def drag_dumpster_fire(v):
    equation_2 = 0.0181*v**2 + 0.0101*v - 0.0375
    return equation_2

#FONCTION drag_banana
#son numero d'article est le 3
def drag_banana(v):
    equation_3 = 0.007*v**2 - 0.0066*v + 0.03
    return equation_3

#FONCTION drag_waffles
#son numero d'article est le 4
def drag_waffles(v):
    equation_4 = 0.0061*v**2 + 0.0101*v - 0.0375
    return equation_4

#FONCTION drag_rubber_chicken
#son numero d'article est le 5
def drag_rubber_chicken(v):
    equation_5 = 0.0007*v**2 - 0.0045*v + 0.0175
    return equation_5

def score(mass, empty_mass, config):
    article_mass = [0,0.75,0.63,1,0.5,1.5] #lbs
    payload = (mass-empty_mass)*2.20462 #conversion en kg en lb
    article_count = 0
    
    for article in config:
        payload -= article_mass[article]
        if article !=0: article_count += 1
        
    return 1.25 * article_count * payload

def config_description(config):
    yap =''
    for article in config:
        if article == 1:
            yap+='flying pig, '
        if article == 2:
            yap+='dumpter fire, '
        if article == 3:
            yap+='banana, '
        if article == 4:
            yap+='waffles'
        if article == 5:
            yap+='rubber chicken'
        return yap

def score_sorter(scores):
    sorted_scores = dict()
    for key in sorted(scores, key = scores.get):
        sorted_scores[key] = scores[key]
    
    return sorted_scores

#FONCTION drag_article
#cette fonction permet d'obtenir le drag de chacun des articles de drag en les appelant par un numero
def drag_article(v, numero_article): 
    if numero_article == 0:
        return 0
    if numero_article == 1:
        return drag_flying_pig(v)
    if numero_article == 2:
        return drag_dumpster_fire(v)
    if numero_article == 3:
        return drag_banana(v)
    if numero_article == 4:
        return drag_waffles(v)
    if numero_article == 5:
        return drag_rubber_chicken(v)

def thrust_components(thrust, angle):
    x = thrust * cos(radians(angle)) 
    y = thrust * sin(radians(angle))
    return x,y 


def x_movement(Fx, m, vx0, dt): 
    if vx0<0:
        vx0 = 0
    ax = Fx/m
    vx = vx0 + ax*dt
    dx = vx0*dt + (1/2)*ax*dt**2
    return vx, dx


def y_movement(Fy, m, vy0, dt):  
    ay = Fy/m
    if ay<0:
        ay = 0 
    vy = vy0 + ay*dt 
    dy = vy0*dt + (1/2)*ay*dt**2 
    return vy, dy

def induced_drag(AR, Cl):

    #Variables:
    #AR: Aspect ratio  #Cl: Coefficient de lift

    #Calcul du facteur d'oswald (e)
    e = 1.78*(1 - 0.045*AR**0.68)-0.64

    #Calcul du induced_drag:
    Cd_induced = Cl**2 / (pi*AR*e)
    return Cd_induced

def coefficient_force(vitesse, Cl, AR, b): 
    rho = 1.225 
    A = b**2/AR
    return 0.5 * rho * vitesse**2 * A * Cl


def csv_lookup(Re):
    Re_lookup = "{:.3f}".format(round(Re)/10e5) #CONVERSION DU REYNOLDS AU MÊME FORMAT QUE LES NOMS DES FICHIERS CSV
    import csv
    #LE CURRENT DIRECTORY EST À DÉFINIR COMME Simulation_decollage POUR QUE LE CODE PUISSE TROUVER LES FICHIERS À LIRE
    with open(f"./polar/E423_T1_Re{Re_lookup}_M0.00_N9.0.csv") as f:
        data = csv.reader(f)
        donnees=[row for row in data if len(row)==10 and row[0]!="alpha"]
    #NETTOYAGE DU FORMAT DE DONNÉEES
    donnees_clean=donnees.copy()
    for liste,listetemp in zip(donnees,donnees_clean):
        for i,elt in enumerate(liste):
            clean_elt=float(str(elt).strip())
            listetemp[i]=clean_elt
    return(donnees_clean)


def xflr5_data(alpha,donnees):
    #DÉFINITION DES BORNES DE L'INTERPOLATION
    if alpha-int(alpha)>0.5:
        alpha_low=int(alpha)+0.5
        alpha_high=int(alpha)+1
    else:
        alpha_low=int(alpha)
        alpha_high=int(alpha)+0.5
    #CALCUL DE L'INTERPOLATION
    for elt in donnees:
        if elt[0]==alpha_low:
            cl_low=elt[1]
            cd_low=elt[2]
        if elt[0]==alpha_high:
            cl_high=elt[1]
            cd_high=elt[2]
    cl=cl_low+((cl_high-cl_low)/(alpha_high-alpha_low))*(alpha-alpha_low)
    cd=cd_low+((cd_high-cd_low)/(alpha_high-alpha_low))*(alpha-alpha_low)
    return(cl,cd)
