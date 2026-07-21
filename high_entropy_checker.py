#!/usr/bin/env python3
"""
Random High Entropy Seed Balance Checker
Generate completely random valid BIP39 seeds and check for any balances
"""

from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum,
                       Bip44, Bip44Coins, Bip44Changes, Bip39EntropyBitLen,
                       Bip39EntropyGenerator)
import requests
import time
import os

def check_balance_multi_api(address):
    """Check balance using multiple APIs for reliability"""
    
    # Try blockchain.info first
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            satoshi = int(response.text.strip())
            return satoshi / 100000000
    except:
        pass
    
    # Try blockchair as backup
    try:
        url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and address in data['data']:
                satoshi = data['data'][address]['address']['balance']
                return satoshi / 100000000
    except:
        pass
    
    # Try blockchain.com API
    try:
        url = f"https://blockchain.com/btc/address/{address}"
        response = requests.get(url, timeout=10)
        # This would need parsing, skip for now
    except:
        pass
    
    return 0.0

def generate_high_entropy_seed():
    """Generate a truly random 12-word BIP39 seed with maximum entropy"""
    # Generate 128 bits of entropy (for 12 words)
    entropy = Bip39EntropyGenerator(Bip39EntropyBitLen.BIT_LEN_128).Generate()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic.ToStr()

def derive_multiple_addresses(seed_phrase, num_addresses=5):
    """Derive multiple addresses from one seed (first 5 addresses in derivation path)"""
    addresses = []
    
    try:
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        
        # Check first 5 addresses in derivation path
        for i in range(num_addresses):
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            address = bip44_acc.PublicKey().ToAddress()
            addresses.append(address)
        
        return addresses
    except Exception as e:
        print(f"Error deriving addresses: {e}")
        return []

def check_seed_for_balance(seed_phrase, seed_num):
    """Check a seed and its first 5 addresses for any balance"""
    
    print(f"\n{'='*80}")
    print(f"Seed #{seed_num}")
    print(f"Phrase: {' '.join(seed_phrase.split()[:4])}... (first 4 words)")
    
    addresses = derive_multiple_addresses(seed_phrase, 5)
    
    if not addresses:
        return False
    
    total_balance = 0.0
    found_balance = False
    
    for idx, address in enumerate(addresses):
        balance = check_balance_multi_api(address)
        
        if balance > 0:
            found_balance = True
            total_balance += balance
            
            print(f"\n💰💰💰 ADDRESS WITH BALANCE FOUND! 💰💰💰")
            print(f"Address {idx}: {address}")
            print(f"Balance: {balance} BTC")
            print(f"Full Seed: {seed_phrase}")
            
            # Save immediately
            with open("/workspace/BALANCES_FOUND.txt", "a") as f:
                f.write("="*80 + "\n")
                f.write(f"FOUND AT: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                f.write(f"Seed: {seed_phrase}\n")
                f.write(f"Address Index: {idx}\n")
                f.write(f"Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n")
                f.write("="*80 + "\n\n")
        
        # Rate limiting between addresses
        time.sleep(0.5)
    
    if found_balance:
        print(f"\nTotal balance from this seed: {total_balance} BTC")
        return True
    else:
        # Just show first address as sample
        print(f"Sample address: {addresses[0][:20]}... | Balance: 0 BTC")
        return False
    
    return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         HIGH ENTROPY RANDOM SEED BALANCE CHECKER                   ║
║                                                                    ║
║  Generating truly random BIP39 seeds with maximum entropy         ║
║  Checking first 5 addresses per seed for any balances             ║
║                                                                    ║
║  Press Ctrl+C to stop                                             ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    seeds_checked = 0
    addresses_checked = 0
    balances_found = 0
    start_time = time.time()
    
    try:
        while True:
            # Generate high entropy random seed
            seed_phrase = generate_high_entropy_seed()
            seeds_checked += 1
            
            # Check this seed
            found = check_seed_for_balance(seed_phrase, seeds_checked)
            
            addresses_checked += 5  # We check 5 addresses per seed
            
            if found:
                balances_found += 1
            
            # Progress update every 10 seeds
            if seeds_checked % 10 == 0:
                elapsed = time.time() - start_time
                rate = seeds_checked / elapsed
                addr_rate = addresses_checked / elapsed
                
                print(f"\n{'='*80}")
                print(f"Progress Update:")
                print(f"  Seeds checked: {seeds_checked}")
                print(f"  Addresses checked: {addresses_checked}")
                print(f"  With balance: {balances_found}")
                print(f"  Rate: {rate:.2f} seeds/min | {addr_rate:.2f} addresses/min")
                print(f"  Running time: {elapsed/60:.1f} minutes")
                print(f"{'='*80}")
            
            # Small delay between seeds
            time.sleep(2)
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Stopped by user")
        elapsed = time.time() - start_time
        print(f"\nFinal Statistics:")
        print(f"  Seeds checked: {seeds_checked}")
        print(f"  Addresses checked: {addresses_checked}")
        print(f"  Addresses with balance: {balances_found}")
        print(f"  Time: {elapsed/60:.1f} minutes")
        print(f"  Rate: {seeds_checked/elapsed*60:.1f} seeds/hour")
        
        if balances_found > 0:
            print(f"\n✅ Found {balances_found} address(es) with balance!")
            print("See BALANCES_FOUND.txt for details")
        else:
            print("\n❌ No addresses with balance found")
            print("(This is expected - the vast majority of random addresses have 0 balance)")

if __name__ == "__main__":
    main()
