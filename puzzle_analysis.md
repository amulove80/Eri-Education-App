# 0.2 BTC Puzzle Analysis

## Target Information
- **Address**: 1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ
- **Prize**: 0.201 BTC (~$20,000+ USD)
- **Status**: UNSOLVED (as of July 2026)
- **Date Created**: 2020-05-10

## Puzzle Description
A seed phrase is hidden in an image containing various visual clues, text references, and encoded messages.

## Identified Seed Word Candidates

### High Confidence Words (directly mentioned in hints):
1. **moon** - Found on clock's hands
2. **tower** - Found on clock's hands
3. **food** - Found on Seattle Space Needle
4. **breathe** - Found on George Floyd's chest and Statue's Neck
5. **this** - Repeated in multiple places: "This is the first prediction," "Fuck this shit," "Find the seed phrase in this picture"
6. **subject** - Underlined on the statue to the right
7. **real** - From "Only real Bitcoin" on Statue of Liberty base
8. **black** - Latin reference "The Pot Calling The Kettle Black" + BLM references

### Medium Confidence Words (from community analysis):
9. **time** - Related to clock imagery
10. **proof** - May be related to "proof of work" or other Bitcoin concepts
11. **only** - From "Only Bitcoin" text
12. **win** - Possible word from image
13. **world** - May be in image
14. **face** - Related to face coverings/masks

### Lower Confidence / Additional Candidates:
- twenty, flag, hand, sign, state, virus, mask, order, digital, coin, chest, picture
- pyramid, weapon, neck, camera, eye, day, first, major, country, home, future

## Important Clues

### Russian Text Translations:
1. **Top Left**: "I hope that many bitcoins will be sent here"
2. **Bottom Left**: "Sum of two numbers" ← CRITICAL CLUE
3. **Long on Right**: "Here are encrypted bitcoins for a rainy day number X"

### Other Clues:
4. **Bill's Cipher** (Above Trump): "Tuesday"
5. **Number 12** on clock pointing to STOP sign → Confirms 12-word seed phrase
6. **Order matters**: The image timeline suggests word order

## Key Insights from Research

1. **Brute Force Failed**: 479 million permutations tested with GPU without match
2. **Not All Words Correct**: Community consensus is that some identified words are wrong
3. **Positional Clues**: The order is likely indicated by the image narrative/timeline
4. **Possible Passphrase**: Some suggest a BIP39 passphrase may be required
5. **Checksum Filtering**: Many combinations fail BIP39 checksum validation

## Strategies to Try

### Strategy 1: Focus on High-Confidence Words Only
Test permutations of the 8-14 most certain words, looking for valid BIP39 combinations.

### Strategy 2: Timeline/Narrative Order
Analyze the image for a timeline or story that indicates word order:
- Events of 2020: pandemic, protests, election
- Spatial layout: left to right, top to bottom
- Clock positions: numerical order

### Strategy 3: "Sum of Two Numbers" Clue
The Russian text "Sum of two numbers" may indicate:
- Two words combine to form meaning
- Numeric positions that should be added
- Two separate seed phrases that combine

### Strategy 4: BIP39 Wordlist Validation
Ensure all candidate words are actually in the BIP39 wordlist (2048 words).

### Strategy 5: Pattern Recognition
Look for:
- Repeated letters/sounds
- Alliteration
- Mnemonic patterns that would be memorable

## Technical Approach

1. **Validate all words against BIP39 wordlist**
2. **Pre-filter using checksum validation** (eliminates ~93.75% of combinations)
3. **Test high-confidence combinations first**
4. **Use GPU acceleration if available**
5. **Consider both standard derivation paths**:
   - BIP44: m/44'/0'/0'/0/0 (most common)
   - BIP32/Electrum: Different derivation

## Next Steps

1. Create optimized solver with checksum pre-filtering
2. Test most probable word combinations
3. Analyze image more carefully for positional clues
4. Consider alternate wallet types (Electrum vs BIP39)
5. Research if passphrase is needed
