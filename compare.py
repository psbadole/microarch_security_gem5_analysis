from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import ISA
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import PrivateL1SharedL2CacheHierarchy
from gem5.components.cachehierarchies.classic.no_cache import NoCache # Added this
import sys

# Setup:
# Argument 1: 'timing' or 'o3'
# Argument 2: 'with_cache' or 'nocache'
cpu_str = sys.argv[1] if len(sys.argv) > 1 else 'timing'
cache_str = sys.argv[2] if len(sys.argv) > 2 else 'with_cache'

cpu_type = CPUTypes.TIMING if cpu_str == 'timing' else CPUTypes.O3

print(f"--- STARTING SIMULATION: {cpu_str} | Cache Mode: {cache_str} ---")

# 1. Define the Cache Hierarchy logic
if cache_str == 'nocache':
    cache_hierarchy = NoCache()
else:
    cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
        l1d_size="32KiB",
        l1i_size="32KiB",
        l2_size="256KiB"
    )

# 2. The Board
board = SimpleBoard(
    clk_freq="3GHz",
    processor=SimpleProcessor(cpu_type=cpu_type, isa=ISA.X86, num_cores=1),
    memory=SingleChannelDDR3_1600("1GiB"),
    cache_hierarchy=cache_hierarchy,
)

# 3. The Workload (Local path to avoid SSL errors)
local_bin = "/home/purti/.cache/gem5/x86-hello64-static"
board.set_se_binary_workload(BinaryResource(local_path=local_bin))

# 4. The Run
Simulator(board=board).run()
