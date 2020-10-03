

import pygame as p
from Breakthru import Breakthruengine


Width = Height= 512 #or 400
Dimension= 11 #board 11x11
Sq_size =Height // Dimension
Max_Fps=15# for animation
Images = {}

def Load_image():
	pieces= [ "Sf", "Gf","GfB"]
	for piece in pieces:
		Images[piece] = p.transform.scale(p.image.load("images/"+ piece +".png"),(Sq_size,Sq_size))
	
def main():
	
	p.init()
	screen = p.display.set_mode((Width,Height))
	clock =p.time.Clock()
	screen.fill(p.Color("white"))
	GS = Breakthruengine.State_Game()
	validmoves = GS.valid_moves()
	moves_made =False # flag when move is made
	
	#drawState_Game(screen, GS)
	Load_image()# only once before loop
	running = True
	selected_sq = {} #no square selected tuple:(row,col)
	players_click =[]# two tuples :
	while running :
		#drawState_Game(screen, GS)
		for e in p.event.get():
			if e.type == p.QUIT:
				running =False
				#mouse handler
			elif e.type == p.MOUSEBUTTONDOWN:
				Location = p.mouse.get_pos()#(x,y) location of the mouse
				col = Location[0]//Sq_size
				row = Location[1]//Sq_size
				if selected_sq == (row,col):
					selected_sq ={}#deselected
					players_click = []# clear click
				else:
					selected_sq = (row,col)
					players_click.append(selected_sq)  # append 1st and 2nd click
				if len(players_click) == 2 :# after two clicks
					move = Breakthruengine.Moves(players_click[0],players_click[1],GS.board)
					print(move.get_notation())
					for i in range(len(validmoves)):
						if move == validmoves[i]:
							GS.make_move(validmoves[i])
							moves_made = True
							selected_sq =()#reset clicks
							players_click = []
			#key handler
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z: # undo when press z
					GS.undo_move()
					moves_made = True
		if moves_made:
			validmoves = GS.valid_moves()
			moves_made = False
		
		screen.fill(p.Color("white"))
		drawState_Game(screen,GS)
		clock.tick(Max_Fps)
		p.display.flip()
	 


#graphics within acurrent game state
def drawState_Game(screen,GS):
	drawBoard(screen)
	drawPieces(screen ,GS.board)

#draw squares on board
def drawBoard(screen):
	colors=[p.Color("gray"),p.Color("gray")]
	for c in range(Dimension):
		for r in range(Dimension):
			color = colors[((r+c)%2)]
			p.draw.rect(screen,color,p.Rect(c*Sq_size,r*Sq_size,Sq_size,Sq_size),2)
#draw pieces on the board
def drawPieces(screen,board):
	for r in range(Dimension):
		for c in range(Dimension):
			piece = board[r][c]
			if piece != "__" : #not empty square
				screen.blit(Images[piece],p.Rect(c*Sq_size,r*Sq_size,Sq_size,Sq_size))

if __name__ == "__main__":
	main()