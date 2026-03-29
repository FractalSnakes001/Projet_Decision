# Projet : Analyse de la Polarisation
**L3 Informatique – 2025–2026**  
**Projet – Fondements Mathématiques pour l’Aide à la Décision**

Nous modélisons des résultats d’élections selon **deux modes électoraux** et nous nous intéressons à la **mesure de la polarisation** de ces résultats.

---

## Instructions pour tester l’implémentation

## Option 1 — Environnement Python (venv + pip)

### Créer un environnement virtuel Python
```bash
python3 -m venv venv
```

### Activer l’environnement

- Linux / macOS :
```bash
source venv/bin/activate
```

- Windows (PowerShell) :
```powershell
.\venv\Scripts\Activate.ps1
```

- Windows (cmd.exe) :
```cmd
.\venv\Scripts\activate.bat
```

### Installer les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Option 2 — Environnement Conda

### Créer l’environnement
```bash
conda env create -f env_python_CONDA.yml
```

### Activer l’environnement
```bash
conda activate DecisionProject_env
```

---

## Lancer le programme principal
```bash
python src/main.py
```

---

## Utiliser le menu en ligne de commande
- Le programme propose un menu interactif.
- Tapez `help` pour voir les commandes disponibles et leur description.

---

Conseil : restez dans l’environnement virtuel (venv ou conda) pendant toute la session pour garantir que toutes les dépendances sont correctement utilisées.