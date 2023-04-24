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
from tkinter import *
from tkinter import ttk

import game


def btncommand(column):
    global app
    if app.tasselected == None or app.tasselected == column:
        app.tasselected = column
        if app.jetonsselected < len(app.gameframes[column].jetons):
            app.gameframes[column].jetons[-(app.jetonsselected + 1)].configure(
                background="#3DAEE9"
            )
            app.jetonsselected += 1
            app.playerbtn["state"] = "normal"
        else:
            for k in app.gameframes[column].jetons:
                k.configure(background="#BBBCBE")
            app.jetonsselected = 0
            app.tasselected = None
            app.playerbtn["state"] = "disabled"


class FrameTas:
    def __init__(self, jetons, column, gamescene):
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
    global app
    app.gameframes.clear()
    app.tasselected = None
    app.jetonsselected = 0
    for widget in app.gamescene.winfo_children():
        widget.destroy()
    for i in range(tas):
        app.gameframes.append(
            FrameTas(random.randrange(1, jetons + 1), i, app.gamescene)
        )
    app.GAME = game.NewGame([i.nbjetons for i in app.gameframes])
    app.playerbtn["state"] = "disabled"
    app.ordibtn["state"] = "normal"


def userplay():
    global app
    app.GAME.player(app.tasselected, app.jetonsselected)
    for i in range(app.jetonsselected):
        app.gameframes[app.tasselected].jetons[i].configure(bg="#BBBCBE")
    updateGame()


def ordiplay():
    global app
    app.GAME.ordi()
    for i in range(app.jetonsselected):
        app.gameframes[tasselected].jetons[i].configure(bg="#BBBCBE")
    for i in range(len(app.GAME.position)):
        if app.GAME.position[i] != len(app.gameframes[i].jetons):
            app.tasselected = i
            app.jetonsselected = len(app.gameframes[i].jetons) - app.GAME.position[i]
            break
    updateGame()


def updateGame():
    global app
    blink()
    app.gameframes[app.tasselected].frame.destroy()
    app.gameframes[app.tasselected] = FrameTas(
        app.GAME.position[app.tasselected], app.tasselected, app.gamescene
    )
    app.tasselected = None
    app.jetonsselected = 0
    app.playerbtn["state"] = "disabled"
    if app.GAME.isEnded():
        app.ordibtn["state"] = "disabled"
        app.startgameframebtn["state"] = "disabled"
        endMsg()


def endMsg():
    global app
    Label(
        app.gamescene,
        text="La partie est finie",
    ).grid(
        sticky=(N, S, W, E),
    )


def checkSpin():
    global app
    if app.tasval.get() == 0 or app.jetonsval.get() == 0:
        app.startgameframebtn["state"] = "disabled"
    else:
        app.startgameframebtn["state"] = "normal"


def blink():
    global app
    for loop in range(3):
        for i in range(app.jetonsselected):
            app.gameframes[app.tasselected].jetons[-(i + 1)].configure(bg="#3DAEE9")
            app.gameframes[app.tasselected].jetons[-(i + 1)].update()
        time.sleep(0.5)
        for i in range(app.jetonsselected):
            app.gameframes[app.tasselected].jetons[-(i + 1)].configure(bg="#BBBCBE")
            app.gameframes[app.tasselected].jetons[-(i + 1)].update()
        time.sleep(0.3)


class App:
    def __init__(self):
        self.gameframes = []
        self.tasselected = None
        self.jetonsselected = 0

        self.GAME = None
        self.ROOT = Tk()
        self.ROOT.title("Marienbad Game")
        s = ttk.Style()
        self.ROOT.tk.call(
            "source",
            os.path.join(
                os.path.abspath(os.path.curdir),
                "ttk-Breeze",
                "breeze.tcl",
            ),
        )
        s.theme_use("Breeze")
        window_width = 600
        window_height = 600
        screen_width = self.ROOT.winfo_screenwidth()
        screen_height = self.ROOT.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.ROOT.geometry(
            str(window_width)
            + "x"
            + str(window_height)
            + "+"
            + str(center_x)
            + "+"
            + str(center_y)
        )

        self.ROOT.columnconfigure(0, weight=1, minsize=80)
        self.ROOT.rowconfigure(0, weight=1, minsize=40)
        self.ROOT.rowconfigure(1, weight=15, minsize=400)
        self.ROOT.rowconfigure(2, weight=1, minsize=40)

        startgameframe = ttk.Frame(self.ROOT)
        self.tasval = IntVar()
        choicetas = ttk.Spinbox(
            startgameframe,
            from_=1,
            to=15,
            textvariable=self.tasval,
            width=5,
            command=checkSpin,
        )
        choicetaslabel = ttk.Label(startgameframe, text="Nombre de tas")
        self.jetonsval = IntVar()
        choicejetons = ttk.Spinbox(
            startgameframe,
            from_=1,
            to=15,
            textvariable=self.jetonsval,
            width=5,
            command=checkSpin,
        )
        choicejetonslabel = ttk.Label(startgameframe, text="Nombre de jetons")
        self.startgameframebtn = ttk.Button(
            startgameframe,
            text="Démarrer le jeu",
            state="disabled",
            command=lambda: [
                startgame(self.tasval.get(), self.jetonsval.get()),
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
        self.startgameframebtn.grid(column=2, row=0, rowspan=2)

        self.gamescene = ttk.Frame(self.ROOT)
        for i in range(15):
            self.gamescene.columnconfigure(i, weight=1, minsize=25)
        self.gamescene.rowconfigure(0, weight=1, minsize=80)
        self.gamescene.grid(column=0, row=1, sticky=(N, S, W, E))

        playframe = ttk.Frame(self.ROOT)
        self.playerbtn = ttk.Button(
            playframe,
            text="Jouer",
            state="disabled",
            command=userplay,
        )
        self.ordibtn = ttk.Button(
            playframe,
            text="L'ordinateur joue",
            state="disabled",
            command=ordiplay,
        )

        playframe.columnconfigure(0, weight=1, minsize=20)
        playframe.columnconfigure(1, weight=1, minsize=20)

        playframe.grid(column=0, row=2, sticky=(N, S, W, E))
        self.playerbtn.grid(column=0, row=0, sticky=(N, S, W, E))
        self.ordibtn.grid(column=1, row=0, sticky=(N, S, W, E))


if __name__ == "__main__":
    app = App()
    app.ROOT.mainloop()
