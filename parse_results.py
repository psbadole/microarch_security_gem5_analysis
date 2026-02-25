import os
import csv

# Define the folders we want to scrape
results_folders = [
    "project_results/inorder_nocache",
    "project_results/ooo_nocache",
    "project_results/inorder_cache",
    "project_results/ooo_cache"
]

# The specific stats we want to extract
# Format: (Display Name, String to search for in stats.txt)
metrics = {
    "SimTicks": "simTicks",
    "IPC": "board.processor.cores0.ipc",
    "SquashedInsts": "board.processor.cores0.commit.squashedInsts",
    "L1D_Misses": "board.cache_hierarchy.l1dcaches.overall_mshr_misses::total"
}

def extract_stat(file_path, stat_name):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if stat_name in line:
                    # gem5 stats format: name   value   # description
                    parts = line.split()
                    return parts[1]
    except FileNotFoundError:
        return "N/A"
    return "Not Found"

# Create the CSV file
with open('simulation_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    header = ["Scenario"] + list(metrics.keys())
    writer.writerow(header)

    # Extract data for each folder
    for folder in results_folders:
        row = [folder.split('/')[-1]] # Just the folder name
        stats_file = os.path.join(folder, "stats.txt")

        for display_name, search_string in metrics.items():
            value = extract_stat(stats_file, search_string)
            row.append(value)

        writer.writerow(row)

print("--- DATA EXTRACTION COMPLETE ---")
print("Open 'simulation_results.csv' in Excel to see your data.")
