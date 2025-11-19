import xml.etree.ElementTree as ET
import pandas as pd
import os
from glob import glob

# Φάκελος με τα XML
xml_dir = "full_sample_xml"
out_tsv = "tsv_outputs/samples_from_xml.tsv"

records = []

# Παραλλαγές tags που ψάχνουμε
env_tags = ["environment (biome)", "environment (feature)", "environmental medium",
            "broad-scale environmental context", "local environmental context"]
mat_tags = ["ref_biomaterial", "type-material", "source_material_id", "environment (material)"]

# Διαβάζουμε όλα τα XML
for xml_file in glob(os.path.join(xml_dir, "*.xml")):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Παίρνουμε assembly και sample_id
        assembly = root.find(".//SUBMITTER_ID")
        assembly = assembly.text if assembly is not None else "NA"
        sample_id = root.find(".//PRIMARY_ID")
        sample_id = sample_id.text if sample_id is not None else "NA"

        # Environment
        env_value = "NA"
        for attr in root.findall(".//SAMPLE_ATTRIBUTE"):
            tag_elem = attr.find("TAG")
            value_elem = attr.find("VALUE")
            if tag_elem is not None and value_elem is not None:
                if tag_elem.text in env_tags:
                    env_value = value_elem.text
                    break

        # Material
        mat_value = "NA"
        for attr in root.findall(".//SAMPLE_ATTRIBUTE"):
            tag_elem = attr.find("TAG")
            value_elem = attr.find("VALUE")
            if tag_elem is not None and value_elem is not None:
                if tag_elem.text in mat_tags:
                    mat_value = value_elem.text
                    break

        records.append({
            "Assembly": assembly,
            "Sample_ID": sample_id,
            "Environment_Biome": env_value,
            "Material": mat_value
        })

    except ET.ParseError:
        print(f"Warning: Failed to parse {xml_file}")

# Δημιουργία DataFrame και αποθήκευση σε TSV
df = pd.DataFrame(records)
df.to_csv(out_tsv, sep="\t", index=False)
print(f"Created TSV with {len(df)} samples: {out_tsv}")