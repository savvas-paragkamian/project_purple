#!/usr/bin/env bash

file="../data/assemblies.csv"
echo $file

if [ ! -f "$file" ]; then
    echo "Error: file '$file' not found"
    exit 1
fi

echo "Reading from file '$file'"

echo "downloading"

mkdir -p ../assemblies

count=0

tail -n +2 "$file" | while IFS=";" read -r accession description; do 

    ((count++))
    echo "start"
    echo "[$count] Assembly: $accession"
    echo "Description: $description"

    curl -s "https://www.ebi.ac.uk/ena/browser/api/fasta/$accession" -o "../assemblies/${accession}.fasta"

    if [[ ! -s "../assemblies/${accession}.fasta" ]]; then
        echo "fasta not found"
    else
        echo "fasta found"
    fi

    sleep 0.1

done
