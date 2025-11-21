#!/usr/bin/env bash

# Define the path to the input CSV file
file="../data/assemblies.csv"
echo $file

# Check if the file exists
if [ ! -f "$file" ]; then
    echo "Error: file '$file' not found"
    exit 1
fi

echo "Reading from file '$file'"

echo "Downloading assemblies..."

# Create the output directory for downloaded FASTA files
mkdir -p ../assemblies

count=0

# Read the file line by line, ignoring the header (using tail -n +2)
# Each line contains an accession and description separated by ";"
tail -n +2 "$file" | while IFS=";" read -r accession description; do 

    ((count++))
    echo "----------------------------------"
    echo "[$count] Assembly: $accession"
    echo "Description: $description"

    # Download the FASTA sequence from ENA
    curl -s "https://www.ebi.ac.uk/ena/browser/api/fasta/$accession" -o "../assemblies/${accession}.fasta"

    # Check if the file was successfully downloaded and is not empty
    if [[ ! -s "../assemblies/${accession}.fasta" ]]; then
        echo "❌ FASTA not found or empty"
    else
        echo "✅ FASTA found and saved"
    fi

    # Small delay to avoid overwhelming the server
    sleep 0.1

done


# ----------------------------------------------------
# CHECK THE SIZE OF DOWNLOADED FASTA FILES
# ----------------------------------------------------

echo ""
echo "======================================"
echo "📈 Checking FASTA file sizes..."
echo ""

# Find the smallest file size among all FASTA files
min_size=$(find ../assemblies -type f -name "*.fasta" -printf "%s\n" | sort -n | head -n 1)

# If no FASTA files exist, print an error message
if [[ -z "$min_size" ]]; then
    echo "⚠️  No FASTA files found to analyze."
else
    echo "🔹 Smallest FASTA file size: ${min_size} bytes"
    echo "🔹 Assemblies with this size:"
    echo "--------------------------------------"
    
    # Print the names and sizes of all files that have the minimal size
    find ../assemblies -type f -name "*.fasta" -size "${min_size}c" -printf "⚠️  %f (%s bytes)\n"
    
    echo "--------------------------------------"
    
    # Count how many assemblies have this minimal size
    empty_count=$(find ../assemblies -type f -name "*.fasta" -size "${min_size}c" | wc -l)
    echo "⚠️  Total assemblies with minimal size: $empty_count"
fi
