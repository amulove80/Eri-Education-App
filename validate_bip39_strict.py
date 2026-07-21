#!/usr/bin/env python3
"""
Validate ALL candidate words against official BIP39 wordlist
ONLY use words that are actually in BIP39!
"""

# Load official BIP39 wordlist
with open("/workspace/bip39_wordlist.txt", "r") as f:
    BIP39_WORDS = set(word.strip().lower() for word in f.readlines())

print(f"Loaded {len(BIP39_WORDS)} official BIP39 words\n")

# All our candidate words
CANDIDATES = [
    "moon", "tower", "food", "breathe", "this", "subject", "real", "black", "only",
    "time", "proof", "world", "one", "brave", "new", "order", "liberty", "eye", 
    "pyramid", "mask", "camera", "chain", "coin", "digital", "key", "system", 
    "history", "verify", "owner", "state", "virus", "future", "change", "vote",
    "day", "home", "face", "sign", "picture", "weapon", "stop", "peace", "justice"
]

print("="*70)
print("VALIDATING CANDIDATE WORDS AGAINST OFFICIAL BIP39 WORDLIST")
print("="*70)

valid_words = []
invalid_words = []

for word in CANDIDATES:
    if word.lower() in BIP39_WORDS:
        valid_words.append(word)
        print(f"✅ {word}")
    else:
        invalid_words.append(word)
        print(f"❌ {word} - NOT IN BIP39 WORDLIST!")

print(f"\n{'='*70}")
print(f"RESULTS")
print("="*70)
print(f"✅ Valid BIP39 words: {len(valid_words)}/{len(CANDIDATES)}")
print(f"❌ Invalid words: {len(invalid_words)}")

if invalid_words:
    print(f"\n🚨 INVALID WORDS (cannot be in seed):")
    for word in invalid_words:
        print(f"   - {word}")
    
    # Find similar BIP39 words
    print(f"\n🔍 Looking for similar BIP39 words:")
    for invalid in invalid_words:
        similar = [w for w in BIP39_WORDS if w.startswith(invalid[:3]) or invalid[:3] in w]
        if similar:
            print(f"   {invalid} → {similar[:5]}")

print(f"\n✅ CONFIRMED VALID BIP39 WORDS ({len(valid_words)}):")
print(f"   {', '.join(sorted(valid_words))}")

# Save valid words
with open("/workspace/confirmed_bip39_words.txt", "w") as f:
    f.write(",".join(sorted(valid_words)))

print(f"\nSaved to: confirmed_bip39_words.txt")
