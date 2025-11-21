

read -p "Enter the name of the file: " file

if [[ ! -f "$file" ]]; then
    echo "Error: File '$file' not found!"
    exit 1
fi

echo "Reading assemblies from '$file'..."
count=0

mkdir -p sequences

# Αν το CSV έχει ελληνικά ή ; αντί για , αλλάζουμε εδώ:
tail -n +2 "$file" | while IFS=';' read -r accession description; do
    ((count++))
    echo ""
    echo "[$count] Assembly: $accession"
    echo "Description: $description"
    echo "----------------------------------"

    # Αποθηκεύει το FASTA σε αρχείο
    curl -s "https://www.ebi.ac.uk/ena/browser/api/fasta/${accession}" -o "sequences/${accession}.fasta"

    # Αν το αρχείο βγήκε άδειο, δείξε προειδοποίηση
    if [[ ! -s "sequences/${accession}.fasta" ]]; then
        echo "⚠️  No FASTA found for ${accession}"
    else
        echo "✅ Sequence saved: sequences/${accession}.fasta"
    fi

    sleep 0.1
done
