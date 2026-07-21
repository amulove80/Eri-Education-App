#!/usr/bin/env python3
"""
CORRECTED SOLVER - Using ONLY valid BIP39 words!
Testing with corrected word list
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# ONLY VALID BIP39 WORDS (confirmed against official wordlist)
VALID_WORDS = {
    "certain": ["moon", "tower", "food", "this", "subject", "real", "black", "only"],
    
    "very_likely": ["time", "proof", "world", "one"],
    
    # "Brave NEW World" → must be "brave ??? world" 
    "brave_world_middle": ["news", "renew"],  # "new" alternatives
    
    # STOP sign → similar words
    "stop_alternatives": ["story", "stomach", "stove"],
    
    # Additional valid
    "other_valid": ["brave", "order", "liberty", "eye", "pyramid", "mask", "camera",
                    "coin", "digital", "key", "system", "history", "verify", "owner",
                    "state", "virus", "future", "change", "vote", "day", "home",
                    "face", "sign", "picture", "weapon", "peace", "just", "adjust",
                    "chair", "chapter", "bread", "breeze"]
}

def test_sequence(words_12, passphrase="", name=""):
    """Test a sequence"""
    if len(words_12) != 12:
        return False
    
    phrase = " ".join(words_12)
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip44_acc.PublicKey().ToAddress()
        
        if address == TARGET_ADDRESS:
            print(f"\n{'='*70}")
            print(f"🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
            print("="*70)
            print(f"Seed: {phrase}")
            if passphrase:
                print(f"Passphrase: {passphrase}")
            print(f"Address: {address}")
            print("="*70)
            return True
    except:
        pass
    return False

def test_corrected_combinations():
    """Test with corrected BIP39-valid words"""
    print("="*70)
    print("TESTING WITH CORRECTED BIP39-VALID WORDS ONLY")
    print("="*70)
    
    tested = 0
    
    # Test "Brave NEWS World" and "Brave RENEW World"
    print("\n1. Testing 'Brave ??? World' with BIP39 alternatives:")
    
    for middle in ["news", "renew"]:
        sequences = [
            ["brave", middle, "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"],
            ["moon", "tower", "food", "brave", middle, "world", "this", "subject", "real", "time", "proof", "only"],
            ["this", "brave", middle, "world", "moon", "tower", "food", "subject", "real", "time", "proof", "only"],
        ]
        
        for seq in sequences:
            for pp in ["", "BREATHE", "breathe"]:
                print(f"  Testing: brave {middle} world... + '{pp}'")
                if test_sequence(seq, pp, f"brave-{middle}-world"):
                    return True
                tested += 1
    
    # Test with STOP alternatives
    print("\n2. Testing STOP sign alternatives (story, stomach, stove):")
    
    for stop_word in ["story", "stomach", "stove"]:
        sequences = [
            [stop_word, "moon", "tower", "food", "this", "subject", "real", "black", "time", "proof", "world", "only"],
            ["moon", "tower", stop_word, "food", "this", "subject", "real", "black", "time", "proof", "world", "only"],
        ]
        
        for seq in sequences:
            for pp in ["", "BREATHE", "breathe"]:
                print(f"  Testing: {stop_word}...")
                if test_sequence(seq, pp, f"stop-{stop_word}"):
                    return True
                tested += 1
    
    # Test with "breathe" alternatives in seed (bread, breeze)
    print("\n3. Testing 'breathe' alternatives as seed words (bread, breeze):")
    
    for breath_alt in ["bread", "breeze"]:
        sequences = [
            ["moon", "tower", "food", breath_alt, "this", "subject", "real", "black", "time", "proof", "world", "only"],
            ["this", "moon", "tower", "food", breath_alt, "subject", "real", "black", "time", "proof", "world", "only"],
        ]
        
        for seq in sequences:
            for pp in ["", "BREATHE", "breathe"]:
                print(f"  Testing: {breath_alt}...")
                if test_sequence(seq, pp, f"breath-{breath_alt}"):
                    return True
                tested += 1
    
    # Test corrected high-confidence combinations
    print("\n4. Testing corrected high-confidence combinations:")
    
    certain = VALID_WORDS["certain"]  # 8 words
    very_likely = VALID_WORDS["very_likely"]  # 4 words
    
    # This makes 12 words exactly
    base_12 = certain + very_likely
    
    print(f"  Base words: {base_12}")
    
    # Test various permutations
    for perm_num, perm in enumerate(itertools.permutations(base_12)):
        if perm_num > 1000:  # Test 1000 permutations
            break
        
        for pp in ["", "BREATHE", "breathe"]:
            if test_sequence(list(perm), pp, f"base-perm-{perm_num}"):
                return True
            tested += 1
        
        if tested % 100 == 0:
            print(f"  Tested {tested} combinations...")
    
    print(f"\nTotal tested: {tested}")
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           CORRECTED BIP39-ONLY SOLVER                        ║
║                                                              ║
║  Using ONLY words from official BIP39 wordlist               ║
║  Key corrections:                                            ║
║    - "new" → "news" or "renew"                              ║
║    - "stop" → "story", "stomach", or "stove"                ║
║    - "breathe" → passphrase or "bread"/"breeze"             ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    start = time.time()
    
    if test_corrected_combinations():
        print(f"\n✅ Solution found in {time.time()-start:.2f}s!")
    else:
        print(f"\n❌ No solution in {time.time()-start:.2f}s")
        print("\nThis means we need to identify more correct words from image")

if __name__ == "__main__":
    main()
