from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment
import Generation as gen
import Distances as ds

# tjr pas d'accent sur mon clavier, desoler en avance (clavier ricain)
# je vais essayer d'implementer la Docstring python comme cela Vscode nous affiche les infos des fonctions
#Exercice 12-13-14-15

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
    en construisant la matrice des couts et en utilisant l'algorithme Hongrois. Scipy

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

    # Resol du probleme d'affectation 
    # row_ind correspond aux candidats, col_ind aux indices des rangs 
    row_ind, col_ind = linear_sum_assignment(W)

    # Calcul du cout total u1*(p) 
    u1_e = W[row_ind, col_ind].sum()

   
    # consensus[c] correspond au rang attribue au candidat c
    consensus = [0 for _ in range(M)]
    for c, j_idx in zip(row_ind, col_ind): #pour iterer au meme temps
        consensus[c] = rangs_possibles[j_idx]

    return int(u1_e), consensus

#on apllique juste k means
#on reprend un squellete fait dans un tp de donnes, mis a jour a pour notre cas
def Calcul_U2_TypeA(profilA, max_iter=50):
    """
    Calcule le score u2*(p) pour un profil de type A avec algorithme K-means (K=2) et la distance de Hamming.

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
    Calcule le score u2*(p) pour un profil de type L avec 
    un algorithme K-means (K=2) et la distance de Spearman.

    Args:
        profilL : profil de type L contenant n bulletins.
        max_iter : nombre maximum d'iterations pour eviter une boucle infinie.

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


#pour la question 14, il suffit d'appliquer la formule de polarisation
def Polarisation_TypeA(profilA, max_iter=50):
    """
    Calcule la mesure de polarisation  pour un profil de type A.

    Args:
        profilA : profil de type A contenant n bulletins.
        max_iter : nombre maximum d'iterations pour le K-means de u2*. default 50

    Returns:
        - float: score de polarisation compris entre 0.0 et 1.0.
        - None si erreur.
    """
    if not profilA or len(profilA) == 0:
        return None
    
    N, M = len(profilA), len(profilA[0])
    if M < 2:
        return None
        
    # Calcul de u1* 
    # Calcul_U1 renvoie (score, bulletin), on ne garde que l'indice 0
    u1_res = Calcul_U1_TypeA(profilA)
    if u1_res[0] is None:
        return None
    u1_etoile = u1_res[0]
    
    # Calcul de u2* (cout du consensus divise en 2 camps)
    u2_res = Calcul_U2_TypeA(profilA, max_iter)
    if u2_res[0] is None:
        return None
    u2_etoile = u2_res[0]
    
    # Application de la formule
    phi = (2.0 / (N * M)) * (u1_etoile - u2_etoile)
    
    return phi

#question 15 affichage final:
def Polarisation_TypeL(profilL, max_iter=50):
    """
    Calcule la mesure de polarisation globale pour un profil de type L .

    Args:
        profilL : profil de type L contenant n bulletins.
        max_iter : nombre maximum d'iterations pour le K-means de u2*.

    Returns:
        - float: score de polarisation compris entre 0.0 et 1.0.
        - None si erreur.
    """
    if not profilL or len(profilL) == 0:
        return None
    
    N, M = len(profilL), len(profilL[0])
    if M < 2:
        return None
        
    # Calcul de u1* via le graphe biparti (Hongrois)
    u1_res = Calcul_U1_TypeL(profilL)
    if u1_res[0] is None:
        return None
    u1_etoile = u1_res[0]
    
    # Calcul de u2* via K-means sur la distance de Spearman
    u2_res = Calcul_U2_TypeL(profilL, max_iter)
    if u2_res[0] is None:
        return None
    u2_etoile = u2_res[0]
    
    # Application de la formule mathematique
    phi = (4.0 / (N * M * M)) * (u1_etoile - u2_etoile)
    
    return phi

#question 15 affichage final:
def Evaluer_Polarisation(N=100, M=10, pas=0.05, nb_simuls=10):
    """
    Evalue et affiche l'evolution de la mesure de polarisation, selon la polarisation utilisee dans Generations.py 

    Args:
        N (int): Nombre de votantes (taille du profil).
        M (int): Nombre de candidats.
        pas (float): Pas d'incrementation pour le parametre Pol (entre 0.0 et 1.0).
        nb_simuls (int): Nombre de profils generes par etape pour diminuer la varience

    Returns:
        -void si ok
        -None si erreur
    """
    if pas <= 0 or N < 2 or M < 2:
        return None

    pol_inputs = np.arange(0.0, 1.0 + pas , pas)
    
    resultats_A = []
    resultats_L = []

    
    for p in pol_inputs:
        somme_phi_A = 0.0
        somme_phi_L = 0.0
        
        for _ in range(nb_simuls):
            # Gen des profils 
            profil_A = gen.random_type_A(N, M, p)
            profil_L = gen.random_type_L(N, M, p)
            
            #Calcul des polarisations 
            phi_A = Polarisation_TypeA(profil_A)
            phi_L = Polarisation_TypeL(profil_L)
            
            #Secu car renvois None si erreur
            somme_phi_A += phi_A if phi_A is not None else 0
            somme_phi_L += phi_L if phi_L is not None else 0
            
        #  Moyenne des resultats 
        resultats_A.append(somme_phi_A / nb_simuls)
        resultats_L.append(somme_phi_L / nb_simuls)
        
    # print("Evaluation terminee. Generation du graphique..")

    # Creation du graphique avec Matplotlib
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # Courbes des resultats
    plt.plot(pol_inputs, resultats_A, marker='o', linestyle='-', color='blue', label='Type A')
    plt.plot(pol_inputs, resultats_L, marker='x', linestyle='-', color='red', label='Type L')
    
    # Ligne de reference  y = x (Pol injectee = Pol mesuree)
    plt.plot([0, 1], [0, 1], 'k--', label='Reference  (y=x)')
    
    plt.title("Evolution de la Polarisation Mesuree vs Polarisation de generation\n(N="+str(N)+" votantes, M="+str(M)+" candidats, "+str(nb_simuls)+" simuls/point)")
    plt.xlabel("Parametre 'Pol' de  generation")
    plt.ylabel("Mesure de polarisation calculee (Phi)")
    plt.xlim(0, 1.05)
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    #force d'avoir le 0.5 pour montrer que purement aleatoire != polarisation mesuree =0.5
    plt.xticks(np.arange(0.0, 1.1, 0.1)) 
    # Affichage
    plt.show()
    return 