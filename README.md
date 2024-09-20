# Pokémon Card Matching Game

This is a Pokémon card matching game built with Python and Tkinter. The game fetches Pokémon data from the PokéAPI and displays a grid of cards. The objective is to match pairs of Pokémon cards.

## Features

- Three difficulty levels: Easy (4x4), Medium (6x6), and Hard (8x8)
- Fetches random Pokémon data from the PokéAPI
- Displays Pokémon images and plays their cries when cards are clicked
- Tracks the number of tries and ends the game when the maximum number of tries is reached

## Requirements

- Python 3.x
- `requests` library
- `Pillow` library

## Installation

### Step 1: Clone the Repository

```sh
git clone https://github.com/yourusername/pokemon-card-matching-game.git
cd pokemon-card-matching-game
```

### Step 2: 

Set Up a Virtual Environment

Create a virtual environment to manage dependencies:

```sh
python3 -m venv env
```

Activate the virtual environment:

On macOS and Linux:

```sh
source env/bin/activate
```

On Windows:

```sh
.\env\Scripts\activate
```

### Step 3: Install Dependencies


Install the required libraries:

```sh
pip install -r requirements.txt
```

### Step 4: Run the Program
Run the game:

```sh
python card_matching_game.py
```

### PokéAPI

This program uses the PokéAPI to fetch Pokémon data, including images and cries. The PokéAPI is a free and open API that provides information about Pokémon.