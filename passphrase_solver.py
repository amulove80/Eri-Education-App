#!/usr/bin/env python3
"""
BREAKTHROUGH SOLVER - Test with BREATHE as BIP39 passphrase!

Key insight: "breathe" is NOT in BIP39 wordlist, so it MUST be the passphrase!
"""

import itertools
from bip_utils import (
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
    Bip39MnemonicValidator
)

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"
PASSPHRASE = "BREATHE"  # The missing piece!

# Words that existed BEFORE May 10, 2020 (when wallet was funded)
# Excluding BLM-related words added after George Floyd (May 25, 2020)
PRE_MAY_10_WORDS = [
    # High confidence - directly labeled
    "moon",     # clock hand
    "tower",    # clock hand
    "food",     # Space Needle
    
    # High confidence - text references
    "this",     # repeated text
    "subject",  # underlined
    "real",     # "only real Bitcoin"
    
    # From title (Brave New World - 1932 book)
    "brave",
    "new", 
    "world",
    
    # Bitcoin/theme words
    "time",     # clock
    "proof",    # proof of work
    "only",     # "only Bitcoin"
    
    # Additional pre-May 10 candidates
    "one",      # underlined "1"
]

def generate_address_with_passphrase(seed_phrase, passphrase):
    """Generate address with BIP39 passphrase"""
    try:
        # Validate mnemonic
        Bip39MnemonicValidator().Validate(seed_phrase)
        
        # Generate seed WITH passphrase
        seed_bytes = Bip39SeedGenerator(seed_phrase, passphrase).Generate()
        
        # Generate BIP44 wallet
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        
        return bip44_acc.PublicKey().ToAddress()
    except:
        return None

def test_with_passphrase():
    """Test 12-word combinations with BREATHE passphrase"""
    print("="*70)
    print("🔥 BREAKTHROUGH SOLVER - Testing with BREATHE passphrase! 🔥")
    print("="*70)
    print(f"\nPassphrase: {PASSPHRASE}")
    print(f"Testing {len(PRE_MAY_10_WORDS)} pre-May 10 words")
    print(f"Words: {PRE_MAY_10_WORDS}\n")
    
    if len(PRE_MAY_10_WORDS) < 12:
        print(f"❌ Only {len(PRE_MAY_10_WORDS)} words, need at least 12")
        return False
    
    attempts = 0
    valid = 0
    
    # Test all 12-word combinations
    print("Testing combinations (choose 12 from available words)...\n")
    
    for combo in itertools.combinations(PRE_MAY_10_WORDS, 12):
        # For each 12-word combination, test a sample of permutations
        # (Full permutation would be 479M per combo - too many)
        
        # Test just the given order first
        phrase = " ".join(combo)
        address = generate_address_with_passphrase(phrase, PASSPHRASE)
        
        if address:
            valid += 1
            if address == TARGET_ADDRESS:
                print(f"\n{'='*70}")
                print("🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
                print("="*70)
                print(f"Seed: {phrase}")
                print(f"Passphrase: {PASSPHRASE}")
                print(f"Address: {address}")
                print("="*70)
                
                with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                    f.write(f"SOLUTION!\n")
                    f.write(f"Seed: {phrase}\n")
                    f.write(f"Passphrase: {PASSPHRASE}\n")
                    f.write(f"Address: {address}\n")
                return True
        
        attempts += 1
        
        if attempts % 10 == 0:
            print(f"Tested {attempts} combinations, {valid} with valid checksum...")
    
    print(f"\n✅ Tested {attempts} combinations")
    print(f"✅ Found {valid} with valid BIP39 checksum")
    print(f"❌ No match to target address")
    return False

def test_specific_sequences():
    """Test specific ordered sequences with passphrase"""
    print("\n" + "="*70)
    print("Testing specific ordered sequences with BREATHE passphrase")
    print("="*70)
    
    sequences = [
        # Based on visual order / timeline
        ["this", "brave", "new", "world", "moon", "tower", "food", "time", "proof", "only", "real", "one"],
        ["moon", "tower", "food", "this", "subject", "real", "brave", "new", "world", "time", "proof", "only"],
        ["brave", "new", "world", "moon", "tower", "food", "this", "subject", "real", "time", "proof", "only"],
        
        # Alphabetical
        ["brave", "food", "moon", "new", "one", "only", "proof", "real", "subject", "this", "time", "tower"],
    ]
    
    for i, seq in enumerate(sequences, 1):
        phrase = " ".join(seq)
        print(f"\nTest {i}: {phrase}")
        
        address = generate_address_with_passphrase(phrase, PASSPHRASE)
        
        if address:
            print(f"  ✅ Valid BIP39, Address: {address[:30]}...")
            if address == TARGET_ADDRESS:
                print(f"\n{'='*70}")
                print("🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
                print("="*70)
                print(f"Seed: {phrase}")
                print(f"Passphrase: {PASSPHRASE}")
                print(f"Address: {address}")
                print("="*70)
                return True
        else:
            print(f"  ❌ Invalid BIP39 checksum")
    
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  BREAKTHROUGH DISCOVERY!                     ║
║                                                              ║
║  "breathe" is NOT in BIP39 wordlist                         ║
║  Therefore it MUST be the BIP39 PASSPHRASE!                 ║
║                                                              ║
║  Testing 12-word seeds + "BREATHE" passphrase               ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Test specific sequences first (fast)
    if test_specific_sequences():
        return True
    
    # Then test combinations (slower)
    #if test_with_passphrase():
    #    return True
    
    print("\n" + "="*70)
    print("No solution found with current word set + BREATHE passphrase")
    print("="*70)
    print("\nPossible reasons:")
    print("1. Need additional words not yet identified")
    print("2. Passphrase might be different case/format")
    print("3. May be 18-word seed instead of 12")
    print("4. Some assumed words are incorrect")

if __name__ == "__main__":
    main()
