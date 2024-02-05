from copy import deepcopy
import time
import math
import sys
import os

ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"


class Node:
	def __init__(self, board, move=None, parent=None, value=None):
		self.board = board
		self.value = value
		self.move = move
		self.parent = parent

	def get_children(self, minimizing_player, mandatory_jumping):
		current_state = deepcopy(self.board)
		available_moves = []
		children_states = []
		big_letter = ""
		queen_row = 0
		if minimizing_player is True:
			available_moves = Checkers.find_available_moves(current_state, mandatory_jumping)
			big_letter = "C"
			queen_row = 7
		else:
			available_moves = Checkers.find_player_available_moves(current_state, mandatory_jumping)
			big_letter = "B"
			queen_row = 0
		for i in range(len(available_moves)):
			old_i = available_moves[i][0]
			old_j = available_moves[i][1]
			new_i = available_moves[i][2]
			new_j = available_moves[i][3]
			state = deepcopy(current_state)
			Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
			children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
		return children_states

	def set_value(self, value):
		self.value = value

	def get_value(self):
		return self.value

	def get_board(self):
		return self.board

	def get_parent(self):
		return self.parent

	def set_parent(self, parent):
		self.parent = parent


class Checkers:

	def __init__(self):
		self.matrix = [[], [], [], [], [], [], [], []]
		self.player_turn = True
		self.computer_pieces = 12
		self.player_pieces = 12
		self.available_moves = []
		self.mandatory_jumping = False

		for row in self.matrix:
			for i in range(8):
				row.append("---")
		self.position_computer()
		self.position_player()

	def position_computer(self):
		for i in range(3):
			for j in range(8):
				if (i + j) % 2 == 1:
					self.matrix[i][j] = ("c" + str(i) + str(j))

	def position_player(self):
		for i in range(5, 8, 1):
			for j in range(8):
				if (i + j) % 2 == 1:
					self.matrix[i][j] = ("b" + str(i) + str(j))

	def print_matrix(self):
		i = 0
		print()
		for row in self.matrix:
			print(i, end="  |")
			i += 1
			for elem in row:
				print(elem, end=" ")
			print()
		print()
		for j in range(8):
			if j == 0:
				j = "     0"
			print(j, end="   ")
		print("\n")

	def get_player_input(self):
		available_moves = Checkers.find_player_available_moves(self.matrix, self.mandatory_jumping)
		if len(available_moves) == 0:
			if self.computer_pieces > self.player_pieces:
				print("{0}{1}\n{2}{2}".format(ansi_red, arr_lang[17], arr_lang[31], ansi_reset)) # You have no moves left, and you have fewer pieces than the computer. YOU LOSE!
				exit()
			else:
				print("{0}{1}\n{2}{3}".format(ansi_yellow, arr_lang[18], arr_lang[7], ansi_reset)) # You have no available moves.\nGAME ENDED!
				exit()
		self.player_pieces = 0
		self.computer_pieces = 0
		while True:

			coord1 = input("{0}[i,j]:".format(arr_lang[21])) # Which piece
			if coord1 == "":
				print("{0}{1}{2}".format(ansi_cyan, arr_lang[7], ansi_reset)) # Game ended!
				exit()
			elif coord1 == "s":
				print("{0}{1}\n{2}{3}".format(ansi_cyan, arr_lang[19], arr_lang[16], ansi_reset)) # You surrendered.\nCoward.
				exit()
			coord2 = input("{0} [i,j]:".format(arr_lang[20])) # Where to
			if coord2 == "":
				print("{0}{1}{2}".format(ansi_cyan, arr_lang[7], ansi_reset)) # Game ended!
				exit()
			elif coord2 == "s":
				print("{0}{1}\n{2}{3}".format(ansi_cyan, arr_lang[19], arr_lang[16], ansi_reset)) # You surrendered.\nCoward.
				exit()
			old = coord1.split(",")
			new = coord2.split(",")

			if len(old) != 2 or len(new) != 2:
				print("{0}{1}{2}".format(ansi_red, arr_lang[9], ansi_reset)) # Illegal input!
			else:
				old_i = old[0]
				old_j = old[1]
				new_i = new[0]
				new_j = new[1]
				if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
					print("{0}{1}{2}".format(ansi_red, arr_lang[9], ansi_reset)) # Illegal input!
				else:
					move = [int(old_i), int(old_j), int(new_i), int(new_j)]
					if move not in available_moves:
						print("{0}{1}{2}".format(ansi_red, arr_lang[22], ansi_reset)) # Illegal move!
					else:
						Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "B", 0)
						for m in range(8):
							for n in range(8):
								if self.matrix[m][n][0] == "c" or self.matrix[m][n][0] == "C":
									self.computer_pieces += 1
								elif self.matrix[m][n][0] == "b" or self.matrix[m][n][0] == "B":
									self.player_pieces += 1
						break

	@staticmethod
	def find_available_moves(board, mandatory_jumping):
		available_moves = []
		available_jumps = []
		for m in range(8):
			for n in range(8):
				if board[m][n][0] == "c":
					if Checkers.check_moves(board, m, n, m + 1, n + 1):
						available_moves.append([m, n, m + 1, n + 1])
					if Checkers.check_moves(board, m, n, m + 1, n - 1):
						available_moves.append([m, n, m + 1, n - 1])
					if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
						available_jumps.append([m, n, m + 2, n - 2])
					if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
						available_jumps.append([m, n, m + 2, n + 2])
				elif board[m][n][0] == "C":
					if Checkers.check_moves(board, m, n, m + 1, n + 1):
						available_moves.append([m, n, m + 1, n + 1])
					if Checkers.check_moves(board, m, n, m + 1, n - 1):
						available_moves.append([m, n, m + 1, n - 1])
					if Checkers.check_moves(board, m, n, m - 1, n - 1):
						available_moves.append([m, n, m - 1, n - 1])
					if Checkers.check_moves(board, m, n, m - 1, n + 1):
						available_moves.append([m, n, m - 1, n + 1])
					if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
						available_jumps.append([m, n, m + 2, n - 2])
					if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
						available_jumps.append([m, n, m - 2, n - 2])
					if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
						available_jumps.append([m, n, m - 2, n + 2])
					if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
						available_jumps.append([m, n, m + 2, n + 2])
		if mandatory_jumping is False:
			available_jumps.extend(available_moves)
			return available_jumps
		elif mandatory_jumping is True:
			if len(available_jumps) == 0:
				return available_moves
			else:
				return available_jumps

	@staticmethod
	def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
		if new_i > 7 or new_i < 0:
			return False
		if new_j > 7 or new_j < 0:
			return False
		if board[via_i][via_j] == "---":
			return False
		if board[via_i][via_j][0] == "C" or board[via_i][via_j][0] == "c":
			return False
		if board[new_i][new_j] != "---":
			return False
		if board[old_i][old_j] == "---":
			return False
		if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
			return False
		return True

	@staticmethod
	def check_moves(board, old_i, old_j, new_i, new_j):

		if new_i > 7 or new_i < 0:
			return False
		if new_j > 7 or new_j < 0:
			return False
		if board[old_i][old_j] == "---":
			return False
		if board[new_i][new_j] != "---":
			return False
		if board[old_i][old_j][0] == "b" or board[old_i][old_j][0] == "B":
			return False
		if board[new_i][new_j] == "---":
			return True

	@staticmethod
	def calculate_heuristics(board):
		result = 0
		mine = 0
		opp = 0
		for i in range(8):
			for j in range(8):
				if board[i][j][0] == "c" or board[i][j][0] == "C":
					mine += 1

					if board[i][j][0] == "c":
						result += 5
					if board[i][j][0] == "C":
						result += 10
					if i == 0 or j == 0 or i == 7 or j == 7:
						result += 7
					if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
						continue
					if (board[i + 1][j - 1][0] == "b" or board[i + 1][j - 1][0] == "B") and board[i - 1][
						j + 1] == "---":
						result -= 3
					if (board[i + 1][j + 1][0] == "b" or board[i + 1][j + 1] == "B") and board[i - 1][j - 1] == "---":
						result -= 3
					if board[i - 1][j - 1][0] == "B" and board[i + 1][j + 1] == "---":
						result -= 3

					if board[i - 1][j + 1][0] == "B" and board[i + 1][j - 1] == "---":
						result -= 3
					if i + 2 > 7 or i - 2 < 0:
						continue
					if (board[i + 1][j - 1][0] == "B" or board[i + 1][j - 1][0] == "b") and board[i + 2][
						j - 2] == "---":
						result += 6
					if i + 2 > 7 or j + 2 > 7:
						continue
					if (board[i + 1][j + 1][0] == "B" or board[i + 1][j + 1][0] == "b") and board[i + 2][
						j + 2] == "---":
						result += 6

				elif board[i][j][0] == "b" or board[i][j][0] == "B":
					opp += 1

		return result + (mine - opp) * 1000

	@staticmethod
	def find_player_available_moves(board, mandatory_jumping):
		available_moves = []
		available_jumps = []
		for m in range(8):
			for n in range(8):
				if board[m][n][0] == "b":
					if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
						available_moves.append([m, n, m - 1, n - 1])
					if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
						available_moves.append([m, n, m - 1, n + 1])
					if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
						available_jumps.append([m, n, m - 2, n - 2])
					if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
						available_jumps.append([m, n, m - 2, n + 2])
				elif board[m][n][0] == "B":
					if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
						available_moves.append([m, n, m - 1, n - 1])
					if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
						available_moves.append([m, n, m - 1, n + 1])
					if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
						available_jumps.append([m, n, m - 2, n - 2])
					if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
						available_jumps.append([m, n, m - 2, n + 2])
					if Checkers.check_player_moves(board, m, n, m + 1, n - 1):
						available_moves.append([m, n, m + 1, n - 1])
					if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
						available_jumps.append([m, n, m + 2, n - 2])
					if Checkers.check_player_moves(board, m, n, m + 1, n + 1):
						available_moves.append([m, n, m + 1, n + 1])
					if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
						available_jumps.append([m, n, m + 2, n + 2])
		if mandatory_jumping is False:
			available_jumps.extend(available_moves)
			return available_jumps
		elif mandatory_jumping is True:
			if len(available_jumps) == 0:
				return available_moves
			else:
				return available_jumps

	@staticmethod
	def check_player_moves(board, old_i, old_j, new_i, new_j):
		if new_i > 7 or new_i < 0:
			return False
		if new_j > 7 or new_j < 0:
			return False
		if board[old_i][old_j] == "---":
			return False
		if board[new_i][new_j] != "---":
			return False
		if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
			return False
		if board[new_i][new_j] == "---":
			return True

	@staticmethod
	def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
		if new_i > 7 or new_i < 0:
			return False
		if new_j > 7 or new_j < 0:
			return False
		if board[via_i][via_j] == "---":
			return False
		if board[via_i][via_j][0] == "B" or board[via_i][via_j][0] == "b":
			return False
		if board[new_i][new_j] != "---":
			return False
		if board[old_i][old_j] == "---":
			return False
		if board[old_i][old_j][0] == "c" or board[old_i][old_j][0] == "C":
			return False
		return True

	def evaluate_states(self):
		t1 = time.time()
		current_state = Node(deepcopy(self.matrix))

		first_computer_moves = current_state.get_children(True, self.mandatory_jumping)
		if len(first_computer_moves) == 0:
			if self.player_pieces > self.computer_pieces:
				print("{0}{1}\n{2}{3}".format(ansi_yellow, arr_lang[23], arr_lang[32], ansi_reset)) # Computer has no available moves left, and you have more pieces left.\nYOU WIN!
				exit()
			else:
				print("{0}{1}\n{2}{3}".format(ansi_yellow, arr_lang[24], arr_lang[7], ansi_reset)) # Computer has no available moves left.\nGAME ENDED!
				exit()
		dict = {}
		for i in range(len(first_computer_moves)):
			child = first_computer_moves[i]
			value = Checkers.minimax(child.get_board(), 4, -math.inf, math.inf, False, self.mandatory_jumping)
			dict[value] = child
		if len(dict.keys()) == 0:
			print("{0}{1}\n{2}{3}".format(ansi_green, arr_lang[25], arr_lang[32], ansi_reset)) # Computer has cornered itself.\nYOU WIN!
			exit()
		new_board = dict[max(dict)].get_board()
		move = dict[max(dict)].move
		self.matrix = new_board
		t2 = time.time()
		diff = t2 - t1
		print("{0} ({1},{2}) {3} ({4},{5}).".format(arr_lang[26], str(move[0]), str(move[1]), arr_lang[27], str(move[2]), str(move[2]))) # Computer has moved xxx to yyy
		print("{0} {1} {2}".format(arr_lang[28], str(diff), arr_lang[29]))

	@staticmethod
	def minimax(board, depth, alpha, beta, maximizing_player, mandatory_jumping):
		if depth == 0:
			return Checkers.calculate_heuristics(board)
		current_state = Node(deepcopy(board))
		if maximizing_player is True:
			max_eval = -math.inf
			for child in current_state.get_children(True, mandatory_jumping):
				ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping)
				max_eval = max(max_eval, ev)
				alpha = max(alpha, ev)
				if beta <= alpha:
					break
			current_state.set_value(max_eval)
			return max_eval
		else:
			min_eval = math.inf
			for child in current_state.get_children(False, mandatory_jumping):
				ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping)
				min_eval = min(min_eval, ev)
				beta = min(beta, ev)
				if beta <= alpha:
					break
			current_state.set_value(min_eval)
			return min_eval

	@staticmethod
	def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
		letter = board[old_i][old_j][0]
		i_difference = old_i - new_i
		j_difference = old_j - new_j
		if i_difference == -2 and j_difference == 2:
			board[old_i + 1][old_j - 1] = "---"

		elif i_difference == 2 and j_difference == 2:
			board[old_i - 1][old_j - 1] = "---"

		elif i_difference == 2 and j_difference == -2:
			board[old_i - 1][old_j + 1] = "---"

		elif i_difference == -2 and j_difference == -2:
			board[old_i + 1][old_j + 1] = "---"

		if new_i == queen_row:
			letter = big_letter
		board[old_i][old_j] = "---"
		board[new_i][new_j] = letter + str(new_i) + str(new_j)

	def play(self, arr_lang):
		print("{0}##### {1} ####{2}".format(ansi_cyan, arr_lang[0], ansi_reset)) # WELCOME TO CHECKERS
		print("\n{0}:".format(arr_lang[1])) # Some basic rules
		print("1.{0} i,j.".format(arr_lang[2])) # You enter the coordinates in the form
		print("2.{0}.".format(arr_lang[3])) # You can quit the game at any time by pressing
		print("3.{0} 's'.".format(arr_lang[4])) # You can surrender at any time by pressing
		print("{0}".format(arr_lang[5])) # Now that you've familiarized yourself with the rules, enjoy!
		while True:
			answer = input("\n{0}[Y/n]: ".format(arr_lang[6])) #First, we need to know, is jumping mandatory?
			if answer == "Y" or answer == "y":
				self.mandatory_jumping = True
				break
			elif answer == "N" or answer == "n":
				self.mandatory_jumping = False
				break
			elif answer == "":
				print("{0}{1}{2}".format(ansi_cyan, arr_lang[7], ansi_reset)) # Game ended!
				exit()
			elif answer == "s":
				print("{0}{1}{2}{3}".format(ansi_cyan, arr_lang[8], arr_lang[30], ansi_reset)) # You've surrendered before the game even started.\nPathetic.
				exit()
			else:
				print("{0}{1}{2}".format(ansi_red, arr_lang[9], ansi_reset)) # Illegal input!
		while True:
			self.print_matrix()
			if self.player_turn is True:
				print("{0}{1}{2}".format(ansi_cyan, arr_lang[10], ansi_reset)) # Player's turn.
				self.get_player_input()
			else:
				print("{0}{1}{2}".format(ansi_cyan, arr_lang[11], ansi_reset)) # Computer's turn.
				print("{0}".format(arr_lang[12])) # Thinking...
				self.evaluate_states()
			if self.player_pieces == 0:
				self.print_matrix()
				print("{0}{1}\n{2}{3}".format(ansi_red, arr_lang[13], arr_lang[31], ansi_reset)) # You have no pieces left.\nYOU LOSE!
				exit()
			elif self.computer_pieces == 0:
				self.print_matrix()
				print("{0}{1}\n{2}{3}".format(ansi_green, arr_lang[14], arr_lang[32], ansi_reset)) # Computer has no pieces left.\nYOU WIN!
				exit()
			elif self.computer_pieces - self.player_pieces == 7:
				wish = input("{0}".format(arr_lang[15])) # You have 7 pieces fewer than your opponent.Do you want to surrender?
				if wish == "" or wish == "yes":
					print("{0}{1}{2}".format(ansi_cyan, arr_lang[16], ansi_reset)) # Coward.
					exit()
			self.player_turn = not self.player_turn


if __name__ == '__main__':

	n = len(sys.argv)
	if len(sys.argv) != 2:
		print("Choose your language:")
		print("$ python checkers.py lang")
		print(os.listdir('lang/'))
		sys.exit(0)
	
	lang = sys.argv[1]
	if not os.path.isfile('lang/' + lang):
		print('Not a valid language. Valid languages:')
		print(os.listdir('lang/'))
		sys.exit(0)

	with open('lang/' + lang, "r") as f:
		arr_lang = [line.rstrip('\n') for line in f]

	checkers = Checkers()
	checkers.play(arr_lang)
