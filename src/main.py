# while loop based command line menu, wrappers for implementations

from dataclasses import dataclass
from itertools import combinations
from Generation import *
from Distances import *
from phi_square import *
from Polarisation import *

@dataclass
class Profile:
    """Simple dataclass to keep track of generated profiles with their parameters."""

    p: float 
    c: int
    v: int
    type: str
    data: list

profiles = list()

def choose_profile():
    ok = False
    while not ok:
        print("Profile index: ", end="")
        index = int(input())

        if index >= len(profiles) or 0 > index:
            print("Error: wrong argument(s). Index out of range.")
        else:
            ok = True
            return index, profiles[index]

def help():
    max = -1
    for s in descriptions:
        max = len(s) if len(s) > max else max

    print("Permitted operations:")
    for (op, desc) in descriptions.items():
        print("   " + " " * (max - len(op)) + op + " | " + desc)

def reset():
    profiles.clear()
    print("Profiles cleared.")

def profile():
    args = list()

    print("Type ? [a | l]", end=" ")
    type = input()
    type = type if type == "a" or type == "l" else None
    args.append(type)

    print("How many candidates ?", end=" ")
    c = int(input()) # will eventually raise value error
    args.append(c)

    print("How many voters ?", end=" ")
    v = int(input()) # will eventually raise value error
    args.append(v)

    print("Polarisation ? [0 <= p <= 1]", end=" ")
    p = float(input()) # will eventually raise value error
    p = p if 0 <= p <= 1 else None
    args.append(v)

    if None in args:
        print("Error: wrong argument(s).")
        return

    elif type == "a":
        res = random_type_A(v, c, p)

    elif type == "l":
        res = random_type_L(v, c, p)

    profile = Profile(p, c, v, type, res)
    profiles.append(profile)
    print("Profile saved.")

def listp():
    for i in range(len(profiles)):
        p = profiles[i]
        print(f"Profile {i}. Type: {p.type} | C: {p.c} | V: {p.v} | Polarisation: {p.p}")

def show():
    index, p = choose_profile()
    print(f"Profile {index}. Type: {'APPROVAL' if p.type == 'a' else 'TOTAL ORDERING'} | C: {p.c} | V: {p.v} | Polarisation: {p.p}")
    for v in p.data:
        for c in v:
            print(c, end=" ")
        print()

def candidatedistance():
    index, profile = choose_profile()

    print("Candidate A" + " " * 4 + "Candidate B" + " " * 4 + "Distance between A and B")

    for (c1, c2) in combinations(range(1, profile.c + 1), 2):
        distance = abs(NombrePreferance(profile.data, c1-1, c2-1, profile.v, profile.type.upper()) - NombrePreferance(profile.data, c2-1, c1-1, profile.v, profile.type.upper()))
        print(c1, " "*14, c2, " "*14, distance, sep="")

def phisquare():
    index, profile = choose_profile()
    distance = computePhiSquare_A(profile.data) if profile.type == "a" else computePhiSquare_L(profile.data)
    print(f"Phi² distance of profile no. {index}: {round(distance, 2)}")

def evolphisquare():
    print("Candidate number ? ", end="")
    c = int(input())
    
    print("Voter number ? ", end="")
    v = int(input())
    
    print("Profile type ? [A | L] ", end="")
    t = input()
    
    print("Polarization step (ex: 0.1) ? ", end="")
    pas = float(input())
    
    print("Repetitions per point ? ", end="")
    rep = int(input())
    
    if c < 1 or v < 1 or (t not in ["A", "L"]) or pas <= 0 or pas > 1 or rep < 1:
        print("Error: wrong argument(s).")
        return
    evol_phi_square_A(v, c, pas, rep) if t == "A" else evol_phi_square_L(v, c, pas, rep)

def hamming():
    index, profile = choose_profile()

    if profile.type != "a":
        print("Error: the profile needs to be of type approval in order to compute Hamming distances in it.")
        return

    print("First ballot index ? ", end="")
    b1 = int(input())
    print("Second ballot index ? ", end="")
    b2 = int(input())

    if b1 < 0 or b2 < 0 or b1 >= profile.v or b2 >= profile.v:
        print("Error: wrong argument(s). Index out of range.")
        return    

    distance = Distance_Bulletins_A(profile.data[b1], profile.data[b2])

    print(f"Hamming distance: {distance}")

def spearman():
    index, profile = choose_profile()

    if profile.type != "l":
        print("Error: the profile needs to be of type approval in order to compute Spearman distances in it.")
        return

    print("First ballot index ? ", end="")
    b1 = int(input())
    print("Second ballot index ? ", end="")
    b2 = int(input())

    if b1 < 0 or b2 < 0 or b1 >= profile.v or b2 >= profile.v:
        print("Error: wrong argument(s). Index out of range.")
        return    

    distance = Distance_Bulletins_L(profile.data[b1], profile.data[b2])

    print(f"Spearman distance: {distance}")

def consensus():
    index, profile = choose_profile()
    (score, ballot) = Calcul_U1_TypeA(profile.data) if profile.type == "a" else Calcul_U1_TypeL(profile.data)

    print(f"Minimum cumulated {'Hamming' if profile.type == 'a' else 'Spearman'} distance: {score}")
    print("Consensus ballot: ", end="")
    for i in ballot:
        print(i, end=" ")
    print()

def consensuscluster():
    index, profile = choose_profile()
    (score, clusters) = Calcul_U2_TypeA(profile.data) if profile.type == "a" else Calcul_U2_TypeL(profile.data)
    print(f"u2* minimum cumulated {'Hamming' if profile.type == 'a' else 'Spearman'} distance by cluster: {score}")
    for k in range(1, len(clusters)+1):
        print(f"Cluster {k}:")
        for i in clusters[k-1]:
            print(i, end=" ")
        print()

def polarisation():
    index, profile = choose_profile()
    result = Polarisation_TypeA(profile.data) if profile.type == "a" else Polarisation_TypeL(profile.data)
    print(f"Polarisation: {round(result, 2)}")

def evolphi():
    print("Candidate number ? ", end="")
    c = int(input())
    print("Voter number ? ", end="")
    v = int(input())
    print("Step ? ", end="")
    s = float(input())
    print("Tries by step number ? ", end="")
    t = int(input())

    if c < 1 or v < 1 or not (0 <= s and s <= 1) or t < 1:
        print("Wrong argument(s).")

    Evaluer_Polarisation(v, c, s, t)

operations = {
    "help": help,
    "reset": reset,
    "profile": profile,
    "listp": listp,
    "show": show,
    "candidatedistance": candidatedistance,
    "phisquare": phisquare,
    "evolphisquare": evolphisquare,
    "hamming": hamming,
    "spearman": spearman,
    "consensus": consensus,
    "consensuscluster": consensuscluster,
    "polarisation": polarisation,
    "evolphi": evolphi,
    "exit": None
}

descriptions = {
    "help": "Print this help paragraph.",
    "reset": "Erase all previously saved profiles.",
    "profile": "Generate & save A or L profile with the wanted candidates, voters numbers & polarisation.",
    "listp": "List the previously created profiles.",
    "show": "Display a particular saved profile.",
    "candidatedistance": "Display the preference distance between every pair of candidate of a particular profile, as defined in question 3.",
    "phisquare": "Compute the phi square distance of a profile as defined in question 5.",
    "evolphisquare": "Graph the evolution of the Phi² polarisation measure as a function of our own polarisation generation parameter.",
    "hamming": "Compute the Hamming distance between two ballots of an approval profile.",
    "spearman": "Compute the Spearman distance between two ballots of a total ordering profile.",
    "consensus": "Compute the consensus, a ballot that minimizes its cumulated Hamming/Spearman distance to a profile.",
    "consensuscluster": "Compute an approximation of an optimal ballot pair, representing the best two profile clusters.",
    "polarisation": "Compute the final phi polarisation measure of a profile.",
    "evolphi": "Graph the evolution of the Phi polarisation measure as a function of our own polarisation generation parameter, for both A/L type profiles.",
    "exit": "Exit the menu, stop the program."
}

def menu():

    ok = True
    while (ok):

        print("> ", end="")
        i = input()

        # IMPLEMENTED OPERATIONS
        if i in operations and operations[i] != None:
            operations[i]()

        # META OPERATIONS
        elif i in operations:

            if (i == "exit"):
                ok = False

        # ERROR
        else:
            print("Wrong operation. Try 'help'.")

        print()

    # POST MENU INSTRUCTIONS ?
    # save on disk etc. ?



menu()





