# Cache Side-Channel Security Analysis using gem5

I built this to understand two things that kept bothering me while 
reading Song et al. (IEEE TC, 2024) on randomized LLC defenses i.e how 
much does speculative execution actually change your cache footprint, 
and what does it really cost to implement cache randomization in 
hardware?

## What this project does

Two focused investigations using gem5 v24.0.0.0:

**Investigation 1:** Compare how TimingSimpleCPU and O3CPU behave on 
identical workloads specifically how speculative execution changes 
the cache footprint and why that matters for side-channel security.

**Investigation 2:** Model the performance overhead of randomized LLC 
defenses by isolating the individual contributions of hashing latency 
and MSHR serialization, then sweep both parameters to find where the 
real cost comes from.

## The custom cache hierarchy

I extended gem5's `PrivateL1SharedL2CacheHierarchy` with a subclass 
called `DeepDiveHierarchy` that adds two security-relevant parameters:

- **Configurable L2 latency** models the overhead of a cryptographic 
  address hasher (Song et al. use a single-cycle design, I approximate 
  this as +2 cycles in randomized mode)
- **Configurable MSHR count** models the serialization effect of 
  restricting parallel cache miss handling
```python
./gem5/build/X86/gem5.opt -d output_dir compare.py \
    [cpu: timing|o3] \
    [cache: with_cache|nocache|randomized] \
    [l2_latency: int] \
    [mshr_count: int]
```

## Results

### Part 1: Speculative execution leaves a bigger cache footprint than 
you'd expect

Same workload, same committed instructions (6,555), different CPU:

| CPU | IPC | L1D Misses | Miss Rate |
|---|---|---|---|
| TimingSimpleCPU | 0.073 | 138 | 5.25% |
| O3CPU | 0.112 | 269 | 8.36% |

OoO gets 1.53x better IPC but generates **95% more L1D cache misses**. 
The reason: 1,144 squashed speculative loads that touched the cache 
along mispredicted paths and were never committed. That transient 
footprint is exactly the mechanism Spectre-class attacks exploit.

### Part 2: MSHR serialization dominates the security overhead, not 
the hasher

5 controlled experiments, same workload (1,642,828 instructions each):

| Experiment | Config | IPC | Overhead |
|---|---|---|---|
| exp1 | O3, lat=20, mshr=16 | 2.2676 | O3 baseline |
| exp2 | Timing, lat=20, mshr=16 | 0.5178 | Timing baseline |
| exp3 | Timing, lat=22, mshr=16 | 0.5171 | 0.14% |
| exp4 | Timing, lat=20, mshr=2 | 0.5059 | 2.31% |
| exp5 | Timing, randomized, mshr=2 | 0.5044 | 2.59% |

The +2 cycle latency penalty costs almost nothing (0.14%). Restricting 
MSHRs to 2 costs 2.31%. The full defense costs 2.59%. So the hasher 
overhead is basically negligible, it's the serialization that hurts. 
This lines up with what Song et al. found on their Rocket-Chip FPGA 
implementation.

### Part 3: There's a performance cliff at MSHR=2

I swept MSHR from 2 to 16 to find where the cost actually kicks in:

| MSHR | IPC | Overhead |
|---|---|---|
| 16 | 0.5178 | 0% |
| 8 | 0.5179 | ~0% |
| 4 | 0.5178 | ~0% |
| 2 | 0.5059 | 2.31% |

Performance is completely flat from MSHR=4 upward — the cost only 
appears at MSHR=2. If you're implementing this defense in hardware, 
MSHR=4 seems like the sweet spot: you get the serialization effect 
that makes eviction set searches harder, with basically zero 
performance penalty.

## Repo structure
```
├── compare.py                  # Main simulation script
├── workload.c                  # 32x32 matrix multiply
├── exp1_o3_base/               # O3 baseline
├── exp2_timing_base/           # Timing baseline  
├── exp3_timing_latonly/        # +2 cycle latency only
├── exp4_timing_mshronly/       # MSHR=2 only
├── exp5_timing_fullsecure/     # Full defense
├── exp_mshr_{2,4,8,16}/        # MSHR sweep
└── exp_lat_{20-25}/            # Latency sweep
```

## How to run
```bash
# Setup
GEM5_RESOURCE_DIR=~/.cache/gem5

# Example: timing CPU, full security config
./gem5/build/X86/gem5.opt -d output_dir \
    compare.py timing randomized 20 2

# Compile the workload
gcc -static -O2 -o workload-x86 workload.c
```

## Reference

Song, W., Xue, Z., Han, J., Li, Z., & Liu, P. (2024). Randomizing 
Set-Associative Caches Against Conflict-Based Cache Side-Channel 
Attacks. *IEEE Transactions on Computers*, 73(4), 1019–1033.

Simulator: gem5 v24.0.0.0 | X86 ISA | Syscall Emulation mode
