#Excercie 3
#desoler tjr pas d'accents car clavier ricain.
#je separe distance et Nb de preferances car peut-etre utile plus tard
#je continue a utiliser la Docstring pour les fonctions, j'espere que c'est plus clair pour tout le monde.


def NombrePreferance(profilA,K,L,M=None,Type='A'):
    """
    renvoie la distance de preferance entre le bulletin k et l pour type A OU L

    Args:
       profilA: une liste de bulletin de type A, 
       K : Candidat que l'on prefere a l (indice liste)
       L : Candidat comparee (indice liste)
       M : taille de profilA >=2 
       Type : 'A' ou 'L' pour le type de profil, par defaut 'A'
    Returns:
       - nombres de votant qui preferent K a L
       - None si erreur
       
    """
    if (Type != 'A' and Type != 'L'):
        return None
    if (M==None and len(profilA)!=0):
        M = len(profilA[0])
    if (M<2) or (K >= M) or (K<0) or (L>=M) or (L<0) or (M==None):
        return None
   
    NbPref = 0
    for bull in profilA:
        #equivalent a dire Bk == 1 et Bl == 0 car 0,1 sont les seulent valeurs possibles
        #aussi mais inverse pour le type L, si K est mieux que L alors Bk < Bl les deux dans {1..M}
        test = (bull[K] > bull[L]) if Type == 'A' else (bull[K] < bull[L])
        if test: 
            NbPref+=1
    return NbPref




def get_PolarDistances(profil,Type='A'):
    """
    renvoie les distances  pour tout les couples de bulletins type A OU L

    Args:
       profilA: une liste de bulletin de type A, ou de type L 
       Type : 'A' ou 'L' pour le type de profil, par defaut 'A'
    Returns:
       - Liste de tuples (a,b) avec a la distance pour le couple b de profils, a(int),  b(int tuple)
        avec le tuple de b correspondant aux indices des candidats (indice liste)
       - None s'il y a une erreur

    """
    #Comme on a besoin de la condition Bv[i] >  Bv[k].
    #on doit parcourir pour tous les couple lors du calcul, je ne vois pas comment
    #faire moins de complexite
    if (Type != 'A' and Type != 'L'):
        return None
    
    M = len(profil)
    if (M==0):
        return None
    
    M = len(profil[0])
    if (M<2):
        return None
    
    result = []
    for k in range(0,M-1):
        for l in range(k+1,M):
            Couple = (k,l)
            Pk_L = NombrePreferance(profil,k,l,M,Type)
            Pl_K = NombrePreferance(profil,l,k,M,Type)
            if (Pk_L == None  or  Pl_K == None):
                return None
            distance = abs(Pk_L - Pl_K)
            result.append((distance,Couple))
    return result
            

            
        