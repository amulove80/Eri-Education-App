#!/usr/bin/env python3
"""
COMMUNITY-DRIVEN SOLVER
Based on extensive community research and specific word identifications
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Community's most confident words (from multiple sources)
COMMUNITY_CONSENSUS = {
    "certain": ["moon", "tower", "food", "this", "subject", "real", "black", "only"],
    "very_likely": ["time", "proof", "world", "one"],
    "probable": ["brave", "new", "order", "liberty", "eye", "pyramid", "mask", "camera"],
}

# Specific sequences mentioned in community analysis
COMMUNITY_SEQUENCES = [
    # From GitHub analysis table (position-based)
    ["subject", "camera", "tower", "mask", "black", "liberty", "eye", "pyramid", "moon", "real", "food", "only"],
    
    # High confidence first
    ["moon", "tower", "food", "black", "this", "subject", "real", "only", "time", "proof", "world", "one"],
    
    # Alphabetical of certain words
    ["black", "food", "moon", "only", "real", "subject", "this", "tower", "time", "proof", "world", "one"],
    
    # Timeline: pre-pandemic → pandemic → BLM → election
    ["world", "time", "food", "tower", "moon", "subject", "this", "black", "real", "proof", "only", "one"],
    
    # Brave New World theme first
    ["brave", "new", "world", "order", "moon", "tower", "food", "this", "subject", "real", "time", "proof"],
]

def test_with_variations(words_12, name=""):
    """Test a sequence with multiple variations"""
    tested = 0
    
    phrase = " ".join(words_12)
    
    # Variations to test
    tests = [
        (phrase, ""),
        (phrase, "BREATHE"),
        (phrase, "breathe"),
        (phrase, "Breathe"),
        (phrase, "brave"),
        (phrase, "BRAVE"),
        (phrase, "2020"),
        (phrase, "brave new world"),
    ]
    
    for test_phrase, passphrase in tests:
        try:
            Bip39MnemonicValidator().Validate(test_phrase)
            seed_bytes = Bip39SeedGenerator(test_phrase, passphrase).Generate()
            bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            address = bip44_acc.PublicKey().ToAddress()
            
            if address == TARGET_ADDRESS:
                print(f"\n{'='*70}")
                print(f"🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
                print("="*70)
                print(f"Name: {name}")
                print(f"Seed: {test_phrase}")
                if passphrase:
                    print(f"Passphrase: {passphrase}")
                print(f"Address: {address}")
                print("="*70)
                return True
            
            tested += 1
        except:
            pass
    
    return False

def test_community_sequences():
    """Test sequences identified by community"""
    print("="*70)
    print("TESTING COMMUNITY-IDENTIFIED SEQUENCES")
    print("="*70)
    
    for i, seq in enumerate(COMMUNITY_SEQUENCES, 1):
        print(f"\nSequence {i}: {' '.join(seq[:6])}...")
        if test_with_variations(seq, f"Community Sequence {i}"):
            return True
    
    return False

def test_certain_words_permutations():
    """Test permutations of only the 'certain' words + fill"""
    print("\n" + "="*70)
    print("TESTING CERTAIN WORDS WITH FILLERS")
    print("="*70)
    
    certain = COMMUNITY_CONSENSUS["certain"]
    fillers = COMMUNITY_CONSENSUS["very_likely"]
    
    print(f"Certain words ({len(certain)}): {certain}")
    print(f"Fillers ({len(fillers)}): {fillers}\n")
    
    # Need 12 total
    needed = 12 - len(certain)
    
    if needed > 0:
        for fill_combo in itertools.combinations(fillers, min(needed, len(fillers))):
            words_12 = list(certain) + list(fill_combo)
            if len(words_12) == 12:
                # Test a few permutations
                for perm_num, perm in enumerate(itertools.permutations(words_12)):
                    if perm_num > 100:  # Limit permutations
                        break
                    if test_with_variations(list(perm), f"Certain+Fill Perm {perm_num}"):
                        return True
                    
                    if perm_num % 20 == 0 and perm_num > 0:
                        print(f"  Tested {perm_num} permutations...")
    
    return False

def test_specific_word_replacements():
    """Try replacing specific words that might be wrong"""
    print("\n" + "="*70)
    print("TESTING WORD REPLACEMENTS")
    print("="*70)
    
    # Base sequence (most likely)
    base = ["moon", "tower", "food", "this", "subject", "real", "black", "only", "time", "proof", "world", "one"]
    
    # Words that might replace others
    replacements = {
        "black": ["brave", "order", "chain", "liberty"],
        "only": ["order", "liberty", "eye"],
        "world": ["new", "brave", "order"],
        "one": ["new", "eye", "pyramid"],
    }
    
    print("Testing word replacements in base sequence...\n")
    
    for word_to_replace, alternatives in replacements.items():
        for alt in alternatives:
            new_seq = [alt if w == word_to_replace else w for w in base]
            print(f"  Trying: replace '{word_to_replace}' with '{alt}'")
            if test_with_variations(new_seq, f"Replace {word_to_replace}->{alt}"):
                return True
    
    return False

def test_all_12_word_combinations_from_top_words():
    """Test all combinations of top 15 words"""
    print("\n" + "="*70)
    print("TESTING ALL COMBINATIONS OF TOP 15 WORDS")
    print("="*70)
    
    top_15 = (COMMUNITY_CONSENSUS["certain"] + 
              COMMUNITY_CONSENSUS["very_likely"] + 
              ["brave", "new", "order"])[:15]
    
    print(f"Top 15 words: {top_15}\n")
    
    tested = 0
    max_tests = 50000
    
    # Test all ways to choose 12 from 15
    from math import factorial
    total_combos = factorial(15) // (factorial(12) * factorial(3))
    print(f"Total combinations: {total_combos}")
    print(f"Will test up to {max_tests} (with permutation sampling)\n")
    
    for combo in itertools.combinations(top_15, 12):
        if tested >= max_tests:
            break
        
        # Test a few permutations of each combo
        for perm_num, perm in enumerate(itertools.permutations(combo)):
            if perm_num > 5:  # Just 5 perms per combo
                break
            
            if test_with_variations(list(perm), f"Top15 Combo {tested}"):
                return True
            
            tested += 1
            if tested >= max_tests:
                break
            
            if tested % 5000 == 0:
                print(f"  Tested {tested} combinations...")
    
    print(f"Tested {tested} total combinations")
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              COMMUNITY-DRIVEN COMPREHENSIVE SOLVER           ║
║                                                              ║
║  Based on extensive community research                       ║
║  Testing most likely words and sequences                     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    import time
    start = time.time()
    
    strategies = [
        test_community_sequences,
        test_specific_word_replacements,
        test_certain_words_permutations,
        test_all_12_word_combinations_from_top_words,
    ]
    
    for strategy in strategies:
        if strategy():
            print(f"\n✅ Found in {time.time() - start:.2f}s")
            return
    
    print(f"\n{'='*70}")
    print(f"All strategies completed in {time.time() - start:.2f}s")
    print(f"No solution found")
    print("="*70)

if __name__ == "__main__":
    main()
