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
