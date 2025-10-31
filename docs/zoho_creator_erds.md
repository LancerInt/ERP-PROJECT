# Zoho Creator ERP ERD Library

These entity-relationship diagrams visualise major data domains. Use them with the data model tables to validate lookups, subforms, and automation logic during implementation.

## 1. Core Masters
```mermaid
erDiagram
    COMPANY ||--o{ WAREHOUSE : owns
    WAREHOUSE ||--o{ GODOWN : contains
    COMPANY ||--o{ PRICE_LIST : publishes
    CUSTOMER ||--o{ PRICE_LIST : uses
    COMPANY ||--o{ VENDOR : registers
    COMPANY ||--o{ CUSTOMER : serves
    WAREHOUSE ||--o{ MACHINE : hosts
    PRODUCT ||--o{ TEMPLATE_LIBRARY : configures
    PRODUCT ||--o{ QC_PARAMETER : requires
    ROLE_DEFINITION ||--o{ USER_ROLE : assigned
    USER_ROLE }o--|| STAKEHOLDER_USER : maps
    STAKEHOLDER_USER }o--|| EMPLOYEE : optional_link
    SERVICE_CATALOG ||--o{ PRODUCT : classifies
    TAX_MASTER ||--o{ PRICE_LIST : references
```

## 2. Purchase & Inbound Logistics
```mermaid
erDiagram
    WAREHOUSE ||--o{ PURCHASE_REQUEST : raises
    PURCHASE_REQUEST ||--o{ PR_LINE : details
    PURCHASE_REQUEST ||--o{ RFQ_HEADER : triggers
    RFQ_HEADER ||--o{ QUOTE_RESPONSE : collects
    QUOTE_RESPONSE }o--|| VENDOR : quoted_by
    RFQ_HEADER ||--|| QUOTE_EVALUATION : summarises
    QUOTE_EVALUATION ||--|| PURCHASE_ORDER : approves
    PURCHASE_ORDER ||--o{ PO_LINE : contains
    PURCHASE_ORDER ||--o{ PO_ETA_UPDATE : tracks
    PURCHASE_ORDER }o--|| VENDOR : issued_to
    PURCHASE_ORDER ||--o{ RECEIPT_ADVICE : fulfilled_by
    RECEIPT_ADVICE ||--o{ RA_LINE : captures
    RECEIPT_ADVICE }o--|| WAREHOUSE : received_at
    RECEIPT_ADVICE ||--o{ FREIGHT_ADVICE : generates
    FREIGHT_ADVICE }o--|| TRANSPORTER : handled_by
    RECEIPT_ADVICE ||--o{ QC_REQUEST : initiates
    RECEIPT_ADVICE ||--o{ INVENTORY_LEDGER : posts
    RECEIPT_ADVICE ||--o{ VENDOR_PAYMENT_ADVICE : payable
```

- **PO_LINE** holds extra and agent commission attributes so landed cost flows through receipts and finance.
- **FREIGHT_ADVICE** nodes encapsulate shipment quantity/UOM and destination metadata for cost-per-unit analysis while remaining a Freight Coordinator → Finance Manager approval.

## 3. Sales, Dispatch & Outbound Freight
```mermaid
erDiagram
    CUSTOMER ||--o{ CUSTOMER_PO_UPLOAD : submits
    CUSTOMER_PO_UPLOAD ||--|| SALES_ORDER : drafts
    SALES_ORDER ||--o{ SO_LINE : contains
    SALES_ORDER }o--|| PRICE_LIST : priced_by
    SALES_ORDER }o--|| WAREHOUSE : served_by
    SALES_ORDER ||--o{ DISPATCH_CHALLAN : issues
    DISPATCH_CHALLAN ||--o{ DC_LINE : aggregates
    DISPATCH_CHALLAN ||--|| SALES_INVOICE_CHECK : validates
    SALES_INVOICE_CHECK ||--o{ RECEIVABLE_LEDGER : records
    DISPATCH_CHALLAN ||--o{ FREIGHT_ADVICE : triggers
    FREIGHT_ADVICE }o--|| TRANSPORTER : handled_by
    FREIGHT_ADVICE ||--o{ FREIGHT_LEDGER : posts
    RECEIVABLE_LEDGER ||--o{ BANK_RECON_EXCEPTION : unmatched
```

- Outbound FREIGHT_ADVICE inherits the same quantity/UOM/destination capture so per-destination cost KPIs are available for customer shipments with Freight Coordinator initiation and Finance Manager approval.

## 4. Production, Inventory & QC
```mermaid
erDiagram
    TEMPLATE_LIBRARY ||--o{ BOM_REQUEST : referenced_by
    BOM_REQUEST ||--o{ MATERIAL_SHORTFALL : flags
    BOM_REQUEST ||--|| WORK_ORDER : feeds
    WORK_ORDER ||--o{ MATERIAL_ISSUE : consumes
    WORK_ORDER ||--o{ PRODUCTION_OUTPUT : produces
    WORK_ORDER }o--|| SALES_ORDER : fulfils
    WORK_ORDER ||--o{ WAGE_VOUCHER : accrues
    PRODUCTION_OUTPUT ||--o{ INVENTORY_LEDGER : posts
    INVENTORY_LEDGER }o--|| WAREHOUSE : located_in
    INVENTORY_LEDGER }o--|| GODOWN : stored_in
    WORK_ORDER ||--o{ QC_REQUEST : submits
    QC_REQUEST ||--o{ QC_LAB_JOB : assigned
    QC_REQUEST ||--|| QC_FINAL_REPORT : concludes
    QC_FINAL_REPORT ||--o{ COUNTER_SAMPLE : stores
```

- WAGE_VOUCHER records originate from the Warehouse Coordinator (Office) and escalate to the Finance Manager for approval, meeting wage governance requirements.

## 5. Job Work, Transfers & Adjustments
```mermaid
erDiagram
    JOB_WORK_TEMPLATE ||--o{ JOB_WORK_ORDER : instantiates
    JOB_WORK_ORDER }o--|| WAREHOUSE : raised_by
    JOB_WORK_ORDER }o--|| VENDOR : processed_by
    JOB_WORK_ORDER ||--o{ JOB_WORK_DC : dispatches
    JOB_WORK_DC ||--o{ JOB_WORK_RECEIPT : returns
    JOB_WORK_RECEIPT ||--o{ QC_REQUEST : triggers
    JOB_WORK_RECEIPT ||--o{ INVENTORY_LEDGER : updates
    WAREHOUSE ||--o{ STOCK_TRANSFER_DC : sends
    STOCK_TRANSFER_DC ||--o{ STOCK_TRANSFER_RECEIPT : closes
    STOCK_TRANSFER_DC ||--o{ FREIGHT_ADVICE : draft
    STOCK_TRANSFER_RECEIPT ||--o{ INVENTORY_LEDGER : updates
    WAREHOUSE ||--o{ WAREHOUSE_SHIFTING : internal_moves
    WAREHOUSE_SHIFTING ||--o{ FREIGHT_ADVICE : optional
    WAREHOUSE ||--o{ STOCK_ADJUSTMENT : records
    STOCK_ADJUSTMENT ||--o{ INVENTORY_LEDGER : impacts
```

- Transfer-related FREIGHT_ADVICE entries mirror the Freight Coordinator → Finance Manager approval path and capture shipment quantity/UOM for per-destination transfer costing.

## 6. Finance & Attendance
```mermaid
erDiagram
    VENDOR_PAYMENT_ADVICE ||--o{ VENDOR_LEDGER : posts
    FREIGHT_ADVICE ||--o{ FREIGHT_LEDGER : posts
    WAGE_VOUCHER ||--o{ WAGE_LEDGER : posts
    SALES_INVOICE_CHECK ||--o{ CUSTOMER_LEDGER : posts
    CUSTOMER_LEDGER ||--o{ PAYMENT_REMINDER : schedules
    BANK_STATEMENT_UPLOAD ||--o{ BANK_RECON_ENTRY : extracts
    BANK_RECON_ENTRY ||--o{ BANK_RECON_EXCEPTION : unresolved
    ATTENDANCE_CAPTURE ||--o{ OVERTIME_REQUEST : references
    OVERTIME_REQUEST ||--o{ WAGE_VOUCHER : generates
    ATTENDANCE_CAPTURE ||--o{ PAYROLL_EXPORT : summarises
    LEAVE_REQUEST }o--|| ATTENDANCE_CAPTURE : adjusts
```

Each ERD abstracts Creator forms into conceptual entities; adapt notation as needed for Creator's lookup and subform schema during build.
