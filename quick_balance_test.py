#!/usr/bin/env python3
"""
Quick balance check - simplified version
Test a few random valid seeds and check their balances
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import random
import requests
import time

CANDIDATES = [
    "black", "brave", "camera", "change", "coin", "day", "digital", "eye", 
    "face", "food", "future", "history", "home", "key", "liberty", "mask", 
    "moon", "one", "only", "order", "owner", "peace", "picture", "proof", 
    "pyramid", "real", "sign", "state", "subject", "system", "this", "time", 
    "tower", "verify", "virus", "vote", "weapon", "world"
]

def derive_address(phrase):
    """Derive Bitcoin address from seed phrase"""
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress()
    except Exception as e:
        print(f"Error deriving address: {e}")
        return None

def check_balance_simple(address):
    """Simple balance check using blockchain.info"""
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            balance_satoshi = int(response.text.strip())
            balance_btc = balance_satoshi / 100000000
            return balance_btc
        else:
            print(f"API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error checking balance: {e}")
        return None

def main():
    print("Testing balance checker with 10 random valid seeds...\n")
    
    for i in range(10):
        # Generate random valid seed
        words = random.sample(CANDIDATES, 12)
        phrase = " ".join(words)
        
        print(f"\nTest {i+1}:")
        print(f"Seed: {' '.join(words[:3])}... (truncated)")
        
        address = derive_address(phrase)
        if address:
            print(f"Address: {address}")
            
            balance = check_balance_simple(address)
            if balance is not None:
                print(f"Balance: {balance} BTC")
                
                if balance > 0:
                    print(f"\n🎉 FOUND ADDRESS WITH BALANCE! 🎉")
                    print(f"Full seed: {phrase}")
                    with open("/workspace/BALANCES_FOUND.txt", "a") as f:
                        f.write(f"Seed: {phrase}\n")
                        f.write(f"Address: {address}\n")
                        f.write(f"Balance: {balance} BTC\n")
                        f.write("="*80 + "\n")
            else:
                print("Could not check balance (API error)")
            
            # Rate limiting
            time.sleep(2)
        else:
            print("Could not derive address")
    
    print("\n✅ Balance check test complete")

if __name__ == "__main__":
    main()
