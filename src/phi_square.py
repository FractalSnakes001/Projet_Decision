from math import comb
import numpy as np 
import matplotlib.pyplot as plt
import Distances as ds
from Generation import *


# Question 5 ------------------------------------------------------------------------------------------------------------------------------------------------------

def computePhiSquare_A(profile):
    """Fonction qui calcule φ^2(p) sachant un profil p de A^n
    
    Args:
        profile : le profil de l'élection - matrice m*n
        
    Returns:
        mesure de polarisation φ^2 du profil en paramètre
    
    """
    it = ds.get_Inner_PolarDistances(profile, Type='A')
    phi_sq = 0
    n = len(profile)
    m = len(profile[0])
    for k in it:
        phi_sq += (n - k[0])
    phi_sq /= (n * comb(m,2))
    return phi_sq
        
def computePhiSquare_L(profile):
    """Fonction qui calcule φ^2(p) sachant un profil p de L^n
    
    Args:
        profile (matrice n*m) : le profil de l'élection
        
    Returns:
        mesure de polarisation φ^2 du profil en paramètre
    
    """
    it = ds.get_Inner_PolarDistances(profile, Type='L')
    phi_sq = 0
    n = len(profile)
    m = len(profile[0])
    for k in it:
        phi_sq += (n - k[0])
    phi_sq /= (n * comb(m,2))
    return phi_sq

#Question 6 ------------------------------------------------------------------------------------------------------------------------------------------------

def evol_phi_square_A(n, m, pas=0.05, rep=10):
    """Fonction qui trace l'évolution de φ^2(p) pour des profils p de A^n générés aléatoirement, avec des niveaux de polarisation différents.
    
    Args:
        n (int) : nombre de votants
        m (int) : nombre de candidats
        pas (float) : pas d'incrementation
        rep (int) : nombre de repetitons par point (reduction varience)
            
    """
    phi_square = []
    pol_values = []
    
    num_steps = int(round(1.0 / pas)) + 1
    
    for i in range(num_steps):
        pol = i * pas
        somme_phi = 0
        
        # red varience
        for k in range(rep):
            profile = random_type_A(n, m, pol)
            somme_phi += computePhiSquare_A(profile)
            
        phi_square.append(somme_phi / rep)
        pol_values.append(pol)
        
    plt.figure()
    plt.plot(pol_values, phi_square, marker='o')
    plt.xlabel("niveau de polarisation")
    plt.ylabel(" φ^2(p)")
    plt.title("Evolution de φ^2(p) en fonction du niveau de polarisation pour des profils de A^n")
    plt.grid()
    plt.show()
    return
    
def evol_phi_square_L(n, m, pas=0.1, rep=10):
    """Fonction qui trace l'évolution de φ^2(p) pour des profils p de L^n générés aléatoirement, avec des niveaux de polarisation différents.
    
    Args:
        n (int) : nombre de votants
        m (int) : nombre de candidats
        pas (float) : pas d'incrementation 
        rep (int) : nombre de repetitons par point (reduc varience)
            
    """
    phi_square = []
    pol_values = []
    
    
    num_steps = int(round(1.0 / pas)) + 1
    
    for i in range(num_steps):
        pol = i * pas
        somme_phi = 0
        
        # reduc var
        for k in range(rep):
            profile = random_type_L(n, m, pol)
            somme_phi += computePhiSquare_L(profile)
            
        phi_square.append(somme_phi / rep)
        pol_values.append(pol)
        
    plt.figure()
    plt.plot(pol_values, phi_square, marker='o')
    plt.xlabel("niveau de polarisation")
    plt.ylabel(" φ^2(p)")
    plt.title("Evolution de φ^2(p) en fonction du niveau de polarisation pour des profils de L^n")
    plt.grid()
    plt.show()
    return