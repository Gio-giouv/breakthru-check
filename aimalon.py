import time
from copy import deepcopy

import Breakthruengine



import gc

MAXDEPTH = 2

class AI():
    def __init__(self, player_turn):

        self.ControlGold = True
        self.maxDepth = MAXDEPTH
        self.player_turn = player_turn
        self.node_expanded = 0

    def AI_choose(self, GS, play):
        # def chooseMove(self, validMoves, captureMoves, gameState, play):
        gc.collect()
        """try to predict a move using minmax algorithm"""
        self.node_expanded = 0
    
        start_time = time.time()
    
        print("AI is thinking")
        # eval_score, selected_Action = self.miniMax(0, validMoves, captureMoves, gameState, play, True)
        eval_score, selected_Action = self.MinMax(0, GS, play, True)
        
        print("MINIMAX : Done, eval = %d, expanded %d" % (eval_score, self.node_expanded))
        print("--- %s seconds ---" % (time.time() - start_time))
        return (selected_Action)
    
    def EvaluationF(self,GS, Goldmove):
        """Evaluate the state to decide the most convenient move"""
        evaluate = 0


        if Goldmove:
            evaluate = (5 * GS.goldfleet*0.2 - 4 * GS.silverfleet*0.4 + 20 * GS.bigship*0.4)/100
        else:
            evaluate = (4 * GS.silverfleet*0.2 - 5 * GS.silverfleet*0.4  - 20 * GS.bigship*0.4)/100

        return evaluate

    def MinMax(self, depth, state, play, is_max_turn):  # , validMoves, captureMoves*/, ):
        GS = deepcopy(state)
        validmoves = GS.valid_moves()
        
       # cMoves = len(captureMoves)
        if depth == self.maxDepth or not play:
            return self.EvaluationF(state, GS.Goldmove),""
        self.node_expanded += 1
       
        best_value = -1000 if is_max_turn else 1000
        action_target = ""
        for action in validmoves:
            new_gameState = self.next_state(action, GS)
            print(new_gameState)
            eval_child = self.MinMax(depth +1, new_gameState, play,not is_max_turn)
            print(eval_child)
            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action
        # print("ci arriva", action_target)
        del new_gameState
        return best_value, action_target

    def next_state(self, move, GS):
        """return the new state after executing the move"""
        # window = Tk()
        # window.eval("tk::PlaceWindow %s center" % window.winfo_toplevel())
        # window.withdraw()
        nextGS = deepcopy(GS)
        nextGS.DEBUG = False
        nextGS.make_move(move)
        return nextGS
    