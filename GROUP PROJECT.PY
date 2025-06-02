import tkinter as tk
import numpy as np
import random
import time

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sorting Game")
        self.root.geometry("400x200")

        tk.Label(root, text="Enter Your Name:", font=("Arial", 14)).pack(pady=10)
        self.name_entry = tk.Entry(root, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        self.error_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.error_label.pack()

        tk.Button(root, text="Start Game", font=("Arial", 14), command=self.start_game).pack(pady=20)

    def start_game(self):
        username = self.name_entry.get().strip()
        if username:
            self.root.destroy()
            main_game(username)
        else:
            self.error_label.config(text="Please enter your name.")

class SortingGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.level = 1
        self.score = 0
        self.num_count = 4
        self.start_time = time.time()
        self.labels = []
        self.max_levels = 5
        self.shown_hint = False

        self.root.title("Sorting Game with Bubble Sort")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        self.title_label = tk.Label(root, text=f"Welcome, {self.username}! Bubble Sort Game", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        self.info_label = tk.Label(root, text="", font=("Arial", 14))
        self.info_label.pack()

        self.hint_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.hint_label.pack()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=30)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.check_btn = tk.Button(self.button_frame, text="Check Order", font=("Arial", 12), command=self.check_order)
        self.check_btn.grid(row=0, column=0, padx=5)

        self.reshuffle_btn = tk.Button(self.button_frame, text="Reshuffle", font=("Arial", 12), command=self.reshuffle)
        self.reshuffle_btn.grid(row=0, column=1, padx=5)

        self.autoshuffle_btn = tk.Button(self.button_frame, text="Auto Shuffle", font=("Arial", 12), command=self.auto_shuffle)
        self.autoshuffle_btn.grid(row=0, column=2, padx=5)

        self.min_btn = tk.Button(self.button_frame, text="Minimize Numbers", font=("Arial", 12), command=self.decrease_numbers)
        self.min_btn.grid(row=0, column=3, padx=5)

        self.max_btn = tk.Button(self.button_frame, text="Maximize Numbers", font=("Arial", 12), command=self.increase_numbers)
        self.max_btn.grid(row=0, column=4, padx=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack()

        self.next_btn = tk.Button(root, text="Next Level", font=("Arial", 12), command=self.next_level, state=tk.DISABLED)
        self.next_btn.pack(pady=10)

        self.generate_numbers()

    def generate_numbers(self):
        for lbl in self.labels:
            lbl.destroy()
        self.labels.clear()

        self.num_count = max(3, min(self.num_count, 10))
        self.numbers = np.array(random.sample(range(1, 99), self.num_count))

        x_offset = 50
        for i, num in enumerate(self.numbers):
            lbl = DraggableLabel(self.root, text=str(num), index=i)
            lbl.place(x=x_offset, y=150)
            self.labels.append(lbl)
            x_offset += 650 // self.num_count

        self.info_label.config(text=f"Level {self.level} | Sort the numbers! ({self.num_count} numbers)", fg="black")
        self.result_label.config(text="")
        self.next_btn.config(state=tk.DISABLED)

        if not self.shown_hint:
            self.hint_label.config(text="Hint: Drag and drop the numbers to sort them.")
            self.shown_hint = True
        else:
            self.hint_label.config(text="")

    def reshuffle(self):
        random.shuffle(self.numbers)
        self.generate_numbers()

    def auto_shuffle(self):
        # Arrange descending numbers left-to-right (ascending visual)
        descending_order = sorted(self.labels, key=lambda lbl: int(lbl.cget("text")), reverse=True)
        sorted_labels = sorted(descending_order, key=lambda lbl: int(lbl.cget("text")))

        x_offset = 50
        spacing = 650 // len(sorted_labels)
        for lbl in sorted_labels:
            lbl.place(x=x_offset, y=150)
            x_offset += spacing

    def increase_numbers(self):
        self.num_count += 1
        self.generate_numbers()

        sorted_labels = sorted(self.labels, key=lambda lbl: int(lbl.cget("text")), reverse=True)
        x_offset = 50
        spacing = 650 // len(sorted_labels)
        for lbl in sorted_labels:
            lbl.place(x=x_offset, y=150)
            x_offset += spacing

    def decrease_numbers(self):
        if self.num_count > 3:
            self.num_count -= 1
            self.generate_numbers()

            sorted_labels = sorted(self.labels, key=lambda lbl: int(lbl.cget("text")))
            x_offset = 50
            spacing = 650 // len(sorted_labels)
            for lbl in sorted_labels:
                lbl.place(x=x_offset, y=150)
                x_offset += spacing

    def bubble_sort(self, arr):
        sorted_arr = arr.copy()
        n = len(sorted_arr)
        for i in range(n):
            for j in range(n - i - 1):
                if sorted_arr[j] > sorted_arr[j + 1]:
                    sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
        return sorted_arr

    def check_order(self):
        user_order = np.array([int(lbl.cget("text")) for lbl in sorted(self.labels, key=lambda l: l.winfo_x())])
        correct_order = self.bubble_sort(self.numbers)

        correct = np.array_equal(user_order, correct_order)

        for i, lbl in enumerate(sorted(self.labels, key=lambda l: l.winfo_x())):
            lbl.configure(bg="lightgreen" if user_order[i] == correct_order[i] else "salmon")

        if correct:
            elapsed = int(time.time() - self.start_time)
            points = max(100 - elapsed * 5, 10)
            self.score += points
            self.result_label.config(text=f"Correct! +{points} points", fg="green")
            self.next_btn.config(state=tk.NORMAL)
        else:
            self.result_label.config(text="Incorrect! Try again!", fg="red")

    def next_level(self):
        self.level += 1
        self.start_time = time.time()

        if self.level > self.max_levels:
            self.info_label.config(text=f"Game Over, {self.username}! Total Score: {self.score}", fg="blue")
            self.check_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
            self.reshuffle_btn.config(state=tk.DISABLED)
            self.autoshuffle_btn.config(state=tk.DISABLED)
            self.min_btn.config(state=tk.DISABLED)
            self.max_btn.config(state=tk.DISABLED)
        else:
            self.generate_numbers()

class DraggableLabel(tk.Label):
    def __init__(self, master, text, index, **kwargs):
        super().__init__(master, text=text, bg="lightblue", width=5, font=("Arial", 16), **kwargs)
        self.index = index
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.lift()
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_start_x + event.x
        y = self.winfo_y() - self._drag_start_y + event.y
        self.place(x=x, y=y)

def main_game(username):
    root = tk.Tk()
    SortingGame(root, username)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginPage(login_root)
    login_root.mainloop()
