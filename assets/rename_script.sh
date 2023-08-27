#!/bin/bash

# Navigate to the parent directory containing the "survey" folder
# cd /path/to/parent/directory

# Loop through each subdirectory inside "survey"
for folder in survey/*/; do
    # Check if the folder contains "age1.json"
    if [[ -f "$folder/age3.json" ]]; then
        # Rename "age1.json" to "3-5.json"
        mv "$folder/age3.json" "$folder/8-12.json"
    fi
done

