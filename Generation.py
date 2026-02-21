#CODE POUR question 1/2
#pour random
import numpy as np 

# pas d'accent sur mon clavier, desoler en avance
# je vais essayer d'implementer Docstring python


#On a N votantes  et M candidats, chaque votante est associe a son bulletin
#Bulletin type A => c'est un tableau de taille M, elements: 0 ou 1.

def generation_random_typeA(nb_V ,nb_C, Pol):
    """renvoie nb_V bulletins aleatoires type A de taille nb_C avec une Polarisation Pol

    Args:
        nb_V (integer): nombre de bulletins a retouner
        nb_C (integer): taille du bulletin
        Pol (float): indice de polarisation dans [0,1], 1=tres polarisee, 0=c
    """
