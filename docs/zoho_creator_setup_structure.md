# Zoho Creator ERP Setup Script & Repository Structure

This guide describes the scaffolding script and repository layout used to organise Zoho Creator exports for forms, workflows, reports, integrations, scripts, and related artefacts. Run the script before your first export to ensure a consistent folder hierarchy across environments.

## 1. Scaffolding Script

The `scripts/setup_creator_repo.sh` script provisions a standard set of directories for every ERP module and shared component.

```bash
./scripts/setup_creator_repo.sh         # create structure (no overwrite)
./scripts/setup_creator_repo.sh --force # recreate structure and reset placeholders
```

### 1.1 Script Features
- Creates module-specific folders under `apps/` for **Purchase, Sales, Production, QC, Logistics, Finance, Attendance**, plus shared masters, templates, dashboards, and test data.
- Generates environment folders under `deploy/` for **dev**, **uat**, and **prod** release assets and pipeline automation.
- Seeds integration stubs for AI PO parsing, face recognition, bank reconciliation, and Tally exports under `integrations/`.
- Adds runbook and change-log workspaces beneath `docs/` to capture operational procedures and configuration history.
- Drops `.gitkeep` markers so empty directories remain version-controlled.
- Provides README templates describing how to populate each top-level area.

### 1.2 Extending the Script
- Append new entries to the `MODULE_DIRS` list for additional Creator modules (e.g., HR, Maintenance) or tooling (e.g., monitoring, backups).
- Update the `README_MAP` dictionary with explanatory text when new top-level collections are introduced.
- Wrap custom setup logic (such as copying boilerplate Deluge scripts) in helper functions invoked from `main()` to maintain readability.

## 2. Repository Branch Structure

Use Git branches to stage Creator artefact changes per module while keeping cross-module dependencies coordinated. A suggested branching strategy is shown below:

```
main
├── env/dev
├── env/uat
└── feature/
    ├── purchase-<ticket-id>
    ├── sales-<ticket-id>
    ├── production-<ticket-id>
    ├── qc-<ticket-id>
    ├── logistics-<ticket-id>
    ├── finance-<ticket-id>
    └── attendance-<ticket-id>
```

- **main** – audited baseline aligned with production Creator configuration.
- **env/dev** – accumulates changes ready for deployment to the development sandbox.
- **env/uat** – mirrors the UAT tenant; only merge when a release candidate is validated.
- **feature/** branches – focused on module-specific changes (forms, workflows, reports, integrations). Prefix with the module name and the Zoho Project/ticket identifier for traceability.

## 3. Directory Map

Once the scaffolding script runs, the repository will follow this high-level layout:

```
apps/
├── purchase/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── integrations/
│   └── scripts/
├── sales/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── integrations/
│   └── scripts/
├── production/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── integrations/
│   └── scripts/
├── qc/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   └── scripts/
├── logistics/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   └── scripts/
├── finance/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── integrations/
│   └── scripts/
├── attendance/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   └── scripts/
└── shared/
    ├── masters/
    ├── templates/
    ├── dashboards/
    └── test_data/

deploy/
├── environments/
│   ├── dev/
│   ├── uat/
│   └── prod/
└── pipelines/

integrations/
├── ai_po_parser/
├── face_recognition/
├── bank_reconciliation/
└── tally_export/

docs/
├── runbooks/
└── change_logs/

scripts/
└── setup_creator_repo.sh
```

### 3.1 Recommended Contents
- **forms/** – JSON/XML exports of Creator forms, field metadata, and layout customisations.
- **workflows/** – Deluge scripts, approval configurations, and scheduled functions.
- **reports/** – custom list views, dashboards, pivot tables, and embedded analytics definitions.
- **integrations/** – REST connectors, API specs, and supporting scripts (e.g., for OpenAI parsers or bank statement ingestion).
- **scripts/** – reusable Deluge functions, migration scripts, and utilities not tied to a single form.
- **deploy/** – CI/CD manifests, release notes, and environment-specific configuration files.
- **integrations/** (root) – adapters for external systems: OpenAI APIs, face recognition, Tally, banking feeds.
- **docs/** – operational runbooks, SOPs, change logs, and architecture references (linking back to the existing blueprint, ERDs, and data models).

## 4. Workflow for Updating Artefacts

1. **Create a feature branch** aligned with the module change (`feature/purchase-1234`).
2. **Export Creator artefacts** (forms, workflows, reports) and place them in the relevant module folders.
3. **Update documentation** (e.g., data models, ERDs) if the change modifies schema or process logic.
4. **Commit and push** the artefacts alongside supporting notes in `docs/change_logs/`.
5. **Open a pull request** targeting `env/dev` or `main` depending on the release schedule.
6. **Run the setup script** (`--force`) when structure resets are required (e.g., repo bootstrap, major reorganisation).

## 5. Next Steps

- Add module-specific README files that describe naming conventions for forms, workflows, and scripts.
- Integrate the scaffolding script with CI to validate required directories exist before merges.
- Capture environment-specific secrets in a secure vault and reference them in `deploy/environments/*` documentation rather than storing plain text in the repository.
