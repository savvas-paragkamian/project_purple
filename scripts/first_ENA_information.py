

# Ask for the filename
echo -n "Enter the name of the file: "
read file

# Check if the file exists
if [ ! -f "$file" ]; then
    echo "Error: File '$file' not found!"
    exit 1
fi

# Define output file
output="output.txt"

# Clear or create the output file
> "$output"

echo "Opening and reading '$file'..."
echo "Saving numbered output to '$output'"
echo "----------------------------------"

count=0  # Initialize line counter

# Read file line by line
while IFS= read -r line; do
    ((count++))                           # Increase counter
    echo "$count: $line" | tee -a "$output"  # Print and save to file
    sleep 0.1                             # Wait 0.1 second
done < "$file"

echo "----------------------------------"
echo "Total lines: $count" | tee -a "$output"
