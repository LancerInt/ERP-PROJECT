# Zoho Zia Prompts – Phase 1 Procure-to-Pay & Inventory Forms

Run the prompts in order after importing all master forms from `zia_master_form_prompts.md`. Each prompt stays within Zoho Zia's 5,000-character input cap and mirrors the authoritative data model definitions. Where a lookup targets a Phase 2 form (e.g., Work Order), note the reminder and add the lookup once that form exists.

## Prompt 1 – Purchase Request (PR)

Create form "Purchase Request" (link name purchase_request). Purpose: capture warehouse demand for goods/services/machinery with warehouse-scoped visibility and approval trail.
Fields:
- Auto-number field "PR No." (link name pr_no); required
- Date field "Request Date" (link name request_date); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Lookup (Godown Master) field "Godown" (link name godown); conditional; filter by selected warehouse when goods tracked in stock
- Lookup (Stakeholder User) field "Requested By" (link name requested_by); required
- Dropdown field "Requestor Role" (link name requestor_role); required; values: Warehouse Manager, Warehouse Coordinator
- Dropdown field "Requirement Type" (link name requirement_type); required; values: Goods, Services, Machinery
- Subform field "Lines" (link name lines); required
- Dropdown field "Priority" (link name priority); optional; values: Low, Medium, High
- Date field "Required By Date" (link name required_by_date); conditional when Requirement Type = Goods
- Multi-line field "Justification" (link name justification)
- File upload field "Attachments" (link name attachments); allow multiple
- Dropdown field "Approval Status" (link name approval_status); required; values: Draft, Pending, Approved, Rejected, Partially Approved
- Subform field "Approval Trail" (link name approval_trail); optional
- Multi-select Lookup (Stakeholder User/Role) field "Visibility Scope" (link name visibility_scope); optional; auto-share targets
- Lookup (BOM Request) field "Created From BOM Request" (link name created_from_bom_request); optional
- Multi-line field "Notes" (link name notes)

Subform "PR Lines" (link name lines):
- Number field "Line No." (link name line_no); required
- Lookup (Product) field "Product/Service" (link name product_service); required
- Multi-line field "Description Override" (link name description_override)
- Decimal field "Quantity Requested" (link name quantity_requested); required
- Dropdown field "UOM" (link name uom); required
- Date field "Required Date" (link name required_date)
- Dropdown field "Purpose" (link name purpose); values: Production, Maintenance, Consumable
- Lookup (Machine) field "Machine Reference" (link name machine_reference); optional
- Checkbox field "Allow RFQ Skip" (link name allow_rfq_skip)
- File upload field "Attachments" (link name attachments)
- Dropdown field "Status" (link name status); required; values: Pending, Approved, Rejected, Fulfilled
- Decimal field "Approved Quantity" (link name approved_quantity); optional

Subform "Approval Trail" (link name approval_trail):
- Dropdown field "Action" (link name action); required; values: Approved, Rejected, Partial
- Lookup (Stakeholder User) field "Actor" (link name actor); required
- Date-Time field "Action Date" (link name action_date); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 2 – RFQ Header

Create form "RFQ Header" (link name rfq_header). Purpose: manage requests for quotation linked to one or more approved PRs.
Fields:
- Auto-number field "RFQ No." (link name rfq_no); required
- Multi-select Lookup (Purchase Request) field "Linked PRs" (link name linked_prs); required
- Lookup (Stakeholder User) field "Created By" (link name created_by); required
- Date field "Creation Date" (link name creation_date); required
- Dropdown field "RFQ Mode" (link name rfq_mode); required; values: Email, Portal, Phone
- File upload field "RFQ Documents" (link name rfq_documents)
- Dropdown field "RFQ Status" (link name rfq_status); required; values: Open, Closed, Cancelled
- Number field "Quote Count Expected" (link name quote_count_expected)
- Checkbox field "Skip RFQ Flag" (link name skip_rfq_flag)
- Multi-line field "Skip RFQ Justification" (link name skip_rfq_justification); conditional when skip flag is checked
- Lookup (Stakeholder User) field "Purchase Manager Approval" (link name purchase_manager_approval); optional
- File upload field "Approval Attachment" (link name approval_attachment); optional
- Subform field "Dispatch ETA Updates" (link name dispatch_eta_updates); optional

Subform "Dispatch ETA Updates" (link name dispatch_eta_updates):
- Date-Time field "Update Date" (link name update_date); required
- Lookup (Stakeholder User) field "Updated By" (link name updated_by); required
- Date field "Expected Arrival" (link name expected_arrival); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 3 – Quote Response

Create form "Quote Response" (link name quote_response). Purpose: capture vendor quotations against an RFQ and PR lines.
Fields:
- Auto-number field "Quote ID" (link name quote_id); required
- Lookup (RFQ Header) field "RFQ" (link name rfq); required
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Date field "Quote Date" (link name quote_date); required
- Date field "Price Valid Till" (link name price_valid_till); optional
- Dropdown field "Currency" (link name currency); required
- Subform field "Quote Lines" (link name quote_lines); required
- Dropdown field "Freight Terms" (link name freight_terms); required; values: Paid, To_Pay, Mixed
- Dropdown field "Payment Terms" (link name payment_terms); required (prefill from vendor, allow override)
- Multi-line field "Delivery Terms" (link name delivery_terms)
- Number field "Lead Time (Days)" (link name lead_time_days)
- File upload field "Attachments" (link name attachments)
- Multi-line field "Remarks" (link name remarks)
- Decimal field "Evaluation Score" (link name evaluation_score); optional (computed)
- Checkbox field "Chosen Flag" (link name chosen_flag)

Subform "Quote Lines" (link name quote_lines):
- Lookup (PR Line) field "PR Line" (link name pr_line); required
- Lookup (Product) field "Product/Service" (link name product_service); required
- Multi-line field "Specification" (link name specification)
- Decimal field "Quantity Offered" (link name quantity_offered); required
- Dropdown field "UOM" (link name uom); required
- Currency field "Unit Price" (link name unit_price); required
- Decimal field "Discount %" (link name discount); optional
- Decimal field "GST %" (link name gst); required
- Currency field "Freight Charge" (link name freight_charge); optional
- Number field "Delivery Timeline" (link name delivery_timeline); optional; in days

## Prompt 4 – Quote Evaluation

Create form "Quote Evaluation" (link name quote_evaluation). Purpose: log comparative analysis, recommendation, and approval for RFQ responses.
Fields:
- Auto-number field "Evaluation ID" (link name evaluation_id); required
- Lookup (RFQ Header) field "RFQ" (link name rfq); required
- Date field "Evaluation Date" (link name evaluation_date); required
- Lookup (Stakeholder User) field "Evaluated By" (link name evaluated_by); required
- Subform field "Comparison Table" (link name comparison_table); required
- Checkbox field "Best Quote Flag" (link name best_quote_flag)
- Lookup (Vendor) field "Recommended Vendor" (link name recommended_vendor); optional
- Multi-line field "Justification Notes" (link name justification_notes); conditional when best quote not chosen
- Dropdown field "Approval Status" (link name approval_status); required; values: Pending, Approved, Rejected
- Subform field "Approval Trail" (link name approval_trail); optional; capture Purchase Manager approval

Subform "Comparison Table" (link name comparison_table):
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Currency field "Total Cost" (link name total_cost); required
- Number field "Lead Time" (link name lead_time); optional; days
- Dropdown field "Freight Terms" (link name freight_terms); optional
- Dropdown field "Payment Terms" (link name payment_terms); optional
- Decimal field "Score" (link name score); optional
- Multi-line field "Remarks" (link name remarks)

Subform "Approval Trail" (link name approval_trail):
- Lookup (Stakeholder User) field "Approver" (link name approver); required
- Dropdown field "Decision" (link name decision); required; values: Approved, Rejected
- Date-Time field "Decision Date" (link name decision_date); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 5 – Purchase Order (PO)

Create form "Purchase Order" (link name purchase_order). Purpose: issue approved orders with revision history, freight estimates, and commission tracking.
Fields:
- Auto-number field "PO No." (link name po_no); required
- Number field "Revision No." (link name revision_no); required; default 0
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Lookup (Company) field "Company" (link name company); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Multi-select Lookup (Purchase Request) field "Linked PRs" (link name linked_prs); required
- Lookup (RFQ Header) field "Linked RFQ" (link name linked_rfq); optional
- Date field "PO Date" (link name po_date); required
- Date field "Expected Delivery Start" (link name expected_delivery_start); optional
- Date field "Expected Delivery End" (link name expected_delivery_end); optional
- Dropdown field "Freight Terms" (link name freight_terms); required
- Dropdown field "Payment Terms" (link name payment_terms); required
- Dropdown field "Currency" (link name currency); required
- Subform field "PO Lines" (link name po_lines); required
- File upload field "Attachments" (link name attachments)
- Multi-line field "Terms & Conditions" (link name terms_and_conditions)
- Subform field "Approval Trail" (link name approval_trail); optional
- Dropdown field "Status" (link name status); required; values: Draft, Approved, Issued, Closed, Cancelled
- Checkbox field "Partial Receipt Flag" (link name partial_receipt_flag)

Subform "PO Lines" (link name po_lines):
- Number field "Line No." (link name line_no); required
- Lookup (Product) field "Product/Service" (link name product_service); required
- Multi-line field "Description" (link name description)
- Decimal field "Quantity Ordered" (link name quantity_ordered); required
- Dropdown field "UOM" (link name uom); required
- Currency field "Unit Price" (link name unit_price); required
- Decimal field "Discount %" (link name discount)
- Decimal field "GST %" (link name gst); required
- Currency field "Extra Commission" (link name extra_commission); optional
- Currency field "Agent Commission" (link name agent_commission); optional
- Currency field "Freight Estimate" (link name freight_estimate); optional
- Date field "Delivery Schedule" (link name delivery_schedule); optional
- Lookup (PR Line) field "Linked PR Line" (link name linked_pr_line); optional
- Lookup (Quote Line) field "Linked RFQ Line" (link name linked_rfq_line); optional
- Multi-line field "Batch Requirement Notes" (link name batch_requirement_notes)

Subform "Approval Trail" (link name approval_trail):
- Lookup (Stakeholder User) field "Approver" (link name approver); required
- Dropdown field "Action" (link name action); required; values: Approved, Rejected
- Date-Time field "Action Date" (link name action_date); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 6 – PO ETA Update

Create form "PO ETA Update" (link name po_eta_update). Purpose: log anticipated arrival revisions per PO.
Fields:
- Auto-number field "Update ID" (link name update_id); required
- Lookup (Purchase Order) field "PO" (link name po); required
- Date-Time field "Update Date" (link name update_date); required
- Lookup (Stakeholder User) field "Updated By" (link name updated_by); required (Purchase Coordinator or Warehouse Coordinator at Office)
- Date field "Expected Arrival Date" (link name expected_arrival_date); required
- Dropdown field "Status" (link name status); required; values: Pending, Updated
- Multi-line field "Remarks" (link name remarks)

## Prompt 7 – Receipt Advice (Inbound)

Create form "Receipt Advice" (link name receipt_advice). Purpose: record goods receipt, packing capture, freight, and wage details per inbound shipment.
Fields:
- Auto-number field "Receipt Advice No." (link name receipt_advice_no); required
- Date field "Receipt Date" (link name receipt_date); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Lookup (Godown Master) field "Godown" (link name godown); required; filter by warehouse context
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Multi-select Lookup (Purchase Order) field "Linked PO(s)" (link name linked_pos); required
- Single-line field "Vehicle Number" (link name vehicle_number)
- Single-line field "Driver Name" (link name driver_name)
- File upload field "Invoice Upload" (link name invoice_upload); required
- File upload field "Packing List Upload" (link name packing_list_upload)
- Subform field "Receipt Lines" (link name receipt_lines); required
- Subform field "Packing Material Lines" (link name packing_material_lines); optional
- Subform field "Freight Details" (link name freight_details); optional
- Subform field "Loading Unloading Wages" (link name loading_unloading_wages); optional
- Dropdown field "QC Routing" (link name qc_routing); required; values: Warehouse, QC Coordinator, QC Manager
- Dropdown field "QC Status" (link name qc_status); required; values: Pending, Pass, Fail, Hold
- Checkbox field "Partial Receipt Flag" (link name partial_receipt_flag)
- Multi-line field "Remarks" (link name remarks)
- Lookup (Stakeholder User) field "Created By" (link name created_by); required
- Date-Time field "Created Time" (link name created_time); required

Subform "Receipt Lines" (link name receipt_lines):
- Number field "Line No." (link name line_no); required
- Lookup (PO Line) field "PO Line" (link name po_line); required
- Lookup (Product) field "Product" (link name product); required
- Single-line field "Batch No." (link name batch_no); conditional when batch tracking enabled
- Date field "Expiry Date" (link name expiry_date); optional
- Decimal field "Quantity Received" (link name quantity_received); required
- Dropdown field "UOM" (link name uom); required
- Currency field "Extra Commission" (link name extra_commission); optional
- Currency field "Agent Commission" (link name agent_commission); optional
- Decimal field "Quantity Accepted" (link name quantity_accepted); optional
- Decimal field "Quantity Rejected" (link name quantity_rejected); optional
- Lookup (Godown Master) field "Godown Location" (link name godown_location); required; filtered by warehouse
- Multi-line field "Remarks" (link name remarks)

Subform "Packing Material Lines" (link name packing_material_lines):
- Lookup (Product) field "Packaging SKU" (link name packaging_sku); required; must be PACKING_MATERIAL
- Decimal field "Quantity" (link name quantity); required
- Dropdown field "UOM" (link name uom); required
- Dropdown field "Condition" (link name condition); optional; values: New, Damaged

Subform "Freight Details" (link name freight_details):
- Dropdown field "Freight Type" (link name freight_type); required; values: Local Drayage, Linehaul
- Lookup (Transporter) field "Transporter" (link name transporter); conditional when payable by company
- Dropdown field "Freight Terms" (link name freight_terms); required; values: Paid, To_Pay, Mixed
- Currency field "Tentative Charge" (link name tentative_charge); optional; pre-fill from PO
- Currency field "Discount" (link name discount); optional
- Dropdown field "Payable By" (link name payable_by); required; values: Company, Vendor
- Decimal field "Quantity Basis" (link name quantity_basis); optional; shipment quantity for cost-per-unit
- Dropdown field "Quantity UOM" (link name quantity_uom); optional; values include Tonnes, KG, KL, Units
- Dropdown field "Destination State" (link name destination_state); optional; auto from warehouse
- Decimal (Formula) field "Cost Per Unit (Calc)" (link name cost_per_unit_calc); calculated
Subform "Freight Payment Schedule" (link name payment_schedule):
- Dropdown field "Freight Type" (link name freight_type); required; values: Local Drayage, Linehaul
- Lookup (Transporter) field "Transporter" (link name transporter); conditional when payable by company
- Date field "Due Date" (link name due_date); required
- Currency field "Amount" (link name amount); required
- Decimal field "TDS %" (link name tds); optional
- Checkbox field "Reminder Flag" (link name reminder_flag); optional


Subform "Loading Unloading Wages" (link name loading_unloading_wages):
- Dropdown field "Wage Type" (link name wage_type); required; values: Loading, Unloading
- Lookup (Vendor) field "Contractor Vendor" (link name contractor_vendor); conditional when payable by company
- Currency field "Amount" (link name amount); required
- Decimal field "TDS Applicable %" (link name tds_applicable); optional
- Dropdown field "Payable By" (link name payable_by); required; values: Company, Vendor
- Multi-line field "Remarks" (link name remarks)

## Prompt 8 – QC Request (Inbound)

Create form "QC Request" (link name qc_request). Purpose: trigger inbound QC checks from receipt advice with traceable parameter selection.
Fields:
- Auto-number field "Request No." (link name request_no); required
- Date field "Request Date" (link name request_date); required
- Lookup (Stakeholder User) field "Requested By" (link name requested_by); required; warehouse roles
- Dropdown field "Requestor Role" (link name requestor_role); required; values: Warehouse Supervisor, Warehouse Coordinator, Warehouse Manager
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Lookup (Product) field "Product" (link name product); required
- Single-line field "Batch" (link name batch); conditional when applicable
- Dropdown field "Stage" (link name stage); required; values: Receipt, In-Process, Finished, Sales Return
- Lookup (Template Library) field "QC Template" (link name qc_template); required
- Subform field "Selected Parameters" (link name selected_parameters); optional
- Image upload field "Sample Photo" (link name sample_photo); required
- Decimal field "Sample Qty" (link name sample_qty); optional
- Dropdown field "Priority" (link name priority); optional; values: Normal, Urgent
- Multi-line field "Remarks" (link name remarks)
- Dropdown field "Status" (link name status); required; values: Requested, In Progress, Completed
- Single-line field "Lab Code" (link name lab_code); optional (can be system-generated)
- Checkbox field "Counter Sample Required" (link name counter_sample_required)

Subform "Selected Parameters" (link name selected_parameters):
- Lookup (QC Parameter Library) field "Parameter" (link name parameter); required
- Checkbox field "Critical" (link name critical); optional; highlight key tests
- Multi-line field "Notes" (link name notes)

## Prompt 9 – Freight Advice (Inbound)

Create form "Freight Advice" (link name freight_advice). Purpose: draft inbound freight payable advice with cost-per-unit reporting, approved by Finance Manager.
Fields:
- Auto-number field "Advice No." (link name advice_no); required
- Dropdown field "Direction" (link name direction); required; default value Inbound
- Lookup (Receipt Advice) field "Receipt Advice" (link name receipt_advice); required
- Lookup (Transporter) field "Transporter" (link name transporter); required
- Dropdown field "Freight Type" (link name freight_type); required; values: Local Drayage, Linehaul
- Lookup (Stakeholder User) field "Created By" (link name created_by); required; Freight Coordinator
- Date field "Created Date" (link name created_date); required
- Currency field "Base Amount" (link name base_amount); required
- Currency field "Discount" (link name discount); optional
- Currency field "Loading Wages Amount" (link name loading_wages_amount); optional
- Currency field "Unloading Wages Amount" (link name unloading_wages_amount); optional
- Decimal field "Quantity Basis" (link name quantity_basis); optional; shipment quantity
- Dropdown field "Quantity UOM" (link name quantity_uom); optional; Tonnes, KG, KL, Units
- Decimal (Formula) field "Cost Per Unit (Calc)" (link name cost_per_unit_calc); calculated
- Dropdown field "Destination State" (link name destination_state); optional
- Currency field "Payable Amount" (link name payable_amount); required
- Subform field "Payment Schedule" (link name payment_schedule); optional
- Subform field "Approval Workflow" (link name approval_workflow); optional
- Dropdown field "Status" (link name status); required; values: Draft, Pending Approval, Approved, Paid

Subform "Payment Schedule" (link name payment_schedule):
- Dropdown field "Freight Type" (link name freight_type); required; inherit from advice
- Lookup (Transporter) field "Transporter" (link name transporter); optional; inherit from advice
- Date field "Due Date" (link name due_date); required
- Currency field "Amount" (link name amount); required
- Decimal field "TDS %" (link name tds); optional
- Checkbox field "Reminder Flag" (link name reminder_flag); optional; drive reminders on due date

Subform "Approval Workflow" (link name approval_workflow):
- Dropdown field "Stage" (link name stage); required; values: Draft Review, Finance Approval
- Lookup (Stakeholder User) field "Approver" (link name approver); required (Finance Manager at minimum)
- Dropdown field "Decision" (link name decision); required; values: Pending, Approved, Rejected
- Date-Time field "Decision Date" (link name decision_date); required when decision != Pending
- Multi-line field "Remarks" (link name remarks)

## Prompt 10 – Vendor Payment Advice (Warehouse Draft)

Create form "Vendor Payment Advice" (link name vendor_payment_advice). Purpose: allow Warehouse Coordinator (Office) to initiate payment advice for PO, receipt, freight, or wage documents before finance approval.
Fields:
- Auto-number field "Advice No." (link name advice_no); required
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Dropdown field "Source Document Type" (link name source_document_type); required; values: PO, Receipt, Freight, Wage, Credit Note
- Lookup field "Source Document" (link name source_document); required; configure dynamic lookups per document type after form creation
- Currency field "Amount" (link name amount); required
- Subform field "Tax Components" (link name tax_components); optional
- Date field "Due Date" (link name due_date); required
- Dropdown field "Payment Method" (link name payment_method); required; values: Bank Transfer, Cash, Cheque, UPI
- Lookup (Stakeholder User) field "Prepared By" (link name prepared_by); required
- Subform field "Approval Workflow" (link name approval_workflow); required; capture Finance Manager then Office Manager approval
- Dropdown field "Status" (link name status); required; values: Draft, Pending, Approved, Paid, On Hold
- Multi-line field "Notes" (link name notes)

Subform "Tax Components" (link name tax_components):
- Dropdown field "Tax Type" (link name tax_type); required; values: TDS, TCS
- Decimal field "Rate %" (link name rate); required
- Currency field "Amount" (link name amount); required

Subform "Approval Workflow" (link name approval_workflow):
- Dropdown field "Stage" (link name stage); required; values: Finance Manager Review, Office Manager Authorization
- Lookup (Stakeholder User) field "Approver" (link name approver); required
- Dropdown field "Decision" (link name decision); required; values: Pending, Approved, Rejected
- Date-Time field "Decision Date" (link name decision_date); required when decision != Pending
- Multi-line field "Remarks" (link name remarks)

## Prompt 11 – Payment Advice Workflow (Finance Execution)

Create form "Payment Advice" (link name payment_advice). Purpose: Finance Manager prepares and Office Manager authorises final payments referencing approved documents.
Fields:
- Auto-number field "Advice No." (link name advice_no); required
- Dropdown field "Beneficiary Type" (link name beneficiary_type); required; values: Vendor, Transporter, Contractor
- Lookup (Vendor/Transporter) field "Beneficiary" (link name beneficiary); required
- Lookup field "Source Document" (link name source_document); required; configure lookup to approved Vendor Payment Advice or direct Receipt/Freight/Wage documents
- Currency field "Amount" (link name amount); required
- Subform field "TDS/TCS Details" (link name tds_tcs_details); optional
- Date field "Due Date" (link name due_date); required
- Dropdown field "Payment Method" (link name payment_method); required; values: Bank Transfer, Cash, Cheque, UPI
- Lookup (Vendor Bank Details) field "Bank Account" (link name bank_account); conditional for bank transfer
- Lookup (Stakeholder User) field "Prepared By" (link name prepared_by); required
- Date field "Prepared Date" (link name prepared_date); required
- Subform field "Finance Manager Approval" (link name finance_manager_approval); required
- Subform field "Office Manager Authorization" (link name office_manager_authorization); required
- Dropdown field "Payment Status" (link name payment_status); required; values: Draft, Pending Finance, Pending Authorization, Approved, Paid
- Single-line field "Payment Reference" (link name payment_reference); optional
- File upload field "Attachments" (link name attachments); optional (bank proof)

Subform "TDS/TCS Details" (link name tds_tcs_details):
- Dropdown field "Tax Type" (link name tax_type); required; values: TDS, TCS
- Single-line field "Section" (link name section); optional
- Decimal field "Rate %" (link name rate); required
- Currency field "Amount" (link name amount); required

Subform "Finance Manager Approval" (link name finance_manager_approval):
- Lookup (Stakeholder User) field "Approved By" (link name approved_by); required
- Date-Time field "Approval Date" (link name approval_date); required
- Multi-line field "Remarks" (link name remarks)

Subform "Office Manager Authorization" (link name office_manager_authorization):
- Lookup (Stakeholder User) field "Authorized By" (link name authorized_by); required
- Date-Time field "Authorization Date" (link name authorization_date); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 12 – Inventory Ledger

Create form "Inventory Ledger" (link name inventory_ledger). Purpose: maintain FIFO-based stock movement per warehouse, godown, and batch.
Fields:
- Auto-number field "Ledger Entry ID" (link name ledger_entry_id); required
- Date field "Transaction Date" (link name transaction_date); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Lookup (Godown Master) field "Godown" (link name godown); required; filter by warehouse context
- Lookup (Product) field "Product" (link name product); required
- Single-line field "Batch" (link name batch); optional
- Decimal field "Quantity In" (link name quantity_in); optional
- Decimal field "Quantity Out" (link name quantity_out); optional
- Dropdown field "UOM" (link name uom); required
- Dropdown field "Transaction Type" (link name transaction_type); required; values: Receipt, Issue, Transfer, Adjustment, Dispatch
- Lookup field "Source Document" (link name source_document); required; configure to support Receipt Advice, Material Issue, Stock Transfer, etc.
- Currency field "Cost" (link name cost); optional; store valuation per entry
- Dropdown field "Status" (link name status); required; values: Available, In Transit, Reserved
- Single-line field "FIFO Layer ID" (link name fifo_layer_id); optional
- Multi-line field "Remarks" (link name remarks)

## Prompt 13 – Material Issue (Machine Spares / Production)

Create form "Material Issue" (link name material_issue). Purpose: track issuance of raw materials, packing materials, or machine spares against work orders with approval by warehouse manager.
Fields:
- Auto-number field "Issue No." (link name issue_no); required
- Date field "Issue Date" (link name issue_date); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Lookup (Work Order) field "Work Order" (link name work_order); required – if the production Work Order form is not yet available, create the form first or revisit this lookup later
- Lookup (Stakeholder User) field "Issued By" (link name issued_by); required
- Lookup (Stakeholder User) field "Approved By" (link name approved_by); optional (Warehouse Manager)
- Subform field "Issue Lines" (link name issue_lines); required
- Multi-line field "Remarks" (link name remarks)

Subform "Issue Lines" (link name issue_lines):
- Lookup (Product) field "Product" (link name product); required
- Single-line field "Batch Out" (link name batch_out); conditional when batch tracking applies
- Lookup (Godown Master) field "Godown" (link name godown); required; filter by warehouse context
- Decimal field "Quantity Issued" (link name quantity_issued); required
- Dropdown field "UOM" (link name uom); required
- Checkbox field "Reserved for Template" (link name reserved_for_template); optional; tick when issuing reserved packing material

## Prompt 14 – Wage Voucher (Production / Loading Support)

Create form "Wage Voucher" (link name wage_voucher). Purpose: initiate wage advice for production or loading/unloading tasks with finance approval. Note: requires the Work Order form from the Production module; if unavailable, create a placeholder Work Order form before running this prompt.
Fields:
- Auto-number field "Voucher No." (link name voucher_no); required
- Lookup (Work Order) field "Work Order" (link name work_order); required
- Dropdown field "Wage Type" (link name wage_type); required; values: Template Rate, Headcount
- Lookup (Vendor) field "Contractor Vendor" (link name contractor_vendor); conditional for contractor payouts
- Multi-select Lookup (Staff) field "Staff Group" (link name staff_group); conditional for headcount wages
- Subform field "Hours / Tasks" (link name hours_tasks); required
- Currency field "Amount" (link name amount); required
- Decimal field "TDS %" (link name tds); optional
- Lookup (Stakeholder User) field "Prepared By" (link name prepared_by); required; Warehouse Coordinator (Office)
- Date field "Prepared Date" (link name prepared_date); required
- Subform field "Approval Workflow" (link name approval_workflow); required; Warehouse Coordinator (Office) → Finance Manager
- Dropdown field "Status" (link name status); required; values: Draft, Pending, Approved, Paid
- Multi-line field "Remarks" (link name remarks)

Subform "Hours / Tasks" (link name hours_tasks):
- Lookup (Staff) field "Staff" (link name staff); optional (mandatory for headcount wages)
- Multi-line field "Task Description" (link name task_description); required
- Decimal field "Hours Worked" (link name hours_worked); optional
- Decimal field "Quantity Produced" (link name quantity_produced); optional (for incentive tracking)

Subform "Approval Workflow" (link name approval_workflow):
- Lookup (Stakeholder User) field "Approver" (link name approver); required
- Date-Time field "Approval Date" (link name approval_date); required
- Multi-line field "Remarks" (link name remarks); optional

## Prompt 15 – Bank Statement Upload

Create form "Bank Statement Upload" (link name bank_statement_upload). Purpose: capture daily bank statements for automated reconciliation against payables/receivables.
Fields:
- Auto-number field "Upload ID" (link name upload_id); required
- Dropdown field "Bank Account" (link name bank_account); required; populate with configured accounts
- Date field "Statement Period Start" (link name statement_period_start); required
- Date field "Statement Period End" (link name statement_period_end); required
- Date field "Upload Date" (link name upload_date); required
- File upload field "Statement File" (link name statement_file); required; accept PDF or CSV
- Dropdown field "Parsing Status" (link name parsing_status); required; values: Pending, Parsed, Error
- Subform field "Auto-Matched Entries" (link name auto_matched_entries); optional
- Subform field "Exceptions" (link name exceptions); optional
- Multi-line field "Remarks" (link name remarks)

Subform "Auto-Matched Entries" (link name auto_matched_entries):
- Single-line field "Statement Line ID" (link name statement_line_id); required
- Dropdown field "Match Type" (link name match_type); required; values: Payable, Receivable
- Lookup (Vendor Ledger/Customer Ledger) field "Linked Document" (link name linked_document); required
- Currency field "Amount" (link name amount); required
- Dropdown field "Status" (link name status); required; values: Confirmed, Pending

Subform "Exceptions" (link name exceptions):
- Single-line field "Statement Line ID" (link name statement_line_id); required
- Date field "Transaction Date" (link name transaction_date); required
- Currency field "Amount" (link name amount); required
- Lookup (Ledger) field "Suggested Match" (link name suggested_match); optional
- Multi-line field "Exception Notes" (link name exception_notes)
- Dropdown field "Resolution Status" (link name resolution_status); required; values: Open, Resolved

## Prompt 16 – Vendor Ledger

Create form "Vendor Ledger" (link name vendor_ledger). Purpose: maintain vendor-facing debit/credit balances with ageing.
Fields:
- Auto-number field "Ledger ID" (link name ledger_id); required
- Lookup (Vendor) field "Vendor" (link name vendor); required
- Dropdown field "Document Type" (link name document_type); required; values: PO, Receipt, Invoice, Freight, Wage, Credit Note
- Lookup field "Document Reference" (link name document_reference); required; configure lookups to relevant source forms
- Date field "Document Date" (link name document_date); required
- Currency field "Debit Amount" (link name debit_amount); optional
- Currency field "Credit Amount" (link name credit_amount); optional
- Subform field "Tax Breakdown" (link name tax_breakdown); optional
- Date field "Due Date" (link name due_date); optional
- Dropdown field "Payment Status" (link name payment_status); required; values: Not Due, Partially Paid, Paid, Overdue
- Dropdown field "Ageing Bucket" (link name ageing_bucket); optional; values: 0-30, 31-60, >60
- Multi-line field "Notes" (link name notes)

Subform "Tax Breakdown" (link name tax_breakdown):
- Dropdown field "Tax Type" (link name tax_type); required; values: GST, TDS, TCS
- Decimal field "Rate %" (link name rate); required
- Currency field "Amount" (link name amount); required

## Prompt 17 – Freight Ledger

Create form "Freight Ledger" (link name freight_ledger). Purpose: track freight obligations, payments, and cost-per-unit analytics by transporter and destination.
Fields:
- Auto-number field "Ledger ID" (link name ledger_id); required
- Dropdown field "Direction" (link name direction); required; values: Inbound, Outbound, Transfer
- Lookup (Transporter) field "Transporter" (link name transporter); required
- Lookup (Freight Advice) field "Freight Advice" (link name freight_advice); required
- Currency field "Amount" (link name amount); required
- Currency field "Discount" (link name discount); optional
- Decimal field "Shipment Quantity" (link name shipment_quantity); optional
- Dropdown field "Quantity UOM" (link name quantity_uom); optional
- Decimal field "Cost Per Unit" (link name cost_per_unit); optional; store computed result
- Dropdown field "Destination State" (link name destination_state); optional
- Subform field "Payment Schedule" (link name payment_schedule); optional
- Currency field "Amount Paid" (link name amount_paid); optional
- Currency field "Balance" (link name balance); required
- Checkbox field "Reminder Flag" (link name reminder_flag); optional; trigger reminders at due date
- Multi-line field "Notes" (link name notes)

Subform "Payment Schedule" (link name payment_schedule):
- Date field "Due Date" (link name due_date); required
- Currency field "Amount" (link name amount); required
- Decimal field "TDS %" (link name tds); optional
- Checkbox field "Reminder Flag" (link name reminder_flag); optional

## Prompt 18 – Wage Ledger

Create form "Wage Ledger" (link name wage_ledger). Purpose: consolidate wage vouchers, weekly payouts, and settlement method for finance reporting.
Fields:
- Auto-number field "Ledger ID" (link name ledger_id); required
- Lookup (Wage Voucher) field "Wage Voucher" (link name wage_voucher); required
- Lookup (Vendor or Staff) field "Contractor/Staff Group" (link name contractor_staff_group); required
- Currency field "Amount" (link name amount); required
- Decimal field "TDS %" (link name tds); optional
- Date field "Payment Week" (link name payment_week); required (week-ending date)
- Dropdown field "Approval Status" (link name approval_status); required; values: Draft, Pending, Approved, Paid
- Dropdown field "Settlement Method" (link name settlement_method); required; values: Bank Transfer, Cash
- Multi-line field "Notes" (link name notes)

