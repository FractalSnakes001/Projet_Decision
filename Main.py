#(paolo) j'ai mit un fichier YML qui permet normalement de creer l'environnement que j'utilise
# comme cela on a tous les memes versions de biblio...etc 
# CONDA: conda env create -f env_python_CONDA.yml.  (puis apres vous activez )
# venv/pip: 1) creer un nouveau environnement (3.11.13)
# venv/pip: 2) activez le puis : pip install -r env_python_PIP.txt


import numpy as np
import math
import sys
import matplotlib.pyplot as plt

print("Numpy :",np.__version__, " chez P: 2.0.1")
print("matplotlib",  plt.matplotlib.__version__, "chez P: 3.10.0")
print("Python", sys.version[:8], " Chez P: 3.11.13") #apres 8 dans la chaine il y a des info non utiles