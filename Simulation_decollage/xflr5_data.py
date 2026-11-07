#FONCTION POUR TRANSFORMER V EN REYNOLDS
def Re_calc(v):
    l=0.2
    nu=1.4207e-5
    return (v*l)/nu

#FONCTION POUR ALLER CHERCHER LES DONNÉES À PARTIR DU BON FICHIER CSV
def csv_lookup(Re):
    Re_lookup = "{:.3f}".format(round(Re)/10e5) #CONVERSION DU REYNOLDS AU MÊME FORMAT QUE LES NOMS DES FICHIERS CSV
    import csv
    #LE CHEMIN D'ACCÈS EST À CHANGER AU BESOIN (JE SUIS PAS SÛR QUE C'EST BIEN FAIT)
    #with open(f"C:/Users/happy/OneDrive/Documents/Uni/Avion Cargo/Code_decollage_2026-27-main/Simulation_decollage/polar/E423_T1_Re{Re_lookup}_M0.00_N9.0.csv") as f:
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

#FONCTION POUR INTERPOLER CL,CD
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

#COMBINAISON DE TOUT
v=14.5# EN M/S, À CHANGER POUR LE VRAI INPUT
alpha=13 #À CHANGER POUR LE VRAI INPUT
donnees=csv_lookup(Re_calc(v))
resultat=xflr5_data(alpha,donnees)
print(resultat)


