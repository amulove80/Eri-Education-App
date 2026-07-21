# 0.2 BTC Puzzle Solver

## Overview

This repository contains tools and analysis for solving the 0.2 BTC puzzle posted in 2020.

**Target Address**: `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ`  
**Prize**: 0.201 BTC (~$20,000+ USD)  
**Status**: UNSOLVED (as of July 2026)

## Files

- `puzzle_analysis.md` - Detailed analysis of clues and hints
- `btc_puzzle_solver.py` - Advanced multi-strategy solver
- `targeted_solver.py` - Focused solver for most likely word combinations
- `validate_words_simple.py` - BIP39 word validation tool
- `valid_bip39_words.txt` - List of all validated candidate words
- `test_solver.py` - Unit tests for the solver

## Quick Start

### Install Dependencies

```bash
pip install bip-utils
```

### Run Targeted Solver

```bash
python3 targeted_solver.py
```

This tests the 14 most confident words (8 high + 6 medium confidence), choosing 12 at a time.

## Identified Words

### High Confidence (8 words)
Based on direct clues in the image:
- moon (clock hands)
- tower (clock hands)
- food (Seattle Space Needle)
- breathe (George Floyd's chest, Statue's Neck)
- this (repeated multiple times)
- subject (underlined on statue)
- real ("Only real Bitcoin")
- black ("The Pot Calling The Kettle Black" + BLM)

### Medium Confidence (6 words)
- time (clock imagery)
- proof (proof of work)
- only ("Only Bitcoin")
- win
- world
- face (face masks)

### Additional Candidates (23 words)
twenty, flag, hand, sign, state, virus, mask, order, digital, coin, chest, picture, pyramid, weapon, neck, camera, eye, day, first, major, country, home, future

**All 37 words are valid BIP39 words.**

## Key Clues

1. **Russian text**: "Sum of two numbers" - Critical unsolved clue
2. **Number 12 on clock** pointing to STOP sign → Confirms 12-word seed
3. **Timeline/narrative** in image may indicate word order
4. **Bill's Cipher**: "Tuesday"
5. Community has tested 479M+ combinations without success

## Strategies

### Current Approach
Testing all combinations of the 14 most likely words (choose 12):
- Total combinations: ~1.02 billion
- With checksum filtering: ~66 million valid to test
- Estimated time: ~20-30 minutes at 50k/sec

### If Current Approach Fails
1. Some "high confidence" words may be incorrect
2. Need to include some "additional" words
3. May require BIP39 passphrase (13th word)
4. "Sum of two numbers" clue may be critical
5. Wallet might use Electrum format instead of BIP39

## Research Notes

- Puzzle has been unsolved for 6+ years
- Extensive GPU brute-force attempts have failed
- Community consensus: gated on specific words/positions, not compute
- Some speculation that puzzle may require additional passphrase
- Bitcoin still in address (verified July 2026)

## Contributing

If you have insights about:
- The "Sum of two numbers" Russian text clue
- Word order based on image timeline
- Additional hidden words in the image
- Alternative wallet formats (Electrum)

Please share your findings!

## Disclaimer

This is for educational and research purposes. The puzzle creator intended it to be solved through careful analysis of the image clues.
