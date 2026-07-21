#!/usr/bin/env python3
"""
FAST Simple Solver - Maximum speed with minimal overhead
Tests keys as fast as possible using different strategies
"""

import hashlib
import secrets
import time
import threading

TARGET = "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v"
START = 0x4000000000000000000000000000000000
END = 0x7fffffffffffffffffffffffffffffffff

# Precompute for speed
TARGET_HASH = TARGET.encode()

def fast_test(privkey_int):
    """Fastest possible key test (simplified)"""
    # In real implementation, would use proper secp256k1
    # This is a mock for demonstration
    seed = hashlib.sha256(privkey_int.to_bytes(32, 'big')).digest()
    # Simulate address check
    return False  # Would check against TARGET

class Solver(threading.Thread):
    def __init__(self, name, strategy, range_start, range_end):
        super().__init__()
        self.name = name
        self.strategy = strategy
        self.range_start = range_start
        self.range_end = range_end
        self.tested = 0
        self.running = True
        
    def run(self):
        print(f"[{self.name}] Started - Strategy: {self.strategy}")
        start_time = time.time()
        
        if self.strategy == "random":
            self.random_search()
        elif self.strategy == "sequential_forward":
            self.sequential_forward()
        elif self.strategy == "sequential_backward":
            self.sequential_backward()
        elif self.strategy == "middle_out":
            self.middle_out()
        
        elapsed = time.time() - start_time
        rate = self.tested / elapsed if elapsed > 0 else 0
        print(f"[{self.name}] Stopped. Tested: {self.tested:,} @ {rate:.0f}/s")
    
    def random_search(self):
        """Test random keys in range"""
        range_size = self.range_end - self.range_start
        while self.running:
            key = secrets.randbelow(range_size) + self.range_start
            fast_test(key)
            self.tested += 1
            
            if self.tested % 500000 == 0:
                print(f"[{self.name}] Random: {self.tested:,}")
    
    def sequential_forward(self):
        """Test keys sequentially from start"""
        key = self.range_start
        while self.running and key <= self.range_end:
            fast_test(key)
            self.tested += 1
            key += 1
            
            if self.tested % 500000 == 0:
                print(f"[{self.name}] Forward: {self.tested:,} @ 0x{key:x}")
    
    def sequential_backward(self):
        """Test keys sequentially from end"""
        key = self.range_end
        while self.running and key >= self.range_start:
            fast_test(key)
            self.tested += 1
            key -= 1
            
            if self.tested % 500000 == 0:
                print(f"[{self.name}] Backward: {self.tested:,} @ 0x{key:x}")
    
    def middle_out(self):
        """Test keys from middle outward"""
        middle = (self.range_start + self.range_end) // 2
        offset = 0
        while self.running:
            # Test middle + offset
            if middle + offset <= self.range_end:
                fast_test(middle + offset)
                self.tested += 1
            
            # Test middle - offset
            if middle - offset >= self.range_start:
                fast_test(middle - offset)
                self.tested += 1
            
            offset += 1
            
            if self.tested % 500000 == 0:
                print(f"[{self.name}] Middle-out: {self.tested:,} offset: {offset:,}")

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                FAST MULTI-STRATEGY SOLVER                          ║
║                                                                    ║
║  Testing maximum keys/second with multiple strategies              ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Split range into 4 segments
    range_size = END - START
    seg_size = range_size // 4
    
    solvers = [
        # Random searches
        Solver("RANDOM-1", "random", START, END),
        Solver("RANDOM-2", "random", START, END),
        
        # Sequential
        Solver("SEQ-FWD", "sequential_forward", START, START + seg_size),
        Solver("SEQ-BWD", "sequential_backward", END - seg_size, END),
        
        # Middle-out
        Solver("MIDDLE-1", "middle_out", START, START + seg_size),
        Solver("MIDDLE-2", "middle_out", START + seg_size*2, START + seg_size*3),
    ]
    
    print(f"Starting {len(solvers)} solver threads...")
    print(f"Range: 0x{START:x} to 0x{END:x}\n")
    
    # Start all
    for s in solvers:
        s.start()
    
    # Monitor
    start_time = time.time()
    try:
        while True:
            time.sleep(10)
            elapsed = time.time() - start_time
            total = sum(s.tested for s in solvers)
            rate = total / elapsed if elapsed > 0 else 0
            
            print(f"\n{'='*70}")
            print(f"Time: {elapsed:.0f}s | Total: {total:,} | Rate: {rate:.0f}/s ({rate*3600:.0f}/hour)")
            print(f"{'='*70}")
    
    except KeyboardInterrupt:
        print("\n\nStopping...")
        for s in solvers:
            s.running = False
    
    # Wait for all
    for s in solvers:
        s.join(timeout=2)
    
    # Final stats
    elapsed = time.time() - start_time
    total = sum(s.tested for s in solvers)
    
    print(f"\n{'='*70}")
    print("FINAL STATS")
    print(f"{'='*70}")
    print(f"Time: {elapsed/60:.1f} min")
    print(f"Keys tested: {total:,}")
    print(f"Average rate: {total/elapsed:.0f} keys/second")
    print(f"Keys per hour: {total/(elapsed/3600):.0f}")
    print(f"\nPer-thread breakdown:")
    for s in solvers:
        print(f"  {s.name}: {s.tested:,}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
