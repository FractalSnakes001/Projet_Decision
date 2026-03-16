#CODE POUR question 1/2
#pour random
import numpy as np 

# pas d'accent sur mon clavier, desoler en avance (clavier ricain)
# je vais essayer d'implementer la Docstring python comme cela Vscode nous affiche les infos des fonctions


#On a N votantes  et M candidats, chaque votante est associe a son bulletin
#Bulletin type A => c'est un tableau de taille M, elements: 0 ou 1.

#l'idee est de d'abord gen un tableau referance aleatoire, ensuite si on tres polarisee on aura une 
#proba elevee d'etre soit proche soit l'oppose. si on est pas du tout polarisee on la proba de notre referance est grande
#Vecteur ref (V1): on est un vecteur de proba de bernoulli avec p 1/2, pour chaque ki dans {1...m}

#le nom ne contient pas generation car faudra l'utiliser comme module donc Generation.random_type...
def random_type_A(nb_V ,nb_C, Pol):
    """
    renvoie nb_V bulletins aleatoires type A de taille nb_C avec une Polarisation Pol

    Args:
        nb_V (int): Nombre de bulletins de vote a generer. Doit etre un entier positif.
        nb_C (int): Nombre de candidats (taille de chaque bulletin). Doit etre un entier positif.
        Pol (float): Indice de polarisation compris dans [0, 1]. 
                     0.0 correspond a polarisation minimale.
                     1.0 correspond a polarisation maximale.
    Returns:
        profil : liste (non Numpy) de bulletins donc N elements de A.

    """
    #vecteur referance avec bernouilli 1/2 pour chaque candidat et son oppose V2
    V1 = np.random.binomial(1,0.5,size=nb_C) 
    V2 = 1 - V1

    #on va creer ensuite nos vecteur de parametres bernoullis avec l'argument de polarisation
    
    #Si Pol=0, proba (= V1) = 1, (identique). Si Pol=1, proba (= V2) = 1.
    P1 = np.abs(V1 - Pol) 
    # Si Pol=0, ce groupe est vide (N2=0). Si Pol=1, proba (=V1) = 1
    P2 = np.abs(V2 - Pol) 
    #N1 + N2 = N, et pour pol=0 on aN1=N | pol=1 on a N1=N/2. donc on tire exactement N/2 V1 et N/2 V2
    N2 = int(np.floor(nb_V * (Pol / 2)))
    N1 = nb_V - N2
    
    profil = []

    #on remarque pour pol=1/2, notre bias vers V1 ou V2 sont totalement supprimees car tout les
    #parametres sont a 1/2 pour P1 et P2. donc on tire totalement aleatoirement
    
    for _ in range(N1):
        bulletin = np.random.binomial(1, P1)
        profil.append(bulletin.tolist())

    
    for _ in range(N2):
        bulletin = np.random.binomial(1, P2)
        profil.append(bulletin.tolist())

    # On retourne le profil complet (élément de A^n) [cite: 29]
    return profil

def random_type_L(nb_V, nb_C, Pol):
    """
   renvoie nb_V bulletins aleatoires type L de taille nb_C avec une Polarisation Pol

    Args:
        nb_V (int): Nombre de bulletins de vote a generer. Doit etre un entier positif.
        nb_C (int): Nombre de candidats (taille de chaque bulletin). Doit etre un entier positif.
        Pol (float): Indice de polarisation compris dans [0, 1]. 
                     0.0 correspond a polarisation minimale.
                     1.0 correspond a polarisation maximale.
    Returns:
        profil : liste (non Numpy) de bulletins donc N elements de L.

    """
    # 1. Vecteur de reference V1 (rangs de 1 a m)
    V1 = np.random.permutation(np.arange(1, nb_C + 1))
    V2 = nb_C + 1 - V1  # Bulletin opposé
    profil = []
    

    #N1 + N2 = N, et pour pol=0 on aN1=N | pol=1 on a N1=N/2. donc on tire exactement N/2 V1 et N/2 V2
    N2 = int(np.floor(nb_V * (Pol / 2)))
    N1 = nb_V - N2

    #pour les permutations aleatoires on va simplement permuter aleatoirement un sous groupe de candidats
    #sous groupe choisit avec bernouilli, on veut pol=0 et pol=1 ne possede aucune permetuation en plus et pol = 1/2 total random
    #triagle avec 0 pour pol =1 et pol=0, et 1 si pol=1/2
    permut_arg =  Pol*2 if Pol<=1/2  else 1 - (2*Pol - 1) 

    for _ in range(N1):
        mask = np.random.binomial(1, permut_arg, size=nb_C) #notre choix de candidats a permuter
        indices = np.where(mask == 1)[0] #nos indices des val a permuter
        bulletin = V1.copy() 
    
        if len(indices) > 0:
            A_permuter = V1[indices] #les val a permuter
            permutees = np.random.permutation(A_permuter) #permutation
            bulletin[indices] = permutees #on remet les valeurs
            
        profil.append(bulletin.tolist())

    #meme chose que pour N1 mais avec V2
    for _ in range(N2):
        mask = np.random.binomial(1, permut_arg, size=nb_C)
        indices = np.where(mask == 1)[0]
        bulletin = V2.copy() 
        
        if len(indices) > 0:
            A_permuter = V2[indices]
            permutees = np.random.permutation(A_permuter)
            bulletin[indices] = permutees
            
        profil.append(bulletin.tolist())


    return profil







