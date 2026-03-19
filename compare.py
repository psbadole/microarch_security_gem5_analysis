from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import ISA
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.cachehierarchies.classic.no_cache import NoCache
import sys

# --- ARGUMENT PARSING ---
# Arg 1: cpu ('timing', 'o3')
# Arg 2: cache mode ('with_cache', 'nocache')
# Arg 3: L2 Latency (default 20)
# Arg 4: MSHR Count (default 16)
cpu_str = sys.argv[1] if len(sys.argv) > 1 else 'timing'
cache_str = sys.argv[2] if len(sys.argv) > 2 else 'with_cache'
l2_lat = int(sys.argv[3]) if len(sys.argv) > 3 else 20
mshr_cnt = int(sys.argv[4]) if len(sys.argv) > 4 else 16

cpu_type = CPUTypes.TIMING if cpu_str == 'timing' else CPUTypes.O3

print(f"--- SIMULATION: {cpu_str} | Cache: {cache_str} | L2 Latency: {l2_lat} | MSHRs: {mshr_cnt} ---")

class DeepDiveHierarchy(PrivateL1SharedL2CacheHierarchy):
    def __init__(self, l2_lat, mshr_cnt):
        super().__init__(
            l1d_size="32KiB",
            l1i_size="32KiB",
            l2_size="256KiB"
        )
        self._l2_latency_val = l2_lat
        self._mshr_count_val = mshr_cnt

    def incorporate_cache(self, board):
        # 1. Standard setup
        super().incorporate_cache(board)

        # 2. Modify L2 Latency with Security Logic
        actual_lat = self._l2_latency_val
        if cache_str == 'randomized':
            # Song et al. (2024) hashing overhead simulation
            actual_lat += 2
            print("--- SECURITY ENABLED: Randomized Indexing Mode ---")

        self.l2cache.tag_latency = actual_lat
        self.l2cache.data_latency = actual_lat
        self.l2cache.response_latency = actual_lat

        # 3. Security/Performance tuning: MSHRs
        # More MSHRs allow more parallel memory requests (good for O3)
        # Fewer MSHRs (1) block side-channel leakage (good for Security)
        self.l2cache.mshrs = self._mshr_count_val
        for cache in self.l1dcaches:
            cache.mshrs = self._mshr_count_val
# 1. Define the Cache Hierarchy logic
if cache_str == 'nocache':
    cache_hierarchy = NoCache()
else:
    cache_hierarchy = DeepDiveHierarchy(l2_lat=l2_lat, mshr_cnt=mshr_cnt)

# 2. The Board
board = SimpleBoard(
    clk_freq="3GHz",
    processor=SimpleProcessor(cpu_type=cpu_type, isa=ISA.X86, num_cores=1),
    memory=SingleChannelDDR3_1600("1GiB"),
    cache_hierarchy=cache_hierarchy,
)

# 3. The Workload (Pointed to your new compiled workload)
# Make sure you successfully ran: gcc -static workload.c -o workload-x86
local_bin = "/home/purti/bootcamp/workload-x86"
board.set_se_binary_workload(BinaryResource(local_path=local_bin))

# 4. The Run
Simulator(board=board).run()
