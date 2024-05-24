import pygame
import sys


class Game:
	"""Class to handle the setup and display of the Sudoku game using Pygame."""

	def __init__(self, width=600, height=700, name='Sudoku Solver'):
		"""
        Initialize the game with the given width, height, and window name.

        Parameters:
            width (int): Width of the game window.
            height (int): Height of the game window.
            name (str): Title of the game window.
        """
		self.width = width
		self.height = height
		self.name = name
		self.screen = None
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.grey = (200, 200, 200)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)
		self.font = None

	def set_up(self):
		"""Initialize Pygame and set up the game window."""
		pygame.init()
		pygame.font.init()  # Initialize the font module
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.name)
		self.font = pygame.font.SysFont('comicsans', 40)  # Initialize font after Pygame is initialized

	def print_sudoku(self, board, selected=None, incorrect=None):
		"""
        Render the Sudoku board on the screen.

        Parameters:
            board (list): 2D list representing the Sudoku board.
            selected (tuple): Coordinates of the selected cell.
            incorrect (list): List of incorrect cell coordinates.
        """
		self.screen.fill(self.white)
		gap = self.width // 9

		for i in range(10):
			thickness = 4 if i % 3 == 0 else 1
			pygame.draw.line(self.screen, self.black, (i * gap, 0), (i * gap, self.height - 100), thickness)
			pygame.draw.line(self.screen, self.black, (0, i * gap), (self.width, i * gap), thickness)

		for i in range(9):
			for j in range(9):
				if board[i][j] != 0:
					color = self.red if incorrect and (i, j) in incorrect else self.black
					text = self.font.render(str(board[i][j]), True, color)
					self.screen.blit(text, (j * gap + 20, i * gap + 10))

		if selected:
			row, col = selected
			pygame.draw.rect(self.screen, self.grey, (col * gap, row * gap, gap, gap), 3)

		# Draw Solve Button
		pygame.draw.rect(self.screen, self.green, (50, self.height - 80, 200, 50))
		solve_text = self.font.render('Solve', True, self.black)
		self.screen.blit(solve_text, (90, self.height - 70))

		# Draw Start Again Button
		pygame.draw.rect(self.screen, self.green, (350, self.height - 80, 200, 50))
		restart_text = self.font.render('Start Again', True, self.black)
		self.screen.blit(restart_text, (360, self.height - 70))

		pygame.display.update()

	def close(self):
		"""Close the Pygame window and quit the game."""
		pygame.quit()
		sys.exit()


class Sudoku:
	"""Class to handle Sudoku game logic."""

	def __init__(self, sudoku):
		"""
        Initialize the Sudoku board and store the initial state.

        Parameters:
            sudoku (list): 2D list representing the initial Sudoku board.
        """
		self.rows = 9
		self.columns = 9
		self.sudoku = sudoku
		self.initial = [row[:] for row in sudoku]  # Deep copy of the initial board

	def find_empty(self):
		"""
        Find an empty cell in the Sudoku board.

        Returns:
            tuple: Coordinates of the empty cell or None if no empty cells are found.
        """
		for i in range(self.rows):
			for j in range(self.columns):
				if self.sudoku[i][j] == 0:
					return i, j
		return None

	def is_valid(self, num, pos):
		"""
        Check if a number can be placed in the given position.

        Parameters:
            num (int): The number to be placed.
            pos (tuple): The position (row, col) to place the number.

        Returns:
            bool: True if the number can be placed, False otherwise.
        """
		for j in range(self.columns):
			if self.sudoku[pos[0]][j] == num and pos[1] != j:
				return False
		for i in range(self.rows):
			if self.sudoku[i][pos[1]] == num and pos[0] != i:
				return False
		box_x = pos[1] // 3
		box_y = pos[0] // 3
		for i in range(box_y * 3, box_y * 3 + 3):
			for j in range(box_x * 3, box_x * 3 + 3):
				if self.sudoku[i][j] == num and (i, j) != pos:
					return False
		return True

	def solve_sudoku(self):
		"""
        Solve the Sudoku puzzle using a backtracking algorithm.

        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
		empty = self.find_empty()
		if not empty:
			return True
		else:
			row, col = empty
		for num in range(1, 10):
			if self.is_valid(num, (row, col)):
				self.sudoku[row][col] = num
				if self.solve_sudoku():
					return True
				self.sudoku[row][col] = 0
		return False

	def reset(self):
		"""Reset the Sudoku board to its initial state."""
		self.sudoku = [row[:] for row in self.initial]  # Reset to the initial board


if __name__ == "__main__":
	initial_board = [
		[5, 3, 0, 0, 7, 0, 0, 0, 0],
		[6, 0, 0, 1, 9, 5, 0, 0, 0],
		[0, 9, 8, 0, 0, 0, 0, 6, 0],
		[8, 0, 0, 0, 6, 0, 0, 0, 3],
		[4, 0, 0, 8, 0, 3, 0, 0, 1],
		[7, 0, 0, 0, 2, 0, 0, 0, 6],
		[0, 6, 0, 0, 0, 0, 2, 8, 0],
		[0, 0, 0, 4, 1, 9, 0, 0, 5],
		[0, 0, 0, 0, 8, 0, 0, 7, 9]
	]

	game = Game()
	game.set_up()
	sudoku = Sudoku(initial_board)
	running = True
	selected = None
	incorrect = []
	solved = False

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				gap = game.width // 9
				if 50 <= pos[0] <= 250 and game.height - 80 <= pos[1] <= game.height - 30:
					incorrect.clear()
					solved = sudoku.solve_sudoku()
				elif 350 <= pos[0] <= 550 and game.height - 80 <= pos[1] <= game.height - 30:
					sudoku.reset()
					incorrect = []
					solved = False
				else:
					if pos[1] < game.height - 100:
						x, y = pos[1] // gap, pos[0] // gap
						selected = (x, y)
			if event.type == pygame.KEYDOWN:
				if selected and event.unicode.isdigit():
					num = int(event.unicode)
					row, col = selected
					sudoku.sudoku[row][col] = num
					if not sudoku.is_valid(num, (row, col)):
						incorrect.append((row, col))
					else:
						if (row, col) in incorrect:
							incorrect.remove((row, col))

		game.print_sudoku(sudoku.sudoku, selected, incorrect)

	game.close()