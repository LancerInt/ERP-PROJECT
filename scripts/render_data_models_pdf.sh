#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_FILE="${REPO_ROOT}/docs/data-models/zoho_creator_data_models.md"
OUTPUT_FILE="${REPO_ROOT}/docs/data-models/zoho_creator_data_models.pdf"
HEADER_FILE="${SCRIPT_DIR}/pandoc/data_models_preamble.tex"
LUA_FILTER="${SCRIPT_DIR}/pandoc/table_formatter.lua"
PDF_ENGINE="${PDF_ENGINE:-xelatex}"

if [[ ! -f "${SOURCE_FILE}" ]]; then
  echo "Source file not found: ${SOURCE_FILE}" >&2
  exit 1
fi

if [[ ! -f "${HEADER_FILE}" ]]; then
  echo "Pandoc header include missing: ${HEADER_FILE}" >&2
  exit 1
fi

if [[ ! -f "${LUA_FILTER}" ]]; then
  echo "Pandoc Lua filter missing: ${LUA_FILTER}" >&2
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
  --from=markdown+pipe_tables+table_captions+autolink_bare_uris \
  --to=pdf \
  --pdf-engine="${PDF_ENGINE}" \
  --metadata=title:"Zoho Creator Data Models" \
  --metadata=author:"ERP Implementation Team" \
  --metadata=lot:true \
  --number-sections \
  --table-of-contents \
  --toc-depth=3 \
  --include-in-header="${HEADER_FILE}" \
  --lua-filter="${LUA_FILTER}" \
  --variable=geometry:margin=0.75in,landscape \
  --variable=colorlinks=true \
  --variable=linkcolor:MidnightBlue \
  --variable=urlcolor:RoyalBlue \
  --variable=fontsize:11pt \
  --wrap=auto \
  --strip-comments \
  --resource-path="${REPO_ROOT}/docs/data-models" \
  --output="${OUTPUT_FILE}"

echo "PDF generated at ${OUTPUT_FILE}"
