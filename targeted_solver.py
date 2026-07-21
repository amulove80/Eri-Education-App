#!/usr/bin/env python3
"""
Targeted puzzle solver - tests specific high-probability combinations
Based on: 8 high confidence + 6 medium confidence = 14 words, choose 12
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

# Most likely 14 words (high + medium confidence)
MOST_LIKELY_WORDS = [
    # High confidence (8)
    "moon", "tower", "food", "breathe", "this", "subject", "real", "black",
    # Medium confidence (6)
    "time", "proof", "only", "win", "world", "face"
]

class TargetedSolver:
    def __init__(self):
        self.attempts = 0
        self.valid_checksums = 0
        self.start_time = time.time()
        self.last_report = time.time()
    
    def is_valid_mnemonic(self, phrase):
        try:
            Bip39MnemonicValidator().Validate(phrase)
            return True
        except:
            return False
    
    def generate_address(self, seed_phrase):
        try:
            seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
            bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            return bip44_acc.PublicKey().ToAddress()
        except:
            return None
    
    def test_combination(self, words):
        self.attempts += 1
        phrase = " ".join(words)
        
        # Check valid checksum first
        if not self.is_valid_mnemonic(phrase):
            return False
        
        self.valid_checksums += 1
        
        # Generate address
        address = self.generate_address(phrase)
        
        if address == TARGET_ADDRESS:
            elapsed = time.time() - self.start_time
            print(f"\n\n{'='*70}")
            print("🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
            print("="*70)
            print(f"\nSeed Phrase: {phrase}")
            print(f"Address: {address}")
            print(f"\nAttempts: {self.attempts:,}")
            print(f"Valid checksums tested: {self.valid_checksums:,}")
            print(f"Time elapsed: {elapsed:.2f} seconds")
            print(f"Rate: {self.attempts/elapsed:.0f} combinations/second")
            print("="*70)
            
            # Save to file
            with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                f.write(f"SOLUTION TO 0.2 BTC PUZZLE\n")
                f.write(f"="*70 + "\n\n")
                f.write(f"Seed Phrase: {phrase}\n")
                f.write(f"Address: {address}\n")
                f.write(f"Found: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            return True
        
        # Progress report
        now = time.time()
        if now - self.last_report >= 10:
            elapsed = now - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            eta_total = (self.total_combinations - self.attempts) / rate if rate > 0 else 0
            
            print(f"Progress: {self.attempts:,}/{self.total_combinations:,} "
                  f"({100*self.attempts/self.total_combinations:.2f}%) | "
                  f"Valid: {self.valid_checksums:,} | "
                  f"Rate: {rate:.0f}/s | "
                  f"Elapsed: {elapsed/60:.1f}m | "
                  f"ETA: {eta_total/60:.1f}m")
            self.last_report = now
        
        return False
    
    def solve_with_combinations(self, words, choose_n=12):
        """Test all combinations of choose_n words from the word list"""
        print(f"\n{'='*70}")
        print(f"Testing combinations: {len(words)} words, choose {choose_n}")
        print("="*70)
        print(f"Words: {words}\n")
        
        # Calculate total combinations
        # We need C(n, r) * r! which equals P(n, r) = n!/(n-r)!
        from math import factorial
        n = len(words)
        r = choose_n
        
        # This is actually just permutations: P(n,r) = n!/(n-r)!
        total = factorial(n) // factorial(n - r)
        
        # For display: show combinations and permutations separately
        n_combinations = factorial(n) // (factorial(r) * factorial(n - r))
        n_permutations_per = factorial(r)
        
        self.total_combinations = total
        
        print(f"Total combinations: {total:,}")
        print(f"  = {n_combinations:,} ways to choose {r} from {n}")
        print(f"  × {n_permutations_per:,} permutations of {r} words")
        
        # Estimate time
        estimated_rate = 50000  # Conservative estimate: 50k/sec
        estimated_seconds = total / estimated_rate
        print(f"\nEstimated time at {estimated_rate:,}/s: {estimated_seconds/60:.1f} minutes")
        print(f"Starting search...\n")
        
        self.start_time = time.time()
        
        try:
            # For each combination of 12 words
            for combo in itertools.combinations(words, choose_n):
                # Test all permutations of those 12 words
                for perm in itertools.permutations(combo):
                    if self.test_combination(perm):
                        return True
            
            print(f"\n{'='*70}")
            print("Search complete - no solution found")
            print("="*70)
            return False
            
        except KeyboardInterrupt:
            print(f"\n\n{'='*70}")
            print("⚠️  Search interrupted by user")
            print("="*70)
            elapsed = time.time() - self.start_time
            print(f"Tested: {self.attempts:,} combinations")
            print(f"Valid checksums: {self.valid_checksums:,}")
            print(f"Time: {elapsed:.2f} seconds ({elapsed/60:.1f} minutes)")
            print(f"Rate: {self.attempts/elapsed:.0f} combinations/second")
            return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║        0.2 BTC Puzzle - Targeted High-Probability Solver      ║
║                                                              ║
║  Target: 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ                  ║
║  Strategy: Test 14 most likely words, choose 12             ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    solver = TargetedSolver()
    
    # Test the 14 most likely words
    result = solver.solve_with_combinations(MOST_LIKELY_WORDS, choose_n=12)
    
    if not result:
        print("\n💡 ANALYSIS:")
        print("The puzzle was not solved with the 14 most confident words.")
        print("This suggests:")
        print("  1. Some of the 'high confidence' words may be incorrect")
        print("  2. Some 'additional' words should be in the set")
        print("  3. A BIP39 passphrase (13th word) may be required")
        print("  4. The 'Sum of two numbers' clue is critical")
        print("  5. The wallet may use Electrum format instead of BIP39")

if __name__ == "__main__":
    main()
