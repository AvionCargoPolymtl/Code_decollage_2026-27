

def dynamic_thrust(pitch, diameter, RPM, Vx, Theoretical):

    parenthese = 4.23333*(10**-4)*RPM*pitch

    correction = Theoretical/(4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)/9.81)

    parenthese = 4.23333*(10**-4)*RPM*pitch-Vx
    return (4.392399 * (10**-8) * RPM*(diameter**3.5)*parenthese/np.sqrt(pitch)/9.81*correction)


