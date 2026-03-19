#!/bin/bash

# We will test MSHR sizes of 1, 2, 4, 8, and 16
for m in 1 2 4 8 16
do
    echo "Running O3 with 100-cycle L2 and MSHR count: $m"
    ./gem5/build/X86/gem5.opt -d "results_ooo_mshr_$m" compare.py o3 with_cache 100 $m
done

echo "Sweep complete! Run your smart_parse.py next."
