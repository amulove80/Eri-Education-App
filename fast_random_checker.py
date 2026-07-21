#!/usr/bin/env python3
"""
FAST Random Seed Balance Checker
Optimized for speed - checks multiple seeds in parallel
"""

from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum,
                       Bip44, Bip44Coins, Bip44Changes, Bip39EntropyBitLen,
                       Bip39EntropyGenerator)
import requests
import time
import concurrent.futures
import threading

results_lock = threading.Lock()
total_checked = 0
total_with_balance = 0

def check_balance_fast(address):
    """Quick balance check with shorter timeout"""
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return int(response.text.strip()) / 100000000
    except:
        pass
    return 0.0

def check_seed_fast(seed_num):
    """Generate and check one seed quickly"""
    global total_checked, total_with_balance
    
    # Generate random seed
    entropy = Bip39EntropyGenerator(Bip39EntropyBitLen.BIT_LEN_128).Generate()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed_phrase = mnemonic.ToStr()
    
    try:
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        
        # Check first 3 addresses (faster than 5)
        for i in range(3):
            bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            address = bip44_acc.PublicKey().ToAddress()
            
            balance = check_balance_fast(address)
            
            with results_lock:
                total_checked += 1
            
            if balance > 0:
                with results_lock:
                    total_with_balance += 1
                
                print(f"\n{'='*80}")
                print(f"💰 BALANCE FOUND! 💰")
                print(f"Address: {address}")
                print(f"Balance: {balance} BTC")
                print(f"Seed: {seed_phrase}")
                print(f"Address Index: {i}")
                print(f"{'='*80}\n")
                
                with open("/workspace/BALANCES_FOUND.txt", "a") as f:
                    f.write("="*80 + "\n")
                    f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                    f.write(f"Seed: {seed_phrase}\n")
                    f.write(f"Address: {address}\n")
                    f.write(f"Address Index: {i}\n")
                    f.write(f"Balance: {balance} BTC\n")
                    f.write("="*80 + "\n\n")
                
                return True
            
            time.sleep(0.3)  # Rate limit
    
    except Exception as e:
        pass
    
    return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║              FAST RANDOM SEED CHECKER                              ║
║                                                                    ║
║  Checking multiple random seeds in parallel                       ║
║  Optimized for maximum throughput                                 ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    global total_checked, total_with_balance
    start_time = time.time()
    seeds_generated = 0
    
    try:
        # Use thread pool for parallel checking
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                # Submit 10 seeds at a time
                futures = []
                for i in range(10):
                    future = executor.submit(check_seed_fast, seeds_generated + i)
                    futures.append(future)
                
                # Wait for batch to complete
                for future in concurrent.futures.as_completed(futures):
                    future.result()
                
                seeds_generated += 10
                
                # Progress update every 50 seeds
                if seeds_generated % 50 == 0:
                    elapsed = time.time() - start_time
                    rate = total_checked / elapsed if elapsed > 0 else 0
                    
                    print(f"[{time.strftime('%H:%M:%S')}] Seeds: {seeds_generated} | "
                          f"Addresses checked: {total_checked} | "
                          f"With balance: {total_with_balance} | "
                          f"Rate: {rate:.1f} addr/min")
    
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n\n⚠️ Stopped")
        print(f"Seeds generated: {seeds_generated}")
        print(f"Addresses checked: {total_checked}")
        print(f"With balance: {total_with_balance}")
        print(f"Time: {elapsed/60:.1f} min")
        print(f"Rate: {total_checked/elapsed*60:.1f} addresses/hour")

if __name__ == "__main__":
    main()
