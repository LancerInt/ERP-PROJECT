# Purchase Module Automation (Deluge)

This guide lists the Deluge workflows that auto-create downstream artifacts in the Purchase module. Each snippet is written for Zoho Creator form workflows and assumes standard library functions (`zoho.creator.createRecord`, `getRecords`, etc.).

## Automation Matrix
- **PR approval → RFQ draft**: One-click generation of RFQ lines from approved PR lines, attaching specs/photos and vendor shortlist.
- **Quote approval → PO**: Creates PO header and lines from the approved quote, preserves PR/RFQ linkage, and bumps PO revision when regenerated.
- **Receipt advice from invoice scan**: Maps scanned invoice lines to PO lines, supports multi-PO receipts and partial quantities.
- **Freight payable draft**: Creates freight payable advice based on receipt advice freight terms (local drayage, linehaul, loading/unloading wages, discounts).
- **QC outcome → Payment advice or Credit Note notification**: Generates payment advice on pass (respecting vendor credit terms) or notifies stakeholders and prepares credit note on fail.
- **Bank statement upload → auto-match payments**: Parses bank uploads and matches against open payment advice.

## Snippets

### 1) PR approval → RFQ draft (single click)
```javascript
// Form: Purchase_Request | Event: On Success (Approval button)
// Input: input.PR_ID, input.approved_lines (collection of line IDs)
if(input.approval_status == "Approved")
{
    pr_lines = Purchase_Request_Lines[ID in input.approved_lines];
    vendor_shortlist = Vendor_Shortlist[PR_ID == input.PR_ID].Vendor; // optional lookup list

    rfq_data = {
        "PR" : input.PR_ID,
        "warehouse" : input.warehouse,
        "status" : "Draft",
        "requested_by" : zoho.loginuser,
        "attachments" : input.attachments // specs/photos
    };
    rfq = zoho.creator.createRecord("ERP_PRO", "RFQ_Header", rfq_data);

    for each  line in pr_lines
    {
        rfq_line = {
            "RFQ_Header" : rfq.get("ID"),
            "Product" : line.Product,
            "UOM" : line.UOM,
            "Quantity" : line.Approved_Quantity,
            "Allow_RFQ_Bypass" : line.RFQ_Bypass,
            "Specs" : line.Specification,
            "Photo" : line.Photo
        };
        zoho.creator.createRecord("ERP_PRO", "RFQ_Lines", rfq_line);
    }

    if(vendor_shortlist != null)
    {
        for each  v in vendor_shortlist
        {
            zoho.creator.createRecord("ERP_PRO", "RFQ_Vendors", {
                "RFQ_Header" : rfq.get("ID"),
                "Vendor" : v
            });
        }
    }
}
```

### 2) Quote approval → PO creation with revisions
```javascript
// Form: Quote_Evaluation | Event: On Success (Approve button by Purchase Manager)
if(input.status == "Approved")
{
    // Auto-create PO header
    po_data = {
        "Vendor" : input.vendor,
        "PR" : input.PR,
        "RFQ" : input.RFQ,
        "Revision_No" : ifnull(input.Prev_PO.Revision_No,0) + 1,
        "Revision_Notes" : input.justification,
        "Payment_Terms" : input.payment_terms,
        "Freight_Terms" : input.freight_terms,
        "Status" : "Draft"
    };
    po = zoho.creator.createRecord("ERP_PRO", "Purchase_Order", po_data);

    quote_lines = Quote_Lines[Quote == input.quote_id];
    for each  ql in quote_lines
    {
        zoho.creator.createRecord("ERP_PRO", "PO_Lines", {
            "Purchase_Order" : po.get("ID"),
            "Product" : ql.Product,
            "Quantity" : ql.Quantity,
            "Rate" : ql.Price,
            "Delivery_Time" : ql.Delivery_Time,
            "GST_Percent" : ql.GST,
            "PR_Line" : ql.PR_Line
        });
    }
}
```

### 3) Receipt advice from invoice scan
```javascript
// Form: Receipt_Advice | Event: On User Input (Invoice upload) + On Success
if(input.Invoice_File != null)
{
    parsed = parse_invoice(input.Invoice_File); // custom parser returning line items
    for each  item in parsed.get("lines")
    {
        // match PO line by SKU or PO number from invoice
        po_line = PO_Lines[PO_Number == item.get("po_number") && Product.Code == item.get("sku")].get(0);
        zoho.creator.createRecord("ERP_PRO", "Receipt_Lines", {
            "Receipt_Advice" : input.ID,
            "PO_Line" : po_line.ID,
            "Received_Qty" : item.get("received_qty"),
            "UOM" : po_line.UOM,
            "Batch_No" : item.get("batch"),
            "Remarks" : item.get("remarks")
        });
    }
}

// On Success: update PO balances
for each  rl in Receipt_Lines[Receipt_Advice == input.ID]
{
    po_line = rl.PO_Line;
    po_line.Balance_Qty = po_line.Balance_Qty - rl.Received_Qty;
    po_line.Status = if(po_line.Balance_Qty > 0, "Partial Receipt", "Received");
    po_line.save();
}
```

### 4) Freight payable draft from receipt advice
```javascript
// Form: Receipt_Advice | Event: On Success
if(input.freight_terms != null)
{
    freight = {
        "Receipt_Advice" : input.ID,
        "Vendor" : input.vendor,
        "Local_Drayage" : input.local_drayage_amount,
        "Linehaul" : input.linehaul_amount,
        "Loading_Wages" : input.loading_wages,
        "Unloading_Wages" : input.unloading_wages,
        "Discount" : input.freight_discount,
        "Payer" : input.freight_terms // Paid / To_Pay
    };
    zoho.creator.createRecord("ERP_PRO", "Freight_Advice", freight);
}
```

### 5) QC outcome → Payment advice or credit note
```javascript
// Form: QC_Final_Report | Event: On Success
if(input.result == "Pass")
{
    // schedule payment advice after credit terms
    pay_date = zoho.currentdate.addDay(input.vendor.Credit_Terms_Days);
    zoho.creator.createRecord("ERP_PRO", "Vendor_Payment_Advice", {
        "Vendor" : input.vendor,
        "Receipt_Advice" : input.receipt_advice,
        "Amount" : input.accepted_value,
        "Due_Date" : pay_date,
        "Status" : "Pending"
    });
}
else
{
    // notify stakeholders & prepare credit note draft
    stakeholders = list();
    stakeholders.add(input.purchase_manager.Email);
    stakeholders.add(input.office_manager.Email);
    stakeholders.add(input.purchase_coordinator.Email);
    sendmail(from:zoho.adminuserid, to:stakeholders, subject:"QC Failed for Receipt " + input.receipt_advice, message:input.remarks);

    zoho.creator.createRecord("ERP_PRO", "Credit_Debit_Note", {
        "Vendor" : input.vendor,
        "Receipt_Advice" : input.receipt_advice,
        "Reason" : "QC Failed",
        "Status" : "Draft"
    });
}
```

### 6) Bank statement upload → auto-match payments
```javascript
// Form: Bank_Statement_Upload | Event: On Success
parsed = parse_bank_statement(input.file);
for each  txn in parsed
{
    advice = Vendor_Payment_Advice[Amount == txn.amount && Status == "Pending" && Vendor.Bank_Account_No == txn.account_no].get(0);
    if(advice != null)
    {
        advice.Status = "Paid";
        advice.Payment_Date = txn.txn_date;
        advice.Reference_No = txn.reference;
        advice.save();
    }
}
```

> **Note**: Replace helper functions like `parse_invoice` or `parse_bank_statement` with implementations based on your chosen parsing libraries/OCR service.
