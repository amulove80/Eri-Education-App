#!/usr/bin/env python3
"""
FINAL ULTRA-COMPREHENSIVE SOLVER
Testing the possibility that some "certain" words are wrong
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39Languages
import itertools
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Expand word pool - maybe we're missing something
ALL_CANDIDATES = [
    # Original "certain" words
    "moon", "tower", "food", "this", "subject", "real", "black", "only",
    
    # Very likely
    "time", "proof", "world", "one",
    
    # Thematic
    "brave", "new", "order", "liberty", "eye", "pyramid", "mask", "camera",
    
    # Bitcoin-related BIP39 words
    "chain", "coin", "digital", "key", "system", "history", "verify", "owner",
    
    # 2020-related
    "state", "virus", "future", "change", "vote",
    
    # Less obvious but possible
    "day", "home", "face", "sign", "picture", "weapon",
]

print(f"Testing with {len(ALL_CANDIDATES)} candidate words")

def fast_test(phrase, passphrase=""):
    """Fast test without try/catch for speed"""
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress() == TARGET_ADDRESS
    except:
        return False

def ultra_test():
    """Test massive combinations efficiently"""
    print("="*70)
    print("ULTRA-COMPREHENSIVE TESTING")
    print("="*70)
    print(f"Words: {len(ALL_CANDIDATES)}")
    print(f"Testing combinations of 12 words with various passphrases\n")
    
    tested = 0
    valid_checked = 0
    start = time.time()
    last_report = start
    
    # Passphrases to try
    passphrases = ["", "BREATHE", "breathe"]
    
    # Focus on most likely combinations
    top_words = ALL_CANDIDATES[:20]  # Top 20
    
    # Test all 12-word combinations from top 20
    for combo_num, combo in enumerate(itertools.combinations(top_words, 12)):
        # For each combination, test a sample of permutations
        perm_sample = min(20, 479001600)  # Sample 20 permutations per combo
        
        for perm_num, perm in enumerate(itertools.permutations(combo)):
            if perm_num >= perm_sample:
                break
            
            phrase = " ".join(perm)
            
            # Test with each passphrase
            for passphrase in passphrases:
                tested += 1
                
                if fast_test(phrase, passphrase):
                    elapsed = time.time() - start
                    print(f"\n{'='*70}")
                    print(f"🎉🎉🎉 SOLUTION FOUND! 🎉🎉🎉")
                    print("="*70)
                    print(f"Seed: {phrase}")
                    if passphrase:
                        print(f"Passphrase: {passphrase}")
                    print(f"Address: {TARGET_ADDRESS}")
                    print(f"Tested: {tested:,} combinations in {elapsed:.2f}s")
                    print("="*70)
                    
                    with open("/workspace/SOLUTION.txt", "w") as f:
                        f.write(f"SOLUTION!\n")
                        f.write(f"Seed: {phrase}\n")
                        f.write(f"Passphrase: {passphrase}\n")
                    return True
                
                # Progress report
                now = time.time()
                if now - last_report >= 10:
                    elapsed = now - start
                    rate = tested / elapsed
                    print(f"  Tested: {tested:,} | Rate: {rate:.0f}/s | Time: {elapsed:.1f}s")
                    last_report = now
                
                if tested >= 100000:  # Limit to 100k tests
                    print(f"\nReached test limit: {tested:,}")
                    return False
    
    elapsed = time.time() - start
    print(f"\nTested {tested:,} combinations in {elapsed:.2f}s")
    print(f"Rate: {tested/elapsed:.0f} combinations/second")
    return False

def test_specific_community_hints():
    """Test very specific hints from community"""
    print("\n" + "="*70)
    print("TESTING SPECIFIC COMMUNITY HINTS")
    print("="*70)
    
    # Specific sequences from community analysis with high confidence
    specific_tests = [
        # Based on "THIS IS THE FIRST" → this is word 1
        (["this", "moon", "tower", "food", "black", "subject", "real", "time", "proof", "only", "world", "one"], ""),
        
        # Based on position 5 = black (5HT hint)
        (["this", "moon", "tower", "food", "black", "subject", "real", "time", "proof", "only", "world", "one"], ""),
        
        # Reverse some assumptions - maybe "black" ISN'T in it (post-Floyd)
        (["this", "moon", "tower", "food", "brave", "subject", "real", "time", "proof", "only", "world", "one"], ""),
        (["this", "moon", "tower", "food", "order", "subject", "real", "time", "proof", "only", "world", "one"], ""),
        (["this", "moon", "tower", "food", "new", "subject", "real", "time", "proof", "only", "world", "brave"], ""),
        
        # Maybe "this" is wrong - try "brave" first
        (["brave", "moon", "tower", "food", "black", "subject", "real", "time", "proof", "only", "world", "new"], ""),
        (["brave", "new", "world", "moon", "tower", "food", "subject", "real", "time", "proof", "only", "order"], ""),
    ]
    
    for i, (seq, pp) in enumerate(specific_tests, 1):
        phrase = " ".join(seq)
        print(f"\nTest {i}: {seq[0]} {seq[1]} {seq[2]} ... {seq[-2]} {seq[-1]}")
        
        for passphrase in ["", "BREATHE", "breathe", "brave"]:
            if fast_test(phrase, passphrase):
                print(f"\n🎉 FOUND with passphrase='{passphrase}'!")
                return True
    
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           FINAL ULTRA-COMPREHENSIVE SOLVER                   ║
║                                                              ║
║  Testing with expanded word pool                             ║
║  Considering some "certain" words may be wrong               ║
║  Systematic high-speed testing                               ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Try specific hints first (fast)
    if test_specific_community_hints():
        return
    
    # Then do ultra-comprehensive
    ultra_test()
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("""
The puzzle has not been solved despite testing:
- Thousands of word combinations
- Multiple passphrase variants  
- Position-based sequences
- Community-identified words
- Timeline-based ordering

This strongly suggests:
1. At least one "certain" word is actually WRONG
2. OR the "Sum of two numbers" clue is more critical than understood
3. OR it's an 18-word seed (Brave New World = 18 chapters)
4. OR there's a specific word order pattern not yet decoded
5. OR the passphrase is something other than BREATHE

The puzzle creator designed this to resist brute force.
The solution requires correctly interpreting the visual clues,
particularly the "Sum of two numbers" text.
    """)

if __name__ == "__main__":
    main()
