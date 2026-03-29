import numpy as np
import math
import sys
from dataclasses import dataclass
import matplotlib.pyplot as plt
import Distances as Ds
from Generation import *
import Polarisation as Polar

@dataclass
class Profile:
    """Simple dataclass to keep track of generated profiles with their parameters."""

    p: float 
    c: int
    v: int
    type: str
    data: list

profiles = list()



def help():
    print("Permitted operations:")
    for (op, desc) in descriptions.items():
        print("\t" + op + ": " + desc)

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

def listprofiles():
    for i in range(len(profiles)):
        p = profiles[i]
        print(f"Profile {i}. Type: {p.type} | C: {p.c} | V: {p.v} | Polarisation: {p.p}")

def show():
    print("Profile number: ", end="")
    index = int(input())

    if index >= len(profiles):
        print("Error: wrong argument(s). Index out of range.")
        return

    p = profiles[index]
    print(f"Profile {index}. Type: { "APPROBATION" if p.type == "a" else "ORDRE TOTAL"} | C: {p.c} | V: {p.v} | Polarisation: {p.p}")
    for v in p.data:
        for c in v:
            print(c, end=" ")
        print()


operations = {
    "help": help,
    "reset": reset,
    "profile": profile,
    "listprofiles": listprofiles,
    "show": show,
    "exit": None
}

descriptions = {
    "help": "Print this help paragraph.",
    "reset": "Erase all previously saved profiles.",
    "profile": "Generate & save A or L profile with the wanted candidates, voters numbers & polarisation.",
    "listprofiles": "List the previously created profiles.",
    "show": "Displays a particular saved profile.",
    "exit": "Exits the menu, stops the program."
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





