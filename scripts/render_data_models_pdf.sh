#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_FILE="${REPO_ROOT}/docs/data-models/zoho_creator_data_models.md"
OUTPUT_FILE="${REPO_ROOT}/docs/data-models/zoho_creator_data_models.pdf"
PDF_ENGINE="${PDF_ENGINE:-xelatex}"

if [[ ! -f "${SOURCE_FILE}" ]]; then
  echo "Source file not found: ${SOURCE_FILE}" >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is required but was not found in PATH." >&2
  echo "Install pandoc (https://pandoc.org/installing.html) and re-run the script." >&2
  exit 1
fi

if ! command -v "${PDF_ENGINE}" >/dev/null 2>&1; then
  echo "The requested PDF engine '${PDF_ENGINE}' is not available." >&2
  echo "Install the engine or set PDF_ENGINE to an available command (e.g. wkhtmltopdf, weasyprint)." >&2
  exit 1
fi

pandoc "${SOURCE_FILE}" \
  --from=gfm+pipe_tables+table_captions \
  --to=pdf \
  --pdf-engine="${PDF_ENGINE}" \
  --metadata=title:"Zoho Creator Data Models" \
  --metadata=author:"ERP Implementation Team" \
  --number-sections \
  --table-of-contents \
  --toc-depth=2 \
  --variable=geometry:margin=1in \
  --variable=colorlinks=true \
  --variable=linkcolor:MidnightBlue \
  --variable=urlcolor:RoyalBlue \
  --variable=fontsize:11pt \
  --wrap=none \
  --strip-comments \
  --resource-path="${REPO_ROOT}/docs/data-models" \
  --output="${OUTPUT_FILE}"

echo "PDF generated at ${OUTPUT_FILE}"
