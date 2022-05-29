from tkinter import *
import tkinter.font as font


class HoverButton(Button):
    def __init__(self, master, button_number, **kw):
        # initiating the button
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind('<Button-1>', self.click)
        self.button_number = button_number
        self.myFont = font.Font(family='Glacial Indifference', size=10, weight=font.BOLD)
        self['font'] = self.myFont
        self.click_number = 0
        self.click_second_number = 0

    def on_enter(self, e):
        # changing the color while hovering over a button
        self['background'] = self['activebackground']

    def on_leave(self, e):
        # changing the color while leaving button
        self['background'] = self.defaultBackground

    def click(self, e):
        #marking clicked buttons
        self.click_number = self.click_number + 1
        self.click_second_number = self.click_second_number + 1
        if self.click_number == 1:
            if self.defaultBackground == "white":
                self.defaultBackground = "black"
                self['text'] = 'ADDED    \n'
                self["fg"] = "green"
                self["justify"] = "left"
            elif self.defaultBackground == "black":
                self.defaultBackground = "white"
                self['text'] = 'REMOVED    \n'
                self["fg"] = "red"
                self["justify"] = "left"
        if self.click_second_number % 2 == 0:
            self["text"] = ""
