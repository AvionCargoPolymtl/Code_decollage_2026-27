from math import pi

#FONCTION induced_drag
def induced_drag(AR, Cl):

    #Variables:
    #AR: Aspect ratio  #Cl: Coefficient de lift

    #Calcul du facteur d'oswald (e)
    e = 1.78*(1 - 0.045*AR**0.68)-0.64

    #Calcul du induced_drag:
    Cd_induced = Cl**2 / (pi*AR*e)
    return Cd_induced


