#!/bin/bash

# 1. Setup
mkdir -p project_results
echo "Starting Research Simulations (Matrix Multiplication)..."

# 2. RUN SCENARIOS
# Baseline: Fast, Out-of-Order, High-Bandwidth (Vulnerable)
echo "Running Baseline (O3 + 16 MSHRs)..."
./gem5/build/X86/gem5.opt -d project_results/baseline compare.py o3 with_cache 20 16 > baseline.log

# Defense 1: Randomized Indexing on O3 (The Performance Tax)
echo "Running Defense (O3 + Randomized + 16 MSHRs)..."
./gem5/build/X86/gem5.opt -d project_results/secure_ooo compare.py o3 randomized 20 16 > secure_ooo.log

# Defense 2: Maximum Security (Timing + Randomized + 1 MSHR)
echo "Running Max Security (Timing + Randomized + 1 MSHR)..."
./gem5/build/X86/gem5.opt -d project_results/secure_max compare.py timing randomized 20 1 > secure_max.log

# 3. GENERATE SUMMARY
echo "--- ARCHITECTURAL RESEARCH SUMMARY ---" > results_summary.txt
echo "Date: $(date)" >> results_summary.txt
echo "Workload: 128x128 Matrix Multiplication" >> results_summary.txt
echo "--------------------------------------" >> results_summary.txt

# Grab IPC for all runs
grep "board.processor.cores.core.ipc" project_results/*/stats.txt >> results_summary.txt

# Grab L2 Miss Rate (Crucial for the Song et al. paper context)
grep "board.cache_hierarchy.l2cache.overall_miss_rate::total" project_results/*/stats.txt >> results_summary.txt

echo "Done! Summary saved to results_summary.txt"
