import random
from itertools import chain
from hoverbutton import HoverButton
from threading import Timer, Lock

THEME_COLOR = "#F4C8AB"

class CellularAutomata():
    def __init__(self, window):
        # generating cellular automata
        self.controller = window
        with open("player_score.txt", "r") as player_score:
            self.player_score = int(player_score.read())
        with open("game_score.txt", "r") as game_score:
            self.game_score = int(game_score.read())
        self.current_cells = []
        self.correct_colors = []
        self.neighbours_numbers = []
        self.alive_neighbours = []
        self.initial_colors = []
        self.user_colors = []
        self.user_color_repetition = 0
        self.twice_before_user_input = []
        self.once_before_user_input = []
        self.create_starting_ca()
        self.controller.update()
        self.defining_neighbours()
        self.start_the_game()
        self.lock = Lock()
        self.second_click()


    def create_starting_ca(self):
        #creating the initial ca
        self.create_ca_list()

    def create_ca_list(self):
        #appending all ca (cellular automaton) objects (buttons) into one list
        iteration = 0
        for num in range(54):
            if num % 9 == 0 and num != 0:
                iteration += 1
            if num == 1:
                x_value = 59 + (num - 10 * iteration) * 76
            else:
                x_value = 59 + (num - 9 * iteration) * 76
            y_value = 89 + iteration * 76
            self.current_cells.append(self.create_one_ca(x_value, y_value, num))
        self.correct_colors = [self.current_cells[num]["background"] for num in range(54)]

    def create_one_ca(self, x_value, y_value, num):
        #creating one ca object
        concatenated = chain(range(12, 15), range(21, 24), range(30, 33))
        if num in concatenated:
            color = random.choice(["white", "black"])
            b = HoverButton(self.controller, button_number=num, width=10, height=5, bg=color, bd=4)
        else:
            b = HoverButton(self.controller, button_number=num, width=10, height=5, bg="white", bd=4)
        if num in range(45, 54):
            b["height"] = 4
        if num in [8, 17, 26, 35, 44, 53]:
            b["width"] = 9
        b.place(x=x_value, y=y_value)
        return b

    def defining_neighbours(self):
        #defining the neighbours of each ca and appending their numbers to the list neighbours_numbers
        for num in range(54):
            x_value = self.current_cells[num].winfo_rootx()
            y_value = self.current_cells[num].winfo_rooty()
            neighbours = []
            for i in [x for x in range(54) if x != num]:
                comparative_x_value = self.current_cells[i].winfo_rootx()
                comparative_y_value = self.current_cells[i].winfo_rooty()
                all_x_values = [comparative_x_value - 76, comparative_x_value, comparative_x_value + 76]
                all_y_values = [comparative_y_value - 76, comparative_y_value, comparative_y_value + 76]
                if x_value in all_x_values and y_value in all_y_values:
                    neighbours.append(i)
            self.neighbours_numbers.append(neighbours)

    def start_the_game(self):
        #counting how many alive (black) neighbours each ca has and appending that number to an alive_neighbours list
        self.alive_neighbours = []
        self.initial_colors = []
        for num in range(54):
            alive_neighbours = 0
            self.initial_colors.append(self.current_cells[num]["bg"])
            for i in range(len(self.neighbours_numbers[num])):
                neighbour_number = self.neighbours_numbers[num][i]
                bg_color = self.current_cells[neighbour_number]["bg"]
                if bg_color == "black":
                    alive_neighbours += 1
            self.alive_neighbours.append(alive_neighbours)

    def next_step(self):
        #showing the next time step
        self.correct_colors = []
        self.saving_user_input()
        self.update_cells_colors()

        for num in range(54):
            self.current_cells[num].config(text="")
            cell_color = self.current_cells[num]["bg"]
            alive_neighbours = self.alive_neighbours[num]
            #game of life rules
            if cell_color == "black" and alive_neighbours in [2, 3]:
                self.current_cells[num].config(bg="black")
            elif cell_color == "white" and alive_neighbours == 3:
                self.current_cells[num].config(bg="black")
                self.current_cells[num].defaultBackground = "black"
            else:
                self.current_cells[num].config(bg="white")
                if cell_color == "black":
                    self.current_cells[num].defaultBackground = "white"
            self.correct_colors.append(self.current_cells[num]["background"])
        # print(f"correct colors: {self.correct_colors}")
        self.check_answer()
        self.start_the_game()

    def saving_user_input(self):
        #saving users answer
        self.user_colors = []
        for num in range(54):
            self.user_colors.append(self.current_cells[num]["bg"])
        if self.user_color_repetition == 0:
            self.twice_before_user_input = self.user_colors
            self.user_color_repetition +=1
        elif self.user_color_repetition == 1:
            self.once_before_user_input = self.user_colors
            self.user_color_repetition += 1
        elif self.user_color_repetition == 2:
            self.twice_before_user_input = self.once_before_user_input
            self.once_before_user_input = self.user_colors
        # print(f"user colors: {self.user_colors}")

    def update_cells_colors(self):
        #changing the cells states (colours) to the initial ones
        for num in range(54):
            self.current_cells[num]["bg"] = self.initial_colors[num]
            self.current_cells[num].defaultBackground = self.initial_colors[num]

    def second_click(self):
        #checking amount of clicks to particular ca in order to prevent the colors from changing unexpectedly
        for num in range(54):
            cell_click_number = self.current_cells[num].click_number
            if cell_click_number == 1:
                self.current_cells[num].click_number = 0
        self.timer = Timer(0.01, self.second_click)
        self.timer.start()
        self.running = True

        #     self.run_event.clear()

    def check_answer(self):
        #comparing users answer (user_colors) to the correct answer (correct_colors) and giving points accordingly
        l1 = self.correct_colors
        l2 = self.user_colors
        if len(l1) == len(l2) and len(l1) == sum([1 for i, j in zip(l1, l2) if i == j]):
            self.player_score += 1
        else:
            self.game_score += 1

    def should_continue(self):
        if all(color == "white" for color in self.initial_colors):
            #saving current results in files
            with open("player_score.txt", "w") as player_score:
                player_score.write(str(self.player_score))
            with open("game_score.txt", "w") as game_score:
                game_score.write(str(self.game_score))
            return True
        elif self.user_color_repetition > 0:
            l1 = self.twice_before_user_input
            l2 = self.once_before_user_input
            if len(l1) == len(l2) and len(l1) == sum([1 for i, j in zip(l1, l2) if i == j]):
                return True


