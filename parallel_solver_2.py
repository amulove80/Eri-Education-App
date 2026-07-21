#!/usr/bin/env python3
"""
PARALLEL SOLVER 2 - Different strategy focusing on most likely combinations
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import random
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Focus on highest confidence words
TOP_WORDS = ["moon", "tower", "food", "this", "subject", "real", "black", "time", "proof", "world", "only", "one"]
ALT_WORDS = ["brave", "order", "liberty", "eye", "pyramid", "mask", "peace", "change", "camera", "coin"]

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
    print("[PARALLEL-2] Starting focused search on top candidates...")
    
    tested = 0
    start = time.time()
    last_report = start
    
    try:
        while True:
            # Strategy: Use 10 from TOP_WORDS, 2 from ALT_WORDS
            top_sample = random.sample(TOP_WORDS, min(10, len(TOP_WORDS)))
            alt_sample = random.sample(ALT_WORDS, 2)
            words = top_sample + alt_sample
            random.shuffle(words)
            
            phrase = " ".join(words)
            
            for pp in PASSPHRASES:
                if test_phrase(phrase, pp):
                    print(f"\n[PARALLEL-2] 🎉 SOLUTION FOUND!")
                    print(f"Seed: {phrase}")
                    print(f"Passphrase: {pp}")
                    
                    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                        f.write(f"SOLUTION (Parallel-2)!\nSeed: {phrase}\nPassphrase: {pp}\n")
                    return
                
                tested += 1
            
            now = time.time()
            if now - last_report >= 30:
                elapsed = now - start
                print(f"[PARALLEL-2] [{time.strftime('%H:%M:%S')}] Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s")
                last_report = now
    
    except KeyboardInterrupt:
        print(f"\n[PARALLEL-2] Stopped. Tested: {tested:,}")

if __name__ == "__main__":
    main()
