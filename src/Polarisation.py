import numpy as np
from scipy.optimize import linear_sum_assignment

# tjr pas d'accent sur mon clavier, desoler en avance (clavier ricain)
# je vais essayer d'implementer la Docstring python comme cela Vscode nous affiche les infos des fonctions


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
        return None
    
    N = len(profilA)
    M = len(profilA[0])
    if M == 0:
        return None

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
        return None
        
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