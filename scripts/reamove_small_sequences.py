import os
import pandas as pd
import shutil

# Φάκελος με ΟΛΑ τα assemblies (.fasta)
assemblies_folder = r"C:\Users\kapos\OneDrive\Υπολογιστής\bash\sequences"

# CSV με τα assemblies που πρέπει να αφαιρεθούν
csv_path = r"C:\Users\kapos\OneDrive\Υπολογιστής\bash\small_seq.csv"

# Φάκελος όπου θα μετακινηθούν τα αρχεία που αφαιρούμε (για ασφάλεια)
removed_folder = r"C:\Users\kapos\OneDrive\Υπολογιστής\bash\removed_assemblies"
os.makedirs(removed_folder, exist_ok=True)

# Διαβάζουμε τα ονόματα από το CSV
to_remove = (
    pd.read_csv(csv_path, header=None)[0]
    .astype(str)
    .str.strip()
    .str.lower()
    .tolist()
)

# Παίρνουμε όλα τα FASTA/FA/FNA αρχεία
all_files = [
    f for f in os.listdir(assemblies_folder)
    if f.lower().endswith((".fasta", ".fa", ".fna", ".fas", ".fastq"))
]

removed = []
not_found = []

# Συγκρίνουμε και μετακινούμε
for filename in all_files:
    low = filename.lower()

    # Αν το όνομα αρχείου περιέχει κάποιο από τα names του CSV
    if any(remove in low for remove in to_remove):
        shutil.move(
            os.path.join(assemblies_folder, filename),
            os.path.join(removed_folder, filename)
        )
        removed.append(filename)

# Output
print("=== Removed assemblies ===")
for f in removed:
    print(f)

print("\n=== Items in CSV NOT found in assemblies folder ===")
for item in to_remove:
    if not any(item in f.lower() for f in all_files):
        print(item)

print("\nDONE!")
