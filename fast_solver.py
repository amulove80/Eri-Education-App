#!/usr/bin/env python3
"""
Fast targeted solver - test specific high-value combinations
Focus on 8 high confidence + 4 from 6 medium = much smaller search space
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

# 8 high confidence words - assume these are ALL correct
HIGH_CONF = ["moon", "tower", "food", "breathe", "this", "subject", "real", "black"]

# 6 medium confidence - choose 4 of these
MEDIUM_CONF = ["time", "proof", "only", "win", "world", "face"]

def test_phrase(phrase_words):
    """Test a single phrase"""
    phrase = " ".join(phrase_words)
    
    # Validate checksum
    try:
        Bip39MnemonicValidator().Validate(phrase)
    except:
        return False, None
    
    # Generate address
    try:
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip44_acc.PublicKey().ToAddress()
        return True, address
    except:
        return False, None

def solve():
    print("="*70)
    print("FAST TARGETED SOLVER")
    print("="*70)
    print(f"\nAssumption: All 8 high-confidence words are correct")
    print(f"Testing: 8 fixed + choose 4 from 6 medium confidence")
    print(f"\nHigh confidence (8): {HIGH_CONF}")
    print(f"Medium confidence (6): {MEDIUM_CONF}")
    
    # Calculate combinations
    from math import factorial
    ways_to_choose_4_from_6 = factorial(6) // (factorial(4) * factorial(2))
    perms_of_12 = factorial(12)
    total = ways_to_choose_4_from_6 * perms_of_12
    
    print(f"\nCombinations:")
    print(f"  - Choose 4 from 6 medium: {ways_to_choose_4_from_6}")
    print(f"  - Permutations of 12: {perms_of_12:,}")
    print(f"  - Total: {total:,}")
    print(f"  - Estimated time at 100/s: {total/100/60:.1f} minutes\n")
    
    attempts = 0
    valid = 0
    start = time.time()
    last_report = start
    
    # For each way to choose 4 from 6 medium words
    for medium_4 in itertools.combinations(MEDIUM_CONF, 4):
        all_12 = HIGH_CONF + list(medium_4)
        print(f"\n--- Testing word set: {all_12}")
        
        # Test all permutations
        for perm in itertools.permutations(all_12):
            attempts += 1
            
            is_valid, address = test_phrase(perm)
            
            if is_valid:
                valid += 1
                
                if address == TARGET_ADDRESS:
                    elapsed = time.time() - start
                    print(f"\n\n{'='*70}")
                    print("🎉 SOLUTION FOUND! 🎉")
                    print("="*70)
                    print(f"Seed: {' '.join(perm)}")
                    print(f"Address: {address}")
                    print(f"Attempts: {attempts:,}")
                    print(f"Time: {elapsed:.1f}s")
                    print("="*70)
                    
                    with open("/workspace/SOLUTION.txt", "w") as f:
                        f.write(f"SOLUTION FOUND!\n")
                        f.write(f"Seed: {' '.join(perm)}\n")
                        f.write(f"Address: {address}\n")
                    return True
            
            # Progress every 10 seconds
            now = time.time()
            if now - last_report >= 10:
                elapsed = now - start
                rate = attempts / elapsed
                eta = (total - attempts) / rate if rate > 0 else 0
                pct = 100 * attempts / total
                
                print(f"  Progress: {attempts:,}/{total:,} ({pct:.2f}%) | "
                      f"Valid: {valid:,} | Rate: {rate:.0f}/s | "
                      f"Elapsed: {elapsed/60:.1f}m | ETA: {eta/60:.1f}m")
                last_report = now
    
    elapsed = time.time() - start
    print(f"\n{'='*70}")
    print(f"Search complete - No solution found")
    print(f"Tested: {attempts:,} | Valid: {valid:,} | Time: {elapsed:.1f}s")
    print("="*70)
    return False

if __name__ == "__main__":
    solve()
