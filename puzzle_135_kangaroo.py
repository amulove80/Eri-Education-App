#!/usr/bin/env python3
"""
Puzzle #135 Solver - CPU-based Pollard's Kangaroo Implementation
WARNING: CPU-only solving will be EXTREMELY slow (thousands of years)
This is a proof-of-concept. Real solving requires GPU cluster.
"""

import hashlib
import ecdsa
from ecdsa import SECP256k1
import time

# Puzzle #135 Parameters
TARGET_ADDRESS = "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v"
PUBLIC_KEY_HEX = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
RANGE_START = 0x4000000000000000000000000000000000
RANGE_END = 0x7fffffffffffffffffffffffffffffffff

# Secp256k1 parameters
curve = SECP256k1.curve
G = SECP256k1.generator
n = SECP256k1.order

def decompress_public_key(pubkey_hex):
    """Decompress compressed public key"""
    pubkey_bytes = bytes.fromhex(pubkey_hex)
    prefix = pubkey_bytes[0]
    x = int.from_bytes(pubkey_bytes[1:], 'big')
    
    # Calculate y from x
    y_squared = (pow(x, 3, curve.p()) + curve.a() * x + curve.b()) % curve.p()
    y = pow(y_squared, (curve.p() + 1) // 4, curve.p())
    
    # Choose correct y based on prefix
    if (prefix == 0x02 and y % 2 != 0) or (prefix == 0x03 and y % 2 == 0):
        y = curve.p() - y
    
    return ecdsa.ellipticcurve.Point(curve, x, y)

def point_to_address(point):
    """Convert EC point to Bitcoin address"""
    # Compressed public key
    prefix = b'\x02' if point.y() % 2 == 0 else b'\x03'
    pubkey = prefix + point.x().to_bytes(32, 'big')
    
    # SHA256 then RIPEMD160
    sha = hashlib.sha256(pubkey).digest()
    ripe = hashlib.new('ripemd160', sha).digest()
    
    # Add version byte (0x00 for mainnet)
    versioned = b'\x00' + ripe
    
    # Double SHA256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
    
    # Base58 encode
    binary = versioned + checksum
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    num = int.from_bytes(binary, 'big')
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    # Add leading '1's for leading zero bytes
    for byte in binary:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    
    return encoded

def pollards_kangaroo_step(point, scalar_bits=135):
    """Single kangaroo jump (simplified)"""
    # Use point's x-coordinate to determine jump size
    x_val = point.x() % (2 ** 20)  # Use lower bits
    jump = 1 << (x_val % scalar_bits)  # Power of 2 jump
    return jump

def simple_kangaroo_search(target_point, range_start, range_end, max_iterations=1000000):
    """
    Simplified Pollard's Kangaroo for demonstration
    Real implementation needs optimized jumps, distinguished points, etc.
    """
    print(f"Starting Kangaroo search...")
    print(f"Range: 0x{range_start:x} to 0x{range_end:x}")
    print(f"Target: {TARGET_ADDRESS}")
    print(f"\n⚠️  WARNING: CPU-only search will be EXTREMELY slow!")
    print(f"⚠️  This is a proof-of-concept. Real solving needs GPU cluster.\n")
    
    # Tame kangaroo starts at midpoint
    tame_start = (range_start + range_end) // 2
    tame_point = tame_start * G
    tame_distance = tame_start
    
    # Wild kangaroo starts at target
    wild_point = target_point
    wild_distance = 0
    
    # Track distinguished points (simplified)
    tame_dps = {}
    wild_dps = {}
    
    start_time = time.time()
    
    for iteration in range(max_iterations):
        # Tame kangaroo jump
        tame_jump = pollards_kangaroo_step(tame_point)
        tame_point = tame_point + (tame_jump * G)
        tame_distance += tame_jump
        
        # Wild kangaroo jump
        wild_jump = pollards_kangaroo_step(wild_point)
        wild_point = wild_point + (wild_jump * G)
        wild_distance += wild_jump
        
        # Check for collision (simplified - just checking every point)
        if tame_point == wild_point:
            private_key = (tame_distance - wild_distance) % n
            if range_start <= private_key <= range_end:
                print(f"\n🎉 FOUND! Private key: 0x{private_key:x}")
                return private_key
        
        # Progress update
        if iteration % 10000 == 0 and iteration > 0:
            elapsed = time.time() - start_time
            rate = iteration / elapsed
            print(f"[{time.strftime('%H:%M:%S')}] Iterations: {iteration:,} | "
                  f"Rate: {rate:.1f}/s | Time: {elapsed:.1f}s")
    
    print(f"\nCompleted {max_iterations:,} iterations without finding solution")
    return None

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║            BITCOIN PUZZLE #135 SOLVER                              ║
║                                                                    ║
║  Using Pollard's Kangaroo Algorithm (CPU Version)                 ║
║                                                                    ║
║  Target: 16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v                       ║
║  Reward: 13.5 BTC                                                 ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Parse target public key
    print("Parsing target public key...")
    target_point = decompress_public_key(PUBLIC_KEY_HEX)
    print(f"✓ Public key decompressed")
    print(f"  X: {target_point.x()}")
    print(f"  Y: {target_point.y()}\n")
    
    # Verify address generation works
    print("Verifying address generation...")
    test_key = RANGE_START + 12345
    test_point = test_key * G
    test_addr = point_to_address(test_point)
    print(f"✓ Test address generated: {test_addr}\n")
    
    print("="*70)
    print("REALITY CHECK:")
    print("="*70)
    print(f"Expected operations: ~2^67.5 ≈ 2.9 × 10^20")
    print(f"CPU rate: ~1,000 ops/sec")
    print(f"Time needed: ~9 × 10^12 years (9 trillion years)")
    print(f"\nFor comparison:")
    print(f"- Age of universe: 13.8 billion years")
    print(f"- RTX 4090 GPU: ~1 billion ops/sec (1,000,000x faster)")
    print(f"- 1000 GPUs: Still needs ~9 million years")
    print("="*70 + "\n")
    
    response = input("Continue with proof-of-concept search? (yes/no): ")
    
    if response.lower() == 'yes':
        # Run limited search to demonstrate
        result = simple_kangaroo_search(target_point, RANGE_START, RANGE_END, max_iterations=100000)
        
        if result:
            print(f"\n🎉 Solution found: 0x{result:x}")
            print(f"Verifying...")
            solution_point = result * G
            solution_addr = point_to_address(solution_point)
            print(f"Address: {solution_addr}")
            
            if solution_addr == TARGET_ADDRESS:
                print("✓ VERIFIED! This is the correct private key!")
                with open("/workspace/PUZZLE_135_SOLUTION.txt", "w") as f:
                    f.write(f"Private Key: 0x{result:x}\n")
                    f.write(f"Address: {solution_addr}\n")
            else:
                print("✗ Address doesn't match (found different key in range)")
        else:
            print("\nNo solution in limited search (expected)")
    else:
        print("\nSearch cancelled. This demonstrates the setup.")
        print("Real solving requires:")
        print("- GPU cluster (100-1000+ GPUs)")
        print("- Optimized Kangaroo implementation")
        print("- Months to years of computation")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped by user")
