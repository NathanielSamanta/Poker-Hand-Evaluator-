from Evaluator import make_card, evaluate_hand
import random
import itertools
import multiprocessing
import matplotlib.pyplot as plt

# Your  Hand
player_c1 = make_card("7", "c")
player_c2 = make_card("2", "c")
player_hand = [player_c1, player_c2]

players = 5
wins = 0
ties = 0

# Wrapper for 7 cards
def evaluate_7_cards(hole_cards, board_cards):
    all_7_cards = hole_cards + board_cards
    min_score = 9999
    for hand_combo in itertools.combinations(all_7_cards, 5):
        score = evaluate_hand(hand_combo[0],hand_combo[1],hand_combo[2],hand_combo[3],hand_combo[4])
        if score < min_score:
            min_score = score
    return min_score

# Helper to rebuild the deck fresh every time
def get_deck():
    suits_char = ["s","h","d","c"]
    ranks_char = ["2","3","4","5","6","7","8","9","10","J","Q","K", "A"]
    deck = [make_card(r, s) for r in ranks_char for s in suits_char]
    # Remove player cards
    deck.remove(player_c1)
    deck.remove(player_c2)
    return deck

def worker_task(N):
    wins = 0
    ties = 0
    for i in range(N):
        #Reset deck and suffle
        deck = get_deck()
        random.shuffle(deck)

        #Deal for players
        opponent_hands = []
        for _ in range(players - 1):
            # Pop 2 cards for each opponent
            op_hand = [deck.pop(), deck.pop()]
            opponent_hands.append(op_hand)

        #Deal board
        board = [deck.pop() for _ in range(5)]

        #player score
        player_score = evaluate_7_cards(player_hand, board)

        player_won = True
        is_tie = False

        for op_hand in opponent_hands:
            op_score = evaluate_7_cards(op_hand, board)
            
            if op_score < player_score: 
                # Opponent has a better score
                player_won = False
                break 
            elif op_score == player_score:
                is_tie = True
                
        # E. Track Results
        if player_won and not is_tie:
            wins += 1
        elif player_won and is_tie:
            ties += 1

    #Results
    return (wins + (ties / 2))
   
def calculate_probabilty(num_of_sims, multicore = True):
    print(f"Running {num_of_sims} simulations...")
    if multicore:
        num_of_cores = multiprocessing.cpu_count()
        sims_per_core = num_of_sims // num_of_cores
        
        # Create a pool of workers
        with multiprocessing.Pool(processes=num_of_cores) as pool:
            # Map the task to all cores
            results = pool.map(worker_task, [sims_per_core] * num_of_cores)

        total_wins = sum(results)

    else:
        total_wins = worker_task(num_of_sims)
    equity = total_wins / num_of_sims
    print(f"Total Equity: {equity*100}%")
    return equity


def expected_value(win_prob, pot, price_to_call):
    loss_prob = 1 - win_prob
    
    # Potential Profit is the money already in the pot.
    # Potential Loss is the bet you are about to risk.
    ev = (win_prob * pot) - (loss_prob * price_to_call)
    if ev > 0:
        decision = f"CALL (EV: +£{ev:.2f})"
    elif ev < 0:
        decision = f"FOLD (EV: -£{abs(ev):.2f})"
    else:
        decision = "BREAK-EVEN (EV: £0.00)"
        
    return decision


if __name__ == "__main__":
    num_of_sims = 100000
    win_prob = calculate_probabilty(num_of_sims)
    print(expected_value(win_prob, 1000, 250))
    