#!/usr/bin/env bash
set -euo pipefail

# Zoho Creator ERP project scaffolding script
# Creates the baseline directory structure for forms, workflows, reports,
# integrations, scripts, dashboards, and related assets.
# Usage:
#   ./scripts/setup_creator_repo.sh [--force] [--modules purchase,sales]

usage() {
  cat <<USAGE
Usage: $0 [options]

Options:
  --force               Recreate directories even if they already exist.
  --modules <list>      Comma-separated list of modules to scaffold. When
                        omitted, all standard ERP modules are created.
  -h, --help            Show this help message and exit.
USAGE
}

FORCE=false
CUSTOM_MODULES=""

while (($#)); do
  case "$1" in
    --force)
      FORCE=true
      shift
      ;;
    --modules)
      if [[ $# -lt 2 ]]; then
        echo "Error: --modules requires a comma-separated value." >&2
        usage
        exit 1
      fi
      CUSTOM_MODULES="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option '$1'" >&2
      usage
      exit 1
      ;;
  esac
done

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

DEFAULT_MODULES=(
  purchase
  sales
  production
  qc
  logistics
  finance
  attendance
)

if [[ -n "$CUSTOM_MODULES" ]]; then
  IFS=',' read -r -a MODULES <<< "$CUSTOM_MODULES"
else
  MODULES=("${DEFAULT_MODULES[@]}")
fi

MODULE_SUBDIRS=(
  forms
  workflows
  reports
  pages
  automations
  scripts
  integrations
  deluge_functions
  schedules
  approvals
  tests
)

SHARED_SUBDIRS=(
  masters
  templates
  dashboards
  test_data
  resources
  deluge_library
  pages
)

GLOBAL_DIRS=(
  deploy/pipelines
  deploy/environments/dev
  deploy/environments/uat
  deploy/environments/prod
  integrations/ai_po_parser
  integrations/face_recognition
  integrations/bank_reconciliation
  integrations/tally_export
  docs/runbooks
  docs/change_logs
  docs/architecture
  docs/release_notes
  tools/scripts
  tools/migrations
)

create_dir() {
  local dir="$1"
  local path="$ROOT_DIR/$dir"
  if [[ -d "$path" ]]; then
    if [[ "$FORCE" == true ]]; then
      echo "[reset]  $dir"
      rm -rf "$path"
    else
      echo "[skip]   $dir (already exists)"
      return
    fi
  fi
  echo "[create] $dir"
  mkdir -p "$path"
  touch "$path/.gitkeep"
}

seed_readme() {
  local path="$1"
  local title="$2"
  local body="$3"
  if [[ -f "$path" && "$FORCE" != true ]]; then
    return
  fi
  echo "[seed]   ${path#"$ROOT_DIR/"}"
  mkdir -p "$(dirname "$path")"
  cat <<README > "$path"
# $title

$body

- Commit Zoho Creator exports (JSON/XML) and supporting artefacts here.
- Update this README with module-specific conventions as they evolve.
README
}

main() {
  echo "Creating Zoho Creator ERP scaffolding under $ROOT_DIR"

  for module in "${MODULES[@]}"; do
    local module_root="apps/$module"
    local module_title=$(echo "$module" | tr '[:lower:]' '[:upper:]')
    create_dir "$module_root"
    seed_readme \
      "$ROOT_DIR/$module_root/README.md" \
      "$module_title Module" \
      "Forms, workflows, reports, and automations for the $module module."
    for subdir in "${MODULE_SUBDIRS[@]}"; do
      create_dir "$module_root/$subdir"
    done
  done

  for subdir in "${SHARED_SUBDIRS[@]}"; do
    create_dir "apps/shared/$subdir"
  done
  seed_readme \
    "$ROOT_DIR/apps/shared/README.md" \
    "Shared Assets" \
    "Common masters, templates, dashboards, and reusable Deluge assets."

  for dir in "${GLOBAL_DIRS[@]}"; do
    create_dir "$dir"
  done

  declare -A README_MAP=(
    ["apps"]="Module-specific artefacts exported from Zoho Creator (forms, workflows, reports, automations)."
    ["deploy"]="Deployment pipelines, environment-specific configuration, and release documentation."
    ["integrations"]="Integration adapters, API scripts, and supporting documentation."
    ["docs/runbooks"]="Operational runbooks for admins and support teams."
    ["docs/change_logs"]="Chronological change history for Creator configurations."
    ["docs/architecture"]="System diagrams, ERDs, and blueprint references."
    ["docs/release_notes"]="Release summaries aligned with Creator deployments."
    ["tools/scripts"]="Utility scripts that support build, migration, or QA tasks."
    ["tools/migrations"]="Data migration playbooks, mapping sheets, and helper scripts."
  )

  for dir in "${!README_MAP[@]}"; do
    local title_base=$(basename "$dir")
    local title_upper=$(echo "$title_base" | tr '[:lower:]' '[:upper:]')
    seed_readme "$ROOT_DIR/$dir/README.md" "$title_upper Directory" "${README_MAP[$dir]}"
  done

  echo "Scaffolding complete."
}

main "$@"
