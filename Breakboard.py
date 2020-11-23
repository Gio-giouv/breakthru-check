import Breakthruengine
import pygame as p
import aimalon
import time
import sys
import os

Width = Height = 512  # or 400
Dimension = 11  # board 11x11
Sq_size = Height // Dimension
Max_Fps = 15  # for animation
Images = {}


def Load_image():
	pieces = ["Sf", "GB", "Gf"]
	for piece in pieces:
		Images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (Sq_size, Sq_size))


def main():
	p.init()
	screen = p.display.set_mode((Width, Height))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	GS = Breakthruengine.State_Game()
	validmoves = GS.valid_moves()
	moves_made = False  # flag when move is made
	
	# drawState_Game(screen, GS)
	Load_image()  # only once before loop
	running = True
	selected_sq = ()  # no square selected tuple:(row,col)
	players_click = []  # two tuples :
	AI = aimalon.AI("G")
	AI2 = aimalon.AI("S")
	AI2.ControlGold = False
	# messagebox part
	# window = Tk()
	# window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
	# window.withdraw()
	monitor = True
	
	while running and not GS.gwin and not GS.swin and not GS.draw:
		# drawState_Game(screen, GS)
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False

			elif GS.Goldmove and AI.ControlGold and monitor:
				monitor = False
				# #     # AI.evaluationFunction(validMoves,captureMoves)
				move = AI.AI_choose(GS, True)
				# print("move: ", move)
				print("AI1")
				GS.make_move(move)
				# if (GS.move.end_col == 10 or GS.move.end_col == 0) or (GS.move.end_row == 0 or GS.move.end_row == 10):
				# 	GS.gwin=True
				# 	print("gold win")
				moves_made = True
				selected_sq = ()  # reset
				players_click = []
			elif GS.Goldmove == False and AI2.ControlGold == False  and monitor:
				monitor = False
				print("\n aI2")
				#     # AI.evaluationFunction(validMoves,captureMoves)
				move = AI2.AI_choose(GS, True)
				GS.make_move(move)
				if GS.piece_captured=='GB':
					GS.swin=True
					print("silver win")
				moves_made = True
				selected_sq = ()  # reset
				players_click = []
			elif e.type == p.MOUSEBUTTONDOWN:
				Location = p.mouse.get_pos()  # (x,y) location of the mouse
				col = Location[0] // Sq_size
				row = Location[1] // Sq_size
				if selected_sq == (row, col):
					selected_sq = {}  # deselected
					players_click = []  # clear click
				else:
					selected_sq = (row, col)
					players_click.append(selected_sq)  # append 1st and 2nd click
				if len(players_click) == 2:  # after two clicks
					move = Breakthruengine.Moves(players_click[0], players_click[1], GS.board)
					print(move.get_notation())
					if move in validmoves:
						GS.make_move(move)
						moves_made = True
						if GS.piece_captured == 'GB':
							GS.swin=True
							print("silver win")
						selected_sq = ()  # reset clicks
						players_click = []
					else:
						players_click = [selected_sq]
			# key handler
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:  # undo when press z
					GS.undo_move()
					moves_made = True
		
		if moves_made:
			validmoves = GS.valid_moves()
			moves_made = False
			monitor = True
		screen.fill(p.Color("white"))
		drawState_Game(screen, GS, validmoves, selected_sq)
		clock.tick(Max_Fps)
		p.display.flip()


# graphics within acurrent game state
def drawState_Game(screen, GS, validmoves, selected_sq):
	drawBoard(screen)
	drawPieces(screen, GS.board)
	# squarecolor(screen, GS, validmoves, selected_sq, p.Color("yellow"))


# draw squares on board
def drawBoard(screen):
	colors = [p.Color("gray"), p.Color("gray")]
	for c in range(Dimension):
		for r in range(Dimension):
			color = colors[((r + c) % 2)]
			p.draw.rect(screen, color, p.Rect(c * Sq_size, r * Sq_size, Sq_size, Sq_size), 2)


# draw pieces on the board
def drawPieces(screen, board):
	for r in range(Dimension):
		for c in range(Dimension):
			piece = board[r][c]
			if piece != "__":  # not empty square
				screen.blit(Images[piece], p.Rect(c * Sq_size, r * Sq_size, Sq_size, Sq_size))


def squarecolor(screen, GS, validmoves, selected_sq, color):
	if selected_sq != ():
		r, c, = selected_sq
		if GS.board[r][c][0] == (
				'g' if GS.Goldmove else 's'):  # selected Square is a piece that can be moves
			s = p.Surface((Sq_size, Sq_size))
			s.set_alpha(100)  # transparency value -> 0 transparent 255 solid
			s.fill(p.Color('green'))
			screen.blit(s, (c * Sq_size, r * Sq_size))
			# highliht moves from that square
			s.fill(color)
			for move in validmoves:
				if move.start_row == r and move.start_col == c:  # all the moves that belong to the pawn in r,c
					screen.blit(s, (move.end_col * Sq_size, move.end_row * Sq_size))


if __name__ == "__main__":
	main()