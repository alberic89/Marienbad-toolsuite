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


def replaceInPosition(position: tuple, oldvalue: int, newvalue: int) -> tuple:
    position = list(position)
    position[position.index(oldvalue)] = newvalue
    return tuple(position)


def firstBit(n: int) -> int:
    return len(bin(n)[2:])


def listAllNumber(position: tuple) -> tuple:
    position.sort()
    numbers = []
    for i in position:
        if i not in numbers:
            numbers.append(i)
    return numbers


def check(position: tuple) -> (bool or int):
    """Vérifie la position en calculant la somme xor du tuple."""
    """Retourne True si égal à 0 et sinon la somme"""
    s = 0
    for i in position:
        s ^= i
    if s == 0:
        return True
    return s


def findSolution(position: tuple, all=False) -> (tuple or bool):
    """Retourne une ou plusieurs solutions à cette position."""
    """Usage : findSolution(<position>) ou findSolution(<position>, all=True)"""
    """Retourne False si pas de solution, ou les solutions sous forme d'un tuple de tuples."""
    # Si la position est gagnante, pas de solutions.
    nsomme = check(position)
    if nsomme == True:
        return False
    nfirstbit = firstBit(nsomme)
    solutions = []
    for tas in listAllNumber(position):
        if firstBit(tas) == nfirstbit:
            solutions.append(replaceInPosition(position, tas, tas ^ nsomme))

    if solutions != []:
        return tuple(solutions)
    return False
