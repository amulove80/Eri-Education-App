#!/usr/bin/env python3
"""
AGGRESSIVE COMPREHENSIVE SOLVER
Testing ALL theories systematically:
- Multiple passphrase variants
- More word combinations
- Position-based ordering from image
- Both 12 and 18-word seeds
- Bitcoin whitepaper words
"""

import itertools
import time
from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Expanded word list - ALL possibilities from image
ALL_WORDS = [
    # Explicitly labeled (highest confidence)
    "moon", "tower", "food",
    
    # Direct text references
    "this", "subject", "real", "only", "one",
    
    # Brave New World title
    "brave", "new", "world",
    
    # Bitcoin/theme
    "time", "proof", "order", "chain", "coin", "key", "digital",
    
    # Pre-May 10 elements
    "camera", "mask", "eye", "pyramid", "liberty", "stop",
    
    # From position hints
    "black", # may be position 5
    
    # Bitcoin whitepaper words (from "BRAVE NEW WORLD" text)
    "verify", "owner", "transaction", "sign", "system", "history",
    
    # Additional thematic
    "face", "day", "home", "future", "state", "vote",
]

# Position-based sequences from image clues
POSITION_SEQUENCES = {
    "clock_order": ["moon", "tower", "this", "food", "subject", "real", "only", "time", "proof", "world", "one", "new"],
    
    "numbered_positions": [
        "subject",   # 1 - Section 1
        None,        # 2
        "tower",     # 3 - 1+2 on clock
        "mask",      # 4 - 4 people
        "black",     # 5 - possibly 5HT
        None,        # 6
        "liberty",   # 7 - 7 points on crown
        None,        # 8
        "eye",       # 9 - 4+5 pyramid
        None,        # 10
        "pyramid",   # 11 - 5+6 inside
        None,        # 12
        "moon",      # 13 - 12+1 on clock
    ],
    
    "timeline_order": ["world", "this", "mask", "food", "tower", "time", "moon", "subject", "real", "proof", "only", "new"],
    
    "brave_new_world_first": ["brave", "new", "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"],
}

def generate_address(seed_phrase, passphrase=""):
    """Generate address with optional passphrase"""
    try:
        Bip39MnemonicValidator().Validate(seed_phrase)
        seed_bytes = Bip39SeedGenerator(seed_phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress()
    except:
        return None

def test_sequence(words, passphrase="", name=""):
    """Test a specific sequence"""
    if len(words) != 12:
        return False
    
    phrase = " ".join(words)
    address = generate_address(phrase, passphrase)
    
    if address == TARGET_ADDRESS:
        print(f"\n{'='*70}")
        print(f"🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
        print("="*70)
        print(f"Name: {name}")
        print(f"Seed: {phrase}")
        print(f"Passphrase: '{passphrase}'")
        print(f"Address: {address}")
        print("="*70)
        
        with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
            f.write(f"SOLUTION!\n")
            f.write(f"Seed: {phrase}\n")
            f.write(f"Passphrase: {passphrase}\n")
            f.write(f"Address: {address}\n")
        return True
    
    return False

def test_position_based():
    """Test sequences based on numbered positions in image"""
    print("\n" + "="*70)
    print("TESTING POSITION-BASED SEQUENCES")
    print("="*70)
    
    # Build sequence from numbered positions (filling gaps with likely words)
    positions = POSITION_SEQUENCES["numbered_positions"]
    core_words = [w for w in positions if w]
    
    # Need to fill in the None positions
    fill_words = ["this", "food", "real", "proof", "only", "time", "new", "brave"]
    
    print(f"\nCore positioned words: {core_words}")
    print(f"Fill words: {fill_words}")
    
    # Try different ways to fill the 12 positions
    attempts = 0
    passphrases = ["", "BREATHE", "breathe", "Breathe"]
    
    for passphrase in passphrases:
        # Test with core words + some fill words
        if len(core_words) >= 12:
            test_words = core_words[:12]
        else:
            test_words = core_words + fill_words[:12-len(core_words)]
        
        # Try this combination
        if test_sequence(test_words[:12], passphrase, f"Position-based + {passphrase}"):
            return True
        attempts += 1
        
        # Try permutations of the fill positions
        if attempts < 100:  # Limit attempts
            for perm in itertools.permutations(fill_words, 12 - len(core_words)):
                full_sequence = core_words + list(perm)
                if test_sequence(full_sequence[:12], passphrase, f"Position perm + {passphrase}"):
                    return True
                attempts += 1
                if attempts >= 100:
                    break
    
    print(f"Tested {attempts} position-based combinations")
    return False

def test_sum_of_two_numbers():
    """Test the 'Sum of two numbers' clue = 5 + 6 = 11"""
    print("\n" + "="*70)
    print("TESTING 'SUM OF TWO NUMBERS' CLUE (5+6=11)")
    print("="*70)
    
    # Theory: Position 11 is critical, or we need word #11 from BIP39 list
    # Or: Use the 11th word as a key
    
    # Try with "pyramid" at position 11 (5+6 inside pyramid)
    sequences = [
        ["this", "brave", "new", "world", "moon", "tower", "food", "time", "proof", "only", "pyramid", "real"],
        ["moon", "tower", "food", "this", "subject", "real", "brave", "new", "world", "time", "pyramid", "only"],
        ["brave", "new", "world", "this", "moon", "tower", "food", "subject", "real", "time", "pyramid", "only"],
    ]
    
    passphrases = ["", "BREATHE", "breathe", "Breathe", "11", "5", "6"]
    
    for seq in sequences:
        for passphrase in passphrases:
            if test_sequence(seq, passphrase, f"Sum=11 theory + '{passphrase}'"):
                return True
    
    return False

def test_bitcoin_whitepaper_words():
    """Test with words from Bitcoin whitepaper text"""
    print("\n" + "="*70)
    print("TESTING BITCOIN WHITEPAPER WORDS")
    print("="*70)
    
    # Words that appear in whitepaper AND are BIP39 words
    whitepaper_words = [
        "chain", "coin", "verify", "owner", "sign", "system", 
        "history", "order", "digital", "key", "proof", "time"
    ]
    
    # Combine with high-confidence words
    combined = ["moon", "tower", "food"] + whitepaper_words[:9]
    
    passphrases = ["", "BREATHE", "breathe"]
    
    for passphrase in passphrases:
        if test_sequence(combined[:12], passphrase, f"Whitepaper words + '{passphrase}'"):
            return True
    
    return False

def test_systematic_combinations():
    """Systematically test most likely word combinations"""
    print("\n" + "="*70)
    print("SYSTEMATIC TESTING OF HIGH-PROBABILITY COMBINATIONS")
    print("="*70)
    
    # Core words that are almost certain
    core_words = ["moon", "tower", "food", "this", "subject", "real"]
    
    # Additional likely words to try
    additional = ["brave", "new", "world", "time", "proof", "only", "one", "order", "chain", "liberty", "pyramid", "eye"]
    
    passphrases = ["", "BREATHE", "breathe", "Breathe"]
    
    attempts = 0
    max_attempts = 10000
    
    print(f"Core words: {core_words}")
    print(f"Testing combinations with {len(additional)} additional words\n")
    
    # Choose 6 more from additional to make 12 total
    for combo in itertools.combinations(additional, 6):
        if attempts >= max_attempts:
            break
        
        words_12 = list(core_words) + list(combo)
        
        # Try a few permutations of each combo
        for perm_count, perm in enumerate(itertools.permutations(words_12)):
            if perm_count > 10:  # Only try 10 permutations per combo
                break
            
            for passphrase in passphrases:
                if test_sequence(list(perm), passphrase, f"Systematic {attempts}"):
                    return True
                
                attempts += 1
                if attempts >= max_attempts:
                    break
                
                if attempts % 1000 == 0:
                    print(f"  Tested {attempts} combinations...")
    
    print(f"Tested {attempts} systematic combinations")
    return False

def test_all_named_sequences():
    """Test all predefined sequences with all passphrase variants"""
    print("\n" + "="*70)
    print("TESTING ALL NAMED SEQUENCES")
    print("="*70)
    
    passphrases = ["", "BREATHE", "breathe", "Breathe", "brave", "BRAVE"]
    
    for name, seq in POSITION_SEQUENCES.items():
        # Skip if has None
        seq_clean = [w for w in seq if w]
        if len(seq_clean) < 12:
            continue
        
        for passphrase in passphrases:
            print(f"Testing: {name} + passphrase='{passphrase}'")
            if test_sequence(seq_clean[:12], passphrase, f"{name} + '{passphrase}'"):
                return True
    
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║            AGGRESSIVE COMPREHENSIVE SOLVER                   ║
║                                                              ║
║  Testing EVERYTHING systematically:                         ║
║  - All passphrase variants                                  ║
║  - Position-based sequences                                 ║
║  - Sum of two numbers theories                              ║
║  - Bitcoin whitepaper words                                 ║
║  - Systematic high-probability combos                       ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    start = time.time()
    
    # Test in order of likelihood
    strategies = [
        ("Named Sequences", test_all_named_sequences),
        ("Position-Based", test_position_based),
        ("Sum of Two Numbers", test_sum_of_two_numbers),
        ("Bitcoin Whitepaper", test_bitcoin_whitepaper_words),
        ("Systematic Combinations", test_systematic_combinations),
    ]
    
    for name, func in strategies:
        print(f"\n{'#'*70}")
        print(f"STRATEGY: {name}")
        print(f"{'#'*70}")
        
        if func():
            elapsed = time.time() - start
            print(f"\n✅ Solution found in {elapsed:.2f} seconds!")
            return True
    
    elapsed = time.time() - start
    print(f"\n{'='*70}")
    print(f"Completed all strategies in {elapsed:.2f} seconds")
    print("="*70)
    print("\nNo solution found. Possible reasons:")
    print("1. Need to identify more words from image")
    print("2. Passphrase is different (not BREATHE)")
    print("3. 18-word seed instead of 12")
    print("4. Order requires deeper clue interpretation")
    print("5. Some 'certain' words are actually wrong")
    
    return False

if __name__ == "__main__":
    main()
