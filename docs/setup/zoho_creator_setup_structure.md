# Zoho Creator ERP Repository Structure Guidelines

This guide documents the recommended folder hierarchy and branching model for organising Zoho Creator exports, Deluge assets, documentation, and automation artefacts. Use it as a checklist when preparing a fresh repository or reviewing an existing workspace.

## 1. Preparing the Directory Layout

Although the original scaffolding script has been retired, the structure it produced remains the standard. Create the directories manually (or via your own automation) before exporting assets from Creator to keep the repository consistent across environments.

### 1.1 Core Steps

1. Create an `apps/` directory with module-specific subfolders for **Purchase, Sales, Production, QC, Logistics, Finance, Attendance**, and any additional modules you introduce (e.g., HR, Maintenance).
2. Inside each module folder, add the following subdirectories to segregate artefacts:
   - `forms/`, `workflows/`, `reports/`, `pages/`, `automations/`, `scripts/`, `integrations/`, `deluge_functions/`, `schedules/`, `approvals/`, `tests/`.
3. Add `apps/shared/` to store cross-module masters, templates, dashboards, reusable Deluge libraries, and Creator pages.
4. Create top-level folders for `integrations/` (external connectors, AI scripts, bank automation), `tools/` (helper scripts and utilities), and `docs/` (architecture, release notes, runbooks, governance material).
5. Seed `deploy/dev`, `deploy/uat`, and `deploy/prod` directories for environment-specific configuration files, along with a `pipelines/` folder for CI definitions.
6. Drop `.gitkeep` files into empty folders so Git can track them until exports populate the directories.

### 1.2 Tailoring the Layout

- Extend each module with extra folders (for example, `blueprints/` or `serverless/`) when Creator introduces new artefact types.
- Mirror the hierarchy in external workspaces (such as vendor collaboration areas) to simplify comparisons and code reviews.
- Maintain a short README in every top-level directory to describe its intended contents and contribution guidelines.

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

Once you apply the directory layout steps, the repository should resemble the structure below:

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
└── render_data_models_pdf.sh
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
6. **Automate directory audits** with lightweight shell scripts or CI checks to ensure required folders stay present after merges.

## 5. Next Steps

- Add module-specific README files that describe naming conventions for forms, workflows, and scripts.
- Create a simple CI check (for example, a shell script) that validates the expected directory structure before merges.
- Capture environment-specific secrets in a secure vault and reference them in `deploy/environments/*` documentation rather than storing plain text in the repository.
