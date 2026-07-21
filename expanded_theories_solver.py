#!/usr/bin/env python3
"""
EXPANDED THEORIES SOLVER
Testing alternative approaches and word selections
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import time

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Extended word pool - including more thematic matches
EXTENDED_VALID = [
    # Core high-confidence
    "moon", "tower", "food", "this", "subject", "real", "black", "only",
    "time", "proof", "world", "one", "brave", "order", "liberty", "eye",
    
    # Medium confidence
    "pyramid", "mask", "camera", "peace", "change", "coin", "digital",
    "virus", "vote", "weapon", "sign", "state", "home", "key", "face",
    
    # Others that could fit thematically
    "day", "owner", "future", "history", "picture", "verify"
]

PASSPHRASES = ["", "BREATHE", "breathe", "Breathe", "ICANTBREATHE", "I CANT BREATHE"]

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
    print(f"\n\n{'='*70}")
    print(f"SOLUTION FOUND!")
    print("="*70)
    print(f"Seed: {phrase}")
    if pp:
        print(f"Passphrase: {pp}")
    print(f"Address: {TARGET_ADDRESS}")
    print("="*70)
    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
        f.write(f"SOLUTION!\nSeed: {phrase}\nPassphrase: {pp}\n")
    return True

def theory_1_replace_uncertain():
    """Replace possibly wrong 'certain' words"""
    print("\n" + "="*70)
    print("THEORY 1: Replace uncertain 'certain' words")
    print("="*70)
    
    # Maybe "this" or "subject" is wrong?
    base = ["moon", "tower", "food", "real", "black", "only", "time", "proof"]
    alternatives = {
        "word9": ["world", "order", "peace"],
        "word10": ["one", "day", "key"],
        "word11": ["brave", "liberty", "vote"],
        "word12": ["order", "sign", "state"]
    }
    
    tested = 0
    start = time.time()
    
    for w9 in alternatives["word9"]:
        for w10 in alternatives["word10"]:
            for w11 in alternatives["word11"]:
                for w12 in alternatives["word12"]:
                    words = base + [w9, w10, w11, w12]
                    
                    # Test multiple orders
                    for perm_num, perm in enumerate(itertools.permutations(words)):
                        if perm_num >= 50:
                            break
                        
                        phrase = " ".join(perm)
                        for pp in PASSPHRASES:
                            if test_phrase(phrase, pp):
                                return found(phrase, pp)
                            tested += 1
                        
                        if tested % 10000 == 0:
                            print(f"  Tested: {tested:,} | Rate: {tested/(time.time()-start):.0f}/s")
    
    print(f"Theory 1: {tested:,} tested\n")
    return False

def theory_2_fewer_certain_words():
    """Only trust the MOST certain words"""
    print("\n" + "="*70)
    print("THEORY 2: Only trust 6 most certain words")
    print("="*70)
    
    # Only absolutely certain
    core = ["moon", "tower", "food", "black", "time", "world"]
    candidates = ["this", "subject", "real", "only", "proof", "one", "brave", 
                  "order", "liberty", "eye", "mask", "camera", "peace", "change"]
    
    tested = 0
    start = time.time()
    
    # Choose 6 more from candidates
    for combo in itertools.combinations(candidates, 6):
        words_12 = list(core) + list(combo)
        
        # Test 30 random permutations
        import random
        for _ in range(30):
            perm = list(words_12)
            random.shuffle(perm)
            phrase = " ".join(perm)
            
            for pp in PASSPHRASES:
                if test_phrase(phrase, pp):
                    return found(phrase, pp)
                tested += 1
            
            if tested % 10000 == 0:
                print(f"  Tested: {tested:,} | Rate: {tested/(time.time()-start):.0f}/s")
    
    print(f"Theory 2: {tested:,} tested\n")
    return False

def theory_3_specific_sequences():
    """Test highly specific sequences from image"""
    print("\n" + "="*70)
    print("THEORY 3: Highly specific sequences")
    print("="*70)
    
    sequences = [
        # Left to right, top to bottom reading
        "brave liberty moon tower food black mask this subject real time world",
        "moon tower brave liberty food black mask this subject real time world",
        
        # 2020 timeline focused (pre-May 25)
        "moon tower food black time world brave liberty peace this subject real",
        "brave moon tower food black time world liberty peace this subject real",
        
        # Moon/Tower first (clock), ending with key words
        "moon tower food this subject real black time proof world order liberty",
        "moon tower food this subject real brave time proof world one liberty",
        
        # Pyramid eye symbolism
        "pyramid eye moon tower food black mask this subject real time world",
        "eye pyramid moon tower food black mask this subject real time world",
        
        # Focus on words that appear in image
        "black face food mask moon this tower world brave liberty order peace",
        "moon tower food world time black mask brave liberty peace camera picture",
        
        # All about brave new world order
        "brave moon tower food world order black time this subject real only",
        "moon brave tower food world order black time this subject real only",
    ]
    
    tested = 0
    
    for i, seq in enumerate(sequences, 1):
        print(f"  Sequence {i}: {seq[:30]}...")
        
        words = seq.split()
        if len(words) == 12:
            # Test this exact sequence with all passphrases
            for pp in PASSPHRASES:
                if test_phrase(seq, pp):
                    return found(seq, pp)
                tested += 1
            
            # Also test some permutations
            for perm_num, perm in enumerate(itertools.permutations(words)):
                if perm_num >= 200:
                    break
                
                phrase = " ".join(perm)
                for pp in PASSPHRASES:
                    if test_phrase(phrase, pp):
                        return found(phrase, pp)
                    tested += 1
    
    print(f"Theory 3: {tested:,} tested\n")
    return False

def theory_4_alternate_passphrases():
    """Try different passphrase interpretations"""
    print("\n" + "="*70)
    print("THEORY 4: Alternative passphrase theories")
    print("="*70)
    
    alt_passphrases = [
        "",
        "BREATHE",
        "breathe",  
        "Breathe",
        "I CANT BREATHE",
        "ICANTBREATHE",
        "I can't breathe",
        "12",  # Number 12 clue
        "brave",  # THIS IS THE FIRST BRAVE
        "Brave",
        "BRAVE NEW WORLD",
        "0.2",  # The puzzle amount
        "2020",  # The year
        "May 10 2020",  # Wallet creation date
    ]
    
    # Use top words
    top_12 = ["moon", "tower", "food", "this", "subject", "real", "black", 
              "only", "time", "proof", "world", "one"]
    
    tested = 0
    start = time.time()
    
    # Test 1000 random permutations with each passphrase
    import random
    for pp in alt_passphrases:
        for _ in range(1000):
            perm = top_12.copy()
            random.shuffle(perm)
            phrase = " ".join(perm)
            
            if test_phrase(phrase, pp):
                return found(phrase, pp)
            tested += 1
        
        if tested % 10000 == 0:
            print(f"  Tested: {tested:,} | Passphrase: {pp[:20]} | Rate: {tested/(time.time()-start):.0f}/s")
    
    print(f"Theory 4: {tested:,} tested\n")
    return False

def theory_5_word_pairs():
    """Focus on likely word pairs"""
    print("\n" + "="*70)
    print("THEORY 5: Build from word pairs")
    print("="*70)
    
    # Likely pairs from image
    pairs = [
        ("moon", "tower"),
        ("brave", "liberty"),
        ("this", "subject"),
        ("black", "mask"),
        ("food", "world"),
        ("time", "proof"),
    ]
    
    # Additional words needed
    extras = ["real", "only", "one", "order", "eye", "peace"]
    
    tested = 0
    start = time.time()
    
    # Start with all pairs, choose some extras
    for extra_count in range(0, 4):  # Need 0-3 extras to make 12
        if 12 - extra_count == len(pairs) * 2:
            for extra_combo in itertools.combinations(extras, extra_count):
                words = []
                for p1, p2 in pairs[:6 - extra_count]:
                    words.extend([p1, p2])
                words.extend(extra_combo)
                
                if len(words) == 12:
                    # Test permutations
                    import random
                    for _ in range(20):
                        perm = words.copy()
                        random.shuffle(perm)
                        phrase = " ".join(perm)
                        
                        for pp in PASSPHRASES:
                            if test_phrase(phrase, pp):
                                return found(phrase, pp)
                            tested += 1
                    
                    if tested % 10000 == 0:
                        print(f"  Tested: {tested:,} | Rate: {tested/(time.time()-start):.0f}/s")
    
    print(f"Theory 5: {tested:,} tested\n")
    return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           EXPANDED THEORIES SOLVER                           ║
║                                                              ║
║  Testing alternative word selections and patterns            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    theories = [
        ("Replace Uncertain Words", theory_1_replace_uncertain),
        ("Fewer Certain Words", theory_2_fewer_certain_words),
        ("Specific Sequences", theory_3_specific_sequences),
        ("Alt Passphrases", theory_4_alternate_passphrases),
        ("Word Pairs", theory_5_word_pairs),
    ]
    
    global_start = time.time()
    
    for name, theory_func in theories:
        try:
            if theory_func():
                print(f"\n✅ SOLUTION FOUND via {name}!")
                return
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted")
            return
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
    
    print(f"\n{'='*70}")
    print(f"All theories tested in {time.time()-global_start:.1f}s")
    print("No solution found")
    print("="*70)

if __name__ == "__main__":
    main()
