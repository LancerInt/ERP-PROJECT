# Cross-Module ER Diagrams

This library focuses on the data connections that span multiple ERP modules, complementing the domain-specific ERDs. Use these diagrams to understand how records interact across purchase, sales, production, QC, logistics, finance, and attendance components.

> **Notation**: Mermaid ER diagrams are oriented with master data on the left and transactional entities on the right. Crow's feet (`||--o{`) denote one-to-many relationships, while double bars (`||`) indicate mandatory participation.

## 1. Master Data Hub

```mermaid
erDiagram
    COMPANY ||--o{ WAREHOUSE : operates
    WAREHOUSE ||--o{ GODOWN : contains
    WAREHOUSE ||--o{ MACHINERY : houses
    COMPANY ||--o{ BANK_ACCOUNT : uses
    COMPANY ||--o{ TAX_REGISTRATION : maintains
    PRODUCT ||--o{ PRODUCT_VARIANT : defines
    PRODUCT ||--o{ UNIT_CONVERSION : supports
    SERVICE ||--o{ SERVICE_RATE_CARD : stores
    STAKEHOLDER ||--o{ ROLE_ASSIGNMENT : holds
    ROLE ||--o{ ROLE_ASSIGNMENT : linked
    PARTNER ||--o{ CONTACT_PERSON : has
    PARTNER }o--o{ COMPANY : transacts
```

## 2. Purchase ↔ Inventory ↔ Finance

```mermaid
erDiagram
    WAREHOUSE ||--o{ PURCHASE_REQUEST : raises
    PURCHASE_REQUEST ||--o{ PR_LINE : includes
    PURCHASE_REQUEST ||--o{ ETA_UPDATE : tracks
    PR_LINE }o--|| PRODUCT : references
    PURCHASE_REQUEST }o--o{ RFQ : derives
    RFQ ||--o{ QUOTE : receives
    QUOTE ||--|| PARTNER : from
    QUOTE ||--o{ QUOTE_EVAL : documented
    QUOTE ||--o{ PURCHASE_ORDER : awards
    PURCHASE_ORDER ||--o{ PO_LINE : contains
    PO_LINE }o--|| PRODUCT : references
    PURCHASE_ORDER ||--o{ FREIGHT_ADVICE : triggers
    RECEIPT_ADVICE ||--o{ RA_LINE : lists
    RECEIPT_ADVICE }o--|| PURCHASE_ORDER : reconciles
    RA_LINE }o--|| PRODUCT_BATCH : updates
    PRODUCT_BATCH }o--|| GODOWN : stored_in
    PRODUCT_BATCH }o--|| INVENTORY_LEDGER : posts
    QUALITY_LOT }o--|| RECEIPT_ADVICE : samples
    QUALITY_LOT ||--o{ QC_RESULT : records
    PAYMENT_ADVICE }o--|| RECEIPT_ADVICE : settles
    PAYMENT_ADVICE }o--|| BANK_TRANSACTION : matched
    BANK_STATEMENT ||--o{ BANK_TRANSACTION : provides
    FREIGHT_ADVICE }o--|| TRANSPORTER : pays
    FREIGHT_ADVICE ||--o{ PAYMENT_SCHEDULE : splits
    PAYMENT_SCHEDULE }o--|| PAYMENT_ADVICE : funded_by
```

- **PO_LINE** carries `Extra Commission` and `Agent Commission` fields so landed cost flows into receipt advice, inventory valuation, and vendor settlement.
- **FREIGHT_ADVICE** persists shipment quantity, UOM, and destination state for cost-per-unit analytics while remaining a Freight Coordinator → Finance Manager approval flow.

## 3. Sales ↔ Logistics ↔ Finance

```mermaid
erDiagram
    CUSTOMER_PO ||--o{ CUSTOMER_PO_LINE : details
    CUSTOMER_PO }o--|| CUSTOMER : belongs
    CUSTOMER_PO ||--o{ SALES_ORDER : generates
    SALES_ORDER ||--o{ SO_LINE : contains
    SO_LINE }o--|| PRODUCT : references
    SALES_ORDER }o--|| PRICE_LIST : validates
    SALES_ORDER ||--o{ DISPATCH_CHALLAN : fulfils
    DISPATCH_CHALLAN ||--o{ DC_LINE : includes
    DC_LINE }o--|| PRODUCT_BATCH : ships
    DISPATCH_CHALLAN ||--o{ FREIGHT_ADVICE : raises
    DISPATCH_CHALLAN ||--o{ SALES_INVOICE : posts
    SALES_INVOICE ||--o{ INVOICE_LINE : details
    SALES_INVOICE }o--|| BANK_TRANSACTION : reconciles
    SALES_INVOICE ||--o{ RECEIVABLE : tracks
    RECEIVABLE }o--|| PAYMENT_COLLECTION : closes
    CREDIT_NOTE }o--|| SALES_INVOICE : adjusts
    SALES_RETURN ||--|| SALES_INVOICE : references
    SALES_RETURN ||--o{ RETURN_LINE : captures
    RETURN_LINE }o--|| PRODUCT_BATCH : restocks
```

- Outbound **FREIGHT_ADVICE** shares the same quantity/UOM/destination metrics, ensuring cost-per-unit reporting by customer geography while Freight Coordinator drafts and Finance Manager approves.

## 4. Production ↔ QC ↔ Wages

```mermaid
erDiagram
    PRODUCTION_TEMPLATE ||--o{ TEMPLATE_REVISION : versions
    TEMPLATE_REVISION ||--o{ TEMPLATE_STEP : defines
    TEMPLATE_REVISION ||--o{ TEMPLATE_QC_PARAM : sets
    WORK_ORDER ||--|| WAREHOUSE : executes_at
    WORK_ORDER }o--|| SALES_ORDER : aligns
    WORK_ORDER ||--o{ WO_CONSUMPTION : consumes
    WO_CONSUMPTION }o--|| PRODUCT_BATCH : draws
    WORK_ORDER ||--o{ WO_OUTPUT : produces
    WO_OUTPUT }o--|| PRODUCT_BATCH : creates
    WORK_ORDER ||--o{ WAGE_ACCRUAL : triggers
    WAGE_ACCRUAL }o--|| STAFF_GROUP : applies
    STAFF_GROUP ||--o{ STAFF_MEMBER : includes
    QC_REQUEST }o--|| WORK_ORDER : samples
    QC_REQUEST ||--o{ QC_JOB : assigns
    QC_JOB }o--|| QC_ANALYST : executed_by
    QC_JOB ||--o{ QC_RESULT : produces
    QC_RESULT }o--|| QC_REPORT : aggregates
    QC_REPORT }o--|| PRODUCT_BATCH : certifies
```

- **WAGE_ACCRUAL/WAGE_VOUCHER** records originate with the Warehouse Coordinator (Office) and route to the Finance Manager for approval, keeping wage advice ownership aligned with finance controls.

## 5. Logistics ↔ Stock Transfer ↔ Job Work

```mermaid
erDiagram
    STOCK_TRANSFER_DC ||--o{ STDC_LINE : moves
    STDC_LINE }o--|| PRODUCT_BATCH : ships
    STOCK_TRANSFER_DC }o--|| WAREHOUSE : source
    STOCK_TRANSFER_RECEIPT }o--|| STOCK_TRANSFER_DC : completes
    STOCK_TRANSFER_RECEIPT ||--o{ STR_LINE : receives
    INTER_WAREHOUSE_SHIFT ||--o{ SHIFT_LINE : relocates
    SHIFT_LINE }o--|| PRODUCT_BATCH : reassigned
    JOBWORK_DC ||--o{ JWDC_LINE : issues
    JWDC_LINE }o--|| PRODUCT_BATCH : sends
    JOBWORK_RA }o--|| JOBWORK_DC : closes
    JOBWORK_RA ||--o{ JWRA_LINE : receives
    JOBWORK_TEMPLATE ||--o{ JW_TEMPLATE_STEP : defines
    JOBWORK_DC ||--|| JOBWORK_TEMPLATE : follows
    JOBWORK_COST ||--|| JOBWORK_RA : derives
    JOBWORK_COST }o--|| FREIGHT_ADVICE : associates
```

- Inter-warehouse freight advice follows the same Freight Coordinator creation and Finance Manager approval, with cost-per-unit and destination state captured for transfer analytics.

## 6. Attendance ↔ HR ↔ Finance

```mermaid
erDiagram
    STAFF_MEMBER }o--|| COMPANY : employed_by
    STAFF_MEMBER }o--|| WAREHOUSE : posted_to
    STAFF_MEMBER ||--o{ SHIFT_ASSIGNMENT : scheduled
    SHIFT_ASSIGNMENT ||--o{ ATTENDANCE_LOG : records
    ATTENDANCE_LOG }o--|| ATTENDANCE_PHOTO : validates
    ATTENDANCE_LOG ||--o{ OVERTIME_REQUEST : proposes
    OVERTIME_REQUEST }o--|| WAGE_ACCRUAL : feeds
    LEAVE_REQUEST }o--|| STAFF_MEMBER : raised_by
    LEAVE_REQUEST }o--|| HR_DECISION : resolved_by
    STAFF_MEMBER }o--o{ ROLE_ASSIGNMENT : optionally
```

These diagrams should be reviewed whenever new modules are added or relationships evolve, ensuring integration points remain consistent across the ERP landscape.
