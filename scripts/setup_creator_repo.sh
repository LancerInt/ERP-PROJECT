#!/usr/bin/env bash
set -euo pipefail

# Zoho Creator ERP project scaffolding script
# Creates the baseline directory structure for forms, workflows, reports,
# integrations, scripts, dashboards, and related assets.
# Usage: ./scripts/setup_creator_repo.sh [--force]

FORCE=false
if [[ ${1-} == "--force" ]]; then
  FORCE=true
fi

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
MODULE_DIRS=(
  "apps/purchase/forms"
  "apps/purchase/workflows"
  "apps/purchase/reports"
  "apps/purchase/integrations"
  "apps/purchase/scripts"
  "apps/sales/forms"
  "apps/sales/workflows"
  "apps/sales/reports"
  "apps/sales/integrations"
  "apps/sales/scripts"
  "apps/production/forms"
  "apps/production/workflows"
  "apps/production/reports"
  "apps/production/integrations"
  "apps/production/scripts"
  "apps/qc/forms"
  "apps/qc/workflows"
  "apps/qc/reports"
  "apps/qc/scripts"
  "apps/logistics/forms"
  "apps/logistics/workflows"
  "apps/logistics/reports"
  "apps/logistics/scripts"
  "apps/finance/forms"
  "apps/finance/workflows"
  "apps/finance/reports"
  "apps/finance/integrations"
  "apps/finance/scripts"
  "apps/attendance/forms"
  "apps/attendance/workflows"
  "apps/attendance/reports"
  "apps/attendance/scripts"
  "apps/shared/masters"
  "apps/shared/templates"
  "apps/shared/dashboards"
  "apps/shared/test_data"
  "deploy/pipelines"
  "deploy/environments/dev"
  "deploy/environments/uat"
  "deploy/environments/prod"
  "integrations/ai_po_parser"
  "integrations/face_recognition"
  "integrations/bank_reconciliation"
  "integrations/tally_export"
  "docs/runbooks"
  "docs/change_logs"
)

create_dir() {
  local dir="$1"
  local path="$ROOT_DIR/$dir"
  if [[ -d "$path" ]]; then
    if [[ "$FORCE" == true ]]; then
      echo "[reset] $dir"
      rm -rf "$path"
    else
      echo "[skip]  $dir (already exists)"
      return
    fi
  fi
  echo "[create] $dir"
  mkdir -p "$path"
  touch "$path/.gitkeep"
}

main() {
  echo "Creating Zoho Creator ERP scaffolding under $ROOT_DIR"
  for dir in "${MODULE_DIRS[@]}"; do
    create_dir "$dir"
  done

  # Seed README files for root collections if missing
  declare -A README_MAP=(
    ["apps"]="Module-specific artefacts exported from Zoho Creator (forms, workflows, reports, scripts)."
    ["deploy"]="Deployment pipelines, environment-specific configuration, and release notes."
    ["integrations"]="Integration adapters, API scripts, and supporting documentation."
    ["docs/runbooks"]="Operational runbooks for admins and support teams."
    ["docs/change_logs"]="Chronological change history for Creator configurations."
  )

  for dir in "${!README_MAP[@]}"; do
    local path="$ROOT_DIR/$dir/README.md"
    if [[ ! -f "$path" || "$FORCE" == true ]]; then
      echo "[seed]   $dir/README.md"
      mkdir -p "$(dirname "$path")"
      cat <<README > "$path"
# ${dir^} Directory

${README_MAP[$dir]}

- Populate this folder with exported artefacts and documentation.
- Commit JSON/XML exports and supporting scripts to maintain history.
README
    fi
  done

  echo "Scaffolding complete."
}

main "$@"
