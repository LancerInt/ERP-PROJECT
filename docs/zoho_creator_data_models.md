# Zoho Creator ERP Data Models

This catalogue organises Zoho Creator forms, subforms, and key fields by module. It expands on the blueprint with implementation-ready attributes, lookups, and automation hooks.

## 1. Core & Shared Masters
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Company** | Company Code, Legal Name, GSTIN, Billing Address, Default Currency, Books Export Flag | Parent entity for warehouses, price lists, tax registrations |
| **Warehouse** | Warehouse Code, Company Lookup, Name, Address, Geo Coordinates, Time Zone, Default Currency, Active Flag | Lookup to Warehouse Coordinator (Office), Warehouse HR Coordinator; subform: Godowns |
| **Godown** (subform) | Godown Code, Name, Storage Conditions, Capacity, Batch Tracking Enabled | Referenced by Inventory Ledger & stock reports |
| **Role Definition** | Role Code, Name, Module Permissions JSON, Approval Levels, Data Scope (HO-only / Warehouse-limited) | Assigned to portal users |
| **Stakeholder User** | Portal User ID, Employee Lookup, Role Multi-select, Default Warehouse Scope, Status | Drives record sharing rules |
| **Employee / Staff** | Staff ID, Name, Employment Type (Staff/Employee), Company, Warehouse/Dept, Designation, Join Date, Face Template ID, Photo, Active Flag | Used in Attendance, Wage, Permissions |
| **Product** | SKU Code, Name, Product Type (Goods/Services), Sub-type, Batch Tracking Flag, QC Responsibility, Unit of Measure, Alternate UOM subform (To UOM, Factor, Specific Gravity), Packing Material Association, Yield Tracking Flags, Wage Method, Shelf Life | Linked to BOM Templates, Price Lists, QC Templates, Inventory |
| **Service Catalogue** | Service Code, Name, Category (Warehouse Expense, Freight, Wages, etc.), Direction (Inbound/Outbound/Both), Default TDS/TCS %, Warehouse Availability | IT Admin maintains extendable list |
| **Machine / Equipment** | Machine ID, Warehouse, Category (Capital Goods/Machine Spares), Service Schedule, Linked Job Work Vendor, Status | Track machine-level job work |
| **Vendor** | Vendor Code, Company, Vendor Type, GSTIN, PAN, Address, Payment Terms, Freight Terms, Credit Limit, TDS/TCS %, Bank Details, Preferred Transporters, Active Flag | Linked to Purchase, Freight, Wages, Job Work |
| **Customer** | Customer Code, Company, GSTIN, Billing/Shipping Addresses, Credit Terms, Freight Terms, Allowed Price Lists (multi), Default Warehouse, Overdue Notification Flag | Linked to Sales Orders, Receivables |
| **Transporter** | Transporter Code, Name, Contact, GSTIN, Freight Modes, Routes, TDS %, Payment Terms, Rating | Shared across inbound/outbound |
| **Price List** | Price List ID, Company, Customer Lookup, Region/Delivery Location, Currency, Validity, Active, Subform Lines (Product, UOM, Rate, Discount, GST %) | Multiple active per customer |
| **Tax Master** | Tax Type (GST/TDS/TCS), Rate %, Effective Dates, Applicable Entity (Product/Service/Freight/Wage), Thresholds, Section Reference | Consumed by finance calculations |
| **Template Library** | Template Type (Production, QC Report, Job Work, Packing, Invoice), Name, Warehouse Scope, Revision, Effective Date, JSON/XML Layout, Status, Digital Signature Requirement | Used by corresponding modules |

## 2. Purchase Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Purchase Request (PR)** | PR No., Warehouse, Godown, Requested By, Requirement Lines (Product/Service, Qty, Required Date, Purpose, Attachments), Status, Visibility Scope | Approval by HO Purchase roles; supports partial approval |
| **RFQ Header** | RFQ No., Linked PR(s), Skip RFQ Flag, Approval Attachment, Quote Count Expected, Dispatch ETA Updates | Generates Quote Responses |
| **Quote Response** | Vendor, RFQ, Price, Qty, Delivery Terms, Freight Terms, Payment Terms, Specs Attachment, Taxes, Validity, Remarks | Evaluated in Quote Evaluation |
| **Quote Evaluation** | RFQ, Comparison Table (subform per vendor), Best Quote Flag, Justification Notes, Approval Trail, Decision Date | Approval by Purchase Manager |
| **Purchase Order (PO)** | PO No., Vendor, Company, Warehouse, Linked PR(s), Linked RFQ, Revision No., PO Lines (Product, Qty, Rate, Taxes, Freight Estimate, Delivery Schedule), Freight Terms, Payment Terms, Attachments | Auto-generated from approved evaluation |
| **PO ETA Update** | PO, Expected Arrival Date, Updated By, Remarks, Timestamp | Editable until receipt |
| **Receipt Advice (Inbound)** | RA No., Warehouse, Vendor, Linked PO(s), Vehicle Info, Packing Material Captured (subform), Received Qty, Batch No., Godown, QC Routing, Freight Details, Attachments (Invoice, Photos) | Updates stock & triggers QC |
| **Freight Advice (Inbound)** | Advice No., Direction=Inbound, Receipt Advice, Transporter, Freight Type (Local/Linehaul), Loading/Unloading Wages, Discounts, Payment Schedule, Approval Workflow | Shared with Finance |
| **Vendor Payment Advice** | Advice No., Vendor, Source Document (PO/RA/Freight/Wage), Amount, TDS/TCS %, Due Date, Payment Method, Approval Trail | Feeds Finance module |

## 3. Sales Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Customer PO Upload** | Upload ID, Customer, PO File, Parsed Metadata (PO No., Date, Delivery Location), Parsing Confidence, Manual Review Flag, Status | Feeds Draft Sales Order |
| **Sales Order (SO)** | SO No., Customer, Warehouse, Price List, Credit Terms, Freight Terms, Lines (Product, Qty, Rate, Taxes, Delivery Schedule, Batch Preference), Status (Draft/Approved/Released) | Must reference active price list |
| **Dispatch Challan (DC)** | DC No., Warehouse, Linked SO Line(s), Consolidated Lines (Product, Qty, Batch, Delivery Location), Transport Info, Freight Rate, Lorry No., Status, Attachments (Weighment slip) | Supports multi-SO aggregation |
| **Sales Invoice Check** | Invoice ID, DC Link, Statutory Invoice Upload, Parsed Totals, Variance Flag, Remarks, Acceptance Timestamp | Drives inventory deduction & receivables |
| **Freight Advice (Outbound)** | Advice No., Direction=Outbound, DC Reference, Transporter, Freight Components, Discounts, Payment Schedule, TDS %, Approval Trail | Shared with Finance |
| **Receivable Ledger** | Customer, Invoice, Amount, Due Date, Payment Status, Reminder Sent Flag, Overdue Escalation Date | Linked to bank reconciliation |

## 4. Production Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **BOM Request** | Request No., Warehouse, Requested By, Template, Output Product, Qty, Auto-calculated Inputs (Available Qty, Shortfall), Approval Status, Excel Export Link | Feeds Purchase Requests |
| **Material Issue** | Issue No., Warehouse, Work Order, Product, Qty Issued, UOM, Godown, Batch Out, Issued By, Approved By | Reduces inventory |
| **Work Order / Production Batch** | Batch ID, Warehouse, Template Revision, Linked SO/DC, Scheduled Dates, Status, Input Consumption (subform), Output Products (subform with Batch, Qty, Purity, AI Content), Damage/Returns, QC Link, Wage Method | Creates production history |
| **Wage Voucher (Production)** | Voucher No., Work Order, Wage Type (Template/Headcount), Staff/Contractor, Hours/Tasks, Amount, TDS %, Approval Steps | Posted to Finance |
| **Production Yield Log** | Batch, Product, Planned Yield %, Actual Output, Purity %, AI Content, Variance, Remarks | Reporting |

## 5. Quality Control Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **QC Parameter Library** | Parameter Code, Description, Unit, Product/Template Association, Acceptable Range, Critical Flag | Referenced in QC requests |
| **QC Request** | Request No., Warehouse, Requestor Role, Product, Batch, Template, Selected Parameters, Sample Photo, Priority, Status | Generates lab jobs |
| **QC Lab Job** | Job No., QC Request, Analyst, Assigned Parameters, Samples Received Timestamp, Results (value, photo), Comments | Multiple jobs per request |
| **QC Final Report** | Report No., QC Request, Template Revision, Summary, Pass/Fail, Digital Signature, Distribution List, Attachments | Shared with stakeholders |
| **Counter Sample Register** | Sample ID, QC Request, Storage Location, Issued To, Issue Date, Expected Return, Actual Return, Reminder Sent | Audit trail |

## 6. Inventory & Logistics Modules
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Inventory Ledger** | Entry ID, Warehouse, Godown, Product, Batch, Qty In/Out, UOM, Transaction Type, Document Link, Cost, Status (Available/In Transit/Reserved) | Supports FIFO valuation |
| **Stock Transfer DC** | Transfer No., From Warehouse, To Warehouse, Product Lines, Batch, In-Transit Qty, Loading Wages, Freight Details, Status | Initiates transfer |
| **Stock Transfer Receipt** | Receipt No., From Warehouse, To Warehouse, Linked Transfer, Received Qty, Batch, Godown, QC Result, Variance | Completes transfer |
| **Warehouse Shifting** | Shifting No., Warehouse, From Godown, To Godown, Products, Reason Code, Freight/Wage Drafts, Approval Workflow, In-Transit Status | Internal movements |
| **Job Work DC** | JW DC No., Job Work Order, Vendor, Issued Materials (Products/Batches/Machines), Transport Info, Freight Draft | Outbound to vendor |
| **Job Work Receipt** | Receipt No., JW DC, Returned Goods, New Batch ID, QC Result, Pending Qty, Charges | Closes or keeps order open |
| **Sales Return Advice** | Return No., Customer, Original Invoice, Returned Products, Qty, Condition, Freight Terms, Approval Trail | Feeds QC & inventory |
| **Stock Adjustment** | Adjustment No., Warehouse, Product, Batch, Godown, Adjustment Type (+/-), Qty, Reason, Evidence Attachments, Value Impact, Approval, Escalation Flag | Enforces thresholds |

## 7. Finance Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Vendor Ledger** | Vendor, Document Reference, Debit/Credit, Tax Components, Due Date, Payment Status | Consolidates payables |
| **Payment Advice Workflow** | Advice No., Vendor/Transporter/Contractor, Source (PO/RA/Freight/Wage), Amount, TDS/TCS, Due Date, Approval Steps (Finance Manager → Office Manager), Payment Method | Initiates payouts |
| **Bank Statement Upload** | Upload ID, Bank Account, Statement Date, File Attachment, Parsing Status, Auto-Matched Entries, Exceptions | Daily reconciliation |
| **Reconciliation Exception** | Exception ID, Statement Entry, Suggested Match, Notes, Resolution Status | Tracks manual handling |
| **Customer Ledger** | Customer, Invoice Reference, Debit/Credit, Due Date, Payment Status, Reminder Dates, Escalation Flags | Receivables |
| **Freight Ledger** | Transporter, Direction (Inbound/Outbound/Transfer), Freight Advice, Amount, Discount, Payment Schedule, Paid Amount, Reminder Flag | Supports reminders |
| **Wage Ledger** | Wage Voucher, Contractor/Staff Group, Amount, TDS, Payment Week, Approval Status, Settlement Method | Links attendance & finance |
| **Credit/Debit Note** | Note No., Vendor/Customer, Source Document, Amount, Tax, Reason, Approval, Ledger Posting | Adjustments |
| **GST Reconciliation Report** | Reporting Period, Data Source (Creator, GSTR-2B/1), Variance Summary, Adjustments | Export to Tally |

## 8. Attendance & HR Module
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **Shift Definition** | Shift Code, Warehouse, Start/End Time, Breaks, Overtime Eligibility, Attendance Calculation Rules | Assigned to staff |
| **Attendance Capture** | Record ID, Staff, Date, Check-in Time, Check-out Time, Photo Entry/Exit, Geo Coordinates, Face Match Confidence, Device ID | Only HR coordinators capture |
| **Leave Request** | Request No., Staff, Type (Full/Half/Permission), Dates, Reason, Attachments, Approval Status, Approver | Notification to relevant HR role |
| **Overtime Request** | Request No., Staff, Date, Hours, Task Description, Supporting Evidence, Approval Status, Wage Integration Flag | Routes to Warehouse Coordinator (Office) |
| **Payroll Export** | Period, Warehouse, Staff Summary, Attendance Metrics, Overtime Hours, Exceptions, Export File | For payroll integration |

## 9. Configuration & Audit
| Form | Key Fields | Relationships & Notes |
| --- | --- | --- |
| **System Parameters** | Parameter Name, Value, Module Scope, Last Updated By, Effective Date | Stores ₹25,000 threshold, reminder intervals |
| **Decision Log** | Decision ID, Topic, Stakeholders, Decision Details, Date | Governance record |
| **Audit Trail** | Module, Record ID, Action, User, Timestamp, Before/After Snapshot | Compliance |

Use this data model document alongside the ERD and flowchart references to maintain alignment between forms, workflows, and reporting.
