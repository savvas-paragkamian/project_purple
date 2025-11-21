python3 - <<  
import pandas as pd
import xml.etree.ElementTree as ET
import os

df = pd.read_csv("sample_ids.tsv", sep="\t")
df_valid = df[df["Sample_ID"] != "NOT_FOUND"]

outdir = "valid_samples_xml"
os.makedirs(outdir, exist_ok=True)

for _, row in df_valid.iterrows():
    root = ET.Element("sample")
    ET.SubElement(root, "assembly").text = row["Assembly"]
    ET.SubElement(root, "sample_id").text = row["Sample_ID"]
    tree = ET.ElementTree(root)
    tree.write(f"{outdir}/{row['Assembly']}.xml", encoding="utf-8", xml_declaration=True)

root_all = ET.Element("samples")
for _, row in df_valid.iterrows():
    sample = ET.SubElement(root_all, "sample")
    ET.SubElement(sample, "assembly").text = row["Assembly"]
    ET.SubElement(sample, "sample_id").text = row["Sample_ID"]

tree_all = ET.ElementTree(root_all)
tree_all.write("all_valid_samples.xml", encoding="utf-8", xml_declaration=True)

print(f"Created {len(df_valid)} XML files in '{outdir}' and one combined XML 'all_valid_samples.xml'")

