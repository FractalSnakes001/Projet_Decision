from math import comb
import numpy as np 
import matplotlib.pyplot as plt
import Projet_Decision.src.Distances as ds


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

def evol_phi_square_A(n, m):
    """Fonction qui trace l'évolution de φ^2(p) pour des profils p de A^n générés aléatoirement, avec des niveaux de polarisation différents.
    
    Args:
        n (int) : nombre de votants
        m (int) : nombre de candidats
            
    """
    phi_square = []
    pol_values = []
    for i in range(11):
        pol = i / 10
        profile = ds.random_type_A(n, m, pol)
        phi_square.append(computePhiSquare_A(profile))
        pol_values.append(pol)
    plt.figure()
    plt.plot(pol_values, phi_square, marker='o')
    plt.xlabel("niveau de polarisation")
    plt.ylabel(" φ^2(p)")
    plt.title("Evolution de φ^2(p) en fonction du niveau de polarisation pour des profils de A^n")
    plt.grid()
    plt.show()
    
def evol_phi_square_L(n, m):
    """Fonction qui trace l'évolution de φ^2(p) pour des profils p de L^n générés aléatoirement, avec des niveaux de polarisation différents.
    
    Args:
        n (int) : nombre de votants
        m (int) : nombre de candidats
            
    """
    phi_square = []
    pol_values = []
    for i in range(11):
        pol = i / 10
        profile = ds.random_type_L(n, m, pol)
        phi_square.append(computePhiSquare_L(profile))
        pol_values.append(pol)
    plt.figure()
    plt.plot(pol_values, phi_square, marker='o')
    plt.xlabel("niveau de polarisation")
    plt.ylabel(" φ^2(p)")
    plt.title("Evolution de φ^2(p) en fonction du niveau de polarisation pour des profils de L^n")
    plt.grid()
    plt.show()
