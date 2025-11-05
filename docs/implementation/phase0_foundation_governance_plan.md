# Phase 0 – Foundation & Governance (Weeks 0–4)

This playbook provides detailed implementation steps, owners, inputs, and deliverables for the foundation sprint. Execute the
activities in weekly waves while maintaining daily stand-ups between Head Office IT Admin, Process Owners, and Implementation
Partner.

## Week 0: Mobilisation & Environment Readiness

### 1. Project Mobilisation
- **Owner**: IT Admin & Office Manager
- **Steps**:
  1. Confirm steering committee members and escalation matrix (Office Manager, Finance Manager, Purchase Manager, Warehouse
     Coordinator at Office, IT Admin).
  2. Finalise project charter, scope guardrails, and success criteria aligned with Blueprint decisions.
  3. Schedule recurring ceremonies: weekly steering review, daily stand-up, fortnightly stakeholder demos.
- **Deliverables**: Approved charter, communication plan, stakeholder roster.

### 2. Zoho Creator Environment Setup
- **Owner**: IT Admin
- **Steps**:
  1. Request/provision Creator environment with production and sandbox workspaces.
  2. Configure Zoho Portal user groups for Head Office, warehouse clusters, and implementation team.
  3. Establish naming conventions for apps, forms, reports, and workflows (prefix by module, e.g., `PUR_PR_Request`).
  4. Configure environment-wide settings: time zone, currency, backup schedule, audit trail retention.
- **Deliverables**: Active Creator environment, admin checklist, documented naming standards.

### 3. Integration Access Preparation
- **Owner**: IT Admin with IT Security
- **Steps**:
  1. Generate OpenAI API credentials for PO parser and face recognition microservices; store in secrets vault.
  2. Set up secure storage for bank statements (S3/Zoho WorkDrive) with daily upload automation folders.
  3. Document Tally export/import process, including voucher formats and GST/TDS/TCS configuration references.
  4. Validate network/firewall allowances for outbound API calls from Zoho Creator deluge functions.
- **Deliverables**: Credential inventory, integration design notes, connectivity validation report.

## Week 1: Master Data Framework

### 4. Master Data Templates Finalisation
- **Owner**: IT Admin & Warehouse Coordinator at Office
- **Steps**:
  1. Review `zoho_creator_data_models.md` and confirm field-level alignment for Company, Warehouse, Godown, Products,
     Services, Vendors, Customers, Transporters, Tax, and User Role mapping forms.
  2. Create CSV/XLSX templates for each master with validation rules, dropdown code lists, and sample records.
  3. Circulate templates for stakeholder sign-off; capture localisation requirements (GST numbers, address formats).
- **Deliverables**: Signed-off master templates, validation checklists.

### 5. Data Cleansing & Governance Policy
- **Owner**: Accounts Manager & Purchase Manager
- **Steps**:
  1. Assign data stewards per master (e.g., Purchase Coordinator for Vendors, Sales Coordinator for Customers).
  2. Define duplicate resolution rules, mandatory fields, and approval workflow for new entries.
  3. Document on-going maintenance cadence (monthly review) and escalation for data quality issues.
- **Deliverables**: Master data governance policy, steward assignments, quality metrics dashboard outline.

### 6. Initial Data Load (Pilot)
- **Owner**: IT Admin with Module Leads
- **Steps**:
  1. Collect cleansed datasets (minimum 5 records per master) to validate import scripts.
  2. Configure Creator forms/subforms per the field definitions; enable lookup relationships and unique constraints.
  3. Execute sandbox import using Creator import tools or Deluge scripts; log data validation errors.
  4. Review imported records with business owners; capture adjustments for production load in Phase 1.
- **Deliverables**: Populated sandbox masters, import runbook, issue tracker.

## Week 2: Security, Roles, and Sharing

### 7. Role Matrix Implementation
- **Owner**: IT Admin & HR Coordinator at Office
- **Steps**:
  1. Translate `zoho_creator_erp_structure.md` stakeholder hierarchy into Creator roles and permission sets.
  2. Configure profile-based access for Head Office vs warehouse stakeholders; include multi-role assignment support.
  3. Map Creator user groups to data sharing rules (warehouse-specific visibility for PRs, SOs, inventory records).
  4. Draft onboarding checklist for new users (role request, approval, provisioning, orientation).
- **Deliverables**: Role-permission matrix in Creator, onboarding SOP, sample user provisioning logs.

### 8. Template & Branding Console
- **Owner**: Office Manager & IT Admin
- **Steps**:
  1. Build admin console form for logo, letterhead, signature blocks, and document footer text.
  2. Configure Creator pages/widgets that reference the console values for POs, SOs, DCs, invoices, QC reports.
  3. Establish version control for templates with effective-dated activation.
- **Deliverables**: Admin console MVP, documented template override procedure.

### 9. Access Control Testing
- **Owner**: IT Admin with QA Lead
- **Steps**:
  1. Create test users for each stakeholder role (including dual-role combinations like Purchase Manager + Office Manager).
  2. Validate form/report access, record-level sharing, and restricted modules.
  3. Log defects in access matrix; obtain sign-off from module owners.
- **Deliverables**: Access test results, defect log, sign-off sheet.

## Week 3: Integration Foundations & Automation Skeletons

### 10. AI Parser & Face Recognition Proof of Concept
- **Owner**: IT Admin & Sales Coordinator
- **Steps**:
  1. Develop Deluge functions calling OpenAI APIs with mock payloads for PO parsing and attendance face matching.
  2. Validate response handling, error logging, and retry mechanisms.
  3. Define fallback manual review workflow for low-confidence responses.
- **Deliverables**: POC scripts, API usage guidelines, confidence threshold matrix.

### 11. Bank Statement & Tally Interfaces
- **Owner**: Finance Manager & Accounts Manager
- **Steps**:
  1. Build daily bank statement import routine (CSV/PDF parsing) and reconciliation staging tables.
  2. Prepare Tally export formats for vouchers (payment advice, wage payouts, freight invoices) and test sample export.
  3. Document reconciliation cadence and exception handling (ageing mismatches, missing entries).
- **Deliverables**: Reconciliation workflow diagram, sample import/export files, exception register template.

### 12. Notification & Reminder Framework
- **Owner**: IT Admin & Finance Manager
- **Steps**:
  1. Configure Creator schedules for ₹25,000 stock adjustment escalation and freight payment due reminders.
  2. Draft notification templates (email/in-app) aligned with branding console.
  3. Validate escalation path (Finance Manager → Office Manager) for overdue payables/receivables.
- **Deliverables**: Activated reminder schedules in sandbox, notification template library.

## Week 4: Change Management & Sign-off

### 13. Training Assets & Sandboxes
- **Owner**: Warehouse Coordinator at Office & HR Coordinator at Office
- **Steps**:
  1. Prepare walkthrough decks/videos for master data maintenance, security policies, integration usage.
  2. Provision sandbox copies for Purchase, Sales, Warehouse, QC, Finance training cohorts.
  3. Capture feedback and update FAQs within Creator help pages.
- **Deliverables**: Training content repository, feedback log, updated help articles.

### 14. Governance Operating Rhythm
- **Owner**: Steering Committee
- **Steps**:
  1. Review readiness checklist covering environment, masters, security, integrations, training.
  2. Approve decision log entries, risk register, and mitigation actions for handover to Phase 1 team.
  3. Freeze baseline configuration snapshots (export application package, master data backups).
- **Deliverables**: Signed readiness checklist, Phase 1 handover pack, archived configuration snapshot.

### 15. Retrospective & Backlog Grooming
- **Owner**: Implementation Partner & IT Admin
- **Steps**:
  1. Conduct Phase 0 retrospective capturing wins, pain points, and improvement actions.
  2. Prioritise backlog items required before Phase 1 (e.g., additional validation rules, integration refinements).
  3. Update roadmap timelines if adjustments are needed.
- **Deliverables**: Retrospective notes, prioritised backlog, updated roadmap.

---

**Success Criteria for Phase Exit**
- Core masters and security model validated in sandbox.
- Integration touchpoints (OpenAI, bank reconciliation, Tally export) demonstrated via POC.
- Governance cadence, training assets, and decision log approved by steering committee.
- Risks and dependencies documented with owners ahead of Phase 1 kickoff.
