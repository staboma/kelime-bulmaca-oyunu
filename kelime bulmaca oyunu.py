import random
import string
import tkinter as tk
from tkinter import messagebox

def create_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def place_word(grid, word):
    size = len(grid)
    word_len = len(word)
    
    placed = False
    while not placed:
        direction = random.choice(['horizontal', 'vertical', 'diagonal', 'horizontal_reverse', 'vertical_reverse', 'diagonal_reverse'])
        if direction == 'horizontal':
            row = random.randint(0, size - 1)
            col = random.randint(0, size - word_len)
            if all(grid[row][col + i] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row][col + i] = word[i]
                placed = True
        elif direction == 'vertical':
            row = random.randint(0, size - word_len)
            col = random.randint(0, size - 1)
            if all(grid[row + i][col] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row + i][col] = word[i]
                placed = True
        elif direction == 'diagonal':
            row = random.randint(0, size - word_len)
            col = random.randint(0, size - word_len)
            if all(grid[row + i][col + i] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row + i][col + i] = word[i]
                placed = True
        elif direction == 'horizontal_reverse':
            row = random.randint(0, size - 1)
            col = random.randint(word_len - 1, size - 1)
            if all(grid[row][col - i] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row][col - i] = word[i]
                placed = True
        elif direction == 'vertical_reverse':
            row = random.randint(word_len - 1, size - 1)
            col = random.randint(0, size - 1)
            if all(grid[row - i][col] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row - i][col] = word[i]
                placed = True
        elif direction == 'diagonal_reverse':
            row = random.randint(word_len - 1, size - 1)
            col = random.randint(word_len - 1, size - 1)
            if all(grid[row - i][col - i] in (' ', word[i]) for i in range(word_len)):
                for i in range(word_len):
                    grid[row - i][col - i] = word[i]
                placed = True

def fill_grid(grid):
    size = len(grid)
    for row in range(size):
        for col in range(size):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(string.ascii_uppercase)

def find_word(grid, word):
    size = len(grid)
    word_len = len(word)
    
    # Search in all directions
    directions = [
        (1, 0),  # down
        (-1, 0),  # up
        (0, 1),  # right
        (0, -1),  # left
        (1, 1),  # down-right diagonal
        (-1, -1),  # up-left diagonal
        (1, -1),  # down-left diagonal
        (-1, 1)   # up-right diagonal
    ]
    
    for row in range(size):
        for col in range(size):
            if grid[row][col] == word[0]:
                for direction in directions:
                    dx, dy = direction
                    if 0 <= row + (word_len - 1) * dx < size and 0 <= col + (word_len - 1) * dy < size:
                        if all(grid[row + i * dx][col + i * dy] == word[i] for i in range(word_len)):
                            return (row, col), (row + (word_len - 1) * dx, col + (word_len - 1) * dy)
    return None

def mark_word(grid, start, end, labels):
    x0, y0 = start
    x1, y1 = end
    dx = (x1 - x0) // max(abs(x1 - x0), 1)  # 0, 1 or -1
    dy = (y1 - y0) // max(abs(y1 - y0), 1)  # 0, 1 or -1
    x, y = x0, y0
    while (x, y) != (x1 + dx, y1 + dy):
        grid[x][y] = grid[x][y].lower()
        labels[x][y].config(bg='purple')
        x += dx
        y += dy

def start_game():
    global grid, words, size, labels
    grid = create_grid(size)
    for word in words:
        place_word(grid, word)
    fill_grid(grid)
    display_grid()

def display_grid():
    for widget in frame.winfo_children():
        widget.destroy()
    global labels
    labels = []
    for row in range(size):
        label_row = []
        for col in range(size):
            lbl = tk.Label(frame, text=grid[row][col], width=2, height=1, borderwidth=2, relief="solid", font=("Arial", 14), bg='gray')
            lbl.grid(row=row, column=col, padx=5, pady=5)
            label_row.append(lbl)
        labels.append(label_row)

def check_word():
    word = word_entry.get().upper()
    if word in words:
        position = find_word(grid, word)
        if position:
            mark_word(grid, position[0], position[1], labels)
            messagebox.showinfo("Tebrikler!", f"'{word}' kelimesini doğru buldunuz.")
            words.remove(word)
        else:
            messagebox.showerror("Hata", f"'{word}' kelimesini bulamadınız.")
    else:
        messagebox.showerror("Hata", f"'{word}' listede yok.")

# Kelime listesi
words = ["PYTHON", "KOD", "BULMACA", "PROGRAM", "YAZILIM", "ALGORITMA", "VERITABANI", "FONKSIYON", "NESNE", "SINIF"]
size = 15
grid = []
labels = []

# Tkinter arayüzü oluşturma
root = tk.Tk()
root.title("Kelime Bulmaca Oyunu")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

word_entry = tk.Entry(root, font=("Arial", 14))
word_entry.pack(pady=10)

check_button = tk.Button(root, text="Kelimeyi Kontrol Et", command=check_word, font=("Arial", 14))
check_button.pack(pady=10)

start_button = tk.Button(root, text="Oyunu Başlat", command=start_game, font=("Arial", 14))
start_button.pack(pady=10)

root.mainloop()
