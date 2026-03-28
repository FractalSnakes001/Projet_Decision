import numpy as np
from scipy.optimize import linear_sum_assignment
import Generation as gen
import Distances as ds

# tjr pas d'accent sur mon clavier, desoler en avance (clavier ricain)
# je vais essayer d'implementer la Docstring python comme cela Vscode nous affiche les infos des fonctions
#Exercice 12-13

def Calcul_U1_TypeA(profilA):
    """
    Calcule le score de consensus u1*(p) pour un profil de type A 
    en utilisant la regle de la majorite coordonnee par coordonnee.

    Args:
        profilA : profil de type A contenant n bulletins.

    Returns:
        - (int, list): (u1_etoile, bulletin_consensus)
        - None si erreur.
    """
    if len(profilA) == 0:
        return None,None
    
    N = len(profilA)
    M = len(profilA[0])
    if M == 0:
        return None,None

    consensus = []
    u1 = 0

    # On evalue chaque candidat de maniere inde
    for i in range(M):
        # On compte le nombre de votants ayant approuve (1) ce candidat
        nb_1 = sum(bull[i] for bull in profilA)
        nb_0 = N - nb_1

        if nb_1 >= nb_0:
            valeur_c = 1
            u1 += nb_0
        else:
            valeur_c = 0
            # L'erreur correspond a ceux qui ont mis 1
            u1 += nb_1
            
        consensus.append(valeur_c)

    return u1, consensus


def Calcul_U1_TypeL(profilL):
    """
    Calcule le score de consensus u1*(p) pour un profil de type L 
    en construisant la matrice des couts et en utilisant l'algorithme Hongrois.

    Args:
        profilL : profil contenant n bulletins type L de m candidats.
                               

    Returns:
        - (int, list): (u1_etoile, bulletin_consensus)
        - None si erreur.
    """
    if  len(profilL) == 0:
        return None,None
        
    N = len(profilL)
    M = len(profilL[0])
    if M == 0 or N==0:
        return None

    # On recupere les rangs possibles 
    rangs_possibles = sorted(profilL[0])

    # Creation de la matrice des couts W de taille M x M
    # Lignes  = candidats, Colonnes  = rangs possibles
    W = np.zeros((M, M))

    for c in range(M): 
        for j_id in range(M): 
            rang = rangs_possibles[j_id]
            cout = 0
            # W[c, j] = Somme des distances de Spearman si on donne le rang cible au candidat c
            for bull in profilL:
                cout += abs(bull[c] - rang)
            W[c, j_id] = cout

    # Res du probleme d'affectation 
    # row_ind correspond aux candidats, col_ind aux indices des rangs affectes
    row_ind, col_ind = linear_sum_assignment(W)

    # Calcul du cout total u1*(p) 
    u1_e = W[row_ind, col_ind].sum()

   
    # consensus[c] correspond au rang attribue au candidat c
    consensus = [0] * M
    for c, j_idx in zip(row_ind, col_ind):
        consensus[c] = rangs_possibles[j_idx]

    return int(u1_e), consensus

#on apllique juste k means
#on reprend un squellete fait dans un tp de donnes, mis a jour a pour notre cas
def Calcul_U2_TypeA(profilA, max_iter=50):
    """
    Calcule le score u2*(p) pour un profil de type A en utilisant 
    un algorithme K-means (K=2) avec la distance de Hamming.

    Args:
        profilA : profil de type A contenant n bulletins.
        max_iter (int): nombre maximum d'iterations pour eviter une boucle infinie. default 50

    Returns:
        - (int, tuple): (u2_etoile, (centre1, centre2))
        - None si erreur.
    """
    if not profilA or len(profilA) == 0:
        return None, None
    
    N, M = len(profilA), len(profilA[0])
    if M < 2:
        return None, None
    
    # 2 bulletins distincts au hasard,pol=1 force distincts
    Brd = gen.random_type_A(2,M,1)
    c1 = Brd[0]
    c2 = Brd[1]
    
    for _ in range(max_iter):
        p1 = []
        p2 = []
        
        # on place chaque votant dans le groupe le plus proche
        for bull in profilA:
            d1 = ds.Distance_Bulletins_A(bull, c1)
            d2 = ds.Distance_Bulletins_A(bull, c2)
            if d1 < d2:
                p1.append(bull)
            else:
                p2.append(bull)
                
        #cas vide
        if not p1 or not p2:
            mid = N // 2
            p1 = profilA[:mid]
            p2 = profilA[mid:]
            
        #  mise a jour : on recalcule les centres optimaux 
        score1, nv_c1 = Calcul_U1_TypeA(p1)
        score2, nv_c2 = Calcul_U1_TypeA(p2)
        
        if c1 == nv_c1 and c2 == nv_c2:
            break
            
        c1 = nv_c1
        c2 = nv_c2
        
    # Le score u2* est la somme des u1* des deux sous-groupes finaux
    u2_etoile = score1 + score2
    return u2_etoile, (c1, c2)





#on apllique juste k means aussi
def Calcul_U2_TypeL(profilL, max_iter=50):
    """
    Calcule le score u2*(p) pour un profil de type L en utilisant 
    un algorithme K-means (K=2) avec la distance de Spearman.

    Args:
        profilL (list of list): profil de type L contenant n bulletins.
        max_iter (int): nombre maximum d'iterations pour eviter une boucle infinie.

    Returns:
        - tuple (int, tuple): (u2_etoile, (centre1, centre2))
        - None, None si erreur.
    """
    if not profilL or len(profilL) == 0:
        return None, None
    
    N, M = len(profilL), len(profilL[0])
    if M < 2:
        return None, None
    
    # 2 bulletins distincts au hasard,pol=1 force distincts
    Brd = gen.random_type_L(2,M,1)
    c1 = Brd[0]
    c2 = Brd[1]
    
    for x in range(max_iter):
        p1 = []
        p2 = []
        
        for bull in profilL:
            d1 = ds.Distance_Bulletins_L(bull, c1)
            d2 = ds.Distance_Bulletins_L(bull, c2)
            if d1 < d2:
                p1.append(bull)
            else:
                p2.append(bull)
                
        # pour les groupes vides
        if not p1 or not p2:
            mid = N // 2
            p1 = profilL[:mid]
            p2 = profilL[mid:]
            
        #mise a jour (via  Algo Hongrois de la Q11)
        score1, nv_c1 = Calcul_U1_TypeL(p1)
        score2, nv_c2 = Calcul_U1_TypeL(p2)
        
        # 4. Condition d'arret
        if c1 == nv_c1 and c2 == nv_c2:
            break
            
        c1 = nv_c1
        c2 = nv_c2
        
    u2_etoile = score1 + score2
    return u2_etoile, (c1, c2)