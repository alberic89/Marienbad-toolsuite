#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  game.py
#
#  Copyright 2023 alberic89 <alberic89@gmx.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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
#

import random
from toolbox import findSolution

random.seed()


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameErrorPosition(Exception):
    def __init__(self, position):
        super().__init__("Position illégale : " + str(position))


class GameErrorEnd(Exception):
    def __init__(self):
        super().__init__("Le jeu est déjà terminé.")


class NewGame:
    # le jeu de départ est donné en paramètre dans une liste
    def __init__(self, jetons: list) -> None:
        self.position = jetons.copy()
        self.sani()


    # les actions du joueur doivent indiqué le tas joué et le nombre de jetons enlevés
    def player(self, tas: int, jetons: int) -> None:
        self.sani()
        self.position[tas] -= jetons

    # l'ordinateur joue le meilleur coup s'il existe, et sinon un coup aléatoire
    def ordi(self):
        self.sani()
        s = findSolution(tuple(self.position), all=True)
        if s == False:
            while True:
                tas = random.randrange(0, len(self.position))
                if self.position[tas] != 0:
                    break
            jetons = random.randrange(1, self.position[tas] + 1)
            self.player(tas, jetons)
        else:
            self.position = list(random.choice(s))

    def isEnded(self):
        for i in self.position:
            if i != 0:
                return False
        return True

    # Vérifie si le jeu est valide
    def sani(self):
        elementsnull = 0
        for i in self.position:
            if i < 0:
                raise GameErrorPosition(self.position)
            elif i == 0:
                elementsnull +=1
        if elementsnull == len(self.position):
            raise GameErrorEnd()
