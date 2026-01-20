import pickle

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41]

# suits:[Spades = 1, hearts = 2, diamons = 4, clubs =8]
SUITS = {
    "s": 0x1000, # Binary: 0001 0000 0000 0000
    "h": 0x2000, # Binary: 0010 0000 0000 0000
    "d": 0x4000, # Binary: 0100 0000 0000 0000
    "c": 0x8000  # Binary: 1000 0000 0000 0000
}

flush_lookup = pickle.load(open('data/flush_lookup.pkl', 'rb'))
unique_lookup = pickle.load(open('data/unique_lookup.pkl', 'rb'))

def make_card(rank_char,suit_char):
    # mapping the rank to integer values
    rank_map = {"2":0,"3":1,"4":2,"5":3,"6":4,"7":5,"8":6,"9":7,"10":8,"J":9,"Q":10,"K":11,"A":12}
    r = rank_map[rank_char]

    #Generating bit values
    prime = PRIMES[r]               # Bits 0-7 Used to create unique fingerprint for each card, through multiplication of primes
    rank_bits = r << 8              # Bits 8-11 # Used for in tiebreaking if a kicker is needed
    suit_bits = SUITS[suit_char]    # Bits 12-15 # Used for flush identification
    bitmask = (1 << (16 + r))       # Bits 16-31 # Used for straight identification
    
    # Combine them all into one 32-bit integer
    return prime | rank_bits | suit_bits | bitmask

def evaluate_hand(c1,c2,c3,c4,c5):
    # Flush Check
    # Suits are stored in bits 12-15, so & 0xF000 will detect
    if (c1 & c2 & c3 & c4 & c5 & 0xF000):
        # It is a flush
        # We OR the cards and shift them 16 bits right to see the card ranks present from our bitmask
        flush_mask = (c1 | c2 | c3 | c4 | c5) >> 16
        return flush_lookup[flush_mask]

        
    # Not a flush block
    # Prime multiplication 
    # extract the first 8 bits for the prime value and multiply them together
    prime_combination = (c1&0xFF) * (c2&0xFF) * (c3&0xFF) * (c4&0xFF) * (c5&0xFF)
    return unique_lookup[prime_combination]
