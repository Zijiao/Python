"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 20    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes current board and the next player to move,
    modifies the board till the game is over using Monte Carlo algorithm.
    """
    while(board.check_win() == None):
        empty_squares = board.get_empty_squares()
        move_square = empty_squares[random.randrange(len(empty_squares))]
        board.move(move_square[0], move_square[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    The function scores the completed board and updates the scores grid
    """
    board_dim = board.get_dim()
    winner = board.check_win()
    if winner == provided.DRAW:
        pass
    elif winner == player:
        for dummy_i in range(board_dim):
            for dummy_j in range(board_dim):
                if board.square(dummy_i, dummy_j) == player:
                    scores[dummy_i][dummy_j] += MCMATCH
                elif board.square(dummy_i, dummy_j) == provided.switch_player(player):
                    scores[dummy_i][dummy_j] -= MCOTHER
    else:
        for dummy_i in range(board_dim):
            for dummy_j in range(board_dim):
                if board.square(dummy_i, dummy_j) == player:
                    scores[dummy_i][dummy_j] -= MCMATCH
                elif board.square(dummy_i, dummy_j) == provided.switch_player(player):
                    scores[dummy_i][dummy_j] += MCOTHER

    
def get_best_move(board, scores):
    """
    return a tuple(row, col) related to an empty square on board and highest score in scores
    """
    board_dim = board.get_dim()
    
    max_score = -1000
    
    for dummy_i in range(board_dim):
        for dummy_j in range(board_dim):
            if scores[dummy_i][dummy_j] > max_score and board.square(dummy_i, dummy_j)== provided.EMPTY:
                max_score = scores[dummy_i][dummy_j]
            
    candidate_squares = []
    
    if len(board.get_empty_squares()) > 0:
        for dummy_i in range(board_dim):
            for dummy_j in range(board_dim):
                if board.square(dummy_i, dummy_j) == provided.EMPTY and scores[dummy_i][dummy_j] == max_score:
                    candidate_squares.append((dummy_i, dummy_j))
        return candidate_squares[random.randrange(len(candidate_squares))]
                    
def mc_move(board, player, trials):        
    """
    This function uses the Monte Carlo simulation to return a move for the machine player 
    in the form of a (row, column) tuple
    """
    board_dim = board.get_dim()
    board_clones = [0] * trials
    list_of_scores = [0] * trials
    temp_list1 = [0] * board_dim
    temp_list2 = [0] * 4
    for dummy_i in range(4):
        temp_list2[dummy_i] = temp_list1
    
    for dummy_i in range(trials):
        board_clones[dummy_i] = board.clone()
        list_of_scores[dummy_i] = temp_list2
    for dummy_i in range(trials):
        mc_trial(board_clones[dummy_i], player)
        mc_update_scores(list_of_scores[dummy_i], board_clones[dummy_i], player)
        
    list_of_scores_sum = [0] * trials
    for dummy_i in range(trials):
        temp_sum = 0
        for dummy_j in range(board_dim):
            temp_sum += sum(list_of_scores[dummy_i][dummy_j])
            list_of_scores_sum[dummy_i] = temp_sum
        
    max_scores_sum = max(list_of_scores_sum)
    candidate_scores = []
    for dummy_i in range(trials):
        if list_of_scores_sum[dummy_i] == max_scores_sum:
            candidate_scores.append(list_of_scores[dummy_i])
    the_scores = candidate_scores[random.randrange(len(candidate_scores))]
    
    return get_best_move(board, the_scores)


# Test game with the console or the GUI.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


