#!/usr/bin/env python3
"""
Smart Balance Checker - Generate valid seeds using proper BIP39 methodology
"""

from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum,
                       Bip44, Bip44Coins, Bip44Changes, Bip39Languages)
import requests
import time
import random

TARGET = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

def check_balance(address):
    """Check balance using blockchain.info API"""
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            satoshi = int(response.text.strip())
            return satoshi / 100000000
        return None
    except:
        return None

def test_valid_random_seeds(count=100):
    """Generate truly valid random BIP39 seeds and check balances"""
    print(f"Generating {count} valid random BIP39 seeds and checking balances...\n")
    
    checked = 0
    with_balance = 0
    
    for i in range(count):
        # Generate a valid 12-word mnemonic
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        phrase = mnemonic.ToStr()
        
        # Derive address
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip44_acc.PublicKey().ToAddress()
        
        # Check if it's our target
        if address == TARGET:
            print(f"\n🎉🎉🎉 TARGET FOUND! 🎉🎉🎉")
            print(f"Seed: {phrase}")
            with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                f.write(f"SOLUTION!\nSeed: {phrase}\nAddress: {address}\n")
            return True
        
        # Check balance
        balance = check_balance(address)
        checked += 1
        
        if balance is not None:
            if balance > 0:
                with_balance += 1
                print(f"\n💰 Address #{i+1} HAS BALANCE: {balance} BTC")
                print(f"Address: {address}")
                print(f"Seed: {phrase}\n")
                
                with open("/workspace/BALANCES_FOUND.txt", "a") as f:
                    f.write("="*80 + "\n")
                    f.write(f"Seed: {phrase}\n")
                    f.write(f"Address: {address}\n")
                    f.write(f"Balance: {balance} BTC\n")
                    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                    f.write("="*80 + "\n\n")
            elif i % 10 == 0:
                print(f"Checked: {checked} | With balance: {with_balance} | Address: {address[:20]}...")
        
        # Rate limit
        time.sleep(1)
    
    print(f"\n✅ Complete: Checked {checked} addresses, {with_balance} with balance")
    return False

if __name__ == "__main__":
    test_valid_random_seeds(50)
