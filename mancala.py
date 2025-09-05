import numpy as np
import random
import sys

# Parses user input in the following format:
# "STATE <N> <p11> <p12> <p13> <p14> <p15> <p16> <p21> <p22> <p23> <p24> <p25> <p26> <p1S> <p2S> <turn> <player>"
def parse_input(in_str):
    in_state = in_str.rstrip().split(' ')
    state_array = np.ones(16, dtype=int)
    state_array[:6] = [int(x) for x in in_state[2:8]]
    state_array[7:13] = [int(x) for x in in_state[8:14]]
    state_array[6] = int(in_state[14])
    state_array[13] = int(in_state[15])
    state_array[14] = int(in_state[17])
    state_array[15] = int(in_state[16])
    return state_array

# Return the next state give a move
def next_state(state, move):
    state[15] += 1
    if(move == "PIE"): # Return flipped board if "PIE"
        state[14] = 1
        return PIE(state)
    
    if(state[14] == 2): # Flip board if p2
        state = PIE(state)
    
    rock_num = state[move - 1]
    for i in range(rock_num): # Sow rocks
        state[(move + i) % 13] += 1
    state[move - 1] -= rock_num

    if (move + rock_num) % 13 == 7: # Check for repeated turns, add 2 to player turn if yes
        state[14] += 2 
    
    if ((rock_num + move - 1) % 13 <= 5 and state[(rock_num + move - 1) % 13] == 1 and state[12 - ((rock_num + move - 1) % 13)] > 0): # Do captures
        state[6] += (state[(rock_num + move - 1) % 13] + state[12 - ((rock_num + move - 1) % 13)]) # Add rocks to p1's pit
        state[(rock_num + move - 1) % 13], state[12 - (rock_num + move - 1) % 13] = 0,0 # Remove captured rocks

    if(state[14] % 2 == 0): # Flip back if p2
        state = PIE(state)

    state = handle_end_game(state) # Checking if the game is over
    
    state[14] = state[14] - 2 if state[14] >= 3 else 3 - state[14] # Use state token to determine who's turn is next
    return state


# Checks if either player's side is empty. If it is then the other player gets their remaining stones
def handle_end_game(state):
    p1_rocks = sum(state[:6])
    p2_rocks = sum(state[7:13])
    if p1_rocks == 0:
        state[13] += p2_rocks # Add remaining rocks to p2's score
        for i in range(7, 13):
            state[i] = 0 # Delete the rocks from the board
    elif p2_rocks == 0:
        state[6] += p1_rocks # Add remaining rocks to p1's score
        for i in range(6):
            state[i] = 0 # Delete the rocks from the board
    return state

# Return True if the game is over
def check_end_game(state):
    p1_rocks = sum(state[:6])
    if p1_rocks == 0:
        return True
    return False


# Swaps the board
def PIE(state):
    temp = state[:7].copy()
    state[:7] = state[7:14]
    state[7:14] = temp
    return state

# Alphabeta implementation
def alphabeta(state, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or check_end_game(state):
        return heuristic(state), None  # Return heuristic value and no move
    
    best_move = None
    
    if maximizingPlayer:
        value = float('-inf')
        for child in [i + 1 for i in range(6) if state[i] != 0]:
            new_state = next_state(state.copy(), child)
            if new_state[14] == 1:
                evaluation, _ = alphabeta(new_state, depth - 1, alpha, beta, True) # Return eval if turn is repeated
            else:
                evaluation, _ = alphabeta(new_state, depth - 1, alpha, beta, False) # Return eval if turn isn't repeated

            if evaluation > value: # Update value
                value = evaluation
                best_move = child
            
            alpha = max(alpha, evaluation)
            if beta <= alpha: # Alpha cutoff
                break  

    else:
        value = float('inf')
        move_list = [i + 1 for i in range(6) if state[i + 7] != 0]
        if state[15] <= 3: # Add PIE to move_list if applicable
                move_list.append("PIE")
        for child in move_list:
            new_state = next_state(state.copy(), child)
            if new_state[14] == 2:
                evaluation, _ = alphabeta(new_state, depth - 1, alpha, beta, False) # Return eval if turn is repeated
            else:
                evaluation, _ = alphabeta(new_state, depth - 1, alpha, beta, True) # Return eval if turn isn't repeated
            
            if evaluation < value: # Update value
                value = evaluation
                best_move = child
            
            beta = min(beta, evaluation)
            if beta <= alpha:# Beta cutoff
                break  
    
    return value, best_move

# Helper function to run based on whether we are p1 or p2
def alphabeta_player(state):
    best_move = 0
    if state[-2] == 1:
        _, best_move = alphabeta(state, 7, float('-inf'), float('inf'), True)
    else:
        _, best_move = alphabeta(state, 7, float('-inf'), float('inf'), False)
    return best_move

# Heuristic function
def heuristic(state):
    return state[6] - state[13]  # Mancala heuristic: score difference

# Main method
def main():
    move = alphabeta_player(parse_input(input()))
    sys.stdout.write(str(move))

if __name__ == "__main__":
    main()