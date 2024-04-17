import tkinter as tk
import random

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CELL_SIZE = 20
DELAY = 100

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        
        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
        self.canvas.pack()
        
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.game_over = False
        
        self.bind_keys()
        self.create_buttons()
        self.update()
    
    def bind_keys(self):
        self.master.bind("<KeyPress-Up>", self.go_up)
        self.master.bind("<KeyPress-Down>", self.go_down)
        self.master.bind("<KeyPress-Left>", self.go_left)
        self.master.bind("<KeyPress-Right>", self.go_right)
    
    def create_buttons(self):
        self.play_button = tk.Button(self.master, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT)
        
        self.continue_button = tk.Button(self.master, text="Continue", command=self.continue_game, state=tk.DISABLED)
        self.continue_button.pack(side=tk.LEFT)
        
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, state=tk.DISABLED)
        self.new_game_button.pack(side=tk.LEFT)
        
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack(side=tk.LEFT)
    
    def play(self):
        self.play_button.config(state=tk.DISABLED)
        self.continue_button.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.NORMAL)
        self.game_over = False
        self.update()
    
    def continue_game(self):
        if self.game_over:
            self.play()
    
    def new_game(self):
        self.play()
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.canvas.delete("food")
        self.canvas.delete("snake")
    
    def create_food(self):
        while True:
            x = random.randint(0, (CANVAS_WIDTH-CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (CANVAS_HEIGHT-CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in self.snake:
                return x, y
    
    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill='green', tags="snake")
    
    def draw_food(self):
        x, y = self.food
        self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill='red', tags="food")
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == "Up":
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + CELL_SIZE, head_y)
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()
    
    def check_collision(self):
        head_x, head_y = self.snake[0]
        
        if (
            head_x < 0 or
            head_x >= CANVAS_WIDTH or
            head_y < 0 or
            head_y >= CANVAS_HEIGHT or
            (head_x, head_y) in self.snake[1:]
        ):
            return True
        return False
    
    def update(self):
        if not self.game_over:
            self.move_snake()
            if self.check_collision():
                self.game_over = True
                self.game_over_text()
            else:
                self.canvas.delete("food")
                self.draw_food()
                self.draw_snake()
                self.master.after(DELAY, self.update)
    
    def game_over_text(self):
        self.canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, text=f"Game Over! Score: {self.score}", fill="white", font=("Helvetica", 20))
        self.play_button.config(state=tk.NORMAL)
        self.continue_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)

    def go_up(self, event):
        if self.direction != "Down":
            self.direction = "Up"

    def go_down(self, event):
        if self.direction != "Up":
            self.direction = "Down"

    def go_left(self, event):
        if self.direction != "Right":
            self.direction = "Left"

    def go_right(self, event):
        if self.direction != "Left":
            self.direction = "Right"

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
