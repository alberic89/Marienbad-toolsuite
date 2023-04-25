#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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

import argparse
import toolbox


def solve(args):
    r = toolbox.findSolution(tuple(args.situation), findall=args.all)
    if r == False:
        print("Aucune solution trouvée.")
    else:
        print(
            "Voici "
            + ("les" if len(r) > 1 else "la")
            + " solution"
            + ("s" if len(r) > 1 else "")
            + " trouvée"
            + ("s" if len(r) > 1 else "")
            + " :"
        )
        for i in r:
            print(i)


def check(args):
    r = toolbox.check(tuple(args.situation))
    print(
        "La position est "
        + ("gagnante" if r == 0 else "perdante")
        + " avec une nim-somme de "
        + str(r)
    )


def generate(args):
    r = toolbox.generatePosition(args.njetons, args.ntas, x_tas_only=args.only)
    print(
        "Voici la liste des positions gagnantes avec "
        + ("exactement " if args.only else "au moins ")
        + str(args.ntas)
        + " tas de au moins "
        + str(args.njetons)
        + " jetons :"
    )
    for i in r:
        print(i)


def play(args):
    import ggame

    app = ggame.App()
    if args.njetons != None:
        app.choicejetons.set(args.njetons)
    if args.ntas != None:
        app.choicetas.set(args.ntas)
    app.startgame()
    app.start()


# Parser principal
parser = argparse.ArgumentParser(
    description="Une collection d'outils utiles pour étudier et jouer au jeu de Marienbad.",
    epilog="Note : toutes les situations doivent être données sous la forme <int> <int> <int> etc. Par exemple : 12 15 9 8 45 21",
)
subparsers = parser.add_subparsers(title="Outils", required=True, dest="outil")
# Parser solve
parser_solve = subparsers.add_parser(
    "solve",
    help="Cherche une ou plusieurs solutions à une situation donnée.",
)
parser_solve.add_argument(
    "--all",
    "-a",
    help="Trouve toutes les solutions possibles",
    action="store_true",
)
parser_solve.add_argument(
    "situation",
    help="Renseigne la situation à résoudre",
    nargs="+",
    type=int,
)
parser_solve.set_defaults(tool=solve)
# Parser check
parser_check = subparsers.add_parser(
    "check", help="Vérifie la nim-somme de la situation."
)
parser_check.add_argument(
    "situation",
    help="Renseigne la situation à vérifier",
    nargs="+",
    type=int,
)
parser_check.set_defaults(tool=check)
# Parser generate
parser_generate = subparsers.add_parser(
    "generate", help="Génère une suite de combinaisons gagnantes."
)
parser_generate.add_argument(
    "njetons",
    help="Nombre de jetons maximum par tas",
    type=int,
)
parser_generate.add_argument(
    "ntas",
    help="Nombre de tas maximum",
    type=int,
)
parser_generate.add_argument(
    "--only",
    "-o",
    help="Ne génère que les positions avec exactement le nombre de tas indiqué.",
    action="store_true",
)
parser_generate.set_defaults(tool=generate)
# Parser play
parser_play = subparsers.add_parser("play", help="Jouer au jeu de Marienbad")
parser_play.add_argument(
    "--njetons",
    "-j",
    help="Nombre de jetons maximum par tas",
    default=None,
    type=int,
)
parser_play.add_argument(
    "--ntas",
    "-t",
    help="Nombre de tas",
    default=None,
    type=int,
)
parser_play.set_defaults(tool=play)

# Parse arguments
args = parser.parse_args()
args.tool(args)
