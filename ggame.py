#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ggame.py
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
import random, os, time
import game
from tkinter import *
from tkinter import ttk

GAME = None


def btncommand(column):
    global tasselected, jetonsselected, playerbtn, gameframes
    if tasselected == None or tasselected == column:
        tasselected = column
        if jetonsselected < len(gameframes[column].jetons):
            gameframes[column].jetons[jetonsselected].configure(background="#3DAEE9")
            jetonsselected += 1
            playerbtn["state"] = "normal"
        else:
            for k in gameframes[column].jetons:
                k.configure(background="#BBBCBE")
            jetonsselected = 0
            tasselected = None
            playerbtn["state"] = "disabled"


class FrameTas:
    def __init__(self, jetons, column):
        global gamescene
        self.frame = ttk.Frame(gamescene)
        self.ncolumn = column
        self.nbjetons = jetons
        self.jetons = []
        self.frame.grid(
            column=self.ncolumn,
            row=0,
            sticky=(N, E, W, S),
        )
        self.generate()

    def generate(self):
        for i in range(self.nbjetons):
            self.jetons.append(
                Button(
                    self.frame,
                    text=" ",
                    width=1,
                    background="#BBBCBE",
                    command=lambda column=self.ncolumn: btncommand(column),
                )
            )
            self.jetons[i].grid(column=0, row=i)


def startgame(tas, jetons):
    random.seed()
    global gameframes, GAME, gamescene

    gameframes.clear()
    tasselected = None
    jetonsselected = 0
    for widget in gamescene.winfo_children():
        widget.destroy()
    for i in range(tas):
        gameframes.append(
            FrameTas(random.randrange(1, jetons + 1), i),
        )
    GAME = game.NewGame([i.nbjetons for i in gameframes])
    playerbtn["state"] = "disabled"
    ordibtn["state"] = "normal"


def userplay():
    global tasselected, jetonsselected, GAME
    GAME.player(tasselected, jetonsselected)
    updateGame()

def ordiplay():
    global gameframes, tasselected, jetonsselected, GAME
    GAME.ordi()
    for i in range(jetonsselected):
        gameframes[tasselected].jetons[i].configure(bg="#BBBCBE")
    for i in range(len(GAME.position)):
        if GAME.position[i] != len(gameframes[i].jetons):
            tasselected = i
            jetonsselected = len(gameframes[i].jetons) - GAME.position[i]
            break
    updateGame()


def updateGame():
    global gameframes, tasselected, jetonsselected, gamescene
    gameframes[tasselected].frame.destroy()
    gameframes[tasselected] = FrameTas(GAME.position[tasselected], tasselected)
    tasselected = None
    jetonsselected = 0
    playerbtn["state"] = "disabled"
    if GAME.isEnded():
        ordibtn["state"] = "disabled"
        endMsg()

def endMsg():
    global gamescene
    Label(gamescene, text="La partie est finie",).grid(
        sticky=(N, S, W, E),
    )

def checkSpin():
    global startgameframebtn
    if tasval.get() == 0 or jetonsval.get() == 0:
        startgameframebtn["state"] = "disabled"
    else :
        startgameframebtn["state"] = "normal"

gameframes = []
tasselected = None
jetonsselected = 0

ROOT = Tk()
ROOT.title("Marienbad Game")
s = ttk.Style()
ROOT.tk.call('source', os.path.abspath(os.path.curdir) + '/ttk-Breeze/breeze.tcl')
s.theme_use("Breeze")
window_width = 600
window_height = 600
screen_width = ROOT.winfo_screenwidth()
screen_height = ROOT.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# set the position of the window to the center of the screen
ROOT.geometry(
    str(window_width)
    + "x"
    + str(window_height)
    + "+"
    + str(center_x)
    + "+"
    + str(center_y)
)

ROOT.columnconfigure(0, weight=1, minsize=80)
ROOT.rowconfigure(0, weight=1, minsize=40)
ROOT.rowconfigure(1, weight=15, minsize=400)
ROOT.rowconfigure(2, weight=1, minsize=40)


startgameframe = ttk.Frame(ROOT)
tasval = IntVar()
choicetas = ttk.Spinbox(
    startgameframe,
    from_=1,
    to=15,
    textvariable=tasval,
    width=5,
    command=checkSpin,
)
choicetaslabel = ttk.Label(startgameframe, text="Nombre de tas")
jetonsval = IntVar()
choicejetons = ttk.Spinbox(
    startgameframe,
    from_=1,
    to=15,
    textvariable=jetonsval,
    width=5,
    command=checkSpin,
)
choicejetonslabel = ttk.Label(startgameframe, text="Nombre de jetons")
startgameframebtn = ttk.Button(
    startgameframe,
    text="Démarrer le jeu",
    state="disabled",
    command=lambda: [
        startgame(tasval.get(), jetonsval.get()),
    ],
)

startgameframe.columnconfigure(0, weight=1, minsize=10)
startgameframe.columnconfigure(1, weight=2, minsize=20)
startgameframe.columnconfigure(2, weight=2, minsize=20)
startgameframe.rowconfigure(
    0,
    weight=1,
)
startgameframe.rowconfigure(
    1,
    weight=1,
)

startgameframe.grid(column=0, row=0, sticky=(N, S, W, E))
choicetas.grid(column=0, row=0, sticky=(N, S, E))
choicetaslabel.grid(column=1, row=0, sticky=(N, S, W))
choicejetons.grid(column=0, row=1, sticky=(N, S, E))
choicejetonslabel.grid(column=1, row=1, sticky=(N, S, W))
startgameframebtn.grid(column=2, row=0, rowspan=2)

gamescene = ttk.Frame(ROOT)
for i in range(15):
    gamescene.columnconfigure(i, weight=1, minsize=25)
gamescene.rowconfigure(0, weight=1, minsize=80)
gamescene.grid(column=0, row=1, sticky=(N, S, W, E))

playframe = ttk.Frame(ROOT)
playerbtn = ttk.Button(
    playframe,
    text="Jouer",
    state="disabled",
    command=userplay,
)
ordibtn = ttk.Button(
    playframe,
    text="L'ordinateur joue",
    state="disabled",
    command=ordiplay,
)

playframe.columnconfigure(0, weight=1, minsize=20)
playframe.columnconfigure(1, weight=1, minsize=20)

playframe.grid(column=0, row=2, sticky=(N, S, W, E))
playerbtn.grid(column=0, row=0, sticky=(N, S, W, E))
ordibtn.grid(column=1, row=0, sticky=(N, S, W, E))

if __name__ == "__main__":
    ROOT.mainloop()
