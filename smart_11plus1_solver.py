#!/usr/bin/env python3
"""
Smart solver - Given 11 words, calculate valid 12th words
BIP39 checksum is embedded in the last word, so given 11 words,
there are only ~8 possible 12th words that create valid checksums
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator, Bip39Languages
import hashlib

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

def get_bip39_wordlist():
    """Get all 2048 BIP39 words"""
    words = set()
    # Generate many random mnemonics to collect all words
    for _ in range(100):
        mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(Bip39WordsNum.WORDS_NUM_24)
        words.update(mnemonic.ToList())
    return sorted(list(words))

def find_valid_12th_words(first_11_words):
    """
    Given 11 words, find all possible 12th words that create valid BIP39 phrases
    
    In BIP39:
    - 12 words = 132 bits total
    - 128 bits entropy + 4 bits checksum
    - The last word encodes the final 7 bits of entropy + 4 bits checksum
    - So there are 2^7 = 128 possible last words, but only ~8 have correct checksum
    """
    wordlist = get_bip39_wordlist()
    valid_phrases = []
    
    print(f"Testing {len(wordlist)} possible 12th words...")
    
    for word_12 in wordlist:
        phrase = " ".join(first_11_words + [word_12])
        
        try:
            # Try to validate
            Bip39MnemonicValidator().Validate(phrase)
            valid_phrases.append((word_12, phrase))
        except:
            pass
    
    return valid_phrases

def test_phrase(phrase):
    """Test if phrase generates target address"""
    try:
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress()
    except:
        return None

def solve_with_11_words(first_11):
    """Try to solve given first 11 words"""
    print("="*70)
    print(f"Testing 11-word sequence:")
    print(f"  {' '.join(first_11)}")
    print("="*70)
    
    valid_completions = find_valid_12th_words(first_11)
    
    print(f"\nFound {len(valid_completions)} valid 12th words:")
    
    for word_12, full_phrase in valid_completions:
        address = test_phrase(full_phrase)
        print(f"  - {word_12:15} → {address}")
        
        if address == TARGET_ADDRESS:
            print(f"\n{'='*70}")
            print(f"🎉 SOLUTION FOUND! 🎉")
            print("="*70)
            print(f"Seed: {full_phrase}")
            print(f"Address: {address}")
            print("="*70)
            
            with open("/workspace/SOLUTION.txt", "w") as f:
                f.write(f"SOLUTION!\n")
                f.write(f"Seed: {full_phrase}\n")
                f.write(f"Address: {address}\n")
            return True
    
    return False

# Test some likely 11-word sequences
TEST_SEQUENCES = [
    # High confidence words, missing one
    ["moon", "tower", "food", "breathe", "this", "subject", "real", "black", "time", "proof", "only"],
    ["moon", "tower", "food", "breathe", "this", "subject", "real", "black", "time", "proof", "world"],
    ["moon", "tower", "food", "breathe", "this", "subject", "real", "black", "time", "only", "world"],
    ["moon", "tower", "food", "breathe", "this", "subject", "real", "black", "proof", "only", "world"],
    ["moon", "tower", "food", "breathe", "this", "subject", "real", "time", "proof", "only", "world"],
    ["moon", "tower", "food", "breathe", "this", "subject", "black", "time", "proof", "only", "world"],
    ["moon", "tower", "food", "breathe", "this", "real", "black", "time", "proof", "only", "world"],
    ["moon", "tower", "food", "breathe", "subject", "real", "black", "time", "proof", "only", "world"],
    ["moon", "tower", "food", "this", "subject", "real", "black", "time", "proof", "only", "world"],
    ["moon", "tower", "breathe", "this", "subject", "real", "black", "time", "proof", "only", "world"],
    ["moon", "food", "breathe", "this", "subject", "real", "black", "time", "proof", "only", "world"],
    ["tower", "food", "breathe", "this", "subject", "real", "black", "time", "proof", "only", "world"],
]

def main():
    print("\n" + "="*70)
    print("SMART 11+1 WORD SOLVER")
    print("="*70)
    print("\nStrategy: Given 11 words, find valid 12th words")
    print("This reduces search space dramatically!\n")
    
    for i, sequence in enumerate(TEST_SEQUENCES, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(TEST_SEQUENCES)}")
        if solve_with_11_words(sequence):
            return True
        print()
    
    print("\n" + "="*70)
    print("No solution found in tested 11-word sequences")
    print("="*70)

if __name__ == "__main__":
    main()
