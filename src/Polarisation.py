import numpy as np
from scipy.optimize import linear_sum_assignment

def Calcul_U1_TypeA(profilA):
    """
    Calcule le score de consensus u1*(p) pour un profil de type A 
    en utilisant la regle de la majorite coordonnee par coordonnee.

    Args:
        profilA (list of list): profil de type A contenant n bulletins.

    Returns:
        - tuple (int, list): (u1_etoile, bulletin_consensus)
        - None si erreur.
    """
    if not profilA or len(profilA) == 0:
        return None
    
    N = len(profilA)
    M = len(profilA[0])
    if M == 0:
        return None

    consensus = []
    u1 = 0

    # On evalue chaque candidat de maniere independante
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
    Calcule le score de consensus u1*(p) pour un profil de type L (ordres totaux)
    en construisant la matrice des couts et en utilisant l'algorithme Hongrois.

    Args:
        profilL (list de list): profil contenant n bulletins de m candidats.
                                Chaque bulletin contient le rang de chaque candidat.

    Returns:
        - tuple (int, list): (u1_etoile, bulletin_consensus)
        - None, None si erreur.
    """
    if not profilL or len(profilL) == 0:
        return None, None
    
    N = len(profilL)
    M = len(profilL[0])
    if M == 0:
        return None, None

    # On recupere les rangs possibles (generalement 1 a M)
    # trier le premier bulletin permet d'etre agnostique (si indexe a 0 ou 1)
    rangs_possibles = sorted(profilL[0])

    # 1. Creation de la matrice des couts W de taille M x M
    # Lignes (c) = candidats, Colonnes (j) = rangs possibles
    W = np.zeros((M, M))

    for c in range(M): 
        for j_idx in range(M): 
            rang_cible = rangs_possibles[j_idx]
            cout = 0
            # W[c, j] = Somme des distances de Spearman si on donne le rang cible au candidat c
            for bull in profilL:
                cout += abs(bull[c] - rang_cible)
            W[c, j_idx] = cout

    # 2. Resolution du probleme d'affectation (Algorithme Hongrois)
    # row_ind correspond aux candidats, col_ind aux indices des rangs affectes
    row_ind, col_ind = linear_sum_assignment(W)

    # 3. Calcul du cout total u1*(p) associe a cette affectation optimale
    u1_etoile = W[row_ind, col_ind].sum()

    # 4. Reconstitution du bulletin de consensus
    # consensus[c] correspond au rang attribue au candidat c
    consensus = [0] * M
    for c, j_idx in zip(row_ind, col_ind):
        consensus[c] = rangs_possibles[j_idx]

    return int(u1_etoile), consensus