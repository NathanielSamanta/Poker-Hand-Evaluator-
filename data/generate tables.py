import itertools
import pickle # Used to save the dictionary to a file

# FIX 1: Primes must start at 2
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

SUITS = {
    "s": 0x1000, 
    "h": 0x2000, 
    "d": 0x4000, 
    "c": 0x8000
}

def make_card(rank_char, suit_char):
    # Updated map to match your loop list (using "10" instead of "T")
    rank_map = {"2":0,"3":1,"4":2,"5":3,"6":4,"7":5,"8":6,"9":7,"10":8,"J":9,"Q":10,"K":11,"A":12}
    r = rank_map[rank_char]

    prime = PRIMES[r]
    rank_bits = r << 8
    suit_bits = SUITS[suit_char]
    bitmask = (1 << (16 + r))
    return prime | rank_bits | suit_bits | bitmask

def get_score(ranks, suits):
    """
    Returns a tuple: (Category Score, Kickers)
    Lower Category Score is Better (1 = Straight Flush, 9 = High Card)
    """
    # Check for Flush
    is_flush = len(set(suits)) == 1

    # Check for Straight
    # distinct_ranks is sorted high-to-low
    distinct_ranks = sorted(list(set(ranks)), reverse=True)
    is_straight = False
    
    if len(distinct_ranks) == 5:
        # Standard Straight (e.g., 6,5,4,3,2)
        if distinct_ranks[0] - distinct_ranks[4] == 4:
            is_straight = True
        # Wheel Straight (A, 5, 4, 3, 2) -> A=12, 5=3...
        elif distinct_ranks == [12, 3, 2, 1, 0]:
            is_straight = True
            # Treat Ace as low for sorting purposes
            distinct_ranks = [3, 2, 1, 0, -1]

    # Count duplicates (for Pairs/Full House)
    # counts values will be like [4, 1] for Quads, [3, 2] for Full House
    counts = sorted([ranks.count(r) for r in set(ranks)], reverse=True)

    #Scores
    if is_flush and is_straight:
        return (1, distinct_ranks)
    if counts == [4, 1]:         
        # Get the quad rank and the kicker rank
        quad_rank = [r for r in set(ranks) if ranks.count(r) == 4][0]
        kicker = [r for r in set(ranks) if ranks.count(r) == 1][0]
        return (2, [quad_rank, kicker])
        
    if counts == [3, 2]:
        trip_rank = [r for r in set(ranks) if ranks.count(r) == 3][0]
        pair_rank = [r for r in set(ranks) if ranks.count(r) == 2][0]
        return (3, [trip_rank, pair_rank])
        
    if is_flush:                 return (4, distinct_ranks)

    if is_straight:              return (5, distinct_ranks)
    
    if counts == [3, 1, 1]:
        trip_rank = [r for r in set(ranks) if ranks.count(r) == 3][0]
        kickers = sorted([r for r in set(ranks) if ranks.count(r) == 1], reverse=True)
        return (6, [trip_rank] + kickers)
        
    if counts == [2, 2, 1]:
        pairs = sorted([r for r in set(ranks) if ranks.count(r) == 2], reverse=True)
        kicker = [r for r in set(ranks) if ranks.count(r) == 1][0]
        return (7, pairs + [kicker])
        
    if counts == [2, 1, 1, 1]:
        pair_rank = [r for r in set(ranks) if ranks.count(r) == 2][0]
        kickers = sorted([r for r in set(ranks) if ranks.count(r) == 1], reverse=True)
        return (8, [pair_rank] + kickers)
        
    return (9, distinct_ranks)

def generate_tables():
    #Generating deck
    print("Generating Cards")
    suits_char = ["s","h","d","c"]
    ranks_char = ["2","3","4","5","6","7","8","9","10","J","Q","K", "A"]
    deck = [make_card(r, s) for r in ranks_char for s in suits_char]
    print("Generated cards")

    #Iterating through hands 
    all_hands = []
    print("Starting card iteration")

    for combo in itertools.combinations(deck, 5):
        # 1. Unpack data
        ranks = [(c >> 8) & 0xF for c in combo]
        suits = [(c >> 12) & 0xF for c in combo]
        
        # 2. Calculate Keys
        prime_prod = 1
        bitmask = 0
        for c in combo:
            prime_prod *= (c & 0xFF)
            bitmask |= (c >> 16)

        category_data = get_score(ranks, suits)
        
        all_hands.append({
            "prime_product": prime_prod,
            "bitmask": bitmask,
            "is_flush": len(set(suits)) == 1,
            "sort_key": category_data # (Category, [Kickers])
        })
        
    print("Finished card iteration")

    #Sorting hands
    #Sorted by category descending, kicker acsending 

    print("sorting hands")
    all_hands.sort(key=lambda x: (x["sort_key"][0], [-k for k in x["sort_key"][1]]))
    print("Hands sorted")

    print("Ranking hands (1-7462)")
    
    flush_lookup = {}
    unique_lookup = {}
    
    current_rank = 1

    for i in range(1, len(all_hands)):
        hand = all_hands[i]
        
        # Check if this hand is different from the previous one
        # (Tie-breaking logic: same cards = same rank)
        if i > 0:
            prev_hand = all_hands[i-1]
            if hand["sort_key"] != prev_hand["sort_key"]:
                current_rank += 1
        
        # Store in the appropriate table
        if hand["is_flush"]:
            flush_lookup[hand["bitmask"]] = current_rank
        else:
            unique_lookup[hand["prime_product"]] = current_rank

    print(f"Ranking finished. Max Rank: {current_rank} (Should be 7462)")
    print("Saving files")

    # Save to files
    with open("data/flush_lookup.pkl", "wb") as f:
        pickle.dump(flush_lookup, f)
    with open("data/unique_lookup.pkl", "wb") as f:
        pickle.dump(unique_lookup, f)
        
    print("Files saved.")

if __name__ == "__main__":
    generate_tables()
