#!/usr/bin/env python3
"""
Order-based solver - Use visual/temporal clues to determine word order
Based on the hypothesis that the image reveals the sequence
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

# Potential ordered sequences based on image analysis
# The image depicts events of 2020 in chronological order

# Hypothesis 1: Timeline of 2020 events
# January-March: virus/pandemic starts
# May: George Floyd / BLM protests  
# Throughout: masks, social distancing
# November: Election (tower=capitol? this=democracy?)
# Overall: world, time, face, breathe

SEQUENCE_HYPOTHESES = [
    {
        "name": "2020 Timeline Narrative",
        "order": ["world", "virus", "breathe", "mask", "face", "black", "subject", "this", "tower", "only", "real", "future"],
        "logic": "World → virus → breathing issues → masks → faces covered → BLM (black) → subject of protests → this moment → tower (capitol) → only → real → future"
    },
    {
        "name": "Image Left-to-Right Top-to-Bottom",
        "order": ["tower", "moon", "time", "food", "this", "black", "breathe", "subject", "real", "proof", "only", "world"],
        "logic": "Reading the image spatially from top-left to bottom-right"
    },
    {
        "name": "Clock-Based Sequence",
        "order": ["moon", "tower", "time", "food", "this", "world", "proof", "only", "real", "breathe", "black", "subject"],
        "logic": "Starting from 12 o'clock (moon/tower on hands) and moving clockwise"
    },
    {
        "name": "High Confidence First",
        "order": ["moon", "tower", "food", "breathe", "this", "subject", "real", "black", "time", "proof", "only", "world"],
        "logic": "Most certain words first, then medium confidence"
    },
    {
        "name": "Reverse Timeline",
        "order": ["future", "real", "only", "tower", "this", "subject", "black", "face", "mask", "breathe", "virus", "world"],
        "logic": "Looking back from the future to 2020 events"
    },
    {
        "name": "BLM Protest Focus",
        "order": ["black", "breathe", "subject", "real", "this", "world", "time", "face", "tower", "proof", "only", "food"],
        "logic": "BLM theme as central: black lives matter, I can't breathe, subject of injustice"
    },
]

def test_sequence(words, name):
    """Test a specific word sequence"""
    if len(words) != 12:
        print(f"  ❌ {name}: Wrong number of words ({len(words)})")
        return False
    
    phrase = " ".join(words)
    
    # Check if valid BIP39
    try:
        Bip39MnemonicValidator().Validate(phrase)
    except Exception as e:
        print(f"  ❌ {name}: Invalid BIP39 checksum")
        return False
    
    # Generate address
    try:
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip44_acc.PublicKey().ToAddress()
        
        if address == TARGET_ADDRESS:
            print(f"\n{'='*70}")
            print(f"🎉 SOLUTION FOUND! 🎉")
            print("="*70)
            print(f"Hypothesis: {name}")
            print(f"Seed: {phrase}")
            print(f"Address: {address}")
            print("="*70)
            
            with open("/workspace/SOLUTION.txt", "w") as f:
                f.write(f"SOLUTION FOUND!\n")
                f.write(f"Hypothesis: {name}\n")
                f.write(f"Seed: {phrase}\n")
                f.write(f"Address: {address}\n")
            return True
        else:
            print(f"  ✅ {name}: Valid BIP39, address: {address[:20]}...")
            return False
            
    except Exception as e:
        print(f"  ❌ {name}: Error generating address: {e}")
        return False

def main():
    print("="*70)
    print("ORDER-BASED PUZZLE SOLVER")
    print("="*70)
    print("\nTesting specific word sequences based on image clues\n")
    
    for hypothesis in SEQUENCE_HYPOTHESES:
        print(f"\nHypothesis: {hypothesis['name']}")
        print(f"Logic: {hypothesis['logic']}")
        print(f"Sequence: {' '.join(hypothesis['order'])}")
        
        if test_sequence(hypothesis['order'], hypothesis['name']):
            return True
    
    print(f"\n{'='*70}")
    print("No solution found in tested hypotheses")
    print("="*70)
    print("\nNext steps:")
    print("1. Analyze the actual puzzle image more carefully")
    print("2. Decode the 'Sum of two numbers' clue")
    print("3. Consider that some identified words may be wrong")
    print("4. Try different word combinations from the candidate list")
    return False

if __name__ == "__main__":
    main()
