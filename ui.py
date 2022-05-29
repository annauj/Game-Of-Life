from tkinter import *
from cellularautomata import CellularAutomata

THEME_COLOR = "#F4C8AB"

class GameInterface(CellularAutomata):
    def __init__(self):
        # creating a window
        self.window = Tk()
        self.window.title("Understanding Game of Life")
        self.window.resizable(0, 0)
        app_width = 810
        app_height = 680
        screen_width = self.window.winfo_width()
        screen_height = self.window.winfo_height()
        x = (screen_width / 2) + (app_width / 2)
        y = (screen_height / 2) + (app_height / 5)
        self.window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

        # crating a canvas
        bg = PhotoImage(file="background_img.png")
        self.canvas = Canvas(self.window, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=bg, anchor="nw")
        self.player_score_label = Label(text="0", fg="black", bg=THEME_COLOR)
        self.player_score_label.config(font=("Glacial Indifference", 28, 'bold'))
        self.player_score_label.place(x=310, y=26)
        self.game_score_label = Label(text="0", fg="black", bg=THEME_COLOR)
        self.game_score_label.config(font=("Glacial Indifference", 28, 'bold'))
        self.game_score_label.place(x=675, y=26)

        # generating cellular automata
        self.cellularautomata = CellularAutomata(self.window)
        self.resume_the_game()

        button_change = Button(self.window, text="Check the answer", command=self.check_answer)
        button_change.config(font=("Glacial Indifference", 15, 'bold'))
        button_change.config(width=20, height=1, bg='white')
        button_change.place(x=284, y=574)



        self.window.mainloop()

    def check_answer(self):
        #checking if answer is correct
        self.cellularautomata.next_step()
        self.update_scoreboard()
        self.who_won()
        if self.cellularautomata.should_continue():
            #creating new board if current board is empty
            self.cellularautomata = CellularAutomata(self.window)

    def who_won(self):
        if self.cellularautomata.player_score >= 10:
            print("You won!")
            self.resume_the_game()
        elif self.cellularautomata.game_score >= 10:
            print("You lost!")
            self.resume_the_game()

    def resume_the_game(self):
        self.cellularautomata.player_score = 0
        self.cellularautomata.game_score = 0
        with open("player_score.txt", "w") as player_score:
            player_score.write("0")
        with open("game_score.txt", "w") as game_score:
            game_score.write("0")

    def update_scoreboard(self):
        #updating the scoreboard
        self.player_score_label.configure(text=self.cellularautomata.player_score)
        self.game_score_label.configure(text=self.cellularautomata.game_score)
