#!/usr/bin/env python3
"""
PARALLEL SOLVER 3 - Test specific high-value patterns
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Must-have words (very high confidence)
MUST_HAVE = ["moon", "tower", "food"]

# Very likely words
VERY_LIKELY = ["this", "subject", "real", "black", "time", "proof", "world", "only", "one"]

# Alternative words
ALTERNATIVES = ["brave", "order", "liberty", "eye", "pyramid", "mask", "peace", "change"]

PASSPHRASES = ["", "BREATHE", "breathe"]

def test_phrase(phrase, passphrase=""):
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress() == TARGET_ADDRESS
    except:
        return False

def main():
    print("[PARALLEL-3] Testing combinations with mandatory words...")
    
    tested = 0
    start = time.time()
    last_report = start
    
    try:
        # Test all combinations with MUST_HAVE words included
        # Choose 7 from VERY_LIKELY and 2 from ALTERNATIVES
        for very_likely_combo in itertools.combinations(VERY_LIKELY, 7):
            for alt_combo in itertools.combinations(ALTERNATIVES, 2):
                words = list(MUST_HAVE) + list(very_likely_combo) + list(alt_combo)
                
                # Test multiple permutations of these 12 words
                for perm_num, perm in enumerate(itertools.permutations(words)):
                    if perm_num >= 100:  # Test 100 permutations per combination
                        break
                    
                    phrase = " ".join(perm)
                    
                    for pp in PASSPHRASES:
                        if test_phrase(phrase, pp):
                            print(f"\n[PARALLEL-3] 🎉 SOLUTION FOUND!")
                            print(f"Seed: {phrase}")
                            print(f"Passphrase: {pp}")
                            
                            with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                                f.write(f"SOLUTION (Parallel-3)!\nSeed: {phrase}\nPassphrase: {pp}\n")
                            return
                        
                        tested += 1
                    
                    now = time.time()
                    if now - last_report >= 30:
                        elapsed = now - start
                        print(f"[PARALLEL-3] [{time.strftime('%H:%M:%S')}] Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s")
                        last_report = now
    
    except KeyboardInterrupt:
        print(f"\n[PARALLEL-3] Stopped. Tested: {tested:,}")

if __name__ == "__main__":
    main()
