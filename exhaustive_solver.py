#!/usr/bin/env python3
"""
EXHAUSTIVE SOLVER - Test systematically until solution found
Using ONLY valid BIP39 words
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import time
import random

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# All 38 confirmed valid BIP39 words
VALID_WORDS = [
    "black", "brave", "camera", "change", "coin", "day", "digital", "eye", 
    "face", "food", "future", "history", "home", "key", "liberty", "mask", 
    "moon", "one", "only", "order", "owner", "peace", "picture", "proof", 
    "pyramid", "real", "sign", "state", "subject", "system", "this", "time", 
    "tower", "verify", "virus", "vote", "weapon", "world"
]

# Most likely subset (top candidates)
TOP_20 = [
    "moon", "tower", "food", "this", "subject", "real", "black", "only",
    "time", "proof", "world", "one", "brave", "order", "liberty", "eye",
    "pyramid", "mask", "camera", "peace"
]

# Passphrases to try
PASSPHRASES = ["", "BREATHE", "breathe", "Breathe"]

def test_phrase(phrase, passphrase=""):
    """Fast test without verbose output"""
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress() == TARGET_ADDRESS
    except:
        return False

def found_solution(phrase, passphrase=""):
    """Report solution"""
    print(f"\n\n{'='*70}")
    print(f"🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
    print("="*70)
    print(f"Seed: {phrase}")
    if passphrase:
        print(f"Passphrase: {passphrase}")
    print(f"Address: {TARGET_ADDRESS}")
    print("="*70)
    
    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
        f.write(f"SOLUTION!\n")
        f.write(f"Seed: {phrase}\n")
        f.write(f"Passphrase: {passphrase}\n")
        f.write(f"Address: {TARGET_ADDRESS}\n")
    return True

def strategy_1_top_12_permutations():
    """Test permutations of top 12 words"""
    print("\n" + "="*70)
    print("STRATEGY 1: Testing permutations of top 12 most likely words")
    print("="*70)
    
    top_12 = TOP_20[:12]
    print(f"Words: {', '.join(top_12)}\n")
    
    tested = 0
    start = time.time()
    
    # Sample permutations (can't test all 479M)
    for perm_num, perm in enumerate(itertools.permutations(top_12)):
        if perm_num >= 50000:  # Test 50k permutations
            break
        
        phrase = " ".join(perm)
        
        for pp in PASSPHRASES:
            if test_phrase(phrase, pp):
                return found_solution(phrase, pp)
            tested += 1
        
        if tested % 5000 == 0:
            elapsed = time.time() - start
            print(f"  Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s | Time: {elapsed:.1f}s")
    
    print(f"Strategy 1 complete: {tested:,} tested\n")
    return False

def strategy_2_all_combinations():
    """Test all ways to choose 12 from top 20"""
    print("\n" + "="*70)
    print("STRATEGY 2: All combinations of 12 from top 20 words")
    print("="*70)
    
    from math import factorial
    n_combos = factorial(20) // (factorial(12) * factorial(8))
    print(f"Total combinations: {n_combos:,}")
    print(f"Testing each with multiple permutations...\n")
    
    tested = 0
    start = time.time()
    
    for combo_num, combo in enumerate(itertools.combinations(TOP_20, 12)):
        # Test 10 random permutations per combo
        combo_list = list(combo)
        
        for _ in range(10):
            random.shuffle(combo_list)
            phrase = " ".join(combo_list)
            
            for pp in PASSPHRASES:
                if test_phrase(phrase, pp):
                    return found_solution(phrase, pp)
                tested += 1
        
        if tested % 5000 == 0:
            elapsed = time.time() - start
            print(f"  Tested: {tested:,} | Combos: {combo_num:,} | Rate: {tested/elapsed:.0f}/s")
    
    print(f"Strategy 2 complete: {tested:,} tested\n")
    return False

def strategy_3_fixed_positions():
    """Fix certain words and vary others"""
    print("\n" + "="*70)
    print("STRATEGY 3: Fixed high-confidence words with variations")
    print("="*70)
    
    # These are almost certain
    fixed = ["moon", "tower", "food", "this", "subject", "real"]
    variable = ["black", "only", "time", "proof", "world", "one", "brave", "order", 
                "liberty", "eye", "pyramid", "mask", "peace", "camera"]
    
    print(f"Fixed: {', '.join(fixed)}")
    print(f"Choosing 6 from: {', '.join(variable)}\n")
    
    tested = 0
    start = time.time()
    
    # Choose 6 from variable to make 12 total
    for combo in itertools.combinations(variable, 6):
        words_12 = list(fixed) + list(combo)
        
        # Test some permutations
        for perm_num, perm in enumerate(itertools.permutations(words_12)):
            if perm_num >= 20:  # 20 perms per combo
                break
            
            phrase = " ".join(perm)
            
            for pp in PASSPHRASES:
                if test_phrase(phrase, pp):
                    return found_solution(phrase, pp)
                tested += 1
            
            if tested % 5000 == 0:
                elapsed = time.time() - start
                print(f"  Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s")
    
    print(f"Strategy 3 complete: {tested:,} tested\n")
    return False

def strategy_4_specific_patterns():
    """Test specific patterns from image clues"""
    print("\n" + "="*70)
    print("STRATEGY 4: Specific patterns based on image clues")
    print("="*70)
    
    patterns = [
        # "this" first (THIS IS THE FIRST...)
        ["this"] + ["moon", "tower", "food", "subject", "real", "black", "only", "time", "proof", "world", "one"],
        
        # brave first  
        ["brave"] + ["moon", "tower", "food", "this", "subject", "real", "black", "only", "time", "proof", "world"],
        
        # moon tower first (clock hands)
        ["moon", "tower"] + ["food", "this", "subject", "real", "black", "only", "time", "proof", "world", "one"],
        
        # With "news" or "renew" (NEW alternative)
        ["brave", "news", "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"],
        ["brave", "renew", "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"],
        
        # With "story" (STOP alternative)
        ["story", "moon", "tower", "food", "this", "subject", "real", "black", "time", "proof", "world", "only"],
        
        # Different endings
        ["moon", "tower", "food", "this", "subject", "real", "black", "only", "time", "proof", "world", "brave"],
        ["moon", "tower", "food", "this", "subject", "real", "black", "only", "time", "proof", "world", "order"],
    ]
    
    # Try to add news/renew to patterns
    for word in ["news", "renew"]:
        with open("/workspace/bip39_wordlist.txt", "r") as f:
            if word in [w.strip() for w in f]:
                patterns.append(["brave", word, "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"])
    
    tested = 0
    
    for i, pattern in enumerate(patterns, 1):
        if len(pattern) == 12:
            print(f"  Pattern {i}: {' '.join(pattern[:4])} ... {' '.join(pattern[-2:])}")
            
            # Test this pattern and some permutations
            for pp in PASSPHRASES:
                phrase = " ".join(pattern)
                if test_phrase(phrase, pp):
                    return found_solution(phrase, pp)
                tested += 1
            
            # Test a few permutations
            for perm_num, perm in enumerate(itertools.permutations(pattern)):
                if perm_num >= 100:
                    break
                
                phrase = " ".join(perm)
                for pp in PASSPHRASES:
                    if test_phrase(phrase, pp):
                        return found_solution(phrase, pp)
                    tested += 1
    
    print(f"Strategy 4 complete: {tested:,} tested\n")
    return False

def strategy_5_random_sampling():
    """Random sampling from all valid words"""
    print("\n" + "="*70)
    print("STRATEGY 5: Random sampling from all 38 valid words")
    print("="*70)
    
    tested = 0
    start = time.time()
    target_tests = 100000
    
    print(f"Testing {target_tests:,} random combinations...\n")
    
    while tested < target_tests:
        # Random 12 words
        words_12 = random.sample(VALID_WORDS, 12)
        phrase = " ".join(words_12)
        
        for pp in PASSPHRASES:
            if test_phrase(phrase, pp):
                return found_solution(phrase, pp)
            tested += 1
        
        if tested % 10000 == 0:
            elapsed = time.time() - start
            print(f"  Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s")
    
    print(f"Strategy 5 complete: {tested:,} tested\n")
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║              EXHAUSTIVE SYSTEMATIC SOLVER                    ║
║                                                              ║
║  Testing multiple strategies with valid BIP39 words only     ║
║  Will run until solution found or all strategies exhausted   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    global_start = time.time()
    
    strategies = [
        ("Top 12 Permutations", strategy_1_top_12_permutations),
        ("All Combinations (Top 20)", strategy_2_all_combinations),
        ("Fixed + Variable", strategy_3_fixed_positions),
        ("Specific Patterns", strategy_4_specific_patterns),
        ("Random Sampling", strategy_5_random_sampling),
    ]
    
    for name, strategy_func in strategies:
        print(f"\n{'#'*70}")
        print(f"EXECUTING: {name}")
        print(f"{'#'*70}")
        
        try:
            if strategy_func():
                elapsed = time.time() - global_start
                print(f"\n✅ SOLUTION FOUND in {elapsed:.1f} seconds!")
                return
        except KeyboardInterrupt:
            print(f"\n\n⚠️ Interrupted by user")
            elapsed = time.time() - global_start
            print(f"Total time: {elapsed:.1f}s")
            return
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            continue
    
    elapsed = time.time() - global_start
    print(f"\n{'='*70}")
    print(f"All strategies completed in {elapsed:.1f}s")
    print(f"No solution found")
    print("="*70)

if __name__ == "__main__":
    main()
