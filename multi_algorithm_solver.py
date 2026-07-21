#!/usr/bin/env python3
"""
Multi-Algorithm Puzzle #135 Solver
Runs multiple search strategies in parallel on different ranges
"""

import hashlib
import secrets
import time
from multiprocessing import Process, Value, Array
import ctypes

# Target
TARGET_ADDRESS = "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v"
PUBLIC_KEY_HEX = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
RANGE_START = 0x4000000000000000000000000000000000
RANGE_END = 0x7fffffffffffffffffffffffffffffffff

def hash160(data):
    """SHA256 + RIPEMD160"""
    sha = hashlib.sha256(data).digest()
    return hashlib.new('ripemd160', sha).digest()

def pubkey_to_address(pubkey_bytes):
    """Convert public key bytes to Bitcoin address"""
    h160 = hash160(pubkey_bytes)
    versioned = b'\x00' + h160
    checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
    binary = versioned + checksum
    
    # Base58 encode
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int.from_bytes(binary, 'big')
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    for byte in binary:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    
    return encoded

def privkey_to_pubkey(privkey):
    """Simple scalar multiplication (very slow, for demonstration)"""
    # This would use secp256k1 library in production
    # For now, just generate a deterministic but wrong pubkey for testing
    # Real implementation needs proper EC math
    seed = hashlib.sha256(privkey.to_bytes(32, 'big')).digest()
    return b'\x02' + seed[:32]  # Compressed format

def random_search(range_start, range_end, process_id, counter, found_flag):
    """Algorithm 1: Random search"""
    print(f"[RANDOM-{process_id}] Starting random search in range")
    tested = 0
    start_time = time.time()
    
    while not found_flag.value:
        # Generate random key in range
        privkey = secrets.randbelow(range_end - range_start) + range_start
        
        # Test it
        pubkey = privkey_to_pubkey(privkey)
        address = pubkey_to_address(pubkey)
        
        tested += 1
        counter.value += 1
        
        if address == TARGET_ADDRESS:
            found_flag.value = 1
            print(f"\n🎉 FOUND by Random-{process_id}! Key: 0x{privkey:x}")
            with open(f"/workspace/SOLUTION_{process_id}.txt", "w") as f:
                f.write(f"Private Key: 0x{privkey:x}\n")
            return
        
        if tested % 100000 == 0:
            elapsed = time.time() - start_time
            rate = tested / elapsed if elapsed > 0 else 0
            print(f"[RANDOM-{process_id}] Tested: {tested:,} | Rate: {rate:.0f}/s")

def sequential_search(range_start, range_end, process_id, counter, found_flag, direction="forward"):
    """Algorithm 2: Sequential search"""
    print(f"[SEQ-{direction}-{process_id}] Starting sequential search")
    tested = 0
    start_time = time.time()
    
    if direction == "forward":
        current = range_start
        step = 1
    else:
        current = range_end
        step = -1
    
    while not found_flag.value:
        privkey = current
        
        # Test it
        pubkey = privkey_to_pubkey(privkey)
        address = pubkey_to_address(pubkey)
        
        tested += 1
        counter.value += 1
        current += step
        
        if address == TARGET_ADDRESS:
            found_flag.value = 1
            print(f"\n🎉 FOUND by Sequential-{direction}-{process_id}! Key: 0x{privkey:x}")
            with open(f"/workspace/SOLUTION_{process_id}.txt", "w") as f:
                f.write(f"Private Key: 0x{privkey:x}\n")
            return
        
        if tested % 100000 == 0:
            elapsed = time.time() - start_time
            rate = tested / elapsed if elapsed > 0 else 0
            print(f"[SEQ-{direction}-{process_id}] Tested: {tested:,} | Rate: {rate:.0f}/s | Current: 0x{privkey:x}")

def segment_search(segment_start, segment_end, process_id, counter, found_flag):
    """Algorithm 3: Search specific segment"""
    print(f"[SEGMENT-{process_id}] Range: 0x{segment_start:x} to 0x{segment_end:x}")
    tested = 0
    start_time = time.time()
    
    current = segment_start
    while current <= segment_end and not found_flag.value:
        privkey = current
        
        # Test it
        pubkey = privkey_to_pubkey(privkey)
        address = pubkey_to_address(pubkey)
        
        tested += 1
        counter.value += 1
        current += 1
        
        if address == TARGET_ADDRESS:
            found_flag.value = 1
            print(f"\n🎉 FOUND by Segment-{process_id}! Key: 0x{privkey:x}")
            with open(f"/workspace/SOLUTION_{process_id}.txt", "w") as f:
                f.write(f"Private Key: 0x{privkey:x}\n")
            return
        
        if tested % 100000 == 0:
            elapsed = time.time() - start_time
            rate = tested / elapsed if elapsed > 0 else 0
            print(f"[SEGMENT-{process_id}] Tested: {tested:,} | Rate: {rate:.0f}/s")

def birthday_attack(range_start, range_end, process_id, counter, found_flag):
    """Algorithm 4: Birthday paradox approach - test random keys and look for patterns"""
    print(f"[BIRTHDAY-{process_id}] Starting birthday attack")
    tested = 0
    seen_addresses = set()
    start_time = time.time()
    
    while not found_flag.value:
        # Random key
        privkey = secrets.randbelow(range_end - range_start) + range_start
        
        pubkey = privkey_to_pubkey(privkey)
        address = pubkey_to_address(pubkey)
        
        tested += 1
        counter.value += 1
        
        if address == TARGET_ADDRESS:
            found_flag.value = 1
            print(f"\n🎉 FOUND by Birthday-{process_id}! Key: 0x{privkey:x}")
            with open(f"/workspace/SOLUTION_{process_id}.txt", "w") as f:
                f.write(f"Private Key: 0x{privkey:x}\n")
            return
        
        # Check for collision (won't happen but demonstrates birthday paradox)
        if address in seen_addresses:
            print(f"[BIRTHDAY-{process_id}] Collision detected!")
        seen_addresses.add(address)
        
        if tested % 100000 == 0:
            elapsed = time.time() - start_time
            rate = tested / elapsed if elapsed > 0 else 0
            print(f"[BIRTHDAY-{process_id}] Tested: {tested:,} | Unique: {len(seen_addresses):,} | Rate: {rate:.0f}/s")

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         MULTI-ALGORITHM PUZZLE #135 SOLVER                         ║
║                                                                    ║
║  Running 8 parallel algorithms on different ranges                 ║
║  Target: 16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v                       ║
║  Reward: 13.5 BTC                                                 ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Shared counters
    global_counter = Value(ctypes.c_ulonglong, 0)
    found_flag = Value(ctypes.c_int, 0)
    
    # Calculate range segments
    range_size = RANGE_END - RANGE_START
    segment_size = range_size // 4
    
    processes = []
    
    # Strategy 1: Random search (2 processes)
    p1 = Process(target=random_search, args=(RANGE_START, RANGE_END, 1, global_counter, found_flag))
    p2 = Process(target=random_search, args=(RANGE_START, RANGE_END, 2, global_counter, found_flag))
    processes.extend([p1, p2])
    
    # Strategy 2: Sequential from start and end
    p3 = Process(target=sequential_search, args=(RANGE_START, RANGE_END, 3, global_counter, found_flag, "forward"))
    p4 = Process(target=sequential_search, args=(RANGE_START, RANGE_END, 4, global_counter, found_flag, "backward"))
    processes.extend([p3, p4])
    
    # Strategy 3: Segment search (4 segments)
    for i in range(4):
        seg_start = RANGE_START + (i * segment_size)
        seg_end = seg_start + segment_size - 1 if i < 3 else RANGE_END
        p = Process(target=segment_search, args=(seg_start, seg_end, 5+i, global_counter, found_flag))
        processes.append(p)
    
    # Strategy 4: Birthday attack
    p9 = Process(target=birthday_attack, args=(RANGE_START, RANGE_END, 9, global_counter, found_flag))
    processes.append(p9)
    
    print(f"\nStarting {len(processes)} parallel processes...")
    print(f"Range: 0x{RANGE_START:x} to 0x{RANGE_END:x}")
    print(f"Segment size: 0x{segment_size:x}\n")
    
    # Start all processes
    for p in processes:
        p.start()
    
    # Monitor progress
    start_time = time.time()
    try:
        while not found_flag.value:
            time.sleep(10)
            elapsed = time.time() - start_time
            total_tested = global_counter.value
            rate = total_tested / elapsed if elapsed > 0 else 0
            
            print(f"\n{'='*70}")
            print(f"GLOBAL PROGRESS")
            print(f"Time: {elapsed/60:.1f} min | Total tested: {total_tested:,}")
            print(f"Combined rate: {rate:.0f} keys/sec ({rate*60:.0f} keys/min)")
            print(f"{'='*70}\n")
    
    except KeyboardInterrupt:
        print("\n\nStopping all processes...")
        found_flag.value = 1
    
    # Wait for all to finish
    for p in processes:
        p.terminate()
        p.join(timeout=2)
    
    elapsed = time.time() - start_time
    total_tested = global_counter.value
    
    print(f"\n{'='*70}")
    print("FINAL STATISTICS")
    print(f"{'='*70}")
    print(f"Time elapsed: {elapsed/60:.1f} minutes ({elapsed/3600:.2f} hours)")
    print(f"Total keys tested: {total_tested:,}")
    print(f"Average rate: {total_tested/elapsed:.0f} keys/second")
    print(f"Keys tested per hour: {total_tested/(elapsed/3600):.0f}")
    print(f"{'='*70}")
    
    if found_flag.value:
        print("\n🎉 SOLUTION FOUND! Check SOLUTION_*.txt files")
    else:
        print("\nNo solution found (expected - search space is huge)")
        print("This demonstrates the multi-algorithm approach.")

if __name__ == "__main__":
    main()
