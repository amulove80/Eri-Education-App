#!/usr/bin/env python3
"""
Validate all candidate words against the BIP39 wordlist
"""

from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator, Bip39Languages, Bip39MnemonicDecoder

def get_bip39_wordlist_fallback():
    """Fallback: return standard BIP39 English words we know are valid"""
    # Just test our specific words against mnemonic validation
    return None  # Will use validation method instead

# Get the official BIP39 English wordlist
def get_bip39_wordlist():
    """Get the complete BIP39 English wordlist"""
    try:
        # Try to load from installed package
        from bip_utils.bip.bip39.bip39_mnemonic_utils import Bip39WordsList
        wordlist = Bip39WordsList(Bip39Languages.ENGLISH)
        return set(wordlist.GetWords())
    except Exception as e:
        # Fallback: Use Bip39MnemonicDecoder to access the wordlist
        try:
            decoder = Bip39MnemonicDecoder(Bip39Languages.ENGLISH)
            # Generate test words to extract wordlist
            wordlist = set()
            for i in range(2048):
                # Generate a mnemonic with this word index
                mnemonic = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
                words = mnemonic.ToList()
                wordlist.update(words)
                if len(wordlist) >= 2048:
                    break
            if len(wordlist) >= 100:  # At least got some words
                return wordlist
        except:
            pass
        
        # Last resort: Download the standard BIP39 wordlist
        print(f"Warning: Could not load wordlist from library, using fallback")
        return get_bip39_wordlist_fallback()

# All candidate words from puzzle analysis
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
    print("BIP39 Word Validation")
    print("="*70 + "\n")
    
    wordlist = get_bip39_wordlist()
    print(f"BIP39 wordlist size: {len(wordlist)} words\n")
    
    def check_words(words, category):
        print(f"\n{category}:")
        print("-" * 50)
        valid = []
        invalid = []
        
        for word in words:
            if word in wordlist:
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
    print(f"\nTotal Valid Words: {len(valid_high) + len(valid_medium) + len(valid_additional)}")
    
    all_valid = valid_high + valid_medium + valid_additional
    all_invalid = invalid_high + invalid_medium + invalid_additional
    
    if all_invalid:
        print(f"\n❌ Invalid words to remove: {all_invalid}")
        
        # Suggest replacements
        print("\n🔍 Checking for similar BIP39 words:")
        for invalid_word in all_invalid:
            similar = [w for w in wordlist if w.startswith(invalid_word[:3])]
            if similar:
                print(f"  {invalid_word} → Possible: {similar[:5]}")
    
    print(f"\n✅ All valid words ({len(all_valid)}):")
    print(f"   {', '.join(all_valid)}")
    
    return all_valid, all_invalid

if __name__ == "__main__":
    validate_candidates()
