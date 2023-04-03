"""
FIT1053: Sem 1 2023 Assignment 1 (Solution Copy)
Authors: David Le, Randil Hettiarachchi, Rathan Murugesan Senthil, Henry Wang
Description: connectk Task
Last updated: 02/04/2023
"""
from collections import Counter
import os
import random

game_parameters = {}
players = [] # list of tuples, where each tuple = (type of player, player number)

def define_parameters():
	"""
	Asks the users to define how big the board is and how many tokens in a row to win.

	:return: The list of available columns for players to input when playing.
	"""
	game_parameters["rows"] = int(input("How many rows (must be >0)? "))
	while game_parameters["rows"] <= 0:
		print("Invalid input, please try again.")
		game_parameters["rows"] = int(input("How many rows (must be >0)? "))

	game_parameters["columns"] = int(input("How many columns (must be >0)? "))
	while game_parameters["columns"] <= 0:
		print("Invalid input, please try again.")
		game_parameters["columns"] = int(input("How many columns (must be >0)? "))

	max_k = max(game_parameters.values())
	
	game_parameters["tokens"] = int(input("How many tokens in a row to win (must be >0)? "))
	while game_parameters["tokens"] > max_k:
		print("Invalid input, please try again.")
		game_parameters["tokens"] = int(input("How many tokens in a row to win (must be >0)? "))

	clear_screen()
	main()

def clear_screen():
	"""
	Clears the terminal for Windows and Linux/MacOS.

	:return: None
	"""
	import os
	os.system('cls' if os.name == 'nt' else 'clear')

def validate_input(prompt, valid_inputs):
	"""
	Repeatedly ask user for input until they enter an input
	within a set valid of options.

	:param prompt: The prompt to display to the user, string.
	:param valid_inputs: The range of values to accept, list
	:return: The user's input, string.
	"""
	input_option = input(prompt)
	# Loops until it the input is valid
	while input_option not in valid_inputs:
		print("Invalid input, please try again.")
		input_option = input(prompt)
	return input_option

def create_board():
	"""
	Returns a 2D list of x rows and y columns to represent
	the game board. Default cell value is 0.

	:return: A 2D list of rowsXcolumns dimensions.
	"""
	return [[0 for i in range(game_parameters["columns"])] for j in range(game_parameters["rows"])]

def print_board(board):
	"""
	Prints the game board to the console.

	:param board: The game board, 2D list of rowsXcolumns dimensions.
	:return: None
	"""
	print(((game_parameters["columns"] - 2) * 2 - 1) * "=" + " Connect" + str(game_parameters["tokens"]) + " " + ((game_parameters["columns"] - 2) * 2 - 1) * "=")
	print("Player 1: X       Player 2: O")
	print("All other players: go by number.")
	print("")
	print("  ",end="")
	for i in range(1, game_parameters["columns"]):
		print(str(i) + "   ",end="")
	print(str(game_parameters["columns"]))

	for row in range(game_parameters["rows"]):
		print(" ---" * game_parameters["columns"])
		for column in range(game_parameters["columns"]):
			if board[row][column] == 0:
				print("|   ",end="")
			elif board[row][column] == 1:
				print("| X ",end="")
			elif board[row][column] == 2:
				print("| O ",end="")
			else:
				print("| " + str(board[row][column]) + " ",end="")
		print("|")
	print(" ---" * game_parameters["columns"])
	print("====" * game_parameters["columns"],end="")
	print("=")

def define_players():
	"""
	Asks the users to set how many players there are. User can determine how many human and CPU players there are. User can also choose CPU difficulty.

	:return: None
	"""
	# Ensures there are at least 2 players
	humans = int(input("How many humans are playing? "))
	cpus = int(input("How many CPUs are playing? "))
	while humans + cpus < 2:
		print("Invalid input, please try again.")
		humans = int(input("How many humans are playing? "))
		cpus = int(input("How many CPUs are playing? "))

	cpu_difficulties = []
	for i in range(cpus):
		difficulty = validate_input("What difficulty should bot " + str((i + 1)) + " be (easy/medium/hard)? ", ["easy", "medium", "hard"])
		cpu_difficulties.append(difficulty)

	for i in range(humans):
		players.append(("human", i + 1))
	for i in range(cpus):
		players.append((cpu_difficulties[i], humans + i + 1))

def drop_piece(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of rowsXcolumns dimensions.
	:param player: The player dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	if board[0][column - 1] == 0:
		for row in range(game_parameters["rows"] - 1, -1, -1):
			if board[row][column - 1] == 0:
				board[row][column - 1] = player
				return True
	else:
		return False

def execute_player_turn(player, board):
	"""
	Prompts user for a legal move given the current game board
	and executes the move.

	:return: Column that the piece was dropped into, int.
	"""
	# Checks if it is valid BEFORE it is converted into integer
	available_columns = [str(i + 1) for i in range(game_parameters["columns"])]
	column = int(validate_input("Player " + str(player) + ", please enter the column you would like to drop your piece into: ", available_columns))
	
	while drop_piece(board, player, column) == False:
		print("That column is full, please try again.")
		column = int(validate_input("Player " + str(player) + ", please enter the column you would like to drop your piece into: ", available_columns))
	return column

def horizontal_check(board, row, column):
	"""
	Checks if there is 4 in a row horizontally. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if column <= game_parameters["columns"] - game_parameters["tokens"]:
		window = [board[row][column + i] for i in range(game_parameters["tokens"])]
		return window
	return False

def vertical_check(board, row, column):
	"""
	Checks if there is 4 in a row vertically. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= game_parameters["tokens"] - 1:
		window = [board[row - i][column] for i in range(game_parameters["tokens"])]
		return window
	return False

def positive_diagonal_check(board, row, column):
	"""
	Checks if there is 4 in a row diagonally (bottom left to top right). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= (game_parameters["tokens"] - 1) and column <= (game_parameters["columns"] - game_parameters["tokens"]):
		window = [board[row - i][column + i] for i in range(game_parameters["tokens"])]
		return window
	return False

def negative_diagonal_check(board, row, column):
	"""
	Checks if there is 4 in a row diagonally (bottom right to top left). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns dimensions
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= (game_parameters["tokens"] - 1) and column >= (game_parameters["tokens"] - 1):
		window = [board[row - i][column - i] for i in range(game_parameters["tokens"])]
		return window
	return False

def end_of_game(board):
	"""
	Checks if the game has ended with a winne or a draw.

	It will check a cell, then all possible horizontal/vertical/diagonal rows stemming from the cell.

	:param board: The game board, 2D list of rowsXcolumns dimensions
	:return: -1 if draw, 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, x if player x wins
	"""
	for row in range(len(board) - 1, -1, -1):
		for column in range(game_parameters["columns"]):
			horizontal_window = horizontal_check(board, row, column)
			vertical_window = vertical_check(board, row, column)
			positive_diagonal_window = positive_diagonal_check(board, row, column)
			negative_diagonal_window = negative_diagonal_check(board, row, column)
			
			for player in players:
				# Makes sure the x_window list exists (preventing AttributeError for .count())
				if (horizontal_window != False and horizontal_window.count(player[1]) == game_parameters["tokens"]) or (vertical_window != False and vertical_window.count(player[1]) == game_parameters["tokens"]) or (positive_diagonal_window != False and positive_diagonal_window.count(player[1]) == game_parameters["tokens"]) or (negative_diagonal_window != False and negative_diagonal_window.count(player[1]) == game_parameters["tokens"]):
					return player[1]
	
	# Distinguishes between a draw and the game not being over
	for row in board:
		for column in row:
			if column == 0:
				return 0
	return -1

def start_game():
	"""
	Runs a game of any amount of players and/or CPUs.

	:return: None
	"""
	board = create_board()
	current_player = 1

	while end_of_game(board) == 0:
		clear_screen()
		print_board(board)

		if players[current_player - 1][0] == "easy":
			cpu_player_easy(board, current_player)
		elif players[current_player - 1][0] == "medium":
			cpu_player_medium(board, current_player)
		elif players[current_player - 1][0] == "hard":
			cpu_player_medium(board, current_player)
		else:
			execute_player_turn(current_player, board)
		
		if current_player != len(players):
			current_player += 1
		else:
			current_player = 1

	clear_screen()
	print_board(board)

	for player in players:
		if end_of_game(board) == player[1]:
			print("Player " + str(player[1]) + " has won!")

	if end_of_game(board) == -1:
		print("There was a tie! No winner!")

def main():
	"""
	Defines the main application loop.
	User chooses a type of game to play or to exit.

	:return: None
	"""
	if game_parameters == {}:
		define_parameters()
	else:
		print("=============== Main Menu ===============")
		print("Welcome to Connect " + str(game_parameters["tokens"]) + "!")
		print("1. View Rules")
		print("2. Configure game")
		print("3. Play!")
		print("4. Exit")
		print("=========================================")

		start_option = validate_input("Choose your option: ", ["1", "2", "3", "4"])
		while start_option != "4":
			if start_option == "1":
				clear_screen()
				print_rules()
				break
			elif start_option == "2":
				define_parameters()
				break
			elif start_option == "3":
				clear_screen()
				define_players()
				clear_screen()
				start_game()
				break

def print_rules():
	"""
	Prints the rules of the game.

	:return: None
	"""
	print("================= Rules =================")
	print("Connect " + str(game_parameters["tokens"]) + " is a game where the")
	print("objective is to get " + str(game_parameters["tokens"]) + " of your pieces")
	print("in a row either horizontally, vertically")
	print("or diagonally. The game is played on a")
	print(str(game_parameters["rows"]) + "x" + str(game_parameters["columns"]) + " grid. The first player to get " + str(game_parameters["tokens"]))
	print("pieces in a row wins the game. If the")
	print("grid is filled and no player has won,")
	print("the game is a draw.")
	print("=========================================")

def cpu_player_easy(board, player):
	"""
	Executes a move for the CPU on easy difficulty. This function 
	plays a randomly selected column.

	:param board: The game board, 2D list of rowsXcolumns dimensions.
	:param player: The player whose turn it is, any positive integer value.
	:return: Column that the piece was dropped into, int.
	"""
	available_columns = []

	# Checks for valid columns that can be dropped in
	for i in range(len(board[0])):
		if (board[0][i] == 0):
			available_columns.append(i)
			
	column = random.choice(available_columns)
	drop_piece(board, player, column + 1)
	return column + 1

def drop_piece_cpu(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: The new possible board
	"""
	if board[0][column - 1] == 0:
		for row in range(game_parameters["rows"] - 1, -1, -1):
			if board[row][column - 1] == 0:
				board[row][column - 1] = player
				break
		return board


def cpu_player_medium(board, player):
	block = None
	for column in range(game_parameters['columns']):
		if (board[0][column] == 0):
			# player1 used just to differentiate it from the parameter
			for player1 in players:
				board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
				possible_player_move = drop_piece_cpu(board_copy, player1[1], column + 1) 

				result = end_of_game(possible_player_move)
				if (result == player): 	
					drop_piece(board, player, column + 1)
					return column + 1 
				elif (result == player1[1]):
					block = column + 1


	if (block != None):
		drop_piece(board, player, block)    
		return block
	return cpu_player_easy(board, player)

def calc_score(cpu, window):
	'''
	Calculates the score for a given window

	:param cpu: The cpu player. 
	:param window: 
	:return: The score of the current window
	'''
	counts = Counter(window)

	score = 0

	if (counts[cpu] == game_parameters['tokens']):
		score += (10) ** 6

	elif (counts['0'] == len(window) - counts[cpu]):
		score +=  counts[cpu] ** 2
	else:
		score += counts[cpu]

	for key in counts.keys():
		if (key != str(cpu) and key != '0'):
			if (counts[key] == game_parameters['tokens']):
				score += -((10) ** 5)  
			elif (counts['0'] == game_parameters['tokens'] - counts[key]):
				score +=  -(counts[key] ** 2)
                
	return score

def horizontal_check_cpu(board, row, column, cpu):
	"""
	Checks if there is 4 in a row horizontally. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: A score rating the window
	"""
	if column <= game_parameters["columns"] - game_parameters["tokens"]:
		window = [board[row][column + i] for i in range(game_parameters["tokens"])]
		return calc_score(cpu, window)
	return 0

def vertical_check_cpu(board, row, column, cpu):
	"""
	Checks if there is 4 in a row vertically. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: A score rating the window
	"""
	if row >= game_parameters["tokens"] - 1:
		window = [board[row - i][column] for i in range(game_parameters["tokens"])]
		return calc_score(cpu, window)
	return 0

def positive_diagonal_check_cpu(board, row, column, cpu):
	"""
	Checks if there is 4 in a row diagonally (bottom left to top right). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: A score rating the window
	"""
	if row >= (game_parameters["tokens"] - 1) and column <= (game_parameters["columns"] - game_parameters["tokens"]):
		window = [board[row - i][column + i] for i in range(game_parameters["tokens"])]
		return calc_score(cpu, window)
	return 0

def negative_diagonal_check_cpu(board, row, column, cpu) :
	"""
	Checks if there is 4 in a row diagonally (bottom right to top left). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of rowsXcolumns dimensions
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: A score rating the window
	"""
	if row >= (game_parameters["tokens"] - 1) and column >= (game_parameters["tokens"] - 1):
		window = [board[row - i][column - i] for i in range(game_parameters["tokens"])]
		return calc_score(cpu, window)
	return 0


def score_board(board, cpu):
	"""
	Scores the current board state

	:param board: The board that is to be scored
	:param cpu: The cpu player
	:return: The score of the current board state.
	"""
	score = 0

	for row in range(game_parameters['rows'] - 1, -1, -1):
		for column in range(game_parameters['columns']):
			if (board[row][column] == 0):
				continue
			score += horizontal_check_cpu(board, row, column, cpu)
			score += vertical_check_cpu(board, row, column, cpu)
			score += positive_diagonal_check_cpu(board, row, column, cpu)
			score += negative_diagonal_check_cpu(board, row, column, cpu)	
	return score
		

def minimax(board, player, counter, start_col, board_scores, cpu):
	""" 
	Simulates gameplay between the player and the hard cpu in order to create possible board states.
	
	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player dropping the piece, int.
	:param counter: The depth of the search that is left over.
	:param start_col: The column that the cpu first dropped in.
	:param board_scores: An array containing the favourability of dropping into that column
	:return: None
	"""
	

	if (counter < 2):
		board_scores[start_col] += score_board(board, cpu)
		if(player == cpu):	
			counter += 1
		for column in range(game_parameters['columns']):
			if (board[0][column] == 0):
				board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
				possible_move = drop_piece_cpu(board_copy, player, column + 1)
				if (player == len(players)):
					minimax(possible_move, 1, counter, start_col, board_scores, cpu)
				else:   
					minimax(possible_move, player + 1, counter, start_col, board_scores, cpu)
                # if(player == cpu):
                # 	board_scores[start_col] += score_board(board, cpu)
                # 	counter += 1


def cpu_player_hard(board, player):
	"""
	Executes a move for the CPU on hard difficulty.
	This function creates a copy of the board to simulate moves.
    
	Minimax algorithm

	It looks for possible moves of the other players and tries to find the best possible response

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: None
	"""
	board_scores = [0] * game_parameters["columns"]
	
	for column in range(game_parameters['columns']):
		if (board[0][column] == 0):
			#Create these possible boards
			board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
			
			possible_cpu_move = drop_piece_cpu(board_copy, player, column + 1)
			if (player == len(players)):
				minimax(possible_cpu_move, 1, 1, column, board_scores, player)
			else:   
				minimax(possible_cpu_move, player + 1, 1, column, board_scores, player)

    
	drop_col = board_scores.index(max(board_scores))
	print(board_scores)
	drop_piece(board, player, drop_col + 1)
	#Find the board with the max score	
	return drop_col + 1	

if __name__ == "__main__":
	main()