The work is done based on existing gem5 bootcamp repository. My work is in compare.py, project_results and GEM5_RESULTS_DOC..

Research Questions
1. How much faster is an Out-of-Order (O3) CPU compared to a secure In-Order core?
2. What is the IPC (Instructions Per Cycle) cost of implementing randomized cache indexing to thwart conflict-based attacks?
3. Can hardware-level cache partitioning effectively prevent cross-core data leakage?

Custom Cache Hierarchy (DeepDiveHierarchy)
I modified the gem5 classic cache model to create a flexible testbed.
Adjustable parameters support dynamic adjustment of L2 Latency and MSHR (Miss Status Holding Register) counts via command-line arguments.
Security Models which includes a randomized mode that simulates the hashing overhead of secure indexing schemes (inspired by Song et al., 2024).

Evaluated Models:
Baseline: An X86 O3 CPU with high MSHR bandwidth—representing modern, fast, but potentially vulnerable silicon.
Secure Baseline: A Timing-Simple CPU that eliminates speculative execution to provide a "ground truth" for secure performance.
Randomized Defense: An implementation of randomized remapping to mitigate Last Level Cache (LLC) side channels

I have attatched a pdf(GEM5_RESULT_DOC) with the compiled Statistics or Performance metrics of all the mentioned experiment. (Will update to github later as simulation takes time)
