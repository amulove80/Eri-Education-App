# Bitcoin Puzzle #135 - Attack Plan

## Target Information
**Status:** UNSOLVED  
**Reward:** 13.5 BTC (~$355,000)  
**Public Key:** EXPOSED (can use Pollard's Kangaroo!)

## Key Range
- **Bits:** 135-bit
- **Range:** 2^134 to 2^135 - 1
- **Hex Start:** `0x40000000000000000000000000000000000`
- **Hex End:** `0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF`

## Why This is Feasible

With an exposed public key, we can use **Pollard's Kangaroo Algorithm** which reduces:
- Brute force complexity: O(2^135) ≈ 4.4 × 10^40 operations
- Kangaroo complexity: O(2^67.5) ≈ 2.9 × 10^20 operations

**That's a ~10^20 speedup!**

## Estimated Computation
According to experts, puzzle #130 (2^130 keyspace) took several years on 256 Tesla V100 GPUs.

Puzzle #135 is 32x harder, but with optimization:
- Needs powerful GPU cluster
- Could take months to years
- But it's SOLVABLE unlike brute force

## Strategy
1. Implement Pollard's Kangaroo ECDLP solver
2. Use optimized GPU code (CUDA)
3. Set up parallel computing
4. Monitor progress continuously

## Next Steps
- Get exact address and public key
- Set up Kangaroo solver
- Begin computational attack
