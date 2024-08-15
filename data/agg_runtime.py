import pandas as pd
import glob
import os


def parse_memory(mem_str):
    """Convert memory usage string to MiB."""
    if 'GiB' in mem_str:
        return float(mem_str.replace('GiB', '')) * 1024
    elif 'MiB' in mem_str:
        return float(mem_str.replace('MiB', ''))
    else:
        return float(mem_str)


def parse_cpu(cpu_str):
    """Convert CPU usage string to float."""
    return float(cpu_str.replace('%', ''))


# Path to the directory containing the CSV files
csv_files_path = './docker_stats'

# Get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_files_path, '*.csv'))

# Initialize an empty DataFrame to store combined data
combined_df = pd.DataFrame()

# Read and concatenate all CSV files
for file in csv_files:
    df = pd.read_csv(file, skipinitialspace=True)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# Convert CPU % and MEM USAGE to numeric values
combined_df['CPU %'] = combined_df['CPU %'].apply(parse_cpu)
combined_df['MEM USAGE / LIMIT'] = combined_df['MEM USAGE / LIMIT'].apply(lambda x: parse_memory(x.split('/')[0]))

# Group by NAME and calculate statistics
stats = combined_df.groupby('NAME').agg({
    'CPU %': ['mean', 'std', 'min', 'max'],
    'MEM USAGE / LIMIT': ['mean', 'std', 'min', 'max']
})

print(stats)
# save the stats in a text file 
stats.to_csv('stats.txt')
