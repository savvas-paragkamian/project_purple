python3 - << 'EOF'
import xml.etree.ElementTree as ET
import pandas as pd
import glob

# Φάκελος με τα XML αρχεία
xml_files = glob.glob("valid_samples_xml/*.xml")  # ή το path για τα XML σου

data = []

for f in xml_files:
    tree = ET.parse(f)
    root = tree.getroot()
    assembly = root.findtext("assembly")
    sample_id = root.findtext("sample_id")
    data.append({"Assembly": assembly, "Sample_ID": sample_id})

# Δημιουργία DataFrame
df = pd.DataFrame(data)

# Αποθήκευση σε TSV
df.to_csv("samples_from_xml.tsv", sep="\t", index=False)

print(f"Converted {len(df)} XML files into 'samples_from_xml.tsv'")
EOF
