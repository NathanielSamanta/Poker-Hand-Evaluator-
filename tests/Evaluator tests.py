PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41]

# suits:[Spades = 1, hearts = 2, diamons = 4, clubs =8]
SUITS = {
    "s": 0x1000, # Binary: 0001 0000 0000 0000
    "h": 0x2000, # Binary: 0010 0000 0000 0000
    "d": 0x4000, # Binary: 0100 0000 0000 0000
    "c": 0x8000  # Binary: 1000 0000 0000 0000
}


def debug_card(card_int):
    prime = card_int & 0xFF
    rank_val = (card_int >> 8) & 0xF
    suit = (card_int >> 12) & 0xF
    bitmask = (card_int >> 16)
    
    print(f"Prime: {prime} (Rank index {PRIMES.index(prime)})")
    print(f"Rank Value Slot: {rank_val}")
    print(f"Suit Slot: {bin(suit)}")
    print(f"Bitmask: {bin(bitmask)}")

debug_card(0b10001000000000001)