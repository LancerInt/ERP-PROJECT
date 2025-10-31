# Zoho Creator ERP Setup Script & Repository Structure

This guide describes the scaffolding script and repository layout used to organise Zoho Creator exports for forms, workflows, reports, integrations, scripts, and related artefacts. Run the script before your first export to ensure a consistent folder hierarchy across environments.

## 1. Scaffolding Script

The `scripts/setup_creator_repo.sh` script provisions a standard set of directories for every ERP module and shared component.

```bash
./scripts/setup_creator_repo.sh \
  # create structure (no overwrite)

./scripts/setup_creator_repo.sh --force \
  # recreate structure and reset placeholders

./scripts/setup_creator_repo.sh --modules purchase,finance \
  # scaffold a subset of modules during pilots
```

### 1.1 Script Features
- Creates module-specific folders under `apps/` for **Purchase, Sales, Production, QC, Logistics, Finance, Attendance** (or a subset defined by `--modules`), with nested directories for forms, workflows, reports, pages, automations, scripts, integrations, Deluge functions, schedules, approvals, and tests.
- Generates shared workspaces for masters, templates, dashboards, test data, reusable Deluge libraries, and Creator pages under `apps/shared/`.
- Builds environment folders under `deploy/` for **dev**, **uat**, and **prod**, plus a reusable `pipelines/` directory for CI configuration.
- Seeds integration stubs for AI PO parsing, face recognition, bank reconciliation, and Tally exports under `integrations/`.
- Adds dedicated `docs/architecture` and `docs/release_notes` areas alongside runbooks and change logs to support governance deliverables.
- Provisions `tools/` folders for automation scripts and migration utilities used during rollout.
- Drops `.gitkeep` markers so empty directories remain version-controlled.
- Provides README templates describing how to populate each top-level and module-specific area; the script rewrites them when `--force` is supplied.

### 1.2 Extending the Script
- Pass `--modules hr,maintenance` to quickly spin up experimental modules without editing the script.
- Update the `MODULE_SUBDIRS` array when Creator introduces new artefact types (e.g., blueprint states, serverless functions).
- Extend `GLOBAL_DIRS` for additional cross-cutting folders such as monitoring, compliance evidence, or incident response.
- Update the `README_MAP` dictionary with explanatory text when new top-level collections are introduced.
- Wrap custom setup logic (such as copying boilerplate Deluge scripts) in helper functions invoked from `main()` to maintain readability.

## 2. Repository Branch Structure

Use Git branches to stage Creator artefact changes per module while keeping cross-module dependencies coordinated. A suggested branching strategy is shown below:

```
main
├── env/dev
├── env/uat
├── release/<yyyy-mm-dd>
├── hotfix/<issue-id>
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
- **release/** – time-boxed staging branches coordinating cross-module drops heading to production.
- **hotfix/** – urgent fixes branched from `main` and merged back once validated.
- **feature/** branches – focused on module-specific changes (forms, workflows, reports, integrations). Prefix with the module name and the Zoho Project/ticket identifier for traceability.

## 3. Directory Map

Once the scaffolding script runs, the repository will follow this high-level layout:

```
apps/
├── purchase/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── sales/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── production/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── qc/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── logistics/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── finance/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
├── attendance/
│   ├── forms/
│   ├── workflows/
│   ├── reports/
│   ├── pages/
│   ├── automations/
│   ├── scripts/
│   ├── integrations/
│   ├── deluge_functions/
│   ├── schedules/
│   ├── approvals/
│   └── tests/
└── shared/
    ├── masters/
    ├── templates/
    ├── dashboards/
    ├── test_data/
    ├── resources/
    ├── deluge_library/
    └── pages/

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
├── change_logs/
├── architecture/
└── release_notes/

tools/
├── scripts/
└── migrations/

scripts/
└── setup_creator_repo.sh
```

### 3.1 Recommended Contents
- **forms/** – JSON/XML exports of Creator forms, field metadata, and layout customisations.
- **workflows/** – Deluge workflows, conditional approvals, and email/SMS alerts.
- **reports/** – custom list views, dashboards, pivot tables, and embedded analytics definitions.
- **pages/** – Creator pages, guided landing pages, and embedded dashboards.
- **automations/** – Blueprint configurations, approval chains, and orchestration scripts.
- **scripts/** – reusable Deluge utilities and helper methods not tied to a single form.
- **integrations/** – REST connectors, API specs, and supporting scripts (e.g., for OpenAI parsers or bank statement ingestion).
- **deluge_functions/** – packaged Deluge libraries shared by multiple workflows.
- **schedules/** – scheduled functions, cron jobs, and related configuration exports.
- **approvals/** – manual approval flow definitions, SLAs, and escalation rules.
- **tests/** – test cases, QA scripts, and sandbox validation evidence for the module.
- **deploy/** – CI/CD manifests, release notes, and environment-specific configuration files.
- **integrations/** (root) – adapters for external systems: OpenAI APIs, face recognition, Tally, banking feeds.
- **docs/** – operational runbooks, SOPs, change logs, architecture references, and release notes (linking back to the existing blueprint, ERDs, and data models).
- **tools/** – helper scripts for migrations, QA automation, and batch utilities maintained outside Creator.

## 4. Workflow for Updating Artefacts

1. **Create a feature branch** aligned with the module change (`feature/purchase-1234`) or a hotfix branch (`hotfix/invoice-rounding`) for urgent fixes.
2. **Export Creator artefacts** (forms, workflows, reports, pages, automations) and place them in the relevant module folders.
3. **Capture test evidence** under `tests/` and document assumptions in `docs/change_logs/`.
4. **Update documentation** (e.g., data models, ERDs, release notes) if the change modifies schema or process logic.
5. **Commit and push** the artefacts alongside supporting notes, then open a pull request targeting `env/dev` or `main` based on the release path.
6. **Run the setup script** with `--force` when structure resets are required (e.g., repo bootstrap, major reorganisation) or `--modules` for incremental pilots.

## 5. Next Steps

- Add module-specific README files that describe naming conventions for forms, workflows, and scripts.
- Integrate the scaffolding script with CI to validate required directories exist before merges.
- Capture environment-specific secrets in a secure vault and reference them in `deploy/environments/*` documentation rather than storing plain text in the repository.
