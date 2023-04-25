#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  toolbox/toolbox.py.py
#
#  Copyright 2023 alberic89 <alberic89@gmx.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from itertools import combinations_with_replacement
from functools import cache

# Les fonctions avec des commentaires sont les principales,
# les autres ne sont que des sous-routines utiles.


def replaceInPosition(position: tuple, oldvalue: int, newvalue: int) -> tuple:
    position = list(position)
    position[position.index(oldvalue)] = newvalue
    return tuple(position)


def firstBit(n: int) -> int:
    return len(bin(n)[2:])


def bitIsOne(n: int, rang: int) -> bool:
    try:
        if bin(n)[2:][-rang] == "1":
            return True
    except IndexError:
        pass
    return False


def listAllNumber(position: tuple) -> tuple:
    numbers = []
    for i in position:
        if i not in numbers:
            numbers.append(i)
    numbers.sort(reverse=True)
    return tuple(numbers)


def check(position: tuple) -> bool or int:
    """Vérifie la position en calculant la somme xor du tuple."""
    """Retourne la somme xor."""
    s = 0
    for i in position:
        s ^= i
    return s


@cache
def findSolution(position: tuple, findall=False) -> tuple or bool:
    """Retourne une ou plusieurs solutions à cette position."""
    """Usage : findSolution(<position>) ou findSolution(<position>, findall=True)"""
    """Retourne False si pas de solution, ou les solutions sous forme d'un tuple de tuples."""
    # Si la position est gagnante, pas de solutions.
    nsomme = check(position)
    if nsomme == 0:
        return False
    nfirstbit = firstBit(nsomme)
    solutions = []
    for tas in listAllNumber(position):
        if bitIsOne(tas, nfirstbit):
            solutions.append(replaceInPosition(position, tas, tas ^ nsomme))
            if findall == False:
                break
    if solutions != []:
        return tuple(solutions)
    return False


@cache
def generatePosition(nbjetons: int, nbtas: int, x_tas_only=False) -> tuple:
    """Génère des positions gagnantes à partir de l'entrée donnée."""
    """Usage : generateTable(<Nombre de jetons maximum par pile>, <nombre """
    """de piles maximum>, <(optionel) Ne générer que des jeux avec le nombre de tas donné>"""
    jetons = tuple(range(1, nbjetons + 1))
    positions = []
    # Ne seront générée que les jeux avec <nbtas> tas si l'option est activée.
    # Sinon, on recommence pour toutes les tailles inférieures ou égales à <nbtas>.
    if x_tas_only:
        tas = tuple([nbtas])
    else:
        tas = tuple(range(1, nbtas + 1))
    for loop in tas:
        # Génère toutes les combinaisons possibles
        for i in combinations_with_replacement(
            jetons, loop
        ):  # Teste les combinaisons
            if check(i) == 0:
                positions.append(i)
    return positions
