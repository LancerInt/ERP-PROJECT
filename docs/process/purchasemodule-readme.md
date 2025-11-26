# Purchase Module Design & Use Cases

This document summarizes how the Purchase module is designed to satisfy the provided business requirements, from request initiation through payment and freight handling.

## Core Flow Overview
1. **Purchase Request (PR) initiation** – Warehouse Coordinator/Manager raises a PR for a warehouse. Visibility is restricted to stakeholders of that warehouse.
2. **One-step PR approval** – Purchase Coordinator/Manager approves, partially approves, or rejects the PR. Partial approvals capture approved quantities per line and justification.
3. **Single-click RFQ generation** – Approved PR lines can spawn RFQ/Quote Requests in one click. The RFQ inherits PR lines, specs, attachments (photos/spec sheets), and vendor shortlist; bypass is allowed per line when permitted by the Purchase Manager.
4. **Quote collection** – Vendors submit quotes with price, quantity, delivery time, product specs, freight terms, payment terms, and optional attachments.
5. **Quote Evaluation** – Dedicated page/log captures best-quote suggestion plus justification when a non-best quote is chosen. Approvals from Purchase Coordinator/Manager are recorded for audit.
6. **Purchase Order (PO) creation** – Once a quote is approved, a PO is auto-generated. POs support linkage to multiple PRs or a single RFQ and maintain revision tracking (Rev 1, Rev 2… with change notes).
7. **Receipt Advice & Intake** – Warehouse Coordinator scans vendor invoice to create a receipt advice that associates to one or more POs. Supports partial receipts (remaining balance tracked) and reports for pending/partially received POs.
8. **Quality Check (QC)** – Product-level QC routing set at product definition (Warehouse Coordinator vs QC Coordinator). QC outcomes trigger notifications to Office Manager, Purchase Manager, Purchase Coordinator, and can initiate credit notes.
9. **Freight & Wages** – Capture freight terms (Paid/To_Pay) per vendor/customer for local drayage and linehaul; include loading/unloading wages and optional freight discounts. Freight Coordinator initiates payable advice, Finance Manager approves.
10. **Payments & Ledger** – Finance Manager issues payment advice per vendor based on QC-passed receipts and vendor credit terms. Bank statement upload auto-matches payments. Age-wise vendor payable reporting is supported.

## Key Use Cases
- **PR creation & visibility**
  - Create PR scoped to a warehouse; only stakeholders for that warehouse can view.
  - Warehouse Manager/Coordinator views: (a) all requests for the warehouse, (b) approved but not received, (c) received in last 30 days, (d) rejected in last 30 days.
- **PR approval**
  - Approve, reject, or partially approve each line; capture approval notes and partial quantities.
- **RFQ/Quote request generation**
  - One-click generation from approved PR lines; attaches specs/photos; allows line-level bypass with Purchase Manager permission.
- **Quote submission**
  - Vendors provide price, quantity, delivery, specs, freight terms, payment terms, attachments; system tracks per-vendor responses.
- **Quote evaluation & audit**
  - Evaluate quotes, record best-price detection, justification for deviations, and approvals on a dedicated Quote Evaluation page; maintain audit log.
- **PO generation & revisions**
  - Auto-create PO from approved quote; support multiple PR linkage and RFQ linkage; maintain revision numbers with change summaries.
- **Receipt advice & partial receipts**
  - Create receipt advice by scanning invoice; associate with multiple POs; handle partial dispatches and track remaining quantities; report pending POs.
- **Quality check routing**
  - Route QC to Warehouse Coordinator or QC Coordinator per product setup; record pass/fail, defects, and notifications; enable credit note initiation.
- **Freight handling**
  - Store freight terms (Paid/To_Pay) for local drayage and linehaul; capture loading/unloading wages; allow freight discount entry; produce freight payable advice and approvals.
- **Payment processing & reconciliation**
  - Generate payment advice based on QC-cleared receipts and credit terms; upload bank statements to auto-match vendor payments; produce age-wise payables.

## RFQ Single-Click Generation Approach
- **Trigger point**: After PR approval, the UI presents a “Generate RFQ” action on the PR detail view.
- **Pre-population**: Selected PR lines, specs, photos, and vendor shortlist are copied into an RFQ draft; line-level bypass flags are honored.
- **Workflow**: Purchase Coordinator reviews/edit the draft and sends RFQ to vendors. Vendor responses populate the Quote records automatically.
- **Traceability**: Each RFQ and subsequent quotes retain back-links to the originating PR lines for reporting and audit.

## Compliance & Reporting
- **Pending PO report** for partial/undelivered quantities.
- **Age-wise vendor payables** based on receipt and payment terms.
- **GST handling** – Track GST per company; keep tax separate from product price for variance checks.
- **Document templates** – Provide packing list, commercial invoice, and e-way bill templates for downstream logistics and compliance.
