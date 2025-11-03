# Phase 1 – Procure-to-Pay & Inventory Control (Weeks 5–12)

This playbook outlines the detailed implementation tasks, owners, inputs, and deliverables for delivering the procure-to-pay (P2P) and inventory control scope after Phase 0 sign-off. Activities are sequenced by week but can be adjusted to match resource availability. Maintain daily stand-ups between Purchase, Warehouse, Finance, and IT Admin leads to monitor progress and unblock dependencies.

## Week 5: Phase Kick-off & Detailed Design Alignment

### 1. Phase Mobilisation & Backlog Refinement
- **Owner**: Office Manager & IT Admin
- **Steps**:
  1. Review Phase 0 exit criteria, confirm sandbox readiness, and baseline configurations to be copied into Phase 1 branch/environment.
  2. Decompose procure-to-pay user stories into sprint backlog items (PR approvals, RFQ, PO, receipt, freight, wage vouchers, inventory ledger, finance hooks).
  3. Assign module owners and confirm acceptance criteria per feature (including partial approvals, ETA updates, and cost-per-unit freight reporting).
- **Deliverables**: Approved Phase 1 backlog, RACI for procure-to-pay activities, sprint calendar.

### 2. Process Walkthrough & Sign-off
- **Owner**: Purchase Manager & Warehouse Coordinator at Office
- **Steps**:
  1. Conduct joint workshops with Warehouse Managers, Finance Manager, and Freight Coordinator to validate process swimlanes (Purchase Request to Payment Advice, Machine Spares Issue, Petty Cash tie-ins).
  2. Finalise exception handling rules: skip-RFQ approvals, partial PO receipts, QC failure escalation, freight discount capture, and cost-per-unit reporting dimensions (per shipment and per destination).
  3. Capture sign-off in decision log and update SOP drafts for subsequent training.
- **Deliverables**: Updated SOPs, signed process walkthrough deck, exception matrix.

## Week 6: Purchase Requests, RFQ, and Quote Evaluation

### 3. Purchase Request Form & Workflow Build
- **Owner**: IT Admin & Purchase Coordinator
- **Steps**:
  1. Configure Purchase Request form per `zoho_creator_data_models.md`, including warehouse/godown lookups, attachment requirements, and visibility rules (warehouse-specific sharing).
  2. Implement approval workflow (Warehouse Coordinator at Office / Purchase roles) with partial approval logic and audit trail for edits.
  3. Create reports: Pending PRs by warehouse, Rejected PRs (30 days), Approved-but-not-received list, visible only to relevant stakeholders.
- **Deliverables**: PR form & workflow in sandbox, warehouse-filtered reports, test cases.

### 4. RFQ & Quote Capture Automation
- **Owner**: Purchase Coordinator & IT Admin
- **Steps**:
  1. Build RFQ form with vendor subform, AI attachment placeholders, and skip-RFQ toggle requiring Purchase Manager approval.
  2. Configure automated email template to vendors including specification attachments and expected response fields.
  3. Create Quote Response subform and Quote Evaluation form with comparative tables, reason capture for non-lowest selections, and approval routing to Purchase Manager.
- **Deliverables**: RFQ/Quote forms, outgoing communication template, evaluation workflow, sample vendor comparison report.

## Week 7: Purchase Orders & Anticipated Arrival Tracking

### 5. Purchase Order Configuration
- **Owner**: Purchase Manager & IT Admin
- **Steps**:
  1. Implement PO form with revision history, linkage to multiple PRs/RFQs, and product lines capturing rate, taxes, extra commission, agent commission, freight/loading estimates, and packing material.
  2. Enable Anticipated Arrival Date updates editable by Warehouse Coordinator at Office / Purchase Coordinator; log changes with timestamp and user.
  3. Build PO status board highlighting open, partially received, and overdue POs.
- **Deliverables**: PO form with revisioning, anticipated arrival update audit log, status dashboard widgets.

### 6. Purchase Order Communication & Document Templates
- **Owner**: Office Manager & IT Admin
- **Steps**:
  1. Connect PO form to branding console from Phase 0 to populate logos, footers, and terms.
  2. Configure PDF/email templates, ensuring freight estimates, commissions, and taxes display separately from product price for compliance.
  3. Set up PO distribution workflow (auto-email to vendor, internal notifications to Warehouse Coordinator and Finance Manager).
- **Deliverables**: PO PDF template, email workflow, communication checklist.

## Week 8: Receipt Advice, Packing Material Capture, and QC Integration

### 7. Receipt Advice & Stock Intake
- **Owner**: Warehouse Coordinator & IT Admin
- **Steps**:
  1. Build Receipt Advice form linking to one or more POs, capturing vendor invoice scan, batch numbers, godown placement, packing material captured, extra/agent commission actuals, freight terms, and partial receipt details.
  2. Automate stock creation entries per product, applying unit conversions (kg ↔ litre via specific gravity) and godown-level inventory updates.
  3. Provide dashboard cards: Pending Receipts, Partially Received POs, Packing Material additions.
- **Deliverables**: Receipt Advice form & automation, inventory update script, receipt monitoring dashboard.

### 8. QC Triggering & Feedback Loop
- **Owner**: QC Coordinator & Warehouse Manager
- **Steps**:
  1. Configure workflow to auto-create inbound QC Request when Receipt Advice flags QC Required, routing to appropriate QC role (Warehouse Coordinator vs QC Coordinator).
  2. Ensure QC outcomes (Pass/Fail/Rework) update receipt status, notify Purchase Manager, and block payment advice until pass.
  3. Capture QC attachments (photos, reports) and integrate with counter-sample register as needed.
- **Deliverables**: QC trigger workflow, notification templates, QC feedback report.

## Week 9: Freight & Wage Advice Automation

### 9. Freight Advice Drafting & Approval
- **Owner**: Freight Coordinator & Finance Manager
- **Steps**:
  1. Reuse Freight Advice form with Direction = Inbound; pre-populate from Receipt Advice including transporter, freight types (Local Drayage/Linehaul), discounts, shipment quantity, UOM, destination state, and auto-calculated cost per unit quantity.
  2. Implement workflow: Freight Coordinator drafts advice → Finance Manager approval → ledger entry + payment schedule generation.
  3. Build reports calculating cost per unit per shipment and aggregated by destination (e.g., cost per metric ton to Maharashtra) using Creator pivot/report builder.
- **Deliverables**: Freight advice workflow, approval audit trail, cost-per-unit reports and destination analytics.

### 10. Wage Advice for Loading/Unloading & Production Support
- **Owner**: Warehouse Coordinator at Office & Finance Manager
- **Steps**:
  1. Configure wage advice form for loading/unloading and production wages initiated by Warehouse Coordinator at Office with TDS handling and weekly payout scheduling.
  2. Implement approval workflow: Warehouse Coordinator at Office submits → Finance Manager approves → Payment Advice queue.
  3. Link petty cash balances for warehouses to cash settlements when applicable and update weekly wage ledger reports.
- **Deliverables**: Wage advice workflow, petty cash linkage, weekly wage summary report.

## Week 10: Inventory Ledger, Machine Spares, and Issue Tracking

### 11. Inventory Ledger & Stock Views
- **Owner**: Warehouse Manager & IT Admin
- **Steps**:
  1. Implement inventory ledger form/subform capturing transactions (Receipt, Issue, Production Consumption, Stock Transfer, Adjustment) with FIFO costing and batch tracking.
  2. Build godown-wise stock reports, batch traceability (find batch by godown and vice versa), and machine spare stock availability dashboards.
  3. Configure scheduled reconciliation to highlight discrepancies between ledger and physical counts for early warning.
- **Deliverables**: Inventory ledger configuration, traceability reports, discrepancy alert automation.

### 12. Machine Spares Issue & Approvals
- **Owner**: Warehouse Coordinator & Warehouse Manager
- **Steps**:
  1. Create Machine Spares Issue form initiated by Warehouse Coordinator with approval step for Warehouse Manager, referencing godown-level machinery.
  2. Automate stock decrement for spares upon approval and log cost to maintenance ledger.
  3. Provide issue register and outstanding approval report to monitor turnaround times.
- **Deliverables**: Machine spares issue workflow, maintenance cost tracking report, approval SLA dashboard.

## Week 11: Finance Hooks & Reconciliation

### 13. Payment Advice & Vendor Ageing
- **Owner**: Finance Manager & Accounts Manager
- **Steps**:
  1. Configure Payment Advice form referencing Receipt Advice, QC status, freight and wage vouchers, and applying GST/TDS/TCS rules with separate tax lines.
  2. Build vendor ageing reports with filters by company, warehouse, and ageing buckets; integrate reminders for payables nearing due dates.
  3. Ensure approval workflow: Finance Manager drafts → Office Manager final authorization per finance governance plan.
- **Deliverables**: Payment advice automation, vendor ageing dashboard, approval logs.

### 14. Bank Reconciliation & Statement Automation
- **Owner**: Finance Manager & IT Admin
- **Steps**:
  1. Extend Phase 0 bank import routines to map payments related to P2P documents; auto-match against payment advice and freight/wage schedules.
  2. Configure daily reconciliation task with exception queue for unmatched transactions, including ability to attach bank statement proof.
  3. Produce reconciliation summary report and escalate unmatched items older than two days to Finance Manager and Office Manager.
- **Deliverables**: Enhanced bank reconciliation script, exception management dashboard, escalation workflow.

## Week 12: UAT, Training, and Go-Live Readiness

### 15. Integrated UAT Cycle
- **Owner**: QA Lead & Purchase Manager
- **Steps**:
  1. Develop UAT scripts covering end-to-end scenarios (PR → RFQ → PO → Receipt → QC → Freight/Wage Advice → Payment Advice → Bank reconciliation, including partial receipts and QC failure cases).
  2. Conduct warehouse-specific UAT sessions ensuring visibility restrictions work; capture defects and retest after fixes.
  3. Validate cost-per-unit freight reports and inventory traceability outputs against expected calculations.
- **Deliverables**: Signed UAT results, defect tracker, acceptance certificates from module owners.

### 16. Training & Change Enablement
- **Owner**: Change Manager & Warehouse Coordinator at Office
- **Steps**:
  1. Tailor training materials for Warehouse Managers, Coordinators, Freight Coordinator, Finance, and Purchase teams with role-based quick reference guides.
  2. Run train-the-trainer sessions emphasising new fields (extra commission, agent commission, cost-per-unit freight) and approval responsibilities.
  3. Update Creator in-app guidance, FAQs, and help videos to reflect Phase 1 processes.
- **Deliverables**: Training attendance logs, updated help centre, feedback incorporation list.

### 17. Cutover Planning & Deployment
- **Owner**: IT Admin & Finance Manager
- **Steps**:
  1. Prepare cutover checklist: data migration for open POs, outstanding PRs, opening inventory balances per godown, and pending freight/wage vouchers.
  2. Schedule go-live window, freeze sandbox changes, and deploy tested application package to production workspace.
  3. Establish hypercare support rota for first four weeks post go-live with defined SLAs for issue resolution.
- **Deliverables**: Cutover plan, production deployment sign-off, hypercare schedule.

---

**Success Criteria for Phase Exit**
- Purchase request to payment advice lifecycle executed successfully in production with real data.
- Inventory ledger reflects batch, godown, and machine spare movements with reconciled balances.
- Freight and wage advice workflows operational with Finance Manager approvals and cost-per-unit reporting.
- Daily bank reconciliation auto-matches P2P payments, with exceptions under control.
- Stakeholders trained and adoption metrics (usage logs, turnaround times) tracked for continuous improvement.
