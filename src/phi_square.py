from math import comb

# Question 4

def computePhiSquare_A(profile):
    """Fonction qui calcule φ^2(p) sachant un profil p de A^n
    
    Args:
        profile : le profil de l'élection - matrice m*n
        
    Returns:
        mesure de polarisation φ^2 du profil en paramètre
    
    """
    it = get_Inner_PolarDistances(profile, Type='A')
    phi_sq = 0
    n = len(profile)
    m = len(profile[0])
    for k in it:
        phi_sq += (n - k)/(n * comb(m,2))
    return phi_sq
        
def computePhiSquare_L(profile):
    """Fonction qui calcule φ^2(p) sachant un profil p de L^n
    
    Args:
        profile : le profil de l'élection - matrice m*n
        
    Returns:
        mesure de polarisation φ^2 du profil en paramètre
    
    """
    it = get_Inner_PolarDistances(profile, Type='L')
    phi_sq = 0
    n = len(profile)
    m = len(profile[0])
    for k in it:
        phi_sq += (n - k)/(n * comb(m,2))
    return phi_sq
