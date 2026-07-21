#!/usr/bin/env python3
"""
Advanced 0.2 BTC Puzzle Solver
Implements multiple strategies to find the correct 12-word BIP39 seed phrase
"""

import itertools
import hashlib
from typing import List, Set
from bip_utils import (
    Bip39MnemonicValidator, 
    Bip39SeedGenerator, 
    Bip44, 
    Bip44Coins, 
    Bip44Changes,
    Bip39WordsNum,
    Bip39Languages
)
import time

# Target Bitcoin address
TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# High confidence words based on puzzle analysis
HIGH_CONFIDENCE_WORDS = [
    "moon",      # Clock hands
    "tower",     # Clock hands
    "food",      # Seattle Space Needle
    "breathe",   # George Floyd's chest / Statue's Neck  
    "this",      # Repeated multiple times
    "subject",   # Underlined on statue
    "real",      # "Only real Bitcoin"
    "black",     # "The Pot Calling The Kettle Black" + BLM
]

# Medium confidence words
MEDIUM_CONFIDENCE_WORDS = [
    "time",      # Clock imagery
    "proof",     # Proof of work
    "only",      # "Only Bitcoin"
    "win",       # Possible from image
    "world",     # May be in image
    "face",      # Face masks
]

# Additional candidate words from community
ADDITIONAL_WORDS = [
    "twenty", "flag", "hand", "sign", "state", "virus", "mask",
    "order", "digital", "coin", "chest", "picture", "pyramid",
    "weapon", "neck", "camera", "eye", "day", "first", "major",
    "country", "home", "future"
]

# All words combined
ALL_CANDIDATE_WORDS = HIGH_CONFIDENCE_WORDS + MEDIUM_CONFIDENCE_WORDS + ADDITIONAL_WORDS


class PuzzleSolver:
    def __init__(self):
        self.attempts = 0
        self.valid_checksums = 0
        self.start_time = time.time()
        
        # Load BIP39 wordlist for validation
        from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator
        self.bip39_wordlist = set()
        
        # Generate a dummy mnemonic to access the wordlist
        try:
            from bip_utils.bip.bip39.bip39_mnemonic import Bip39Languages, Bip39WordsNum
            from bip_utils.bip.bip39.bip39_mnemonic_decoder import _Bip39MnemonicDecoderConst
            # Access the English wordlist
            self.bip39_wordlist = set(_Bip39MnemonicDecoderConst.WORDLISTS[Bip39Languages.ENGLISH])
        except:
            print("Warning: Could not load BIP39 wordlist for validation")
            self.bip39_wordlist = set(ALL_CANDIDATE_WORDS)  # Fallback

    def validate_words(self, words: List[str]) -> List[str]:
        """Validate that words are in BIP39 wordlist"""
        valid = []
        invalid = []
        
        for word in words:
            if word.lower() in self.bip39_wordlist:
                valid.append(word.lower())
            else:
                invalid.append(word)
        
        if invalid:
            print(f"⚠️  Invalid BIP39 words found: {invalid}")
        
        return valid

    def is_valid_mnemonic(self, phrase: str) -> bool:
        """Check if a mnemonic phrase has valid checksum"""
        try:
            # This will throw exception if checksum is invalid
            Bip39MnemonicValidator().Validate(phrase)
            return True
        except:
            return False

    def generate_address_from_seed(self, seed_phrase: str) -> str:
        """Generate Bitcoin address from seed phrase"""
        try:
            # Generate seed from mnemonic
            seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
            
            # Generate BIP44 wallet (Legacy address format)
            bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            
            return bip44_acc.PublicKey().ToAddress()
        except Exception as e:
            return None

    def test_combination(self, words: List[str]) -> bool:
        """Test a single word combination"""
        self.attempts += 1
        
        phrase = " ".join(words)
        
        # Fast check: validate checksum first
        if not self.is_valid_mnemonic(phrase):
            return False
        
        self.valid_checksums += 1
        
        # Generate address
        address = self.generate_address_from_seed(phrase)
        
        if address == TARGET_ADDRESS:
            elapsed = time.time() - self.start_time
            print(f"\n🎉 SOLUTION FOUND! 🎉")
            print(f"Seed Phrase: {phrase}")
            print(f"Address: {address}")
            print(f"Attempts: {self.attempts:,}")
            print(f"Valid checksums: {self.valid_checksums:,}")
            print(f"Time: {elapsed:.2f}s")
            return True
        
        # Progress update every 10,000 attempts
        if self.attempts % 10000 == 0:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            print(f"Tested: {self.attempts:,} | Valid: {self.valid_checksums:,} | "
                  f"Rate: {rate:.0f}/s | Time: {elapsed:.0f}s")
        
        return False

    def strategy_high_confidence_only(self):
        """Strategy 1: Test only high confidence words"""
        print("\n" + "="*70)
        print("STRATEGY 1: High Confidence Words Only")
        print("="*70)
        print(f"Testing permutations of: {HIGH_CONFIDENCE_WORDS}")
        
        words = self.validate_words(HIGH_CONFIDENCE_WORDS)
        if len(words) < 12:
            print(f"❌ Only {len(words)} valid words, need 12")
            return False
        
        total = 1
        for i in range(12):
            total *= (len(words) - i)
        print(f"Total combinations to test: {total:,}\n")
        
        for combo in itertools.permutations(words, 12):
            if self.test_combination(combo):
                return True
        
        return False

    def strategy_high_plus_medium(self):
        """Strategy 2: Test high + medium confidence words"""
        print("\n" + "="*70)
        print("STRATEGY 2: High + Medium Confidence Words")
        print("="*70)
        
        words = self.validate_words(HIGH_CONFIDENCE_WORDS + MEDIUM_CONFIDENCE_WORDS)
        print(f"Testing permutations of {len(words)} words: {words}")
        
        if len(words) < 12:
            print(f"❌ Only {len(words)} valid words, need 12")
            return False
        
        # Calculate total combinations
        total = 1
        for i in range(12):
            total *= (len(words) - i)
        print(f"Total combinations to test: {total:,}\n")
        
        if total > 10_000_000_000:  # 10 billion
            print(f"⚠️  Warning: This would take too long. Trying subset approaches...")
            return False
        
        for combo in itertools.permutations(words, 12):
            if self.test_combination(combo):
                return True
        
        return False

    def strategy_fixed_positions(self):
        """Strategy 3: Test with some words in fixed positions"""
        print("\n" + "="*70)
        print("STRATEGY 3: Fixed Position Testing")
        print("="*70)
        print("Testing combinations with certain words in fixed positions\n")
        
        # Based on community hints, try fixing some high-confidence words
        # and permuting the rest
        base_words = HIGH_CONFIDENCE_WORDS[:8]
        fill_words = MEDIUM_CONFIDENCE_WORDS[:6]
        
        all_words = self.validate_words(base_words + fill_words)
        
        if len(all_words) < 12:
            print(f"❌ Only {len(all_words)} valid words, need 12")
            return False
        
        # Try different fixed position strategies
        # Example: Fix first and last words, permute middle
        for combo in itertools.combinations(all_words, 12):
            for perm in itertools.permutations(combo):
                if self.test_combination(perm):
                    return True
                
                # Limit to prevent infinite loops
                if self.attempts > 1_000_000:
                    print("Reached attempt limit for this strategy")
                    return False
        
        return False

    def strategy_specific_candidates(self, word_list: List[str], max_attempts: int = 100_000_000):
        """Test specific word list with attempt limit"""
        print(f"\nTesting permutations of {len(word_list)} words")
        print(f"Words: {word_list}")
        
        words = self.validate_words(word_list)
        
        if len(words) != 12:
            print(f"❌ Need exactly 12 words, got {len(words)}")
            return False
        
        total = 1
        for i in range(12):
            total *= (len(words) - i)
        print(f"Total combinations: {total:,}")
        print(f"Max attempts: {max_attempts:,}\n")
        
        tested = 0
        for combo in itertools.permutations(words, 12):
            if self.test_combination(combo):
                return True
            
            tested += 1
            if tested >= max_attempts:
                print(f"Reached attempt limit: {max_attempts:,}")
                return False
        
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           0.2 BTC Puzzle Solver - Advanced Edition           ║
║                                                              ║
║  Target: 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ                  ║
║  Prize: 0.201 BTC (~$20,000+ USD)                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    solver = PuzzleSolver()
    
    # Validate all candidate words first
    print("\n📋 Validating candidate words against BIP39 wordlist...")
    valid_high = solver.validate_words(HIGH_CONFIDENCE_WORDS)
    valid_medium = solver.validate_words(MEDIUM_CONFIDENCE_WORDS)
    valid_additional = solver.validate_words(ADDITIONAL_WORDS)
    
    print(f"✅ High confidence: {len(valid_high)}/{len(HIGH_CONFIDENCE_WORDS)} valid")
    print(f"✅ Medium confidence: {len(valid_medium)}/{len(MEDIUM_CONFIDENCE_WORDS)} valid")
    print(f"✅ Additional: {len(valid_additional)}/{len(ADDITIONAL_WORDS)} valid")
    
    # Try different strategies
    strategies = [
        ("High Confidence Only (8 words)", lambda: solver.strategy_high_confidence_only()),
        ("High + Medium Confidence", lambda: solver.strategy_high_plus_medium()),
    ]
    
    for strategy_name, strategy_func in strategies:
        print(f"\n\n{'='*70}")
        print(f"Attempting: {strategy_name}")
        print(f"{'='*70}")
        
        solver.attempts = 0
        solver.valid_checksums = 0
        solver.start_time = time.time()
        
        try:
            if strategy_func():
                print("\n✅ Solution found!")
                return
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            elapsed = time.time() - solver.start_time
            print(f"Tested {solver.attempts:,} combinations in {elapsed:.2f}s")
            return
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue
    
    print("\n\n" + "="*70)
    print("❌ No solution found with current strategies")
    print("="*70)
    print("\nPossible reasons:")
    print("1. Some identified words are incorrect")
    print("2. A BIP39 passphrase is required (13th word)")
    print("3. The puzzle uses Electrum wallet format instead of BIP39")
    print("4. Additional clues in the image haven't been decoded")
    print("5. The 'Sum of two numbers' clue is critical and not yet understood")


if __name__ == "__main__":
    main()
