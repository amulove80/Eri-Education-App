#!/usr/bin/env python3
"""
MASSIVE BRUTE FORCE - Test huge number of combinations
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import random
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Load all 2048 BIP39 words
with open("/workspace/bip39_wordlist.txt", "r") as f:
    ALL_BIP39 = [w.strip() for w in f if w.strip()]

# Our candidate words
CANDIDATES = [
    "black", "brave", "camera", "change", "coin", "day", "digital", "eye", 
    "face", "food", "future", "history", "home", "key", "liberty", "mask", 
    "moon", "one", "only", "order", "owner", "peace", "picture", "proof", 
    "pyramid", "real", "sign", "state", "subject", "system", "this", "time", 
    "tower", "verify", "virus", "vote", "weapon", "world"
]

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

def found(phrase, pp=""):
    print(f"\n\n{'='*80}")
    print("🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
    print("="*80)
    print(f"Seed: {phrase}")
    if pp:
        print(f"Passphrase: {pp}")
    print(f"Address: {TARGET_ADDRESS}")
    print("="*80)
    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
        f.write(f"SOLUTION!\nSeed: {phrase}\nPassphrase: {pp}\nAddress: {TARGET_ADDRESS}\n")
    return True

def strategy_massive_random():
    """Test millions of random combinations"""
    print("\n" + "="*80)
    print("STRATEGY: Massive random sampling")
    print("Testing 10,000,000 random combinations from all 38 candidates")
    print("="*80)
    
    tested = 0
    start = time.time()
    target = 10_000_000
    
    while tested < target:
        # Random 12 words from candidates
        words = random.sample(CANDIDATES, 12)
        phrase = " ".join(words)
        
        for pp in PASSPHRASES:
            if test_phrase(phrase, pp):
                return found(phrase, pp)
            tested += 1
        
        if tested % 100000 == 0:
            elapsed = time.time() - start
            rate = tested / elapsed
            remaining = (target - tested) / rate / 60
            print(f"  Tested: {tested:,} | Rate: {rate:.0f}/s | ETA: {remaining:.1f}min")
    
    print(f"\nCompleted: {tested:,} tested in {time.time()-start:.1f}s")
    return False

def strategy_expand_search():
    """Include words from full BIP39 list that relate to themes"""
    print("\n" + "="*80)
    print("STRATEGY: Expanded thematic search")
    print("Including additional BIP39 words related to puzzle themes")
    print("="*80)
    
    # Add more thematic words from BIP39
    themes = {
        "protest": ["abuse", "action", "angry", "battle", "brother", "charge", 
                   "crowd", "cry", "defend", "drama", "fire", "force", "guard"],
        "2020": ["city", "clock", "crowd", "danger", "date", "decade", "era"],
        "government": ["act", "army", "city", "country", "court", "flag", 
                      "law", "member", "nation", "office", "power", "public"],
        "vision": ["view", "visual", "watch", "witness"],
        "truth": ["claim", "confirm", "correct", "detect", "discover", "exact", 
                 "true", "truth", "value"],
    }
    
    expanded = CANDIDATES.copy()
    for theme_words in themes.values():
        for word in theme_words:
            if word in ALL_BIP39 and word not in expanded:
                expanded.append(word)
    
    print(f"Expanded to {len(expanded)} candidate words")
    print(f"Testing 1,000,000 random combinations...\n")
    
    tested = 0
    start = time.time()
    target = 1_000_000
    
    while tested < target:
        words = random.sample(expanded, 12)
        phrase = " ".join(words)
        
        for pp in PASSPHRASES:
            if test_phrase(phrase, pp):
                return found(phrase, pp)
            tested += 1
        
        if tested % 50000 == 0:
            elapsed = time.time() - start
            print(f"  Tested: {tested:,} | Rate: {tested/elapsed:.0f}/s")
    
    print(f"\nCompleted: {tested:,} tested")
    return False

def strategy_weighted_random():
    """Weight towards most likely words"""
    print("\n" + "="*80)
    print("STRATEGY: Weighted random sampling")
    print("Higher probability for most certain words")
    print("="*80)
    
    # Weights - higher = more likely
    weights = {
        # Very high confidence
        "moon": 10, "tower": 10, "food": 10,
        
        # High confidence
        "this": 8, "subject": 8, "real": 8, "black": 8,
        "time": 8, "proof": 8, "world": 8, "only": 8,
        
        # Medium
        "one": 5, "brave": 5, "order": 5, "liberty": 5,
        "eye": 5, "pyramid": 5, "mask": 5,
        
        # Lower
        "camera": 3, "peace": 3, "change": 3, "coin": 3,
        "digital": 3, "virus": 3, "vote": 3, "weapon": 3,
    }
    
    # Default weight 1 for others
    word_list = []
    for word in CANDIDATES:
        weight = weights.get(word, 1)
        word_list.extend([word] * weight)
    
    print(f"Testing 5,000,000 weighted random combinations...\n")
    
    tested = 0
    start = time.time()
    target = 5_000_000
    
    while tested < target:
        # Sample with replacement, then deduplicate
        sampled = []
        while len(sampled) < 12:
            word = random.choice(word_list)
            if word not in sampled:
                sampled.append(word)
        
        phrase = " ".join(sampled)
        
        for pp in PASSPHRASES:
            if test_phrase(phrase, pp):
                return found(phrase, pp)
            tested += 1
        
        if tested % 100000 == 0:
            elapsed = time.time() - start
            rate = tested / elapsed
            remaining = (target - tested) / rate / 60
            print(f"  Tested: {tested:,} | Rate: {rate:.0f}/s | ETA: {remaining:.1f}min")
    
    print(f"\nCompleted: {tested:,} tested")
    return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                    MASSIVE BRUTE FORCE SOLVER                      ║
║                                                                    ║
║  Will test millions of combinations until solution is found        ║
║  Press Ctrl+C to stop                                             ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    global_start = time.time()
    
    strategies = [
        strategy_weighted_random,
        strategy_massive_random,
        strategy_expand_search,
    ]
    
    for strategy in strategies:
        try:
            if strategy():
                elapsed = time.time() - global_start
                print(f"\n✅ SOLUTION FOUND in {elapsed:.1f}s ({elapsed/60:.1f}min)!")
                return
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            elapsed = time.time() - global_start
            print(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f}min)")
            return
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    elapsed = time.time() - global_start
    print(f"\n{'='*80}")
    print(f"All strategies completed in {elapsed:.1f}s ({elapsed/60:.1f}min)")
    print("No solution found")
    print("="*80)

if __name__ == "__main__":
    main()
