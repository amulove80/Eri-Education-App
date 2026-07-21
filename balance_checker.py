#!/usr/bin/env python3
"""
BALANCE CHECKER - Check balances for valid seed phrases
"""

from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import itertools
import random
import time
import requests
import json

TARGET_ADDRESS = "1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ"

CANDIDATES = [
    "black", "brave", "camera", "change", "coin", "day", "digital", "eye", 
    "face", "food", "future", "history", "home", "key", "liberty", "mask", 
    "moon", "one", "only", "order", "owner", "peace", "picture", "proof", 
    "pyramid", "real", "sign", "state", "subject", "system", "this", "time", 
    "tower", "verify", "virus", "vote", "weapon", "world"
]

PASSPHRASES = ["", "BREATHE", "breathe"]

def derive_address(phrase, passphrase=""):
    """Derive Bitcoin address from seed phrase"""
    try:
        Bip39MnemonicValidator().Validate(phrase)
        seed_bytes = Bip39SeedGenerator(phrase, passphrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        return bip44_acc.PublicKey().ToAddress()
    except:
        return None

def check_balance(address, session):
    """Check balance using blockchain.info API"""
    try:
        # Use blockchain.info API (no rate limit for single address)
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            # Returns balance in satoshis
            balance = int(response.text.strip())
            return balance / 100000000  # Convert to BTC
        return None
    except Exception as e:
        # If blockchain.info fails, try blockchair
        try:
            url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and address in data['data']:
                    balance = data['data'][address]['address']['balance']
                    return balance / 100000000
            return None
        except:
            return None

def save_finding(phrase, passphrase, address, balance):
    """Save any address with balance"""
    with open("/workspace/BALANCES_FOUND.txt", "a") as f:
        f.write("="*80 + "\n")
        f.write(f"Seed: {phrase}\n")
        f.write(f"Passphrase: {passphrase}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Balance: {balance} BTC\n")
        f.write("="*80 + "\n\n")
    
    print(f"\n💰 BALANCE FOUND: {balance} BTC")
    print(f"Address: {address}")
    print(f"Seed: {phrase}")
    if passphrase:
        print(f"Passphrase: {passphrase}")

def check_combinations():
    """Generate and check combinations"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║              BALANCE CHECKER FOR VALID SEEDS                       ║
║                                                                    ║
║  Generating valid seed phrases and checking their balances         ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    checked = 0
    valid_seeds = 0
    with_balance = 0
    start = time.time()
    
    # Track checked addresses to avoid duplicates
    checked_addresses = set()
    
    print("Generating random valid seed phrases and checking balances...")
    print("(This will run continuously - press Ctrl+C to stop)\n")
    
    batch_size = 100
    addresses_batch = []
    phrases_batch = []
    
    try:
        while True:
            # Generate random seed
            words = random.sample(CANDIDATES, 12)
            phrase = " ".join(words)
            
            for passphrase in PASSPHRASES:
                address = derive_address(phrase, passphrase)
                
                if address and address not in checked_addresses:
                    checked_addresses.add(address)
                    valid_seeds += 1
                    
                    # Add to batch
                    addresses_batch.append(address)
                    phrases_batch.append((phrase, passphrase))
                    
                    # When batch is full, check balances
                    if len(addresses_batch) >= batch_size:
                        for addr, (phr, pp) in zip(addresses_batch, phrases_batch):
                            balance = check_balance(addr, session)
                            checked += 1
                            
                            if balance is not None and balance > 0:
                                with_balance += 1
                                save_finding(phr, pp, addr, balance)
                                
                                # Check if it's the target
                                if addr == TARGET_ADDRESS:
                                    print("\n🎉🎉🎉 TARGET ADDRESS FOUND! 🎉🎉🎉")
                                    print(f"Seed: {phr}")
                                    if pp:
                                        print(f"Passphrase: {pp}")
                                    with open("/workspace/SOLUTION_FOUND.txt", "w") as f:
                                        f.write(f"SOLUTION!\nSeed: {phr}\nPassphrase: {pp}\n")
                                    return True
                            
                            # Rate limiting
                            time.sleep(0.1)
                        
                        # Clear batch
                        addresses_batch = []
                        phrases_batch = []
                        
                        # Progress update
                        elapsed = time.time() - start
                        print(f"Checked: {checked:,} addresses | Valid seeds: {valid_seeds:,} | "
                              f"With balance: {with_balance} | Rate: {checked/elapsed:.1f}/s | "
                              f"Time: {elapsed/60:.1f}min")
                
            if checked % 1000 == 0 and checked > 0:
                # Occasional progress
                elapsed = time.time() - start
                print(f"[{time.strftime('%H:%M:%S')}] Checked: {checked:,} | "
                      f"Valid: {valid_seeds:,} | Balance: {with_balance} | "
                      f"Rate: {checked/elapsed:.1f}/s")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user")
        elapsed = time.time() - start
        print(f"\nFinal Stats:")
        print(f"  Addresses checked: {checked:,}")
        print(f"  Valid seed phrases: {valid_seeds:,}")
        print(f"  Addresses with balance: {with_balance}")
        print(f"  Time elapsed: {elapsed/60:.1f} minutes")
        print(f"  Rate: {checked/elapsed:.1f} addresses/second")
        
        if with_balance > 0:
            print(f"\n✅ Found {with_balance} address(es) with balance!")
            print("See BALANCES_FOUND.txt for details")
        
        return False

def main():
    check_combinations()

if __name__ == "__main__":
    main()
