# Zoho Creator ERP Data Model – Field Maps

The diagrams below provide a pictorial overview of every form and field defined in the Zoho Creator ERP data model. Each module
has its own Mermaid `classDiagram`, enabling designers and developers to visualise structures while cross-referencing the
comprehensive field catalogue.

---

## Core & Shared Masters
```mermaid
classDiagram
    class Company {
        +Company Code
        +Legal Name
        +Trade Name
        +GSTIN
        +PAN
        +CIN
        +Registered Address
        +Billing Address
        +Contact Email
        +Contact Phone
        +Default Currency
        +Books Export Flag
        +Active From
        +Active To
        +Notes
    }
    class Warehouse {
        +Warehouse Code
        +Company
        +Name
        +Warehouse Type
        +Address
        +City
        +State
        +Country
        +Pincode
        +Geo Latitude
        +Geo Longitude
        +Time Zone
        +Default Currency
        +Warehouse Coordinator (Office)
        +Warehouse HR Coordinator
        +Warehouse Manager(s)
        +Warehouse Coordinator(s)
        +Warehouse Supervisor(s)
        +Active Flag
        +Notes
    }
    class Godown {
        +Godown Code
        +Warehouse
        +Godown Name
        +Storage Condition
        +Capacity UOM
        +Capacity Value
        +Batch Tracking Enabled
        +Default QC Hold Area
        +Active Flag
        +Notes
    }
    class Machinery {
        +Machine ID
        +Warehouse
        +Godown
        +Machine Name
        +Category
        +Commission Date
        +Maintenance Vendor
        +Next Service Due
        +Status
        +Notes
    }
    class RoleDefinition {
        +Role Code
        +Role Name
        +Module Permissions
        +Data Scope
        +Default Share Rules
        +Active Flag
    }
    class ApprovalLevel {
        +Module
        +Stage
        +Min Amount
        +Max Amount
    }
    class StakeholderUser {
        +Portal User ID
        +Employee Record
        +Primary Email
        +Mobile
        +Assigned Roles
        +Default Warehouse
        +Warehouse Scope
        +Status
        +Last Accessed
        +Notes
    }
    class StaffMaster {
        +Staff ID
        +Staff Type
        +First Name
        +Last Name
        +Gender
        +Date of Birth
        +Company
        +Primary Location
        +Department
        +Designation
        +Employment Start Date
        +Employment End Date
        +Employment Status
        +HR Owner
        +Shift Assignment
        +Overtime Eligible
        +Contractor Flag
        +Contractor Vendor
        +Face Template ID
        +Photo Reference
        +Contact Number
        +Emergency Contact
        +Address
        +Remarks
    }
    class StaffBank {
        +Account Holder
        +Bank Name
        +IFSC Code
        +Account Number
        +Account Type
    }
    class StaffIDProof {
        +Document Type
        +Document Number
        +Expiry Date
        +Attachment
    }
    class Product {
        +SKU Code
        +Product Name
        +Product Type
        +Goods Sub-Type
        +Service Sub-Type
        +Custom Service Category
        +Description
        +Batch Tracking Required
        +Shelf Life (Days)
        +QC Responsibility
        +QC Template
        +UOM
        +Specific Gravity
        +Conversion Notes
        +Packing Material Default
        +Yield Tracking Required
        +Yield Parameters
        +Wage Method
        +Freight Class
        +Active Flag
        +Created By
        +Created Date
        +Last Modified By
        +Last Modified Date
    }
    class SecondaryUOM {
        +To UOM
        +Conversion Factor
        +Specific Gravity Override
        +Valid From
        +Valid To
    }
    class ServiceCatalogue {
        +Service Code
        +Name
        +Category
        +Direction
        +Default TDS %
        +Default TCS %
        +Warehouse Availability
        +Description
        +Active Flag
    }
    class Vendor {
        +Vendor Code
        +Vendor Name
        +Vendor Type
        +Company
        +GSTIN
        +PAN
        +Address
        +City
        +State
        +Country
        +Pincode
        +Contact Person
        +Contact Email
        +Contact Phone
        +Payment Terms
        +Custom Payment Days
        +Freight Terms
        +Freight Split Notes
        +Credit Limit
        +Credit Days
        +TDS Rate %
        +TCS Rate %
        +Preferred Transporters
        +Allowed Warehouses
        +Attachments
        +Active Flag
        +Created Date
    }
    class VendorBank {
        +Account Nickname
        +Bank Name
        +Branch
        +IFSC
        +Account Number
        +Payment Method
    }
    class Customer {
        +Customer Code
        +Customer Name
        +Company
        +GSTIN
        +PAN
        +Billing Address
        +Credit Terms
        +Custom Credit Days
        +Freight Terms
        +Freight Split Notes
        +Allowed Price Lists
        +Default Warehouse
        +Overdue Notification Recipients
        +Contact Person
        +Contact Email
        +Contact Phone
        +Documents
        +Active Flag
    }
    class ShippingAddress {
        +Address Label
        +Address
        +Delivery Region
        +Default Price List
        +Contact Person
        +Contact Phone
    }
    class Transporter {
        +Transporter Code
        +Name
        +GSTIN
        +Contact Person
        +Contact Email
        +Contact Phone
        +Freight Modes
        +Coverage Routes
        +TDS Rate %
        +Payment Terms
        +Rating
        +Documents
        +Active Flag
    }
    class PriceList {
        +Price List ID
        +Company
        +Customer
        +Delivery Region
        +Currency
        +Effective From
        +Effective To
        +Default Freight Terms
        +Status
        +Notes
    }
    class PriceLine {
        +Product
        +UOM
        +Rate
        +Discount %
        +GST %
        +Freight Component
        +Valid From
        +Valid To
    }
    class TaxMaster {
        +Tax Type
        +Section Reference
        +Rate %
        +Effective From
        +Effective To
        +Applicable On
        +Threshold Amount
        +Company Scope
        +Notes
    }
    class TemplateLibrary {
        +Template ID
        +Template Type
        +Name
        +Warehouse Scope
        +Revision No.
        +Effective From
        +Effective To
        +Layout JSON/XML
        +Requires Digital Signature
        +Created By
        +Status
    }
    class TemplateApproval {
        +Approved By
        +Approval Date
        +Remarks
    }
    Company "1" -- "many" Warehouse
    Warehouse "1" -- "many" Godown
    Godown "1" -- "many" Machinery
    RoleDefinition "1" -- "many" ApprovalLevel
    StakeholderUser "1" -- "many" RoleDefinition : assigned
    StaffMaster "1" -- "many" StaffBank
    StaffMaster "1" -- "many" StaffIDProof
    Product "1" -- "many" SecondaryUOM
    Vendor "1" -- "many" VendorBank
    Customer "1" -- "many" ShippingAddress
    PriceList "1" -- "many" PriceLine
    TemplateLibrary "1" -- "many" TemplateApproval
```

---

## Purchase Module
```mermaid
classDiagram
    class PurchaseRequest {
        +PR No.
        +Request Date
        +Warehouse
        +Godown
        +Requested By
        +Requestor Role
        +Requirement Type
        +Priority
        +Required By Date
        +Justification
        +Attachments
        +Approval Status
        +Visibility Scope
        +Created From BOM Request
        +Notes
    }
    class PRLine {
        +Line No.
        +Product/Service
        +Description Override
        +Quantity Requested
        +UOM
        +Required Date
        +Purpose
        +Machine Reference
        +Allow RFQ Skip
        +Attachments
        +Status
        +Approved Quantity
    }
    class PRApproval {
        +Action
        +Actor
        +Action Date
        +Remarks
    }
    class RFQHeader {
        +RFQ No.
        +Linked PRs
        +Created By
        +Creation Date
        +RFQ Mode
        +RFQ Documents
        +RFQ Status
        +Quote Count Expected
        +Skip RFQ Flag
        +Skip RFQ Justification
        +Purchase Manager Approval
        +Approval Attachment
    }
    class ETAUpdate {
        +Update Date
        +Updated By
        +Expected Arrival
        +Remarks
    }
    class QuoteResponse {
        +Quote ID
        +RFQ
        +Vendor
        +Quote Date
        +Price Valid Till
        +Currency
        +Freight Terms
        +Payment Terms
        +Delivery Terms
        +Lead Time (Days)
        +Attachments
        +Remarks
        +Evaluation Score
        +Chosen Flag
    }
    class QuoteLine {
        +PR Line
        +Product/Service
        +Specification
        +Quantity Offered
        +UOM
        +Unit Price
        +Discount %
        +GST %
        +Freight Charge
        +Delivery Timeline
    }
    class QuoteEvaluation {
        +Evaluation ID
        +RFQ
        +Evaluation Date
        +Evaluated By
        +Best Quote Flag
        +Recommended Vendor
        +Justification Notes
        +Approval Status
    }
    class ComparisonRow {
        +Vendor
        +Total Cost
        +Lead Time
        +Freight Terms
        +Payment Terms
        +Score
        +Remarks
    }
    class PurchaseOrder {
        +PO No.
        +Revision No.
        +Vendor
        +Company
        +Warehouse
        +Linked PRs
        +Linked RFQ
        +PO Date
        +Expected Delivery Start
        +Expected Delivery End
        +Freight Terms
        +Payment Terms
        +Currency
        +Attachments
        +Terms & Conditions
        +Status
        +Partial Receipt Flag
    }
    class POLine {
        +Line No.
        +Product/Service
        +Description
        +Quantity Ordered
        +UOM
        +Unit Price
        +Discount %
        +GST %
        +Extra Commission
        +Agent Commission
        +Freight Estimate
        +Delivery Schedule
        +Linked PR Line
        +Linked RFQ Line
        +Batch Requirement Notes
    }
    class POETAUpdate {
        +Update ID
        +PO
        +Update Date
        +Updated By
        +Expected Arrival Date
        +Status
        +Remarks
    }
    class ReceiptAdvice {
        +Receipt Advice No.
        +Receipt Date
        +Warehouse
        +Godown
        +Vendor
        +Linked PO(s)
        +Vehicle Number
        +Driver Name
        +Invoice Upload
        +Packing List Upload
        +QC Routing
        +QC Status
        +Partial Receipt Flag
        +Remarks
        +Created By
        +Created Time
        +Freight Payment Schedule
    }
    class ReceiptLine {
        +Line No.
        +PO Line
        +Product
        +Batch No.
        +Expiry Date
        +Quantity Received
        +UOM
        +Extra Commission
        +Agent Commission
        +Quantity Accepted
        +Quantity Rejected
        +Godown Location
        +Remarks
    }
    class PackingMaterialLine {
        +Packaging SKU
        +Quantity
        +UOM
        +Condition
    }
    class FreightDetail {
        +Freight Type
        +Transporter
        +Freight Terms
        +Tentative Charge
        +Discount
        +Payable By
        +Quantity Basis
        +Quantity UOM
        +Destination State
        +Cost Per Unit (Calc)
    }
    class FreightPaymentSchedule {
        +Freight Type
        +Transporter
        +Due Date
        +Amount
        +TDS %
        +Reminder Flag
    }
    class LoadingWage {
        +Wage Type
        +Contractor Vendor
        +Amount
        +TDS Applicable %
        +Payable By
        +Remarks
    }
    class FreightAdviceInbound {
        +Advice No.
        +Direction
        +Receipt Advice
        +Transporter
        +Freight Type
        +Created By
        +Created Date
        +Base Amount
        +Discount
        +Loading Wages Amount
        +Unloading Wages Amount
        +Quantity Basis
        +Quantity UOM
        +Cost Per Unit (Calc)
        +Destination State
        +Payable Amount
        +Payment Schedule
        +Status
    }
    class VendorPaymentAdvice {
        +Advice No.
        +Vendor
        +Source Document Type
        +Source Document
        +Amount
        +Due Date
        +Payment Method
        +Prepared By
        +Status
        +Notes
    }
    class TaxComponent {
        +Tax Type
        +Rate %
        +Amount
    }
    PurchaseRequest "1" -- "many" PRLine
    PurchaseRequest "1" -- "many" PRApproval
    RFQHeader "1" -- "many" ETAUpdate
    RFQHeader "1" -- "many" QuoteResponse
    QuoteResponse "1" -- "many" QuoteLine
    QuoteEvaluation "1" -- "many" ComparisonRow
    PurchaseOrder "1" -- "many" POLine
    ReceiptAdvice "1" -- "many" ReceiptLine
    ReceiptAdvice "1" -- "many" PackingMaterialLine
    ReceiptAdvice "1" -- "many" FreightDetail
    ReceiptAdvice "1" -- "many" LoadingWage
    ReceiptAdvice "1" -- "many" FreightPaymentSchedule
    FreightAdviceInbound "1" -- "many" FreightPaymentSchedule
    FreightAdviceOutbound "1" -- "many" FreightPaymentSchedule
    FreightAdviceInbound "1" -- "many" LoadingWage
    VendorPaymentAdvice "1" -- "many" TaxComponent
```

---

## Sales Module
```mermaid
classDiagram
    class CustomerPOUpload {
        +Upload ID
        +Customer
        +Upload Date
        +PO File
        +AI Parser Confidence
        +Parsed PO Number
        +Parsed PO Date
        +Delivery Location
        +Manual Review Required
        +Review Comments
        +Status
        +Linked Sales Order
    }
    class ParsedPOLine {
        +Product Description
        +Quantity
        +UOM
        +Price
        +Parsed SKU
        +Confidence %
    }
    class SalesOrder {
        +SO No.
        +Customer
        +Company
        +Warehouse
        +Price List
        +Credit Terms
        +Freight Terms
        +Customer PO Reference
        +SO Date
        +Required Ship Date
        +Remarks
        +Approval Status
        +Approved By
        +Approval Date
        +Assigned Warehouse Stakeholders
    }
    class SOLine {
        +Line No.
        +Product
        +Batch Preference
        +Quantity Ordered
        +UOM
        +Unit Price
        +Discount %
        +GST %
        +Delivery Schedule Date
        +Remarks
        +Reserved Qty
    }
    class DispatchChallan {
        +DC No.
        +Warehouse
        +Dispatch Date
        +Transporter
        +Freight Rate Type
        +Freight Rate Value
        +Freight Amount Total
        +Lorry No.
        +Driver Contact
        +Documents
        +Status
        +Created By
        +Freight Advice Link
    }
    class DCLine {
        +Product
        +Batch
        +Quantity Dispatched
        +UOM
        +Linked SO Line
        +Weight
    }
    class DeliveryLocation {
        +Sequence
        +Shipping Address
        +Quantity for Location
        +Estimated Arrival
    }
    class SalesInvoiceCheck {
        +Invoice Check ID
        +DC Reference
        +Statutory Invoice Upload
        +Invoice Number
        +Invoice Date
        +Total Value (Upload)
        +Total Value (SO)
        +Variance Amount
        +Variance Flag
        +Remarks
        +Acceptance Timestamp
        +Accepted By
    }
    class FreightAdviceOutbound {
        +Advice No.
        +Direction
        +Dispatch Challan
        +Transporter
        +Freight Type
        +Created By
        +Created Date
        +Base Amount
        +Discount
        +Loading Wages Amount
        +Unloading Wages Amount
        +Shipment Quantity
        +Quantity UOM
        +Cost Per Unit (Calc)
        +Destination State
        +Payable Amount
        +Payment Schedule
        +Status
    }
    class ReceivableLedger {
        +Ledger ID
        +Customer
        +Invoice Reference
        +Invoice Date
        +Due Date
        +Amount
        +Amount Paid
        +Balance
        +Payment Status
        +Escalation Flag
        +Notes
    }
    class ReceivableReminder {
        +Reminder Date
        +Reminder Sent By
        +Reminder Method
    }
    CustomerPOUpload "1" -- "many" ParsedPOLine
    SalesOrder "1" -- "many" SOLine
    DispatchChallan "1" -- "many" DCLine
    DispatchChallan "1" -- "many" DeliveryLocation
    ReceivableLedger "1" -- "many" ReceivableReminder
```

---

## Production Module
```mermaid
classDiagram
    class BOMRequest {
        +Request No.
        +Request Date
        +Warehouse
        +Requested By
        +Production Template
        +Output Product
        +Output Quantity
        +Required Completion Date
        +Shortfall Summary
        +Approval Status
        +Approved By
        +Approved Date
        +Excel Export Link
        +Notes
    }
    class BOMInput {
        +Product
        +Required Qty
        +Available Qty
        +Shortfall Qty
        +Purpose
    }
    class MaterialIssue {
        +Issue No.
        +Issue Date
        +Warehouse
        +Work Order
        +Issued By
        +Approved By
        +Remarks
    }
    class IssueLine {
        +Product
        +Batch Out
        +Godown
        +Quantity Issued
        +UOM
        +Reserved for Template
    }
    class WorkOrder {
        +Batch ID
        +Work Order No.
        +Warehouse
        +Production Template
        +Template Revision
        +Linked Sales Order
        +Linked Dispatch Challan
        +Planned Start Date
        +Planned End Date
        +Actual Start Date
        +Actual End Date
        +Stage Status
        +QC Request
        +Wage Method
        +Yield Log Reference
        +Rework Flag
        +Parent Batch
        +Notes
    }
    class WorkOrderInput {
        +Product
        +Planned Qty
        +Actual Qty
        +UOM
        +Batch Used
        +Godown
        +Yield Loss %
    }
    class WorkOrderOutput {
        +Product
        +Batch ID
        +Quantity Produced
        +UOM
        +Purity %
        +AI Content
        +QC Status
    }
    class WorkOrderDamage {
        +Stage
        +Description
        +Quantity Lost
        +UOM
        +Handling Action
    }
    class WorkOrderWageRef {
        +Wage Voucher
        +Amount
    }
    class WageVoucher {
        +Voucher No.
        +Work Order
        +Wage Type
        +Contractor Vendor
        +Staff Group
        +Amount
        +TDS %
        +Prepared By (Warehouse Coordinator - Office)
        +Prepared Date
        +Approval Workflow (→ Finance Manager)
        +Status
        +Remarks
    }
    class WageTask {
        +Staff
        +Task Description
        +Hours Worked
        +Quantity Produced
    }
    class ProductionYieldLog {
        +Log ID
        +Work Order
        +Product
        +Planned Yield %
        +Actual Output Qty
        +Purity %
        +AI Content
        +Variance %
        +Remarks
        +Report Date
    }
    BOMRequest "1" -- "many" BOMInput
    MaterialIssue "1" -- "many" IssueLine
    WorkOrder "1" -- "many" WorkOrderInput
    WorkOrder "1" -- "many" WorkOrderOutput
    WorkOrder "1" -- "many" WorkOrderDamage
    WorkOrder "1" -- "many" WorkOrderWageRef
    WageVoucher "1" -- "many" WageTask
```

---

## Quality Control Module
```mermaid
classDiagram
    class QCParameter {
        +Parameter Code
        +Parameter Name
        +Unit
        +Applicable Template
        +Applicable Product
        +Acceptable Min
        +Acceptable Max
        +Critical Flag
        +Notes
    }
    class QCRequest {
        +Request No.
        +Request Date
        +Requested By
        +Requestor Role
        +Warehouse
        +Product
        +Batch
        +Stage
        +QC Template
        +Sample Photo
        +Sample Qty
        +Priority
        +Remarks
        +Status
        +Lab Code
        +Counter Sample Required
    }
    class QCSelectedParameter {
        +Parameter
        +Override Range Min
        +Override Range Max
        +Notes
    }
    class QCLabJob {
        +Job No.
        +QC Request
        +Analyst
        +Sample Received Date
        +Results Attachment
        +Comments
        +Status
    }
    class QCJobParameter {
        +Parameter
        +Result Value
        +Result Text
        +Result Photo
        +Pass/Fail
    }
    class QCFinalReport {
        +Report No.
        +QC Request
        +Template Revision
        +Prepared By
        +Prepared Date
        +Overall Result
        +Remarks
        +Digital Signature
        +Distribution List
        +Attachments
    }
    class CounterSample {
        +Sample ID
        +QC Request
        +Storage Location
        +Shelf
        +Bin
        +Issued To
        +Issue Date
        +Expected Return Date
        +Actual Return Date
        +Reminder Sent
        +Disposal Date
        +Disposal Approved By
    }
    QCRequest "1" -- "many" QCSelectedParameter
    QCLabJob "1" -- "many" QCJobParameter
```

---

## Inventory, Logistics & Returns
```mermaid
classDiagram
    class InventoryLedger {
        +Ledger Entry ID
        +Transaction Date
        +Warehouse
        +Godown
        +Product
        +Batch
        +Quantity In
        +Quantity Out
        +UOM
        +Transaction Type
        +Source Document
        +Cost
        +Status
        +FIFO Layer ID
        +Remarks
    }
    class StockTransferDC {
        +Transfer No.
        +Created Date
        +From Warehouse
        +To Warehouse
        +Dispatch Date
        +Transporter
        +Freight Terms
        +Loading Wages
        +Freight Amount
        +Status
        +Documents
    }
    class StockTransferLine {
        +Product
        +Batch
        +Quantity
        +UOM
        +Source Godown
        +Destination Godown
    }
    class StockTransferReceipt {
        +Receipt No.
        +Receipt Date
        +From Warehouse
        +To Warehouse
        +Linked Transfer
        +Received By
        +QC Result
        +Variance Notes
        +Status
    }
    class StockTransferReceiptLine {
        +Product
        +Batch
        +Quantity Dispatched
        +Quantity Received
        +UOM
        +Received Godown
        +Condition
    }
    class WarehouseShifting {
        +Shifting No.
        +Warehouse
        +Request Date
        +From Godown
        +To Godown
        +Reason Code
        +Other Reason
        +Status
        +In-Transit Flag
        +Attachments
    }
    class ShiftingProduct {
        +Product
        +Batch
        +Quantity
        +UOM
    }
    class ShiftingExpense {
        +Expense Type
        +Vendor
        +Amount
        +Payable By
        +Approval Status
    }
    class JobWorkOrder {
        +Order No.
        +Warehouse
        +Vendor
        +Template
        +Template Revision
        +Start Date
        +Expected Completion Date
        +Turnaround Threshold
        +Freight Terms
        +Status
        +Alerts Enabled
    }
    class JobWorkMaterial {
        +Material Type
        +Product/Machine
        +Batch
        +Quantity
        +UOM
    }
    class JobWorkOutput {
        +Product
        +Expected Quantity
        +UOM
        +Expected Batch Suffix
    }
    class JobWorkDC {
        +JW DC No.
        +Job Work Order
        +Vendor
        +Dispatch Date
        +Transporter
        +Freight Terms
        +Documents
        +Status
    }
    class JobWorkDCMaterial {
        +Material Type
        +Product/Machine
        +Batch
        +Quantity
        +UOM
        +Expected Return Date
    }
    class JobWorkReceipt {
        +Receipt No.
        +Receipt Date
        +Job Work Order
        +JW DC Reference
        +Vendor
        +New Batch ID
        +QC Result
        +Pending Quantity
        +Status
    }
    class JobWorkReturn {
        +Product
        +Batch
        +Quantity Received
        +UOM
        +Viability
    }
    class JobWorkCharge {
        +Charge Type
        +Amount
        +TDS %
        +Payable By
    }
    class SalesReturnAdvice {
        +Return No.
        +Return Date
        +Customer
        +Original Invoice
        +Returned By
        +Received Warehouse
        +Freight Terms
        +QC Requirement
        +Approval Status
        +Remarks
    }
    class SalesReturnLine {
        +Product
        +Batch
        +Quantity Returned
        +UOM
        +Condition
        +Viability Notes
        +Packing Material Captured
    }
    class SalesReturnFreight {
        +Freight Type
        +Transporter
        +Amount
        +Discount
        +Payable By
    }
    class SalesReturnWage {
        +Charge Type
        +Contractor Vendor
        +Amount
        +TDS %
        +Payable By
    }
    class StockAdjustment {
        +Adjustment No.
        +Adjustment Date
        +Warehouse
        +Godown
        +Product
        +Batch
        +Adjustment Type
        +Quantity
        +UOM
        +Reason Code
        +Other Reason
        +Evidence Attachments
        +Value Impact
        +Finance Review Required
        +Approval Status
        +Approved By
        +Approval Date
        +Notified To
        +Notes
    }
    StockTransferDC "1" -- "many" StockTransferLine
    StockTransferReceipt "1" -- "many" StockTransferReceiptLine
    WarehouseShifting "1" -- "many" ShiftingProduct
    WarehouseShifting "1" -- "many" ShiftingExpense
    JobWorkOrder "1" -- "many" JobWorkMaterial
    JobWorkOrder "1" -- "many" JobWorkOutput
    JobWorkDC "1" -- "many" JobWorkDCMaterial
    JobWorkReceipt "1" -- "many" JobWorkReturn
    JobWorkReceipt "1" -- "many" JobWorkCharge
    SalesReturnAdvice "1" -- "many" SalesReturnLine
    SalesReturnAdvice "1" -- "many" SalesReturnFreight
    SalesReturnAdvice "1" -- "many" SalesReturnWage
```

---

## Finance Module
```mermaid
classDiagram
    class VendorLedger {
        +Ledger ID
        +Vendor
        +Document Type
        +Document Reference
        +Document Date
        +Debit Amount
        +Credit Amount
        +Due Date
        +Payment Status
        +Ageing Bucket
        +Notes
    }
    class LedgerTax {
        +Tax Type
        +Rate %
        +Amount
    }
    class PaymentAdvice {
        +Advice No.
        +Beneficiary Type
        +Beneficiary
        +Source Document
        +Amount
        +Due Date
        +Payment Method
        +Bank Account
        +Prepared By
        +Prepared Date
        +Payment Status
        +Payment Reference
        +Attachments
    }
    class AdviceTax {
        +Tax Type
        +Section
        +Rate %
        +Amount
    }
    class FinanceApproval {
        +Approved/Authorized By
        +Date
        +Remarks
    }
    class BankStatementUpload {
        +Upload ID
        +Bank Account
        +Statement Period Start
        +Statement Period End
        +Upload Date
        +Statement File
        +Parsing Status
        +Remarks
    }
    class BankMatch {
        +Statement Line ID
        +Match Type
        +Linked Document
        +Amount
        +Status
    }
    class BankException {
        +Statement Line ID
        +Transaction Date
        +Amount
        +Suggested Match
        +Exception Notes
        +Resolution Status
    }
    class CustomerLedger {
        +Ledger ID
        +Customer
        +Document Type
        +Document Reference
        +Document Date
        +Debit Amount
        +Credit Amount
        +Due Date
        +Payment Status
        +Notes
    }
    class ReminderFlag {
        +Reminder Date
        +Reminder Sent By
        +Reminder Method
    }
    class FreightLedger {
        +Ledger ID
        +Direction
        +Transporter
        +Freight Advice
        +Amount
        +Discount
        +Shipment Quantity
        +Quantity UOM
        +Cost Per Unit
        +Destination State
        +Amount Paid
        +Balance
        +Reminder Flag
        +Notes
    }
    class PaymentSchedule {
        +Due Date
        +Amount
        +TDS %
        +Reminder Flag
    }
    class WageLedger {
        +Ledger ID
        +Wage Voucher
        +Contractor/Staff Group
        +Amount
        +TDS %
        +Payment Week
        +Approval Status
        +Settlement Method
        +Notes
    }
    class CreditDebitNote {
        +Note No.
        +Note Type
        +Vendor/Customer
        +Source Document
        +Amount
        +Tax
        +Reason
        +Approval Status
        +Approved By
        +Approval Date
        +Ledger Posting Reference
    }
    class GSTReconciliation {
        +Report ID
        +Reporting Period
        +Data Source
        +Variance Summary
        +Export File
    }
    class GSTAdjustment {
        +Adjustment Type
        +Amount
        +Notes
        +Approved By
    }
    class PettyCashRegister {
        +Register ID
        +Warehouse
        +Coordinator
        +Opening Balance
        +Current Balance
        +Last Reconciled Date
    }
    class PettyCashTxn {
        +Transaction Date
        +Voucher Reference
        +Amount
        +Type
        +Notes
    }
    VendorLedger "1" -- "many" LedgerTax
    PaymentAdvice "1" -- "many" AdviceTax
    PaymentAdvice "1" -- "many" FinanceApproval
    BankStatementUpload "1" -- "many" BankMatch
    BankStatementUpload "1" -- "many" BankException
    CustomerLedger "1" -- "many" ReminderFlag
    FreightLedger "1" -- "many" PaymentSchedule
    GSTReconciliation "1" -- "many" GSTAdjustment
    PettyCashRegister "1" -- "many" PettyCashTxn
```

---

## Attendance & HR Module
```mermaid
classDiagram
    class ShiftDefinition {
        +Shift Code
        +Warehouse
        +Shift Name
        +Start Time
        +End Time
        +Break Duration (mins)
        +Overtime Eligibility
        +Attendance Calculation Rule
        +Grace Period Minutes
        +Approval Required
    }
    class AttendanceCapture {
        +Record ID
        +Staff
        +Date
        +Check-in Time
        +Check-out Time
        +Entry Photo
        +Exit Photo
        +Geo Latitude
        +Geo Longitude
        +Face Match Confidence
        +Device ID
        +Shift
        +Attendance Status
        +Overtime Hours
        +Notes
    }
    class LeaveRequest {
        +Request No.
        +Staff
        +Leave Type
        +Start Date
        +End Date
        +Duration (Hours)
        +Reason
        +Attachment
        +Status
        +Approver
        +Approval Date
    }
    class OvertimeRequest {
        +Request No.
        +Staff
        +Date
        +Shift
        +Hours Worked
        +Task Description
        +Supporting Evidence
        +Approval Status
        +Approved By
        +Wage Integration Flag
    }
    class PayrollExport {
        +Export ID
        +Period Start
        +Period End
        +Warehouse
        +Attendance Metrics
        +Overtime Hours Total
        +Exceptions
        +Export File
    }
    class PayrollStaffSummary {
        +Staff
        +Present Days
        +Absent Days
        +Overtime Hours
        +Wages Amount
    }
    class AttendanceDeviceLog {
        +Log ID
        +Device ID
        +Event Time
        +Event Type
        +Status
        +Error Message
    }
    PayrollExport "1" -- "many" PayrollStaffSummary
```

---

## Configuration & Audit
```mermaid
classDiagram
    class SystemParameters {
        +Parameter Name
        +Parameter Value
        +Module Scope
        +Description
        +Last Updated By
        +Effective Date
    }
    class DecisionLog {
        +Decision ID
        +Topic
        +Stakeholders
        +Decision Details
        +Decision Date
        +Follow-up Actions
    }
    class AuditTrail {
        +Audit ID
        +Module
        +Record ID
        +Action
        +User
        +Timestamp
        +Before Snapshot
        +After Snapshot
        +Remarks
    }
```

Use these diagrams alongside the detailed data model tables to validate Creator form design, workflow automation, and reporting
schema coverage.
