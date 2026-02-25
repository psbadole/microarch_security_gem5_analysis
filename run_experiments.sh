#!/bin/bash

# Create a clean directory for all results
mkdir -p project_results

echo "Starting Batch Simulations..."

# Run Scenario 1: In-Order + No Cache
./gem5/build/X86/gem5.opt -d project_results/inorder_nocache compare.py timing nocache

# Run Scenario 2: Out-of-Order + No Cache
./gem5/build/X86/gem5.opt -d project_results/ooo_nocache compare.py o3 nocache

# Run Scenario 3: In-Order + With Cache
./gem5/build/X86/gem5.opt -d project_results/inorder_cache compare.py timing with_cache

# Run Scenario 4: Out-of-Order + With Cache
./gem5/build/X86/gem5.opt -d project_results/ooo_cache compare.py o3 with_cache

echo "All 4 runs finished! Check the 'project_results' folder."
