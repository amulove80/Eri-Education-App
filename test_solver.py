#!/usr/bin/env python3
"""
Test the puzzle solver with known seed phrases to verify it works correctly
"""

from btc_puzzle_solver import PuzzleSolver

def test_known_address():
    """Test with a known seed phrase to verify the address generation works"""
    solver = PuzzleSolver()
    
    # Test with a well-known example seed
    test_phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    expected_address = "1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA"
    
    print("Testing address generation with known seed...")
    print(f"Seed: {test_phrase}")
    
    address = solver.generate_address_from_seed(test_phrase)
    print(f"Generated: {address}")
    print(f"Expected: {expected_address}")
    
    if address == expected_address:
        print("✅ Address generation working correctly!\n")
        return True
    else:
        print("❌ Address generation mismatch!\n")
        return False

def test_checksum_validation():
    """Test checksum validation"""
    solver = PuzzleSolver()
    
    print("Testing checksum validation...")
    
    # Valid mnemonic
    valid = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    print(f"Valid mnemonic: {solver.is_valid_mnemonic(valid)}")
    
    # Invalid mnemonic (wrong checksum)
    invalid = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
    print(f"Invalid mnemonic: {not solver.is_valid_mnemonic(invalid)}")
    
    print()

def test_word_validation():
    """Test BIP39 word validation"""
    solver = PuzzleSolver()
    
    print("Testing word validation...")
    
    test_words = ["moon", "tower", "food", "notaword", "bitcoin", "real"]
    valid = solver.validate_words(test_words)
    
    print(f"Input words: {test_words}")
    print(f"Valid BIP39 words: {valid}")
    print()

if __name__ == "__main__":
    print("="*70)
    print("BTC Puzzle Solver - Unit Tests")
    print("="*70 + "\n")
    
    test_known_address()
    test_checksum_validation()
    test_word_validation()
    
    print("="*70)
    print("All tests completed!")
    print("="*70)
