import math

from functions import (
    reynolds_calc, dynamic_thrust, thrust_components, 
    x_movement, y_movement, coefficient_force,
    csv_lookup, xflr5_data, induced_drag, drag_article
)


# ==============================================================================
# BOUCLE DE SIMULATION (sim_loop)
# ==============================================================================
def sim_loop(masse, config_articles, b, AR, corde, alpha, dt=0.05):
    g = 9.81
    poids = masse * g
    
    # Position et vitesse initiales
    x, y = 0.0, 0.0
    vx, vy = 0.0, 0.0
    t = 0.0
    
    # Paramètres d'hélice pour dynamic_thrust
    pitch, diameter, RPM = 6, 12, 9104    #pouces, valeur avec le 3036-899kv
    Theoretical = 2.7 #kg, valeur avec le 3026-890kv

    while True:
        v = math.sqrt(vx**2 + vy**2)
        if v < 0.1: v = 0.1 # Évite la division par zéro quand l'avion est à l'arrêt

        # --- Aérodynamique ---
        Re = reynolds_calc(v, corde)
        
        # Utilisation des fichiers CSV du dossier ./polar/
        # On cherche les données avec csv_lookup, puis on interpole avec xflr5_data
        try:
            donnees_csv = csv_lookup(Re)
            Cl, Cd_profil = xflr5_data(alpha, donnees_csv)
        except Exception as e:
            Cl, Cd_profil = 0.0, 0.0
            
        Cd_ind = induced_drag(AR, Cl)
        
        # --- Forces ---
        portance = coefficient_force(v, Cl, AR, b)
        
        trainee_profil = coefficient_force(v, Cd_profil, AR, b)
        trainee_induite = coefficient_force(v, Cd_ind, AR, b)
        trainee_fuselage = coefficient_force(v, 0.05, AR, b) # Cd estimé du fuselage (0.05)
        
        # Addition de la traînée pour tous les articles de la configuration actuelle
        trainee_articles_totale = 0
        for numero_article in config_articles:
            trainee_articles_totale += drag_article(v, numero_article)
            
        trainee_totale = trainee_profil + trainee_induite + trainee_fuselage + trainee_articles_totale
        
        # Poussée (Thrust)
        poussee = dynamic_thrust(pitch, diameter, RPM, v, Theoretical)
        poussee_x, poussee_y = thrust_components(poussee, alpha)
        
        force_x = poussee_x - trainee_totale
        
        if portance >= poids:
            force_y = portance + poussee_y - poids
        else:
            force_y = 0.0 # Reste plaqué au sol
            
        vx, dx = x_movement(force_x, masse, vx, dt)
        x += dx
        
        if force_y > 0:
            vy, dy = y_movement(force_y, masse, vy, dt)
            y += dy
            
        t += dt
        
        # --- Conditions d'arrêt ---
        # 1. Succès : l'avion décolle
        if portance >= poids or y > 0:
            return t, x
            
        # 2. Échec : piste trop courte (100m) ou temps trop long
        if x > 100 or t > 60:
            return None, x

# ==============================================================================
# PROGRAMME PRINCIPAL (main)
# ==============================================================================
def main():
    # Liste des configurations à tester (en utilisant les numéros d'articles de 1 à 5)
    #1: flying pig
    #2: dumpster fire
    #3: banana
    #4: waffles
    #5: rubber chicken
    configurations = [
        [0, 0, 0], [0, 1, 1], [0, 2, 2], [0, 3, 3], [0, 4, 4], [0, 5, 5], 
         [1, 0, 0], [1, 1, 1], [1, 2, 2], [1, 3, 3], [1, 4, 4], [1, 5, 5], 
         [2, 0, 0], [2, 1, 1], [2, 2, 2], [2, 3, 3], [2, 4, 4], [2, 5, 5], 
         [3, 0, 0], [3, 1, 1], [3, 2, 2], [3, 3, 3], [3, 4, 4], [3, 5, 5], 
         [4, 0, 0], [4, 1, 1], [4, 2, 2], [4, 3, 3], [4, 4, 4], [4, 5, 5], 
         [5, 0, 0], [5, 1, 1], [5, 2, 2], [5, 3, 3], [5, 4, 4], [5, 5, 5]
    ]
    
    # Paramètres de l'avion
    b     = 1.52  # Envergure (m)
    AR    = 6.9  # Allongement
    corde = 0.22 # Corde (m)
    alpha = 10.0  # Angle d'attaque de décollage (doit correspondre aux données CSV)
    dt    = 0.001  # Intervalle de temps de la simulation
    
    limite_distance = 13.8 # 45 pieds en mètres
    pas_masse = 0.1        # Incrément de poids
    
    print("Début de la simulation d'optimisation...")
    print("Lecture des fichiers ./polar/ en cours...\n")
    
    for i, config in enumerate(configurations):
        masse = 1.0 # Masse initiale au début du test
        masse_max = 0
        
        while True:
            result = sim_loop(masse, config, b, AR, corde, alpha, dt)
            temps, distance = result
            
            # Si l'avion ne décolle pas ou s'il dépasse les 45 pieds (13.8m)
            if temps is None or distance > limite_distance:
                # La masse maximale est celle qui a fonctionné au tour d'avant
                masse_max = masse - pas_masse
                print(config, masse_max)
                break
                
            masse += pas_masse
            
        # Calcul du score
        

if __name__ == "__main__":
    main()
