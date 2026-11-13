import pandas as pd
import numpy as np

foil_name = 'E423'
alpha = 5
Re = 247892.9056961357

def Interpolate_coef(x_lower, x_upper, y_lower, y_upper, x_target):
    xp = np.array([x_lower, x_upper])
    yp = np.array([y_lower, y_upper])
    y_target = np.interp(x_target, xp, yp)
    return y_target

def ReadCSV(Re, alpha, foil_name):
    Re_r = round(Re/10e6, 4) 
    if Re_r % 0.001 != 0:
        Re_lower = str(round(Re_r - (Re_r % 0.001),3))
        Re_upper = str((round(float(Re_lower),3) + 0.001))
        Re_lower_df = pd.read_csv(f"./polar/{foil_name}_T1_Re{Re_lower}_M0.00_N9.0.csv", skiprows=9)
        Re_upper_df = pd.read_csv(f"./polar/{foil_name}_T1_Re{Re_upper}_M0.00_N9.0.csv", skiprows=9)
        alpha_index = Re_lower_df.index[Re_lower_df['alpha']==alpha][0]
        Cl_lower = Re_lower_df.at[alpha_index, "CL"]
        Cl_upper = Re_upper_df.at[alpha_index, "CL"]
        Cl = Interpolate_coef(float(Re_lower), float(Re_upper), Cl_lower, Cl_upper, Re_r)
        Cd_lower = Re_lower_df.at[alpha_index, "CD"]
        Cd_upper = Re_upper_df.at[alpha_index, "CD"]
        Cd = Interpolate_coef(float(Re_lower), float(Re_upper), Cd_lower, Cd_upper, Re_r)
    else:
        Re_df = pd.read_csv(f"./polar/{foil_name}_T1_Re{Re_r}_M0.00_N9.0.csv", skiprows=9)
        alpha_index = Re_df.index[Re_df['alpha']==alpha][0]
        Cl = Re_df.at[alpha_index, "CL"]
        Cd = Re_df.at[alpha_index, "CD"]
    
    return Cl, Cd