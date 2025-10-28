# Zoho Creator ERP Module Flowcharts

This document provides module-specific process flowcharts derived from the master blueprint. Each diagram highlights primary forms, decision points, and role hand-offs. Use these visual references while configuring Zoho Creator workflows and approvals.

## Purchase Module
```mermaid
flowchart TD
    PR[Purchase Request\nWarehouse Coordinator / Manager] --> APPR{HO Purchase Approval?}
    APPR -->|Approve| RFQ[RFQ Creation\nPurchase Coordinator]
    APPR -->|Reject| PRClose[Request Closed]
    RFQ --> QuoteLoop{RFQ Required?}
    QuoteLoop -->|Yes| QColl[Collect Vendor Quotes]
    QuoteLoop -->|No| SkipNote[Skip RFQ Approval\nPurchase Manager]
    QColl --> Eval[Quote Evaluation & Justification]
    SkipNote --> Eval
    Eval --> PMApprove{Purchase Manager Approves?}
    PMApprove -->|Approved| PO[Purchase Order Issued]
    PMApprove -->|Revision Needed| Revise[Revise Specs / Reopen RFQ]
    PMApprove -->|Rejected| PRClose
    PO --> ETA[Update Anticipated Arrival]
    ETA --> RA[Receipt Advice\nWarehouse Coordinator]
    RA --> QCCheck{QC Required?}
    QCCheck -->|Pass| StockIn[Inventory Update]
    QCCheck -->|Fail| NCR[Notify HO & Credit Note]
    RA --> FreightAdvice[Freight Advice Draft\nFreight Coordinator]
    FreightAdvice --> FreightApproval[Finance Manager Approval]
    StockIn --> PayAdvice[Vendor Payment Advice\nFinance Manager]
    PayAdvice --> Recon[Bank Reconciliation]
```

## Sales Module
```mermaid
flowchart TD
    CPO[Customer PO Upload\nSales Coordinator] --> Parse[AI Parsing & Validation]
    Parse --> DraftSO[Draft Sales Order]
    DraftSO --> ApproveSO{SO Approved by\nSales Manager/Coordinator?}
    ApproveSO -->|Yes| AssignWH[Assign Warehouse & Pricelist]
    ApproveSO -->|No| Clarify[Clarify with Customer]
    AssignWH --> InvChk{Stock Available?}
    InvChk -->|Yes| DCInit[Dispatch Challan Draft]
    InvChk -->|No| ProdPlan[Trigger Production / Purchase]
    DCInit --> FreightInfo[Capture Transport & Freight Terms]
    FreightInfo --> DCCreate[Dispatch Challan Issued]
    DCCreate --> Invoice[Invoice Verification\nvs Statutory Copy]
    Invoice --> Variance{Variance Detected?}
    Variance -->|No| InvoiceAccept[Invoice Accepted]
    Variance -->|Yes| Escalate[Notify Office & Sales Managers]
    InvoiceAccept --> Receivable[Accounts Receivable]
    InvoiceAccept --> FreightAdvice[Outbound Freight Advice]
    FreightAdvice --> FinanceApprove[Finance Manager Approval]
    Receivable --> Collections[Payment Tracking & Reminders]
```

## Production Module
```mermaid
flowchart TD
    BOMReq[BOM Request\nWarehouse Coordinator] --> WMApprove{Warehouse Manager Approval?}
    WMApprove -->|Approved| BOMCalc[Auto Calculate Inputs & Shortfall]
    WMApprove -->|Rejected| CloseReq[Request Closed]
    BOMCalc --> Issue[Material Issue\n Warehouse Stores]
    Issue --> WO[Work Order / Batch Created]
    WO --> Stage1[Mixing / Production]
    Stage1 --> Stage2[Packing / Filling]
    Stage2 --> Stage3[QC Sample Submission]
    Stage3 --> QCDecision{QC Outcome?}
    QCDecision -->|Pass| CloseBatch[Batch Closed & Inventory Updated]
    QCDecision -->|Reformulate| Rework[Create Rework Batch]
    QCDecision -->|Fail| Scrap[Notify & Scrap / Return]
    WO --> WageCalc[Wage Calculation\n Template or Headcount]
    WageCalc --> WageApproval[Finance Approval Workflow]
```

## Quality Control Module
```mermaid
flowchart TD
    SampleReq[QC Request\nWarehouse Supervisor/Coordinator] --> ParamSel[Parameter Selection]
    ParamSel --> SamplePhoto[Upload Sample Photo]
    SamplePhoto --> QCAck[QC Coordinator Acknowledges & Assigns Lab Code]
    QCAck --> AssignAnalyst[Assign QC Analyst Jobs]
    AssignAnalyst --> Analyses[Analysts Record Results & Photos]
    Analyses --> AllDone{All Job Orders Complete?}
    AllDone -->|No| Pending[Await Remaining Tests]
    AllDone -->|Yes| FinalReport[QC Coordinator/Manager Drafts Report]
    FinalReport --> SignOff[Digital Signature & Release]
    SignOff --> ShareResult[Auto-share with Warehouse & Stakeholders]
    SignOff --> CounterSample[Counter Sample Register]
    CounterSample --> Reminder[Overdue Return Reminder]
```

## Inventory & Stock Transfer Module
```mermaid
flowchart TD
    TransferReq[Stock Transfer Request\nSending Warehouse] --> DraftDC[Transfer DC Draft]
    DraftDC --> LoadWage[Record Loading Wages]
    DraftDC --> InTransit[Mark Inventory In-Transit]
    InTransit --> FreightAdvice[Draft Local Drayage Freight Advice]
    FreightAdvice --> HOApprove[Warehouse Coordinator Office Approval]
    HOApprove --> FinanceApprove[Finance Manager Approval]
    InTransit --> ReceiptAdvice[Receiving Warehouse Receipt Advice]
    ReceiptAdvice --> QCCheck{QC Required?}
    QCCheck -->|Pass| StockUpdate[Inventory Updated & Batch Stored]
    QCCheck -->|Fail| Exception[Notify for Investigation]
```

## Finance Module
```mermaid
flowchart TD
    VendorBill[Vendor Invoice / Freight / Wage Inputs] --> Validate[3-Way Match & QC Status]
    Validate --> PayWorkflow[Payment Advice Draft\nFinance Manager]
    PayWorkflow --> OfficeMgrAuth[Office Manager Authorization]
    OfficeMgrAuth --> BankUpload[Payment Execution & Bank Statement]
    BankUpload --> ReconDaily[Daily Bank Statement Upload]
    ReconDaily --> AutoMatch[Auto Reconciliation]
    AutoMatch --> Exceptions{Unmatched Entries?}
    Exceptions -->|No| CloseCycle[Ledger Updated & Locked Monthly]
    Exceptions -->|Yes| Investigate[Finance Investigation & Adjustments]
    Receivables[Customer Payments Due] --> Reminder[Auto Reminder After 2 Weeks]
    Reminder --> FollowUp[Sales & Finance Follow-up]
```

## Logistics & Freight Coordination
```mermaid
flowchart TD
    Trigger[Inbound/Outbound Movement] --> FreightTerms[Read Freight Terms]
    FreightTerms --> DraftAdvice[Draft Freight Advice]
    DraftAdvice --> Discount[Optional Discount & TDS]
    Discount --> ApprovalFlow[Finance Manager Approval]
    ApprovalFlow --> PaymentSchedule[Set Payment Schedule]
    PaymentSchedule --> Reminder[Reminder on Schedule Due Date]
    PaymentSchedule --> Ledger[Update Transporter Ledger]
```

## Job Work Module
```mermaid
flowchart TD
    JWReq[Job Work Request\nWarehouse Coordinator] --> TemplateSel[Select Job Work Template]
    TemplateSel --> IssueRM[Issue Raw Material / Machine]
    IssueRM --> DispatchJW[Job Work DC]
    DispatchJW --> FreightDraft[Freight & Wage Drafts]
    DispatchJW --> VendorProc[Vendor Processing]
    VendorProc --> ReceiptJW[Job Work Receipt Advice]
    ReceiptJW --> Partial{Partial Receipt?}
    Partial -->|Yes| UpdatePending[Keep Balance Open]
    Partial -->|No| CloseJW[Close Job Work Order]
    ReceiptJW --> QCCheck[QC Workflow if required]
    QCCheck --> WageFinance[Process Job Work Charges & Freight Payments]
```

## Sales Return Module
```mermaid
flowchart TD
    ReturnReq[Sales Return Advice\nWarehouse / Customer] --> Approval{Sales/Office Manager Approval?}
    Approval -->|Rejected| CloseReturn[Return Closed]
    Approval -->|Approved| Receive[Receive Goods & Capture Packing]
    Receive --> QCOutcome{QC Result}
    QCOutcome -->|Resaleable| Restock[Restock Inventory]
    QCOutcome -->|Reformulate| SendProd[Create Reformulation Batch]
    QCOutcome -->|Scrap| ScrapDispose[Dispose & Record Loss]
    Receive --> FreightCost[Freight & Wage Drafts]
    FreightCost --> FinanceApproval[Finance Manager Approval]
    Restock --> DebitNote[Debit Note Generation]
```

## Stock Adjustment Module
```mermaid
flowchart TD
    AdjReq[Adjustment Request\nWarehouse Coordinator/Manager] --> ReasonSel[Select Reason & Upload Evidence]
    ReasonSel --> Threshold{Value > ₹25,000?}
    Threshold -->|Yes| Escalate[Notify Office Manager & Finance]
    Threshold -->|No| NormalFlow[Proceed]
    NormalFlow --> OfficeApprove[Warehouse Coordinator Office Approval]
    Escalate --> OfficeApprove
    OfficeApprove --> UpdateStock[Update Inventory & Ledger]
    UpdateStock --> MonthlyRpt[Monthly Adjustment Report]
```

## Attendance & HR Module
```mermaid
flowchart TD
    StaffCreate[Staff Creation\nWarehouse HR Coordinator] --> HOApprove{HO HR Approval?}
    HOApprove -->|Approved| ActiveStaff[Active Staff Record]
    HOApprove -->|Rejected| ReviseStaff[Revise Submission]
    ActiveStaff --> ShiftAssign[Assign Shifts & Overtime Eligibility]
    ShiftAssign --> Attendance[Daily Attendance Capture\nGeo + Face Match]
    Attendance --> Overtime[Overtime Request]
    Overtime --> OfficeReview[Warehouse Coordinator Office Review]
    OfficeReview --> FinanceWage[Finance Wage Processing]
    Attendance --> LeaveReq[Leave / Permission Request]
    LeaveReq --> ApproveLeave{Approved by HR Coordinator?}
    ApproveLeave -->|Yes| CalendarUpdate[Update Attendance Calendar]
    ApproveLeave -->|No| NotifyStaff[Notify Decision]
    Attendance --> Reports[HO HR Reports & Payroll Export]
```
```
