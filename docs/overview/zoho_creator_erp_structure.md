# ERP Structure and Hierarchy

This document maps the enterprise structure, governance hierarchy, and master data ownership that underpin the Zoho Creator ERP implementation. Use it to align role provisioning, data sharing rules, and reporting scopes across Head Office (HO) and warehouse teams.

## 1. Enterprise Topology

| Layer | Description | Key Entities |
| --- | --- | --- |
| Head Office (HO) | Central authority overseeing all companies and warehouses. Houses strategic roles, finance, purchase, sales, QC, IT, and HR leadership. | Companies, HO Departments, Corporate Staff |
| Companies | Legal entities for purchase, sales, accounts, and finance transactions. Stock is consolidated at warehouse level irrespective of owning company. | Company master, GST/TDS/TCS registrations, bank accounts |
| Warehouses / Plants | Operational units with independent stock, production, QC, attendance, and petty cash. Each warehouse may contain multiple godowns. | Warehouse master, Godown master, Machinery, Local HR |
| Godowns | Physical storage zones within a warehouse. Batch-level inventory is tracked against godowns. | Godown master, Batch inventory |
| External Partners | Vendors, customers, transporters, job work vendors, contractors. | Partner masters, freight and payment terms |

## 2. Stakeholder Hierarchy and Role Bundles

Stakeholders can hold multiple roles. The following hierarchy clarifies reporting lines and scope of control.

### 2.1 Head Office Roles

- **Office Manager** – Final authority on operational approvals, sales invoice validation, stock adjustments, escalations.
- **Purchase Manager** – Oversees procurement strategy, quote approvals, vendor negotiations, PO revisions.
- **Purchase Coordinator** – Manages RFQs, quote evaluation, PO drafting, ETA updates, coordinates with warehouses.
- **Sales Manager** – Approves sales orders, dispatch plans, customer pricing exceptions.
- **Sales Coordinator** – Operates day-to-day SO creation, dispatch challan initiation, freight details capture.
- **Finance Manager** – Controls payment advice, ledger reconciliation, bank uploads, freight settlements, voucher approvals.
- **Accounts Manager** – Issues credit/debit notes, ensures statutory compliance, manages ageing reports.
- **Freight Coordinator** – Creates freight advisories (inbound/outbound), tracks payment schedules, monitors transporter performance.
- **QC Manager / QC Coordinator / QC Analyst** – Define QC templates, assign lab jobs, consolidate reports, manage counter samples.
- **Warehouse Coordinator (Office)** – Liaison between HO and multiple warehouses for stock, freight, wage approvals, and attendance oversight.
- **HR Coordinator (Office)** – Maintains enterprise staff master, approves warehouse HR actions, runs attendance analytics.
- **IT Admin** – Owns master data creation (roles, services, templates), branding assets, automation thresholds, integration credentials.

### 2.2 Warehouse Roles

Each warehouse holds a local command chain.

- **Warehouse Manager** – Responsible for production planning, stock approvals, QC routing, wage attestations.
- **Warehouse Coordinator** – Handles daily stock movements, receipt advice, issue slips, freight data capture, local reporting.
- **Warehouse Supervisors** – Execute floor operations, raise QC and stock adjustment requests, supervise godown movements.
- **Warehouse HR Coordinator** – Manages local staff attendance, shift rosters, overtime proposals, subject to HO approval.
- **Warehouse Employees/Staff** – Operational workforce recorded in attendance; may not have ERP login access.

### 2.3 Cross-Site Responsibilities

- **Trusted Petty Cash Custodian** (per warehouse) – Draws advances from HO finance, settles cash vouchers for local expenses.
- **Template Owners** – Assigned per warehouse for production templates and job work instructions to maintain localized variations.
- **Shared Service Teams** – QC, IT, HR at HO may service multiple warehouses with role-based sharing controls.

## 3. Master Data Ownership and Governance

| Master | Primary Owner | Notes |
| --- | --- | --- |
| Company, Warehouse, Godown | IT Admin | Warehouses linked to companies; godowns tied to warehouses. |
| Stakeholder Roles & User Assignments | IT Admin | Multi-role assignments, Creator portal provisioning, periodic audits. |
| Products & Services | IT Admin with functional delegates | Categorised into goods/services with subtypes; includes unit conversions, QC requirement flags. |
| Vendors, Customers, Contractors, Transporters | Purchase/Sales/Finance Managers | Shared partner master with company-specific tax/credit terms. |
| Templates (Production, QC, Job Work) | Warehouse Manager & QC Manager | Version controlled with approval workflows. |
| Tax Masters (GST, TDS, TCS) | Finance Manager | Maintain rates per company; referenced across transactions. |
| Price Lists | Sales Manager | Customer-specific, location-based, multi-version support. |
| Freight Matrices | Freight Coordinator | Defines drayage vs linehaul terms, discounts, direction flags. |
| Attendance Shifts & Geo-Fences | HR Coordinator (Office) | Coordinates with Warehouse HR for roster approvals. |

## 4. Data Visibility Rules

- **Warehouse Scoped Access** – Warehouse Managers, Coordinators, Supervisors, and HR Coordinators see records tagged to their warehouse; Office stakeholders see multi-warehouse data per role.
- **Company Scoped Financials** – Finance and Accounts roles filter ledgers, GST/TDS/TCS reports by company while operational stock remains warehouse-centric.
- **Document Attachments** – Source documents (POs, invoices, QC reports) inherit parent record permissions; sensitive QC data can be limited to QC roles and designated managers.
- **Petty Cash** – Custodian sees own float ledger; Finance and Warehouse Coordinator (Office) monitor all.

## 5. Reporting Hierarchy

- **Executive Dashboards** – Office Manager, Finance Manager, Purchase Manager access consolidated KPIs across companies/warehouses.
- **Warehouse Dashboards** – Warehouse leadership monitors stock, production, QC status, wage commitments, freight outstanding.
- **Role-Specific Reports** – QC labs, HR, Freight Coordinator, Accounts each receive tailored reports with escalations (e.g., overdue freight, attendance anomalies).

## 6. Governance Cadence

- Weekly cross-functional sync between HO leads (Purchase, Sales, Production, QC, Finance) to review inter-warehouse dependencies.
- Monthly IT Admin audit of role assignments, template revisions, and automation thresholds.
- Quarterly compliance review for GST/TDS/TCS accuracy and bank reconciliation efficacy.

This structure document should be revisited when adding new warehouses, expanding services, or evolving role responsibilities.
