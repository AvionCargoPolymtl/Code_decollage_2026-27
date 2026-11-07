import numpy as np
from math import *

def reynolds_calc (vitesse, corde):
    nu = 1.4207e-5 
    return (vitesse * corde) / nu


def dynamic_thrust(pitch, diameter, RPM, Vx, Theoretical):

    parenthese = 4.23333*(10**-4)*RPM*pitch

    correction = Theoretical/(4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)/9.81)

    parenthese = 4.23333*(10**-4)*RPM*pitch-Vx
    return (4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)/9.81*correction)


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
