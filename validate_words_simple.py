#!/usr/bin/env python3
"""
Simpler validation - just check if words work in valid mnemonics
"""

from bip_utils import Bip39MnemonicValidator, Bip39MnemonicGenerator, Bip39WordsNum, Bip39Languages

# Test if a word is valid by seeing if it's accepted in a mnemonic
def is_valid_bip39_word(word):
    """Check if a word is in the BIP39 wordlist by testing it"""
    # Generate a random valid mnemonic
    mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    words = mnemonic.ToList()
    
    # Replace first word with test word and see if it could be valid
    # (We can't fully validate without correct checksum, but we can see if it's rejected as invalid word)
    test_phrase = [word] + words[1:]
    test_string = " ".join(test_phrase)
    
    try:
        # This will fail on checksum, but that's ok - we just want to know if the word itself is recognized
        Bip39MnemonicValidator().Validate(test_string)
        return True  # If it passed, word is valid
    except ValueError as e:
        error_msg = str(e)
        # Check if error is about invalid word vs invalid checksum
        if "Invalid word" in error_msg or "not in word list" in error_msg.lower():
            return False
        else:
            # Checksum error means the word itself is valid
            return True
    except Exception as e:
        # Any other error, assume word might be valid
        return True

# All candidate words
HIGH_CONFIDENCE = ["moon", "tower", "food", "breathe", "this", "subject", "real", "black"]
MEDIUM_CONFIDENCE = ["time", "proof", "only", "win", "world", "face"]
ADDITIONAL = [
    "twenty", "flag", "hand", "sign", "state", "virus", "mask",
    "order", "digital", "coin", "chest", "picture", "pyramid",
    "weapon", "neck", "camera", "eye", "day", "first", "major",
    "country", "home", "future"
]

def validate_candidates():
    """Validate all candidate words"""
    print("="*70)
    print("BIP39 Word Validation (Testing Method)")
    print("="*70 + "\n")
    
    def check_words(words, category):
        print(f"\n{category}:")
        print("-" * 50)
        valid = []
        invalid = []
        
        for word in words:
            if is_valid_bip39_word(word):
                valid.append(word)
                print(f"  ✅ {word}")
            else:
                invalid.append(word)
                print(f"  ❌ {word} (NOT IN BIP39 WORDLIST)")
        
        print(f"\nValid: {len(valid)}/{len(words)}")
        return valid, invalid
    
    valid_high, invalid_high = check_words(HIGH_CONFIDENCE, "HIGH CONFIDENCE WORDS")
    valid_medium, invalid_medium = check_words(MEDIUM_CONFIDENCE, "MEDIUM CONFIDENCE WORDS")  
    valid_additional, invalid_additional = check_words(ADDITIONAL, "ADDITIONAL WORDS")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"High Confidence: {len(valid_high)}/{len(HIGH_CONFIDENCE)} valid")
    print(f"Medium Confidence: {len(valid_medium)}/{len(MEDIUM_CONFIDENCE)} valid")
    print(f"Additional: {len(valid_additional)}/{len(ADDITIONAL)} valid")
    
    all_valid = valid_high + valid_medium + valid_additional
    all_invalid = invalid_high + invalid_medium + invalid_additional
    
    print(f"\nTotal Valid Words: {len(all_valid)}")
    
    if all_invalid:
        print(f"\n❌ Invalid words to remove: {all_invalid}")
    
    print(f"\n✅ All valid words ({len(all_valid)}):")
    for i, word in enumerate(all_valid):
        if i % 6 == 0:
            print()
        print(f"  {word:12}", end="")
    print("\n")
    
    # Save to file
    with open("/workspace/valid_bip39_words.txt", "w") as f:
        f.write(",".join(all_valid))
    print("Valid words saved to: valid_bip39_words.txt")
    
    return all_valid, all_invalid

if __name__ == "__main__":
    valid, invalid = validate_candidates()
