"""
FIT1053: Sem 1 2023 Assignment 1 (Solution Copy)
Authors: David Le, Randil Hettiarachchi, Rathan Murugesan Senthil, Henry Wang
Last updated: 02/04/2023
"""
import random
import os

def clear_screen():
	"""
	Clears the terminal for Windows and Linux/MacOS.

	:return: None
	"""
	os.system('cls' if os.name == 'nt' else 'clear')

def print_rules():
	"""
	Prints the rules of the game.

	:return: None
	"""
	print("================= Rules =================")
	print("Connect 4 is a two-player game where the")
	print("objective is to get four of your pieces")
	print("in a row either horizontally, vertically")
	print("or diagonally. The game is played on a")
	print("6x7 grid. The first player to get four")
	print("pieces in a row wins the game. If the")
	print("grid is filled and no player has won,")
	print("the game is a draw.")
	print("=========================================")

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
	Returns a 2D list of 6 rows and 7 columns to represent
	the game board. Default cell value is 0.

	:return: A 2D list of 6x7 dimensions.
	"""
	board = [
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0]
	]
	return board

def print_board(board):
	"""
	Prints the game board to the console.

	:param board: The game board, 2D list of 6x7 dimensions.
	:return: None
	"""
	print("========== Connect4 =========")
	print("Player 1: X       Player 2: O")
	print("")
	print("  1   2   3   4   5   6   7")
	for row in range(6):
		print(" --- --- --- --- --- --- ---")
		for column in range(7):
			if board[row][column] == 0:
				print("|   ",end="")
			elif board[row][column] == 1:
				print("| X ",end="")
			else: # When the the element is 2
				print("| O ",end="")
		print("|")
	print(" --- --- --- --- --- --- ---")
	print("=============================")

def drop_piece(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player who is dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	# Checks if the top row (at a given column) is clear
	if board[0][column - 1] == 0:
		# Checks from bottom up
		for row in range(5, -1, -1):
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
	column = int(validate_input("Player " + str(player) + ", please enter the column you would like to drop your piece into: ", ["1", "2", "3", "4", "5", "6", "7"]))
	while drop_piece(board, player, column) == False:
		print("That column is full, please try again.")
		column = int(validate_input("Player " + str(player) + ", please enter the column you would like to drop your piece into: ", ["1", "2", "3", "4", "5", "6", "7"]))
	return column

def horizontal_check(board, row, column):
	"""
	Checks if there is 4 in a row horizontally. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of 6x7
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if column <= 3:
		window = [board[row][column + i] for i in range(4)]
		return window
	return False

def vertical_check(board, row, column):
	"""
	Checks if there is 4 in a row vertically. Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of 6x7
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= 3:
		window = [board[row - i][column] for i in range(4)]
		return window
	return False

def positive_diagonal_check(board, row, column):
	"""
	Checks if there is 4 in a row diagonally (bottom left to top right). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of 6x7
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= (3) and column <= (3):
		window = [board[row - i][column + i] for i in range(4)]
		return window
	return False

def negative_diagonal_check(board, row, column):
	"""
	Checks if there is 4 in a row diagonally (bottom right to top left). Takes all possible 'windows' (list of 4).

	:param board: The game board, 2D list of 6x7 dimensions
	:param row: The row of the current cell it is checking
	:param column: The column of the current cell it is checking
	:return: The 'window' (list). If a 'window' is not possible, it returns False
	"""
	if row >= (3) and column >= (3):
		window = [board[row - i][column - i] for i in range(4)]
		return window
	return False

def end_of_game(board):
	"""
	Checks if the game has ended with a winner
	or a draw.

	It will check a cell, then all possible horizontal/vertical/diagonal rows stemming from the cell.

	:param board: The game board, 2D list of 6 rows x 7 columns.
	:return: 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if draw.
	"""
	currently_draw = False
	for row in range(len(board) - 1, -1, -1):
		for column in range(7):
			horizontal_window = horizontal_check(board, row, column)
			vertical_window = vertical_check(board, row, column)
			positive_diagonal_window = positive_diagonal_check(board, row, column)
			negative_diagonal_window = negative_diagonal_check(board, row, column)
			
			# Makes sure the x_window list exists (preventing AttributeError for .count())
			if (horizontal_window != False and horizontal_window.count(1) == 4) or (vertical_window != False and vertical_window.count(1) == 4) or (positive_diagonal_window != False and positive_diagonal_window.count(1) == 4) or (negative_diagonal_window != False and negative_diagonal_window.count(1) == 4):
				return 1
			if (horizontal_window != False and horizontal_window.count(2) == 4) or (vertical_window != False and vertical_window.count(2) == 4) or (positive_diagonal_window != False and positive_diagonal_window.count(2) == 4) or (negative_diagonal_window != False and negative_diagonal_window.count(2) == 4):
				return 2

	# Distinguishes between a draw and the game not being over
	for row in board:
		for column in row:
			if column == 0:
				return 0
	return 3
		
def local_2_player_game():
	"""
	Runs a local 2 player game of Connect 4.

	:return: None
	"""
	board = create_board()
	current_player = 1

	while end_of_game(board) == 0:
		clear_screen()
		print_board(board)
		execute_player_turn(current_player, board)
		
		if current_player == 1:
			current_player = 2
		else:
			current_player = 1

	clear_screen()
	print_board(board)

	if end_of_game(board) == 1:
		print("Player 1 has won!")
	elif end_of_game(board) == 2:
		print("Player 2 has won!")
	elif end_of_game(board) == 3:
		print("There was a tie! No winner!")

def main():
	"""
	Defines the main application loop.
    User chooses a type of game to play or to exit.

	:return: None
	"""
	print("=============== Main Menu ===============")
	print("Welcome to Connect 4!")
	print("1. View Rules")
	print("2. Play a local 2 player game")
	print("3. Play a game against the computer")
	print("4. Exit")
	print("=========================================")

	start_option = validate_input("Choose your option: ", ["1", "2", "3", "4"])
	while start_option != "4":
		if start_option == "1":
			print_rules()
			break
		elif start_option == "2":
			local_2_player_game()
			break
		elif start_option == "3":
			game_against_cpu()
			break

def cpu_player_easy(board, player):
	"""
	Executes a move for the CPU on easy difficulty. This function 
	plays a randomly selected column.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	available_columns = []
	for i in range(len(board[0])):
		if (board[0][i] == 0):
			available_columns.append(i)
			
	column = random.choice(available_columns)
	drop_piece(board, player, column + 1)
	return column + 1 # The column dropped into for the player is + 1

# def win_draw_check(board, player):
# 	'''
# 	Checks the current board to see if there is a opportunity to win or if the bot needs to prevent the other player from winning

# 	:param board: The current board state
# 	:param player: The cpu player
	
# 	:return: If a winning opportunity was detected, then the column that it was dropped into will be returned. If a block was detected, then an array containing the column that the block needs to be dropped in will be returned. If nothing was detected, an array with None will be returned.
# 	'''
# 	block = None #Saving what wins need to be blocked

# 	for row in range(len(board) - 1, -1, -1):
# 		for column in range(7):
# 			if (board[row][column] == 0):
# 				continue
# 			vertical = medium_vertical_check(board, row, column) 
# 			horizontal = medium_horizontal_check(board, row, column)
# 			left_diagonal = medium_diagonal_left_check(board, row, column)
# 			right_diagonal = medium_diagonal_right_check(board, row, column)

# 			if (horizontal == player):
# 				drop_piece(board, player, column +4)
# 				return column + 4
# 			elif (horizontal != 0):
# 				block = column + 4
# 			if (vertical == player):
# 				drop_piece(board, player, column + 1)
# 				return column + 1
# 			elif (vertical != 0):
# 				block = column + 1
# 			if (left_diagonal != None):
# 				if (left_diagonal[0] == player):
# 					drop_piece(board, player, left_diagonal[1]+1)
# 					return left_diagonal[1] + 1
# 				elif (left_diagonal[0] != 0):
# 					block = left_diagonal[1] + 1
# 			if (right_diagonal != None):
# 				if (right_diagonal[0] == player):
# 					drop_piece(board, player, right_diagonal[1] + 1)
# 					return right_diagonal[1] + 1
# 				elif (right_diagonal[0] != 0):
# 					block = right_diagonal[1] + 1
# 	return [block] #It is returned in an array so that it is able to be differentiated from when the piece has already been dropped.

# def cpu_player_medium(board, player):
	# """
	# Executes a move for the CPU on medium difficulty.
	# It first checks for an immediate win and plays that move if possible. 
	# If no immediate win is possible, it checks for an immediate win 
	# for the opponent and blocks that move. If neither of these are 
	# possible, it plays a random move.

	# :param board: The game board, 2D list of 6x7 dimensions.
	# :param player: The player whose turn it is, integer value of 1 or 2.
	# :return: Column that the piece was dropped into, int.
	# """

# 	check_result = win_draw_check(board, player)
	
# 	if (isinstance(check_result, int)):
# 		return check_result
# 	else:
# 		if (check_result[0] != None):
# 			drop_piece(board, player, check_result[0])
# 			return check_result[0]
# 		else:
# 			# If no immediate win, then execute as cpu_easy would
# 			return cpu_player_easy(board, player)

def drop_piece_cpu(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	for row in range(len(board) - 1, -1, -1):
		if (board[row][column - 1] == 0): # column - 1 because the columns start from 1 for the player
			board[row][column - 1] = player
			return board
			
def cpu_player_medium(board, player):
	"""
	Executes a move for the CPU on medium difficulty.
	It first checks for an immediate win and plays that move if possible. 
	If no immediate win is possible, it checks for an immediate win 
	for the opponent and blocks that move. If neither of these are 
	possible, it plays a random move.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""

	block = None
	for column in range(7):
		if (board[0][column] == 0):
			board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
			possible_player_move = drop_piece_cpu(board_copy, player , column + 1) 
			board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
			possible_enemy_move = drop_piece_cpu(board_copy, 3 - player , column + 1) 
			result = end_of_game(possible_player_move)
			result2 = end_of_game(possible_enemy_move)
			if (result == player): 	
				drop_piece(board, player, column + 1)
				return column + 1 
			elif (result2 == 3 - player):
				block = column + 1


	if (block != None):
		drop_piece(board, player, block)    
		return block
	return cpu_player_easy(board, player)

# def medium_horizontal_check(board, row, column):
# 	'''
# 	Checks if a win/loss is possible through a horizontal set of 4.

# 	:param board: The current board state
# 	:param row: The row of the square being checked
# 	:param column: The column of the square being checked

# 	:return: 0 if nothing is detected, 1 or 2 if a win/loss is possible.
# 	'''
# 	checking = board[row][column] 
# 	if (column + 3 >= 6):
# 		return 0 
# 	for column_check in range(1, 3):
# 		if(board[row][column+column_check] != checking):
# 			return 0
# 	if (board[row][column + 3] ==0 and (row == 5 or board[row + 1][column +3] != 0)):			
# 		return checking
# 	return 0

# def medium_vertical_check(board, row, column):
# 	'''
# 	Checks if a win/loss is possible through a vertical set of 4.

# 	:param board: The current board state
# 	:param row: The row of the square being checked
# 	:param column: The col
# Copy and paste drop_piece here
def drop_piece_cpu(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	for row in range(len(board) - 1, -1, -1):
		if (board[row][column - 1] == 0): # column -1 because the columns start from 1 for the player
			board[row][column - 1] = player
			return board
			
# def calc_score(cpu, window):
# 	'''
# 	Calculates the score for a given window

# 	:param cpu: The cpu player. 
# 	:param window: 
# 	:return: The score of the current window
# 	'''
# 	counts = Counter(window)

# 	score = 0

# 	if (counts[cpu] == game_parameters['tokens']):
# 	for row_check in range(1, 3):
# 		if(board[row-row_check][column] != checking):
# 			return 0
# 	if (board[row - 3][column] ==0):			
# 		return checking		
# 	return 0


# def medium_diagonal_left_check(board, row, column):
# 	'''
# 	Checks if a win/loss is possible through a diagonal set of 4 leaning towards the left

# 	:param board: The current board state
# 	:param row: The row of the square being checked
# 	:param column: The column of the square being checked

# 	:return: None if nothing was detected or a tuple containing whether dropping the piece will make the cpu win or will prevent it from losing as well as the column that the piece needs to be dropped into.
# 	'''
# 	checking = board[row][column] 

# 	if (row - 2 >= 0 and column - 2 >= 0):
# 		for i in range(1, 3):
# 			if (board[row - i][column-i] != checking):
# 				return None

# 		if ( board[row -2][column -3] != 0 and board[row-3][row-3] == 0):
# 			return (checking, column -3) 
# 		elif (row < 5  and board[row+1][column+1] != 0):
# 			return (checking, column + 1)
# 		else:
# 			return None


# def medium_diagonal_right_check(board, row, column):
# 	'''
# 	Checks if a win/loss is possible through a diagonal set of 4 leaning towards the right

# 	:param board: The current board state
# 	:param row: The row of the square being checked
# 	:param column: The column of the square being checked

# 	:return: None if nothing was detected or a tuple containing whether dropping the piece will make the cpu win or will prevent it from losing as well as the column that the piece needs to be dropped into.
# 	'''
# 	checking = board[row][column] 
# 	if (row - 3 >= 0 and column + 3 < 7):
# 		for i in range(1, 3):
# 			if (board[row - i][column+i] != checking):
# 				return None
		
# 		if (board[row -2][column +3] != 0):
# 			return (checking, column +3) 
# 		elif (board[row-2][column-1] != 0 and (row + 1 == 5 and board[row - 1][column -1] == 0)):
# 				return (checking, column - 1)
# 		else:
# 			return None

#HARD --------------------------------------
def calc_score(cpu, window):
	'''
	Calculates the score for a given window

	:param cpu: The cpu player. 
	:param window: 
	:return: The score of the current window
	'''
	if (window.count(cpu) == 4):
		return 1000
	elif (window.count(cpu) == 3 and window.count(0) == 1):
		return 10
	elif (window.count(cpu) == 2 and window.count(0) == 2):
		return 4
	elif (window.count(3 - cpu) == 2 and window.count(0) == 2):
		return -4
	elif (window.count(3 - cpu) == 3 and window.count(0) == 1):
		return -10
	elif(window.count(3 - cpu) == 4):
		return -1000

	else:
		return 0

# Occurs left to right. No need to go other way as this would check the same thing
def hard_horizontal_check(board, row, column, cpu):
	'''
	Creates a horizontal window that will then be scored for how favourable it is for the cpu

	:param board: The board from which a window will be extracted
	:param row: The row that the window will come from
	:param column: The column from which the window will start
	:param cpu: The cpu player
	:return: The calculated score for the horizontal window

	 '''
	if (column >= 4):
		return 0 
	window = [board[row][column + i] for i in range(4)]
	return calc_score(cpu, window)

#No need to check downwards as check vertically would have been done from the lower piece 
def hard_vertical_check(board, row, column, cpu):
	'''
	Creates a vertical window that will then be scored for how favourable it is for the cpu

	:param board: The board from which a window will be extracted
	:param row: The row that the window will come from
	:param column: The column from which the window will start
	:param cpu: The cpu player
	:return: The calculated score for the vertical window
	'''
	if (row <= 2):
		return 0 
	window = [board[row - i][column] for i in range(4)]
	return calc_score(cpu, window)

def hard_diagonal_check_left(board, row, column, cpu):
	'''
	Creates a forward leaning diagonal window that will then be scored for how favourable it is for the cpu

	:param board: The board from which a window will be extracted
	:param row: The row that the window will come from
	:param column: The column from which the window will start
	:param cpu: The cpu player
	:return: The calculated score for the forward leaning diagonal window

	'''
	if (3 <= row <= 5 and 3 <= column <= 6):
		window = [board[row - i][column - i] for i in range(4)]
		return calc_score(cpu, window)
	return 0


def hard_diagonal_check_right(board, row, column, cpu):
	'''
	Creates a backwards sloping window that will then be scored for how favourable it is for the cpu

	:param board: The board from which a window will be extracted
	:param row: The row that the window will come from
	:param column: The column from which the window will start
	:param cpu: The cpu player
	:return: The calculated score for the backwards sloping window
	'''

	if (3 <= row <= 5 and 0 <= column <= 3):
		window = [board[row - i][column + i] for i in range(4)]
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

	for row in range(len(board) - 1, -1, -1):
		for column in range(7):
			if (board[row][column] == 0):
				continue
			score += hard_horizontal_check(board, row, column, cpu)
			score += hard_vertical_check(board, row, column, cpu)
			score += hard_diagonal_check_left(board, row, column, cpu)
			score += hard_diagonal_check_right(board, row, column, cpu)	
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
	board_scores[start_col] += score_board(board, cpu)
	if (counter == 2):
		return None
	counter += 1
	
	for column in range(7):
		if (board[0][column] == 0):
			# Create these possible boards
			board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
			
			possible_move = drop_piece_cpu(board_copy, player, column + 1)
			
			if (counter < 2):
				minimax(possible_move, 3 - player, counter, start_col, board_scores, cpu)

def cpu_player_hard(board, player):
	"""
	Executes a move for the CPU on hard difficulty.
	This function creates a copy of the board to simulate moves.
    
	This uses the minimax algorithm.
	It looks for possible moves of the other player and tries to find the best possible response

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: None
	"""
	board_scores = [0] * 7 
	
	for column in range(7):
		if (board[0][column] == 0):
			# Create these possible boards
			board_copy = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
			
			possible_cpu_move = drop_piece_cpu(board_copy, player, column + 1)
			minimax(possible_cpu_move, 3 - player, 0, column, board_scores, player)
		                                                                          
	drop_col = board_scores.index(max(board_scores))
	drop_piece(board, player, drop_col + 1)
	# Find the board with the max score	
	return drop_col + 1


def game_against_cpu():
	"""
	Runs a game of Connect 4 against the computer.

	:return: None
	"""
	board = create_board()
	level_of_difficulty = validate_input("Choose your difficulty (easy, medium, hard): ", ["easy", "medium", "hard"])

	while end_of_game(board) == 0:
		print_board(board)
		execute_player_turn(1, board)
		if level_of_difficulty == "easy":
			cpu_player_easy(board, 2)
		elif level_of_difficulty == "medium":
			cpu_player_medium(board, 2)
		elif level_of_difficulty == "hard":
			cpu_player_hard(board,2)
			
	print_board(board)
	if end_of_game(board) == 1:
		print("Player 1 has won!")
		return 1
	elif end_of_game(board) == 2:
		print("Player 2 has won!")
		return 2
	elif end_of_game(board) == 3:
		print("There was a tie! No winner!")
	print_board(board)

if __name__ == "__main__":
	main()