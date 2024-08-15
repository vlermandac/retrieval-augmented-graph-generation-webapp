#!/bin/sh

# Directory to save the CSV files
output_dir="docker_stats"
mkdir -p "$output_dir"

# Counter for file naming
counter=1

# Loop to run the docker stats command every 3 seconds
while true; do
  # Get the current timestamp
  timestamp=$(date +'%Y%m%d_%H%M%S')

  # Define the output file name
  output_file="$output_dir/docker_stats_$timestamp.csv"

  # Run the docker stats command and save the output to the CSV file
  docker stats --no-stream --format 'table {{.Name}},{{.CPUPerc}},{{.MemUsage}}' > "$output_file"

  # Print a message
  echo "Saved stats to $output_file"

  # Increment the counter
  ((counter++))

  # Wait for 3 seconds
  sleep 3

done
