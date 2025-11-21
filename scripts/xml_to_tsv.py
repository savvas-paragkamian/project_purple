#!/usr/bin/env bash

xml_folder="./sequences_xml"
output_file="sample_ids.tsv"

# Check if folder exists
if [ ! -d "$xml_folder" ]; then
    echo "Error: folder '$xml_folder' not found!"
    exit 1
fi

# Write header to TSV
echo -e "Assembly\tSample_ID" > "$output_file"

found=0
not_found=0
count=0

echo "🔍 Extracting Sample IDs from XML files..."

# Loop through XMLs
for xml in "$xml_folder"/*.xml; do
    ((count++))
    assembly=$(basename "$xml" .xml)

    # Search for all possible sample references (broader search)
    sample_id=$(grep -oE '(SAMEA[0-9]+|SAMD[0-9]+|SRS[0-9]+|ERS[0-9]+|ERX[0-9]+)' "$xml" | head -n 1)

    if [ -z "$sample_id" ]; then
        sample_id="NOT_FOUND"
        ((not_found++))
    else
        ((found++))
    fi

    echo -e "${assembly}\t${sample_id}" >> "$output_file"
    echo "[$count] $assembly → $sample_id"
done

echo "---------------------------------------------"
echo "✅ Total assemblies checked: $count"
echo "📦 Found sample IDs: $found"
echo "⚠️  Missing sample IDs: $not_found"
echo "💾 Results saved to: $output_file"
