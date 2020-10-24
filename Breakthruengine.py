import pygame
from tkinter import messagebox
import numpy as np


class State_Game:
	def __init__(self):
		self.board =[
			["__", "__", "__", "__", "__", "__", "__", "__", "__", "__", "__"],
			["__", "__", "__", "Sf", "Sf", "Sf", "Sf", "Sf", "__", "__", "__"],
			["__", "__", "__", "__", "__", "__", "__", "__", "__", "__", "__"],
			["__", "Sf", "__", "__", "Gf", "Gf", "Gf", "__", "__", "Sf", "__"],
			["__", "Sf", "__", "Gf", "__", "__", "__", "Gf", "__", "Sf", "__"],
			["__", "Sf", "__", "Gf", "__", "GB", "__","Gf", "__", "Sf", "__"],
			["__", "Sf", "__", "Gf", "__", "__", "__", "Gf", "__", "Sf", "__"],
			["__", "Sf", "__", "__", "Gf", "Gf", "Gf", "__", "__", "Sf", "__"],
			["__", "__", "__", "__", "__", "__", "__", "__", "__", "__", "__"],
			["__", "__", "__", "Sf", "Sf", "Sf", "Sf", "Sf", "__", "__", "__"],
			["__", "__", "__", "__", "__", "__", "__", "__", "__", "__", "__"]]
		self.function_move = {"f": self.fleet_moves,"B":self.fleet_moves}
		self.secondmove=0
		self.silverfleet=20
		self.goldfleet=12
		
		self.bigship=1
		self.piece_captured=[]
		self.Goldmove = True
		self.movetrack =[]
		self.DEBUG = True
	# takes a move as parapameter and execute
	def make_move(self,move):
		
		if move.piece_move == "GB" and self.secondmove==0:
			
			self.board[move.start_row][move.start_col] = "__"
		
			if self.board[move.end_row][move.end_col] != "__":
				self.piece_captured.append(self.board[move.end_row][move.end_col])
				if self.piece_captured[-1][1] == 'Sf':
					self.silverfleet -= 1
					if self.silverfleet == 0:
						self.goldwin(window, False)
			self.board[move.end_row][move.end_col] = move.piece_move
			self.secondmove = 2
			self.movetrack.append(move)# track the move so we can undo it later
			if (move.end_col == 10 or move.end_col == 0) or (move.end_row == 0 or move.end_row == 10):
				self.goldWin(window, True)
			if self.secondmove == 2:
				self.secondmove = 0
				self.Goldmove = not self.Goldmove #swap players
		elif move.piece_move == "Gf"or move.piece_move =="Sf":
			
			self.board[move.start_row][move.start_col] = "__"
			if self.board[move.end_row][move.end_col] != "__":
				
				self.piece_captured.append(self.board[move.end_row][move.end_col])
				if self.piece_captured[-1][1] == 'Gf':
					
					self.goldfleet-=1
					
				elif self.piece_captured[-1][1] == 'Sf':
					
					self.silverfleet -= 1
					
					if self.silverfleet == 0:
						self.goldwin(window, False)
				elif self.piece_captured[-1][1] == 'GB':
					self.silverwin(window)
				
			self.board[move.end_row][move.end_col] = move.piece_move
			
			self.movetrack.append(move)
			self.secondmove = self.secondmove + 1
			if move.piece_captured !="__":
				self.secondmove =2
			if self.secondmove == 2 :
				self.secondmove=0
				self.Goldmove = not self.Goldmove
			
	#undo the last move
	def undo_move(self):
		if len(self.movetrack) !=   0:
			move =self.movetrack.pop()
			self.board[move.start_row][move.start_col] = move.piece_move
			self.board[move.end_row][move.end_col] = move.piece_captured
			self.Goldmove = not self.Goldmove # switch to silver
	# consider valid moves
	def valid_moves(self):
		
		moves= self.possible_moves()# for now
		#for i in range(len(moves),-1,-1):
			#self.make_move((moves[i]))
		return moves
	def possible_moves(self):
		moves = []
		
		for r in range(len(self.board)):  # number of row
			for c in range(len(self.board[r])):  # number of col in the row
				turn = self.board[r][c][0]
				if (turn == "G" and self.Goldmove) or (turn == "S" and not self.Goldmove):
					piece = self.board[r][c][1]
					if piece == 'f':
						if self.secondmove == 1 :
							lastPiece = self.movetrack[-1]
							if r != lastPiece.end_row or c != lastPiece.end_col:  # avoid 2-times moving of the same piece
								self.function_move[piece](r, c, moves)
						else:

							self.function_move[piece](r, c, moves)# call move function
						
					else:
						self.function_move[piece](r, c, moves)
		return moves
		# moves = []
		# for r in range(len(self.board)):# number of row
		# 	for c in range(len(self.board[r])): # number of col in the row
		# 		turn = self.board[r][c][0]
		# 		if (turn == "G" and self.Goldmove)  or (turn == "S" and not self.Goldmove):
		# 			piece = self.board[r][c][1]
		# 			# call move function
		# 			if piece == "f":
		# 				if self.secondmove == 1:
		# 					lastpiece = self.movetrack[-1]
		# 					if r != lastpiece.end_row and c!= lastpiece.end_col:
		# 						self.function_move[piece](r,c,moves)
		# 				else:
		# 					self.function_move[piece](r,c,moves)
		# 			elif piece =="B" and self.secondmove == 0:
		# 				self.function_move[piece](r,c,moves)
						
						
	#get all the fleet moves add moves on list
	def fleet_moves(self,r,c,moves):
		
		directions = ((-1,0),(0,-1),(1,0),(0,1))
		colorenemy = "S" if self.Goldmove else "G"
		for d in directions:
			for i in range(1,11):
				endrow = r + d[0]*i
				endcol = c + d[1]*i
				if 0 <= endrow < 10 and 0 <= endcol <10:
					endpiece = self.board[endrow][endcol]
				#if self.Goldmove: # gold fleet moves
					
					if endpiece  == "__":
						moves.append(Moves((r,c),(endrow,endcol),self.board))
					elif self.secondmove==0:
						if self.board[r+1][c-1][0] == colorenemy :
							moves.append(Moves((r,c),(r+1,c-1),self.board))
							
						elif  self.board[r-1][c-1][0] == colorenemy :
							moves.append(Moves((r, c), (r - 1, c - 1),self.board))
							
						elif self.board[r - 1][c + 1][0] == colorenemy :
							moves.append(Moves((r, c), (r - 1, c + 1),self.board))
							
						elif self.board[r + 1][c + 1][0] == colorenemy :
							moves.append(Moves((r, c), (r + 1, c + 1),self.board))
							
						break
					else:break
					
				else:break
	
	def goldwin(self, window, bigship):
		if bigship:
			messagebox.showinfo("Gold player wins", "the bigship escaped from the silver fleet")
		else:
			messagebox.showinfo("Gold player wins", "the silver fleet was destroyed")
		window.deiconify()
		window.destroy()
		window.quit()
		self.state = False
	
	def silverwin(self, window):
		messagebox.showinfo("Silver player wins", "the bigship was captured")
		window.deiconify()
		window.destroy()
		window.quit()
		self.state = False
	
	# if c-1>= 0 :# captures to the up left
		# 	if self.board[r-1][c-1][0] == colorenemy:
		# 		moves.append(Moves((r,c),(r-1,c-1),self.board))
		# if c+1<=10:# captures up to right
		# 	if self.board[r-1][c+1][0] == colorenemy:
		# 		moves.append(Moves((r,c),(r-1,c+1),self.board))
		# if c - 1 >= 0:  # captures to the down left
		# 	if self.board[r+1][c-1][0] == colorenemy:
		# 		moves.append(Moves((r, c), (r+1, c-1), self.board))
		# if c + 1 <= 10:  # captures down to right
		# 	if self.board[r+1][c + 1][0] == colorenemy:
		# 		moves.append(Moves((r, c), (r + 1, c + 1), self.board))
		
	
	#def bigf_moves(self,r,c,moves):
	#	pass
	
class   Moves():
	#map keys to values
	ranks_to_rows = {"1":10,"2":9,"3":8, "4":7,"5":6,"6":5,"7":4,"8":3,"9":2,"10":1,"11":0}
	row_to_ranks = {v:k for k,v in ranks_to_rows.items()}
	ranks_to_cols = {"a":0,"b":1,"c":2, "d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9,"k":10}
	col_to_ranks = {v:k for k,v in ranks_to_cols.items()}
	
	def __init__(self,start_sq,end_sq,board):
		self.start_row = start_sq[0]
		self.start_col = start_sq[1]
		self.end_row = end_sq[0]
		self.end_col = end_sq[1]
		self.piece_move = board[self.start_row][self.start_col]
		self.piece_captured = board[self.end_row][self.end_col]
		self.IDmove = self.start_row*1000000+self.start_col*10000+self.end_row*100+self.end_col
		print(self.IDmove)
#overriding equal methods
	
	def __eq__(self,other):
		if  isinstance(other,Moves):
			return self.IDmove  ==  other.IDmove
		return False
	
	def get_notation(self):
		return self.get_rank(self.start_row,self.start_col)+self.get_rank(self.end_row,self.end_col)
	
	def get_rank(self,r,c):
		return self.col_to_ranks[c]+self.row_to_ranks[r]