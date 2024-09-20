import tkinter as tk
import random
import requests
from io import BytesIO
from PIL import Image, ImageTk

imgWidth = 9
imgRatio = 0.75

class CardMatchingGame:
    def __init__(self, root, rows=4, cols=4, max_tries=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.max_tries = max_tries
        self.tries = 0
        self.pokemon_data = self.fetch_pokemon_data(rows * cols // 2)
        self.grid = self.create_grid(rows, cols)
        self.revealed = [[False] * cols for _ in range(rows)]
        self.buttons = [[None] * cols for _ in range(rows)]
        self.first_selection = None
        self.input_blocked = False
        self.pairs_found = 0
        self.total_pairs = rows * cols // 2
        self.tries_label = None
        self.create_ui()

    def fetch_pokemon_data(self, count):
        pokemon_data = []
        random_indexes = random.sample(range(1, 152), count)  # Generate random indexes between 1 and 151
        for i in random_indexes:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
            data = response.json()
            image_url = data['sprites']['front_default']
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            image = image.resize((imgWidth * 10, imgWidth * 10), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            pokemon_data.append((data['name'], photo))
        return pokemon_data

    def create_grid(self, rows, cols):
        cards = self.pokemon_data * 2
        random.shuffle(cards)
        return [cards[i * cols:(i + 1) * cols] for i in range(rows)]

    def create_ui(self):
        self.tries_label = tk.Label(self.root, text=f"Lives: {self.max_tries - self.tries}")
        self.tries_label.grid(row=0, column=0, columnspan=self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                button = tk.Button(self.root, text="*", width=imgWidth, height=int(imgWidth*imgRatio),
                                   command=lambda i=i, j=j: self.on_card_click(i, j))
                button.grid(row=i+1, column=j, padx=5, pady=5)
                self.buttons[i][j] = button
        self.update_tries_label()

    def update_tries_label(self):
        self.tries_label.config(text=f"Lives: {self.max_tries - self.tries}")

    def on_card_click(self, i, j):
        if self.input_blocked:
            return
        if self.revealed[i][j]:
            return

        self.revealed[i][j] = True
        _, image = self.grid[i][j]
        self.buttons[i][j].config(image=image, text="", compound=tk.TOP, width=image.width(), height=image.height())

        if self.first_selection is None:
            self.first_selection = (i, j)
        else:
            x1, y1 = self.first_selection
            x2, y2 = i, j
            if self.grid[x1][y1][0] == self.grid[x2][y2][0]:
                self.pairs_found += 1
                if self.pairs_found == self.total_pairs:
                    self.show_game_over("Congratulations! You've found all pairs!")
            else:
                self.input_blocked = True
                self.root.after(1000, self.hide_cards, x1, y1, x2, y2)
                self.root.after(1000, self.enable_input)
                self.tries += 1
                self.update_tries_label()
                if self.tries >= self.max_tries:
                    self.show_game_over("Game over! You've reached the maximum number of tries.")
            self.first_selection = None

    def hide_cards(self, x1, y1, x2, y2):
        self.revealed[x1][y1] = False
        self.revealed[x2][y2] = False
        self.buttons[x1][y1].config(image='', text="*", width=imgWidth, height=int(imgWidth*imgRatio))
        self.buttons[x2][y2].config(image='', text="*", width=imgWidth, height=int(imgWidth*imgRatio))

    def show_game_over(self, message):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)
        tk.Label(self.root, text=message).grid(row=self.rows + 1, column=0, columnspan=self.cols)
    
    def enable_input(self):
        self.input_blocked = False

def select_difficulty():
    grid_size = None  # Declare grid_size as a local variable

    def set_difficulty(size):
        nonlocal grid_size
        grid_size = size
        difficulty_window.destroy()

    difficulty_window = tk.Tk()
    difficulty_window.title("Select Difficulty")

    tk.Button(difficulty_window, text="Easy (3x3)", command=lambda: set_difficulty(3)).pack(pady=10)
    tk.Button(difficulty_window, text="Medium (4x4)", command=lambda: set_difficulty(4)).pack(pady=10)
    tk.Button(difficulty_window, text="Hard (5x5)", command=lambda: set_difficulty(5)).pack(pady=10)

    difficulty_window.mainloop()

    return grid_size

if __name__ == "__main__":
    grid_size = select_difficulty()
    if grid_size:
        root = tk.Tk()
        root.title("Pokémon Card Matching Game")
        button_width = imgWidth * 10 + 10  # Button width including padding
        button_height = int(imgWidth * imgRatio * 10) + 10  # Button height including padding
        window_width = (grid_size + 2) * button_width
        window_height = (grid_size + 2) * button_height + 50  # Additional space for the tries label
        root.geometry(f"{window_width}x{window_height}")  # Adjust the window size
        game = CardMatchingGame(root, rows=grid_size, cols=grid_size)
        root.mainloop()