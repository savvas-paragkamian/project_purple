#!/usr/bin/env bash
# ena_fetch_fasta_and_sample_xml.sh
# Usage: ./ena_fetch_fasta_and_sample_xml.sh assemblies.txt [out_dir]
# Requires: curl, jq

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <assemblies_txt> [out_dir]" >&2
  exit 1
fi

ASSEMBLIES_FILE="$1"
OUT_DIR="${2:-ena_out}"
mkdir -p "$OUT_DIR/assemblies" "$OUT_DIR/samples"

for cmd in curl jq; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Error: '$cmd' is required." >&2; exit 1; }
done

PORTAL_BASE="https://www.ebi.ac.uk/ena/portal/api/search"
BROWSER_XML_BASE="https://www.ebi.ac.uk/ena/browser/api/xml"

# We ask ENA for sample + FASTA links in one shot
ASM_FIELDS="assembly_accession,sample_accession,fasta_ftp,assembly_name,scientific_name"

# Helper: safe URL encode via jq
urlenc() { jq -sRr @uri <<<"$1"; }

# Helper: normalize ftp:// to https:// (curl can do ftp, but https is often simpler)
normalize_ftp_to_https() {
  sed -E 's|^ftp://|https://|'
}

# Helper: download with retries (3 attempts)
get_file() {
  local url="$1"
  local out="$2"
  curl -sS --fail -L --retry 3 --retry-delay 1 "$url" -o "$out"
}

while IFS= read -r acc_raw; do
  acc="$(echo "$acc_raw" | tr -d '\r' | xargs)"
  [[ -z "$acc" || "$acc" =~ ^# ]] && continue

  echo "[INFO] Assembly: $acc"

  # Query assembly record
  asm_url="${PORTAL_BASE}?result=assembly&query=$(urlenc "assembly_accession=\"$acc\"")&fields=$(urlenc "$ASM_FIELDS")&format=json"
  asm_json="$OUT_DIR/assemblies/${acc}.json"

  if ! curl -sS --fail "$asm_url" -o "$asm_json"; then
    echo "[WARN] Failed assembly lookup for $acc" >&2
    continue
  fi
  sleep 0.1

  # Extract sample accession and fasta_ftp list (semicolon-separated)
  sample_acc="$(jq -r 'try .[0].sample_accession // empty' "$asm_json" || true)"
  fasta_list="$(jq -r 'try .[0].fasta_ftp // empty' "$asm_json" || true)"

  # --- Download assembly FASTA files ---
  if [[ -n "$fasta_list" ]]; then
    IFS=';' read -r -a fasta_array <<<"$fasta_list"
    for f in "${fasta_array[@]}"; do
      f_url="$(echo "$f" | normalize_ftp_to_https)"
      fname="$(basename "$f")"
      out_fp="$OUT_DIR/assemblies/${acc}__${fname}"
      echo "    ↳ FASTA: $f_url"
      if get_file "$f_url" "$out_fp"; then
        :
      else
        echo "[WARN] Failed to download FASTA: $f_url" >&2
      fi
      sleep 0.1
    done
  else
    echo "    ↳ No FASTA links (fasta_ftp) reported by ENA."
  fi

  # --- Get sample metadata as XML ---
  if [[ -n "$sample_acc" ]]; then
    xml_url="${BROWSER_XML_BASE}/${sample_acc}"
    xml_out="$OUT_DIR/samples/${sample_acc}.xml"
    echo "    ↳ Sample XML: $sample_acc"
    if get_file "$xml_url" "$xml_out"; then
      :
    else
      echo "[WARN] Failed to fetch sample XML for $sample_acc" >&2
    fi
    sleep 0.1
  else
    echo "    ↳ No linked sample_accession."
  fi

done < "$ASSEMBLIES_FILE"

echo "[DONE] Assemblies (FASTA) and sample XML saved in: $OUT_DIR"
