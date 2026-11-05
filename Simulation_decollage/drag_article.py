#Variables:  #v: vitesse
#les coefficients ont ete calcules prealablement
#chaque fonction renvoie le drag de l'article en fonction de la vitesse

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

#FONCTION drag_article
#cette fonction permet d'obtenir le drag de chacun des articles de drag en les appelant par un numero
def drag_article(v, numero_article): 
    if numero_article == 1:
        return drag_flying_pig(v)
    elif numero_article == 2:
        return drag_dumpster_fire(v)
    elif numero_article == 3:
        return drag_banana(v)
    elif numero_article == 4:
        return drag_waffles(v)
    elif numero_article == 5:
        return drag_rubber_chicken(v)

#Affichage du resultat
#Retirer des commentaires et choisir v & numero_article
#print(f"{drag_article(v, numero_article)} N")
    