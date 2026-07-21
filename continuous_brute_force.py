#!/usr/bin/env python3
"""
CONTINUOUS BRUTE FORCE - Run indefinitely until solution found
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import random
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

CANDIDATES = [
    "black", "brave", "camera", "change", "coin", "day", "digital", "eye", 
    "face", "food", "future", "history", "home", "key", "liberty", "mask", 
    "moon", "one", "only", "order", "owner", "peace", "picture", "proof", 
    "pyramid", "real", "sign", "state", "subject", "system", "this", "time", 
    "tower", "verify", "virus", "vote", "weapon", "world"
]

# Weights for weighted sampling
WEIGHTS = {
    "moon": 10, "tower": 10, "food": 10,
    "this": 8, "subject": 8, "real": 8, "black": 8,
    "time": 8, "proof": 8, "world": 8, "only": 8,
    "one": 5, "brave": 5, "order": 5, "liberty": 5,
}

PASSPHRASES = ["", "BREATHE", "breathe", "Breathe"]

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
    print("""
╔════════════════════════════════════════════════════════════════════╗
║              CONTINUOUS BRUTE FORCE SEARCH                         ║
║                                                                    ║
║  Testing combinations until solution is found                      ║
║  Press Ctrl+C to stop                                             ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create weighted word list
    word_list = []
    for word in CANDIDATES:
        weight = WEIGHTS.get(word, 3)
        word_list.extend([word] * weight)
    
    tested = 0
    start = time.time()
    last_report = start
    
    try:
        while True:
            # Weighted random sampling
            sampled = []
            while len(sampled) < 12:
                word = random.choice(word_list)
                if word not in sampled:
                    sampled.append(word)
            
            phrase = " ".join(sampled)
            
            for pp in PASSPHRASES:
                if test_phrase(phrase, pp):
                    print(f"\n\n{'='*80}")
                    print("🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
                    print("="*80)
                    print(f"Seed: {phrase}")
                    if pp:
                        print(f"Passphrase: {pp}")
                    print(f"Address: {TARGET_ADDRESS}")
                    print("="*80)
                    
                    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                        f.write(f"SOLUTION!\n")
                        f.write(f"Seed: {phrase}\n")
                        f.write(f"Passphrase: {pp}\n")
                        f.write(f"Address: {TARGET_ADDRESS}\n")
                    
                    return
                
                tested += 1
            
            # Report every 30 seconds
            now = time.time()
            if now - last_report >= 30:
                elapsed = now - start
                rate = tested / elapsed
                print(f"[{time.strftime('%H:%M:%S')}] Tested: {tested:,} | "
                      f"Rate: {rate:.0f}/s | Time: {elapsed/60:.1f}min")
                last_report = now
    
    except KeyboardInterrupt:
        elapsed = time.time() - start
        print(f"\n\n⚠️ Stopped by user")
        print(f"Tested: {tested:,} combinations in {elapsed/60:.1f} minutes")
        print(f"Rate: {tested/elapsed:.0f} tests/second")

if __name__ == "__main__":
    main()
