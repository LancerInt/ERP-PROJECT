# Zoho Creator ERP Module Flowcharts

This document provides module-specific process flowcharts derived from the master blueprint. Each diagram highlights primary forms, decision points, and role hand-offs. Use these visual references while configuring Zoho Creator workflows and approvals.

## Purchase Module
```mermaid
flowchart TD
    subgraph Intake[Request & RFQ]
        PR[PR raised\n(Warehouse Coord/Manager)] --> APRV{Approve / Partial Approve?\n(Purchase Coord/Manager)}
        APRV -->|Reject| PRReject[Notify requester & close PR]
        APRV -->|Approve lines| RFQGen[Auto-create RFQ draft with shortlisted vendors]\n:::auto
        APRV -->|Partial| PRPartial[Store approved qty per line + justification]
        RFQGen --> RFQSend[Send RFQ to vendors / allow bypass per line]
        RFQSend --> Quotes[Vendor quotes captured per PR line]
    end

    subgraph Evaluation[Evaluation & PO]
        Quotes --> Eval[Quote evaluation & audit log]
        Eval --> PMDecision{Purchase Manager decision?}
        PMDecision -->|Approve| POCreation[Auto-create PO + rev tracking]\n:::auto
        PMDecision -->|Revision Needed| Reopen[Reopen RFQ / adjust specs]
        PMDecision -->|Reject| ClosePR[Close PR]
    end

    subgraph Fulfilment[Receipt, QC & Freight]
        POCreation --> ETA[Update expected arrival dates]
        ETA --> InvoiceScan[Scan vendor invoice]
        InvoiceScan --> RA[Auto-create Receipt Advice (multi-PO) + lines]\n:::auto
        RA --> QCReq{QC required by product?}
        QCReq -->|Yes| QCAuto[Auto-create QC request with template]\n:::auto
        QCReq -->|No| SkipQC[Bypass QC]
        RA --> FreightDraft[Auto-draft inbound freight & wage schedules]\n:::auto
    end

    subgraph Settlement[Payments]
        QCAuto --> QCOutcome{QC result}
        SkipQC --> QCOutcome
        QCOutcome -->|Pass| PayDraft[Auto-create vendor payment advice after credit terms]\n:::auto
        QCOutcome -->|Fail| CreditNote[Notify stakeholders & draft credit note]\n:::auto
        FreightDraft --> FreightApproval[Finance Manager approval]
        PayDraft --> BankRecon[Bank upload auto-match]\n:::auto
        FreightApproval --> BankRecon
    end

    classDef auto fill:#e0f7ff,stroke:#00a6fb,stroke-width:1px;
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
    BOMCalc --> Issue["Material Issue\\n(Warehouse Stores)"]
    Issue --> WO[Work Order / Batch Created]
    WO --> Stage1[Mixing / Production]
    Stage1 --> Stage2[Packing / Filling]
    Stage2 --> Stage3[QC Sample Submission]
    Stage3 --> QCDecision{QC Outcome?}
    QCDecision -->|Pass| CloseBatch[Batch Closed & Inventory Updated]
    QCDecision -->|Reformulate| Rework[Create Rework Batch]
    QCDecision -->|Fail| Scrap[Notify & Scrap / Return]
    WO --> WageCalc["Wage Calculation\\n(Template or Headcount)"]
    WageCalc --> WageDraft["Wage Advice Draft\\n(Warehouse Coordinator Office)"]
    WageDraft --> WageApproval["Finance Manager Approval"]
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
    InTransit --> FreightDraft["Freight Advice Draft\\n(Freight Coordinator)"]
    FreightDraft --> FinanceApprove["Finance Manager Approval"]
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
    FreightTerms --> DraftAdvice["Freight Advice Draft\\n(Freight Coordinator)"]
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
    ReceiptJW --> QCCheck["QC Workflow (if required)"]
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
    NormalFlow --> OfficeApprove["Warehouse Coordinator (Office) Approval"]
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
    Overtime --> OfficeReview["Warehouse Coordinator (Office) Review"]
    OfficeReview --> FinanceWage[Finance Wage Processing]
    Attendance --> LeaveReq[Leave / Permission Request]
    LeaveReq --> ApproveLeave{Approved by HR Coordinator?}
    ApproveLeave -->|Yes| CalendarUpdate[Update Attendance Calendar]
    ApproveLeave -->|No| NotifyStaff[Notify Decision]
    Attendance --> Reports[HO HR Reports & Payroll Export]
```
