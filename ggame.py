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
                os.getcwd(),
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
            command=self.checkSpin,
        )
        choicetaslabel = ttk.Label(startgameframe, text="Nombre de tas")
        self.jetonsval = IntVar()
        choicejetons = ttk.Spinbox(
            startgameframe,
            from_=1,
            to=15,
            textvariable=self.jetonsval,
            width=5,
            command=self.checkSpin,
        )
        choicejetonslabel = ttk.Label(startgameframe, text="Nombre de jetons")
        self.startgameframebtn = ttk.Button(
            startgameframe,
            text="Démarrer le jeu",
            state="disabled",
            command=lambda: [
                self.startgame(self.tasval.get(), self.jetonsval.get()),
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
            text="Jouer ce coup",
            state="disabled",
            command=self.userplay,
        )
        self.ordibtn = ttk.Button(
            playframe,
            text="Meilleur coup",
            state="disabled",
            command=self.ordiplay,
        )

        playframe.columnconfigure(0, weight=1, minsize=20)
        playframe.columnconfigure(1, weight=1, minsize=20)

        playframe.grid(column=0, row=2, sticky=(N, S, W, E))
        self.playerbtn.grid(column=0, row=0, sticky=(N, S, W, E))
        self.ordibtn.grid(column=1, row=0, sticky=(N, S, W, E))

    def start(self):
        self.ROOT.mainloop()

    def stop(self):
        self.ROOT.destroy()

    def startgame(self, tas, jetons):
        random.seed()
        self.gameframes.clear()
        self.tasselected = None
        self.jetonsselected = 0
        for widget in self.gamescene.winfo_children():
            widget.destroy()
        for i in range(tas):
            self.gameframes.append(
                self.FrameTas(
                    self,
                    random.randrange(1, jetons + 1),
                    i,
                )
            )
        self.GAME = game.NewGame([i.nbjetons for i in self.gameframes])
        self.playerbtn["state"] = "disabled"
        self.ordibtn["state"] = "normal"

    def userplay(self):
        self.GAME.player(self.tasselected, self.jetonsselected)
        for i in range(self.jetonsselected):
            self.gameframes[self.tasselected].jetons[i].configure(bg="#BBBCBE")
        self.updateGame()

    def ordiplay(self):
        self.GAME.ordi()
        for i in range(self.jetonsselected):
            self.gameframes[self.tasselected].jetons[i].configure(bg="#BBBCBE")
        for i in range(len(self.GAME.position)):
            if self.GAME.position[i] != len(self.gameframes[i].jetons):
                self.tasselected = i
                self.jetonsselected = (
                    len(self.gameframes[i].jetons) - self.GAME.position[i]
                )
                break
        self.updateGame()

    def updateGame(self):
        self.blink()
        for i in range(self.jetonsselected):
            self.gameframes[self.tasselected].jetons.pop().destroy()
        self.tasselected = None
        self.jetonsselected = 0
        self.playerbtn["state"] = "disabled"
        if self.GAME.isEnded():
            self.ordibtn["state"] = "disabled"
            self.startgameframebtn["state"] = "disabled"
            self.endMsg()

    def endMsg(self):
        self.GAME = None
        Label(
            self.gamescene,
            text="La partie est finie",
        ).grid(
            sticky=(N, S, W, E),
        )

    def checkSpin(self):
        if self.tasval.get() == 0 or self.jetonsval.get() == 0:
            self.startgameframebtn["state"] = "disabled"
        else:
            self.startgameframebtn["state"] = "normal"

    def blink(self):
        for loop in range(3):
            for i in range(self.jetonsselected):
                self.gameframes[self.tasselected].jetons[-(i + 1)].configure(
                    bg="#3DAEE9"
                )
                self.gameframes[self.tasselected].jetons[-(i + 1)].update()
            time.sleep(0.5)
            for i in range(self.jetonsselected):
                self.gameframes[self.tasselected].jetons[-(i + 1)].configure(
                    bg="#BBBCBE"
                )
                self.gameframes[self.tasselected].jetons[-(i + 1)].update()
            time.sleep(0.3)

    class FrameTas:
        def __init__(self, parent, jetons, column):
            self.parent = parent
            self.frame = ttk.Frame(self.parent.gamescene)
            self.column = column
            self.nbjetons = jetons
            self.jetons = []
            self.frame.grid(
                column=self.column,
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
                        command=self.btncommand,
                    )
                )
                self.jetons[i].grid(column=0, row=i)

        def btncommand(self):
            if (
                self.parent.tasselected == None
                or self.parent.tasselected == self.column
            ):
                self.parent.tasselected = self.column
                if self.parent.jetonsselected < len(self.jetons):
                    self.jetons[-(self.parent.jetonsselected + 1)].configure(
                        background="#3DAEE9"
                    )
                    self.parent.jetonsselected += 1
                    self.parent.playerbtn["state"] = "normal"
                else:
                    for k in self.jetons:
                        k.configure(background="#BBBCBE")
                    self.parent.jetonsselected = 0
                    self.parent.tasselected = None
                    self.parent.playerbtn["state"] = "disabled"


if __name__ == "__main__":
    app = App()
    app.start()
