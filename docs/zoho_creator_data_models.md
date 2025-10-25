# Zoho Creator ERP Data Models

This catalogue enumerates every Zoho Creator form, subform, and lookup that powers the ERP. Each section lists all fields
required by the business requirements, grouped by module. Use these definitions when building forms, importing legacy data,
and configuring automation.

**Field Legend**

* **Type** – Suggested Zoho Creator field type (Single Line, Dropdown, Date-Time, Lookup, File Upload, Subform, etc.).
* **Req.** – `Y` if mandatory at record creation, `C` if conditionally mandatory, blank otherwise.
* **Notes** – Validation, defaulting, lookup behaviour, automation hooks.

---

## 1. Core & Shared Masters

### Company
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Company Code | Single Line (Unique) | Y | Short code used across modules and exports |
| Legal Name | Single Line | Y | Registered legal entity name |
| Trade Name | Single Line |  | Optional doing-business-as name |
| GSTIN | Single Line | Y | GST registration; validate 15-character format |
| PAN | Single Line |  | For TDS/TCS calculations |
| CIN | Single Line |  | Corporate Identification Number |
| Registered Address | Address | Y | Multi-line address |
| Billing Address | Address | Y | Defaults on invoices |
| Contact Email | Email |  | Finance escalation |
| Contact Phone | Phone |  | |
| Default Currency | Dropdown | Y | Values maintained in system parameters |
| Books Export Flag | Checkbox |  | Toggle for Tally integration |
| Active From | Date | Y | Effective start date |
| Active To | Date |  | Optional sunset |
| Notes | Multi-line |  | Additional remarks |

### Warehouse
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Warehouse Code | Single Line (Unique) | Y | Used in stock and logistics documents |
| Company | Lookup (Company) | Y | Owning entity |
| Name | Single Line | Y | Display name |
| Warehouse Type | Dropdown | Y | Head Office / Factory / Job Work Partner |
| Address | Address | Y | Physical location |
| City | Single Line | Y | |
| State | Dropdown | Y | For GST place of supply |
| Country | Dropdown | Y | |
| Pincode | Single Line | Y | |
| Geo Latitude | Decimal | Y | Attendance geofence |
| Geo Longitude | Decimal | Y | Attendance geofence |
| Time Zone | Dropdown | Y | For SLA calculations |
| Default Currency | Dropdown | Y | Inherits from company by default |
| Warehouse Coordinator (Office) | Lookup (Stakeholder User) | C | Required for warehouses |
| Warehouse HR Coordinator | Lookup (Stakeholder User) |  | Optional |
| Warehouse Manager(s) | Multi-select Lookup (Stakeholder User) |  | |
| Warehouse Coordinator(s) | Multi-select Lookup (Stakeholder User) |  | |
| Warehouse Supervisor(s) | Multi-select Lookup (Stakeholder User) |  | |
| Godown List | Subform | Y | Contains godown level stock segregation |
| Machinery List | Subform |  | Reference to machinery installed |
| Active Flag | Checkbox | Y | Deactivate to hide from new transactions |
| Notes | Multi-line |  | |

#### Godown (subform)
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Godown Code | Single Line | Y | Unique within warehouse |
| Godown Name | Single Line | Y | |
| Storage Condition | Dropdown |  | Ambient / Cold / Hazardous |
| Capacity UOM | Dropdown |  | |
| Capacity Value | Decimal |  | Max storage |
| Batch Tracking Enabled | Checkbox | Y | Controls batch-level location |
| Default QC Hold Area | Checkbox |  | Flags quarantine |

#### Machinery (subform)
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Machine ID | Single Line | Y | Unique equipment identifier |
| Machine Name | Single Line | Y | |
| Category | Dropdown | Y | Capital Goods / Machine Spares / Production Line |
| Commission Date | Date |  | |
| Maintenance Vendor | Lookup (Vendor) |  | For service/job work |
| Next Service Due | Date |  | |
| Status | Dropdown | Y | Active / Under Maintenance / Retired |

### Role Definition
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Role Code | Single Line | Y | Unique role identifier |
| Role Name | Single Line | Y | |
| Module Permissions | Multi-line JSON | Y | CRUD/approval rights per module |
| Data Scope | Dropdown | Y | Global / Company / Warehouse |
| Approval Levels | Subform |  | Specifies approvals handled |
| Default Share Rules | Multi-line |  | Creator share settings template |
| Active Flag | Checkbox | Y | |

#### Approval Levels (subform)
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Module | Dropdown | Y | Purchase / Sales / Production / etc. |
| Stage | Dropdown | Y | Request / Evaluation / Payment |
| Min Amount | Currency |  | Threshold |
| Max Amount | Currency |  | |

### Stakeholder User
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Portal User ID | Single Line | Y | Zoho portal identifier |
| Employee Record | Lookup (Staff Master) | Y | Links to staff |
| Primary Email | Email | Y | |
| Mobile | Phone |  | |
| Assigned Roles | Multi-select Lookup (Role Definition) | Y | Supports multi-role users |
| Default Warehouse | Lookup (Warehouse) |  | |
| Warehouse Scope | Multi-select Lookup (Warehouse) |  | Overrides default |
| Status | Dropdown | Y | Active / Suspended |
| Last Accessed | Date-Time |  | |
| Notes | Multi-line |  | |

### Staff Master (Employees & Staff)
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Staff ID | Single Line (Unique) | Y | Official staff number |
| Staff Type | Dropdown | Y | Employee (Stakeholder) / Staff |
| First Name | Single Line | Y | |
| Last Name | Single Line |  | |
| Gender | Dropdown |  | |
| Date of Birth | Date |  | |
| Company | Lookup (Company) | Y | Employer entity |
| Primary Location | Lookup (Warehouse) | Y | For attendance |
| Department | Dropdown |  | |
| Designation | Single Line | Y | |
| Employment Start Date | Date | Y | |
| Employment End Date | Date |  | |
| Employment Status | Dropdown | Y | Active / On Leave / Resigned |
| HR Owner | Lookup (Stakeholder User) | Y | Controls approvals |
| Shift Assignment | Lookup (Shift Definition) |  | Defaults attendance |
| Overtime Eligible | Checkbox |  | |
| Contractor Flag | Checkbox |  | For wages via vendor |
| Contractor Vendor | Lookup (Vendor) | C | Mandatory if contractor flag checked |
| Bank Account | Subform |  | Payment details |
| ID Proofs | Subform |  | Attachments |
| Face Template ID | Single Line | Y | External face recognition ID |
| Photo Reference | Image Upload | Y | Stored for 7 days |
| Contact Number | Phone |  | |
| Emergency Contact | Phone |  | |
| Address | Address |  | |
| Remarks | Multi-line |  | |

#### Bank Account (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Account Holder | Single Line | Y | |
| Bank Name | Single Line | Y | |
| IFSC Code | Single Line | Y | Validate format |
| Account Number | Single Line | Y | Mask display |
| Account Type | Dropdown |  | |

#### ID Proofs (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Document Type | Dropdown | Y | Aadhaar / PAN / License / Other |
| Document Number | Single Line | Y | |
| Expiry Date | Date |  | |
| Attachment | File Upload | Y | |

### Product Master
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| SKU Code | Single Line (Unique) | Y | Cross-module identifier |
| Product Name | Single Line | Y | |
| Product Type | Dropdown | Y | Goods / Services |
| Goods Sub-Type | Dropdown | C | RAW_MATERIAL / PACKING_MATERIAL / FINISHED_GOOD / SEMI_FINISHED / TRADED_PRODUCTS / CAPITAL_GOOD / MACHINE_SPARES / CONSUMABLES |
| Service Sub-Type | Dropdown | C | Warehouse Expense / Wages / Freight / Miscellaneous / Staff Welfare / Vehicle / Custom |
| Custom Service Category | Lookup (Service Catalogue) | C | For IT-admin defined services |
| Description | Multi-line |  | |
| Batch Tracking Required | Checkbox | C | Required for goods |
| Shelf Life (Days) | Number |  | For expiry |
| QC Responsibility | Dropdown |  | Warehouse Coordinator / QC Coordinator / QC Manager |
| QC Template | Lookup (Template Library) |  | Default QC parameters |
| UOM | Dropdown | Y | Base unit |
| Secondary UOMs | Subform |  | For conversions |
| Specific Gravity | Decimal |  | Used for kg ↔ litre |
| Conversion Notes | Multi-line |  | |
| Packing Material Default | Lookup (Product) |  | Default packaging |
| Yield Tracking Required | Checkbox |  | |
| Yield Parameters | Multi-select |  | Physical Qty / Purity % / AI Content |
| Wage Method | Dropdown |  | Template Rate / Headcount / None |
| Freight Class | Dropdown |  | Logistics reference |
| Active Flag | Checkbox | Y | |
| Created By | Lookup (Stakeholder User) | Y | |
| Created Date | Date-Time | Y | |
| Last Modified By | Lookup (Stakeholder User) |  | |
| Last Modified Date | Date-Time |  | |

#### Secondary UOMs (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| To UOM | Dropdown | Y | |
| Conversion Factor | Decimal | Y | Base to secondary |
| Specific Gravity Override | Decimal |  | Optional |
| Valid From | Date |  | |
| Valid To | Date |  | |

### Service Catalogue
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Service Code | Single Line | Y | |
| Name | Single Line | Y | |
| Category | Dropdown | Y | Warehouse Expense / Wages / Freight / Misc / Custom |
| Direction | Dropdown | Y | Inbound / Outbound / Both |
| Default TDS % | Decimal |  | |
| Default TCS % | Decimal |  | |
| Warehouse Availability | Multi-select Lookup (Warehouse) |  | |
| Description | Multi-line |  | |
| Active Flag | Checkbox | Y | |

### Vendor
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Vendor Code | Single Line | Y | |
| Vendor Name | Single Line | Y | |
| Vendor Type | Multi-select Dropdown | Y | Material / Service / Freight / Wages / Job Work / Contractor |
| Company | Lookup (Company) | Y | |
| GSTIN | Single Line | C | Mandatory if taxable |
| PAN | Single Line | Y | |
| Address | Address | Y | |
| City | Single Line | Y | |
| State | Dropdown | Y | |
| Country | Dropdown | Y | |
| Pincode | Single Line | Y | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Payment Terms | Dropdown | Y | Net 15 / Net 30 / Custom |
| Custom Payment Days | Number | C | Mandatory when Payment Terms = Custom |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Freight Split Notes | Multi-line |  | |
| Credit Limit | Currency |  | |
| Credit Days | Number |  | |
| TDS Rate % | Decimal |  | |
| TCS Rate % | Decimal |  | |
| Bank Details | Subform |  | Multiple accounts |
| Preferred Transporters | Multi-select Lookup (Transporter) |  | |
| Allowed Warehouses | Multi-select Lookup (Warehouse) |  | |
| Attachments | File Upload |  | Agreements |
| Active Flag | Checkbox | Y | |
| Created Date | Date-Time | Y | |

#### Vendor Bank Details (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Account Nickname | Single Line | Y | |
| Bank Name | Single Line | Y | |
| Branch | Single Line |  | |
| IFSC | Single Line | Y | |
| Account Number | Single Line | Y | |
| Payment Method | Dropdown |  | NEFT / RTGS / Cheque / UPI |

### Customer
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Customer Code | Single Line | Y | |
| Customer Name | Single Line | Y | |
| Company | Lookup (Company) | Y | |
| GSTIN | Single Line | C | Mandatory if taxable |
| PAN | Single Line |  | |
| Billing Address | Address | Y | |
| Shipping Addresses | Subform | Y | Supports multiple |
| Credit Terms | Dropdown | Y | Net 15 / Net 30 / Net 45 / Custom |
| Custom Credit Days | Number | C | Mandatory when Credit Terms = Custom |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Freight Split Notes | Multi-line |  | |
| Allowed Price Lists | Multi-select Lookup (Price List) | Y | |
| Default Warehouse | Lookup (Warehouse) | Y | |
| Overdue Notification Recipients | Multi-select Lookup (Stakeholder User) |  | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Documents | File Upload |  | Contracts |
| Active Flag | Checkbox | Y | |

#### Shipping Address (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Address Label | Single Line | Y | |
| Address | Address | Y | |
| Delivery Region | Dropdown | Y | For price list mapping |
| Default Price List | Lookup (Price List) |  | Auto-selection |
| Contact Person | Single Line |  | |
| Contact Phone | Phone |  | |

### Transporter
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Transporter Code | Single Line | Y | |
| Name | Single Line | Y | |
| GSTIN | Single Line |  | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Freight Modes | Multi-select Dropdown | Y | Local Drayage / Linehaul |
| Coverage Routes | Multi-line |  | |
| TDS Rate % | Decimal |  | |
| Payment Terms | Dropdown |  | |
| Rating | Number (1-5) |  | |
| Documents | File Upload |  | Insurance |
| Active Flag | Checkbox | Y | |

### Price List
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Price List ID | Single Line | Y | |
| Company | Lookup (Company) | Y | |
| Customer | Lookup (Customer) |  | Optional if customer-specific |
| Delivery Region | Dropdown |  | For auto-selection |
| Currency | Dropdown | Y | |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Default Freight Terms | Dropdown |  | Overrides customer |
| Status | Dropdown | Y | Draft / Active / Archived |
| Price Lines | Subform | Y | Product level rates |
| Notes | Multi-line |  | |

#### Price Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| UOM | Dropdown | Y | |
| Rate | Currency | Y | |
| Discount % | Decimal |  | |
| GST % | Decimal | Y | |
| Freight Component | Currency |  | Optional |
| Valid From | Date |  | |
| Valid To | Date |  | |

### Tax Master
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Tax Type | Dropdown | Y | GST / TDS / TCS |
| Section Reference | Single Line |  | |
| Rate % | Decimal | Y | |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Applicable On | Multi-select Dropdown | Y | Product / Service / Freight / Wage |
| Threshold Amount | Currency |  | |
| Company Scope | Lookup (Company) | Y | |
| Notes | Multi-line |  | |

### Template Library
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Template ID | Single Line | Y | |
| Template Type | Dropdown | Y | Production / QC Report / Job Work / Packing / Invoice |
| Name | Single Line | Y | |
| Warehouse Scope | Multi-select Lookup (Warehouse) | Y | |
| Revision No. | Number | Y | Rev 1, Rev 2, etc. |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Layout JSON/XML | Multi-line | Y | Stores dynamic layout |
| Requires Digital Signature | Checkbox |  | |
| Created By | Lookup (Stakeholder User) | Y | |
| Approval Log | Subform |  | |
| Status | Dropdown | Y | Draft / Active / Retired |

#### Approval Log (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Approved By | Lookup (Stakeholder User) | Y | |
| Approval Date | Date-Time | Y | |
| Remarks | Multi-line |  | |

---
## 2. Purchase Module

### Purchase Request (PR)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| PR No. | Auto Number | Y | |
| Request Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | Visibility restricted |
| Godown | Dropdown (filtered) | C | Required for stock items |
| Requested By | Lookup (Stakeholder User) | Y | |
| Requestor Role | Dropdown | Y | Warehouse Manager / Coordinator |
| Requirement Type | Dropdown | Y | Goods / Services / Machinery |
| Lines | Subform | Y | Detailed requirements |
| Priority | Dropdown |  | Low / Medium / High |
| Required By Date | Date | C | Mandatory when Requirement Type = Goods |
| Justification | Multi-line |  | |
| Attachments | File Upload |  | Specs, photos |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Rejected / Partially Approved |
| Approval Trail | Subform |  | Audit |
| Visibility Scope | Multi-select Lookup (Stakeholder User / Role) |  | Auto-share |
| Created From BOM Request | Lookup (BOM Request) |  | Traceability |
| Notes | Multi-line |  | |

#### PR Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Line No. | Number | Y | |
| Product/Service | Lookup (Product) | Y | |
| Description Override | Multi-line |  | |
| Quantity Requested | Decimal | Y | |
| UOM | Dropdown | Y | |
| Required Date | Date |  | |
| Purpose | Dropdown |  | Production / Maintenance / Consumable |
| Machine Reference | Lookup (Machine) |  | For spares/job work |
| Allow RFQ Skip | Checkbox |  | Requires approval |
| Attachments | File Upload |  | Photos |
| Status | Dropdown | Y | Pending / Approved / Rejected / Fulfilled |
| Approved Quantity | Decimal |  | For partial approval |

#### Approval Trail (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Action | Dropdown | Y | Approved / Rejected / Partial |
| Actor | Lookup (Stakeholder User) | Y | |
| Action Date | Date-Time | Y | |
| Remarks | Multi-line |  | |

### RFQ Header
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| RFQ No. | Auto Number | Y | |
| Linked PRs | Multi-select Lookup (Purchase Request) | Y | |
| Created By | Lookup (Stakeholder User) | Y | |
| Creation Date | Date | Y | |
| RFQ Mode | Dropdown | Y | Email / Portal / Phone |
| RFQ Documents | File Upload |  | Specs |
| RFQ Status | Dropdown | Y | Open / Closed / Cancelled |
| Quote Count Expected | Number |  | Typically 3 |
| Skip RFQ Flag | Checkbox |  | Requires purchase manager approval |
| Skip RFQ Justification | Multi-line | C | Mandatory when skip flag = true |
| Purchase Manager Approval | Lookup (Stakeholder User) |  | |
| Approval Attachment | File Upload |  | |
| Dispatch ETA Updates | Subform |  | Anticipated arrival |

#### Dispatch ETA Updates (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Update Date | Date-Time | Y | |
| Updated By | Lookup (Stakeholder User) | Y | |
| Expected Arrival | Date | Y | |
| Remarks | Multi-line |  | |

### Quote Response
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Quote ID | Auto Number | Y | |
| RFQ | Lookup (RFQ Header) | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Quote Date | Date | Y | |
| Price Valid Till | Date |  | |
| Currency | Dropdown | Y | |
| Quote Lines | Subform | Y | |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Payment Terms | Dropdown | Y | Inherit from vendor but editable |
| Delivery Terms | Multi-line |  | |
| Lead Time (Days) | Number |  | |
| Attachments | File Upload |  | Vendor quote |
| Remarks | Multi-line |  | |
| Evaluation Score | Decimal |  | Computed |
| Chosen Flag | Checkbox |  | |

#### Quote Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| PR Line | Lookup (PR Line) | Y | |
| Product/Service | Lookup (Product) | Y | |
| Specification | Multi-line |  | |
| Quantity Offered | Decimal | Y | |
| UOM | Dropdown | Y | |
| Unit Price | Currency | Y | |
| Discount % | Decimal |  | |
| GST % | Decimal | Y | |
| Freight Charge | Currency |  | |
| Delivery Timeline | Number |  | Days |

### Quote Evaluation
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Evaluation ID | Auto Number | Y | |
| RFQ | Lookup (RFQ Header) | Y | |
| Evaluation Date | Date | Y | |
| Evaluated By | Lookup (Stakeholder User) | Y | |
| Comparison Table | Subform | Y | Vendor comparisons |
| Best Quote Flag | Checkbox |  | |
| Recommended Vendor | Lookup (Vendor) |  | |
| Justification Notes | Multi-line | C | Mandatory when best quote not chosen |
| Approval Status | Dropdown | Y | Pending / Approved / Rejected |
| Approval Trail | Subform |  | Purchase Manager approval |

#### Comparison Table (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Vendor | Lookup (Vendor) | Y | |
| Total Cost | Currency | Y | Sum of lines |
| Lead Time | Number |  | |
| Freight Terms | Dropdown |  | |
| Payment Terms | Dropdown |  | |
| Score | Decimal |  | Weighted |
| Remarks | Multi-line |  | |

### Purchase Order (PO)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| PO No. | Auto Number | Y | |
| Revision No. | Number | Y | Rev 0 default |
| Vendor | Lookup (Vendor) | Y | |
| Company | Lookup (Company) | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Linked PRs | Multi-select Lookup (Purchase Request) | Y | |
| Linked RFQ | Lookup (RFQ Header) |  | |
| PO Date | Date | Y | |
| Expected Delivery Start | Date |  | |
| Expected Delivery End | Date |  | |
| Freight Terms | Dropdown | Y | |
| Payment Terms | Dropdown | Y | |
| Currency | Dropdown | Y | |
| PO Lines | Subform | Y | |
| Attachments | File Upload |  | Signed PO |
| Terms & Conditions | Multi-line |  | |
| Approval Trail | Subform |  | |
| Status | Dropdown | Y | Draft / Approved / Issued / Closed / Cancelled |
| Partial Receipt Flag | Checkbox |  | |

#### PO Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Line No. | Number | Y | |
| Product/Service | Lookup (Product) | Y | |
| Description | Multi-line |  | |
| Quantity Ordered | Decimal | Y | |
| UOM | Dropdown | Y | |
| Unit Price | Currency | Y | |
| Discount % | Decimal |  | |
| GST % | Decimal | Y | |
| Freight Estimate | Currency |  | Tentative freight |
| Delivery Schedule | Date |  | |
| Linked PR Line | Lookup (PR Line) |  | |
| Linked RFQ Line | Lookup (Quote Line) |  | |
| Batch Requirement Notes | Multi-line |  | |

### PO ETA Update (Anticipated Arrival)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Update ID | Auto Number | Y | |
| PO | Lookup (Purchase Order) | Y | |
| Update Date | Date-Time | Y | |
| Updated By | Lookup (Stakeholder User) | Y | Purchase Coordinator or Warehouse Coordinator |
| Expected Arrival Date | Date | Y | |
| Status | Dropdown | Y | Pending / Updated |
| Remarks | Multi-line |  | |

### Receipt Advice (Inbound)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Receipt Advice No. | Auto Number | Y | |
| Receipt Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Godown | Dropdown | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Linked PO(s) | Multi-select Lookup (Purchase Order) | Y | |
| Vehicle Number | Single Line |  | |
| Driver Name | Single Line |  | |
| Invoice Upload | File Upload | Y | Vendor invoice |
| Packing List Upload | File Upload |  | |
| Receipt Lines | Subform | Y | Products received |
| Packing Material Lines | Subform |  | Packaging capture |
| Freight Details | Subform |  | Local/Linehaul |
| Loading Unloading Wages | Subform |  | |
| QC Routing | Dropdown | Y | Warehouse / QC Coordinator / QC Manager |
| QC Status | Dropdown | Y | Pending / Pass / Fail / Hold |
| Partial Receipt Flag | Checkbox |  | |
| Remarks | Multi-line |  | |
| Created By | Lookup (Stakeholder User) | Y | |
| Created Time | Date-Time | Y | |

#### Receipt Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Line No. | Number | Y | |
| PO Line | Lookup (PO Line) | Y | |
| Product | Lookup (Product) | Y | |
| Batch No. | Single Line | C | Mandatory when batch tracking enabled |
| Expiry Date | Date |  | |
| Quantity Received | Decimal | Y | |
| UOM | Dropdown | Y | |
| Quantity Accepted | Decimal |  | Post QC |
| Quantity Rejected | Decimal |  | |
| Godown Location | Dropdown | Y | Filters by warehouse |
| Remarks | Multi-line |  | |

#### Packing Material Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Packaging SKU | Lookup (Product) | Y | Must be PACKING_MATERIAL |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |
| Condition | Dropdown |  | New / Damaged |

#### Freight Details (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Freight Type | Dropdown | Y | Local Drayage / Linehaul |
| Transporter | Lookup (Transporter) | C | Required when company pays |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Tentative Charge | Currency |  | Pre-filled from PO |
| Discount | Currency |  | Optional |
| Payable By | Dropdown | Y | Company / Vendor |
| Payment Schedule | Subform |  | Instalments |

#### Loading Unloading Wages (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Wage Type | Dropdown | Y | Loading / Unloading |
| Contractor Vendor | Lookup (Vendor) | C | Mandatory if payable by company |
| Amount | Currency | Y | |
| TDS Applicable % | Decimal |  | |
| Payable By | Dropdown | Y | Company / Vendor |
| Remarks | Multi-line |  | |

#### Payment Schedule (nested subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Due Date | Date | Y | |
| Amount | Currency | Y | |
| TDS % | Decimal |  | |
| Reminder Flag | Checkbox |  | Triggers auto reminders |

### Freight Advice (Inbound)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Advice No. | Auto Number | Y | |
| Direction | Dropdown | Y | Inbound |
| Receipt Advice | Lookup (Receipt Advice) | Y | |
| Transporter | Lookup (Transporter) | Y | |
| Freight Type | Dropdown | Y | Local Drayage / Linehaul |
| Base Amount | Currency | Y | |
| Discount | Currency |  | |
| Loading Wages Amount | Currency |  | |
| Unloading Wages Amount | Currency |  | |
| Payable Amount | Currency | Y | Base - discount + wages |
| Payment Schedule | Subform |  | |
| Approval Workflow | Subform |  | Freight Coordinator → Finance Manager |
| Status | Dropdown | Y | Draft / Pending Approval / Approved / Paid |

### Vendor Payment Advice
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Advice No. | Auto Number | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Source Document Type | Dropdown | Y | PO / Receipt / Freight / Wage / Credit Note |
| Source Document | Lookup (Varies) | Y | Dynamic lookup |
| Amount | Currency | Y | |
| Tax Components | Subform |  | TDS/TCS |
| Due Date | Date | Y | |
| Payment Method | Dropdown | Y | Bank Transfer / Cash / Cheque / UPI |
| Prepared By | Lookup (Stakeholder User) | Y | |
| Approval Workflow | Subform | Y | Finance Manager → Office Manager |
| Status | Dropdown | Y | Draft / Pending / Approved / Paid / On Hold |
| Notes | Multi-line |  | |

#### Tax Components (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Tax Type | Dropdown | Y | TDS / TCS |
| Rate % | Decimal | Y | |
| Amount | Currency | Y | |

---
## 3. Sales Module

### Customer PO Upload
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Upload ID | Auto Number | Y | |
| Customer | Lookup (Customer) | Y | |
| Upload Date | Date-Time | Y | |
| PO File | File Upload | Y | PDF |
| AI Parser Confidence | Decimal | Y | |
| Parsed PO Number | Single Line |  | |
| Parsed PO Date | Date |  | |
| Delivery Location | Dropdown |  | Suggest price list |
| Parsed Lines | Subform |  | Output of parser |
| Manual Review Required | Checkbox |  | Auto checked if confidence < threshold |
| Review Comments | Multi-line |  | |
| Status | Dropdown | Y | Uploaded / Parsed / Converted / Archived |
| Linked Sales Order | Lookup (Sales Order) |  | |

#### Parsed Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product Description | Single Line |  | |
| Quantity | Decimal |  | |
| UOM | Dropdown |  | |
| Price | Currency |  | |
| Parsed SKU | Lookup (Product) |  | Auto-mapped |
| Confidence % | Decimal |  | |

### Sales Order (SO)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| SO No. | Auto Number | Y | |
| Customer | Lookup (Customer) | Y | |
| Company | Lookup (Company) | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Price List | Lookup (Price List) | Y | Filter by customer |
| Credit Terms | Dropdown | Y | Inherit from customer |
| Freight Terms | Dropdown | Y | |
| Customer PO Reference | Lookup (Customer PO Upload) |  | |
| SO Date | Date | Y | |
| Required Ship Date | Date |  | |
| Lines | Subform | Y | |
| Remarks | Multi-line |  | |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | Lookup (Stakeholder User) |  | |
| Approval Date | Date-Time |  | |
| Assigned Warehouse Stakeholders | Multi-select Lookup (Stakeholder User) |  | Auto-share |

#### SO Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Line No. | Number | Y | |
| Product | Lookup (Product) | Y | Must exist in price list |
| Batch Preference | Single Line |  | |
| Quantity Ordered | Decimal | Y | |
| UOM | Dropdown | Y | |
| Unit Price | Currency | Y | From price list |
| Discount % | Decimal |  | |
| GST % | Decimal | Y | |
| Delivery Schedule Date | Date |  | |
| Remarks | Multi-line |  | |
| Reserved Qty | Decimal |  | Updated at dispatch |

### Dispatch Challan (DC)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| DC No. | Auto Number | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Dispatch Date | Date | Y | |
| Transporter | Lookup (Transporter) |  | |
| Freight Rate Type | Dropdown |  | Per km / Flat |
| Freight Rate Value | Currency |  | |
| Freight Amount Total | Currency |  | |
| Lorry No. | Single Line |  | |
| Driver Contact | Phone |  | |
| Linked SO Lines | Multi-select Lookup (SO Line) | Y | |
| DC Lines | Subform | Y | Consolidated products |
| Delivery Locations | Subform |  | For multi-drop |
| Documents | File Upload |  | DC PDF |
| Status | Dropdown | Y | Draft / Released / Delivered / Closed |
| Created By | Lookup (Stakeholder User) | Y | |
| Freight Advice Link | Lookup (Freight Advice) |  | Outbound |

#### DC Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line | C | Required if batch tracking |
| Quantity Dispatched | Decimal | Y | |
| UOM | Dropdown | Y | |
| Linked SO Line | Lookup (SO Line) | Y | |
| Weight | Decimal |  | Optional for weighment |

#### Delivery Locations (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Sequence | Number | Y | |
| Shipping Address | Lookup (Customer Shipping Address) | Y | |
| Quantity for Location | Decimal | Y | |
| Estimated Arrival | Date |  | |

### Sales Invoice Check
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Invoice Check ID | Auto Number | Y | |
| DC Reference | Lookup (Dispatch Challan) | Y | |
| Statutory Invoice Upload | File Upload | Y | External invoice |
| Invoice Number | Single Line | Y | |
| Invoice Date | Date | Y | |
| Total Value (Upload) | Currency | Y | Parsed |
| Total Value (SO) | Currency | Y | Computed |
| Variance Amount | Currency | Y | |
| Variance Flag | Dropdown | Y | Within Tolerance / Requires Review |
| Remarks | Multi-line |  | |
| Acceptance Timestamp | Date-Time |  | |
| Accepted By | Lookup (Stakeholder User) |  | |

### Freight Advice (Outbound)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Advice No. | Auto Number | Y | |
| Direction | Dropdown | Y | Outbound |
| Dispatch Challan | Lookup (Dispatch Challan) | Y | |
| Transporter | Lookup (Transporter) | Y | |
| Freight Type | Dropdown | Y | Local Drayage / Linehaul |
| Base Amount | Currency | Y | |
| Discount | Currency |  | |
| Loading Wages Amount | Currency |  | |
| Unloading Wages Amount | Currency |  | |
| Payable Amount | Currency | Y | |
| Payment Schedule | Subform |  | |
| Approval Workflow | Subform |  | Freight Coordinator → Finance Manager |
| Status | Dropdown | Y | Draft / Pending Approval / Approved / Paid |

### Receivable Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger ID | Auto Number | Y | |
| Customer | Lookup (Customer) | Y | |
| Invoice Reference | Lookup (Sales Invoice Check) | Y | |
| Invoice Date | Date | Y | |
| Due Date | Date | Y | |
| Amount | Currency | Y | |
| Amount Paid | Currency |  | |
| Balance | Currency | Y | |
| Payment Status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Reminder Dates | Subform |  | Auto reminders |
| Escalation Flag | Checkbox |  | Trigger after 2 weeks |
| Notes | Multi-line |  | |

#### Reminder Dates (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Reminder Date | Date | Y | |
| Reminder Sent By | Lookup (Stakeholder User) |  | |
| Reminder Method | Dropdown |  | Email / Call |

---
## 4. Production Module

### BOM Request
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Request No. | Auto Number | Y | |
| Request Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Requested By | Lookup (Stakeholder User) | Y | Warehouse Coordinator |
| Production Template | Lookup (Template Library) | Y | |
| Output Product | Lookup (Product) | Y | |
| Output Quantity | Decimal | Y | |
| Required Completion Date | Date |  | |
| Auto-calculated Inputs | Subform | Y | Computed from template |
| Shortfall Summary | Multi-line |  | |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | Lookup (Stakeholder User) |  | |
| Approved Date | Date-Time |  | |
| Excel Export Link | URL |  | Download BOM |
| Notes | Multi-line |  | |

#### Auto-calculated Inputs (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Required Qty | Decimal | Y | |
| Available Qty | Decimal | Y | From stock |
| Shortfall Qty | Decimal | Y | Negative allowed |
| Purpose | Dropdown | Y | RM / PM / Wage |

### Material Issue
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Issue No. | Auto Number | Y | |
| Issue Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Work Order | Lookup (Work Order) | Y | |
| Issued By | Lookup (Stakeholder User) | Y | |
| Approved By | Lookup (Stakeholder User) |  | |
| Issue Lines | Subform | Y | |
| Remarks | Multi-line |  | |

#### Issue Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch Out | Single Line | C | Required when batch tracking |
| Godown | Dropdown | Y | |
| Quantity Issued | Decimal | Y | |
| UOM | Dropdown | Y | |
| Reserved for Template | Checkbox |  | Packing material reservation |

### Work Order / Production Batch
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Batch ID | Auto Number | Y | |
| Work Order No. | Single Line | Y | Display |
| Warehouse | Lookup (Warehouse) | Y | |
| Production Template | Lookup (Template Library) | Y | Includes revision |
| Template Revision | Number | Y | |
| Linked Sales Order | Lookup (Sales Order) |  | |
| Linked Dispatch Challan | Lookup (Dispatch Challan) |  | |
| Planned Start Date | Date | Y | |
| Planned End Date | Date |  | |
| Actual Start Date | Date |  | |
| Actual End Date | Date |  | |
| Stage Status | Dropdown | Y | Material Issue / Mixing / Packing / QC / Closed |
| Input Consumption | Subform | Y | Actual usage |
| Output Products | Subform | Y | Manufactured goods |
| Damage Report | Subform |  | Damage / scrap |
| QC Request | Lookup (QC Request) |  | |
| Wage Method | Dropdown |  | Template Rate / Headcount |
| Wage Vouchers | Subform |  | Linked vouchers |
| Yield Log Reference | Lookup (Production Yield Log) |  | |
| Rework Flag | Checkbox |  | For reformulation |
| Parent Batch | Lookup (Work Order) |  | For rework linkage |
| Notes | Multi-line |  | |

#### Input Consumption (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Planned Qty | Decimal | Y | From template |
| Actual Qty | Decimal | Y | |
| UOM | Dropdown | Y | |
| Batch Used | Single Line | C | |
| Godown | Dropdown | Y | |
| Yield Loss % | Decimal |  | Capture deviations |

#### Output Products (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch ID | Single Line | Y | Auto-generated |
| Quantity Produced | Decimal | Y | |
| UOM | Dropdown | Y | |
| Purity % | Decimal | C | Required when yield tracking includes purity |
| AI Content | Decimal | C | Required when tracked |
| QC Status | Dropdown | Y | Pending / Pass / Fail / Hold |

#### Damage Report (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Stage | Dropdown | Y | Mixing / Packing / QC |
| Description | Multi-line | Y | |
| Quantity Lost | Decimal |  | |
| UOM | Dropdown |  | |
| Handling Action | Dropdown |  | Scrap / Rework |

#### Wage Vouchers (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Wage Voucher | Lookup (Wage Voucher) | Y | |
| Amount | Currency | Y | |

### Wage Voucher (Production)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Voucher No. | Auto Number | Y | |
| Work Order | Lookup (Work Order) | Y | |
| Wage Type | Dropdown | Y | Template Rate / Headcount |
| Contractor Vendor | Lookup (Vendor) | C | Mandatory for contractor |
| Staff Group | Multi-select Lookup (Staff) | C | Mandatory for headcount |
| Hours / Tasks | Subform | Y | |
| Amount | Currency | Y | |
| TDS % | Decimal |  | |
| Prepared By | Lookup (Stakeholder User) | Y | |
| Prepared Date | Date | Y | |
| Approval Workflow | Subform | Y | Warehouse Coordinator (Office) → Finance |
| Status | Dropdown | Y | Draft / Pending / Approved / Paid |
| Remarks | Multi-line |  | |

#### Hours / Tasks (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Staff | Lookup (Staff) |  | Required for headcount |
| Task Description | Multi-line | Y | |
| Hours Worked | Decimal |  | |
| Quantity Produced | Decimal |  | For incentive |

### Production Yield Log
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Log ID | Auto Number | Y | |
| Work Order | Lookup (Work Order) | Y | |
| Product | Lookup (Product) | Y | |
| Planned Yield % | Decimal |  | |
| Actual Output Qty | Decimal | Y | |
| Purity % | Decimal | C | |
| AI Content | Decimal | C | |
| Variance % | Decimal | Y | |
| Remarks | Multi-line |  | |
| Report Date | Date | Y | |

---

## 5. Quality Control Module

### QC Parameter Library
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter Code | Single Line | Y | |
| Parameter Name | Single Line | Y | |
| Unit | Single Line |  | |
| Applicable Template | Lookup (Template Library) |  | |
| Applicable Product | Lookup (Product) |  | |
| Acceptable Min | Decimal |  | |
| Acceptable Max | Decimal |  | |
| Critical Flag | Checkbox |  | |
| Notes | Multi-line |  | |

### QC Request
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Request No. | Auto Number | Y | |
| Request Date | Date | Y | |
| Requested By | Lookup (Stakeholder User) | Y | Warehouse roles |
| Requestor Role | Dropdown | Y | Warehouse Supervisor / Coordinator / Manager |
| Warehouse | Lookup (Warehouse) | Y | |
| Product | Lookup (Product) | Y | |
| Batch | Single Line | C | |
| Stage | Dropdown | Y | Receipt / In-Process / Finished / Sales Return |
| QC Template | Lookup (Template Library) | Y | |
| Selected Parameters | Subform |  | Optional overrides |
| Sample Photo | Image Upload | Y | |
| Sample Qty | Decimal |  | |
| Priority | Dropdown |  | Normal / Urgent |
| Remarks | Multi-line |  | |
| Status | Dropdown | Y | Requested / In Progress / Completed |
| Lab Code | Single Line |  | Generated by coordinator |
| Counter Sample Required | Checkbox |  | |

#### Selected Parameters (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter | Lookup (QC Parameter Library) | Y | |
| Override Range Min | Decimal |  | |
| Override Range Max | Decimal |  | |
| Notes | Multi-line |  | |

### QC Lab Job
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Job No. | Auto Number | Y | |
| QC Request | Lookup (QC Request) | Y | |
| Analyst | Lookup (Stakeholder User) | Y | |
| Assigned Parameters | Subform | Y | |
| Sample Received Date | Date | Y | |
| Results Attachment | File Upload |  | Raw data |
| Comments | Multi-line |  | |
| Status | Dropdown | Y | Assigned / In Progress / Completed |

#### Assigned Parameters (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter | Lookup (QC Parameter Library) | Y | |
| Result Value | Decimal |  | |
| Result Text | Multi-line |  | |
| Result Photo | Image Upload |  | |
| Pass/Fail | Dropdown |  | |

### QC Final Report
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Report No. | Auto Number | Y | |
| QC Request | Lookup (QC Request) | Y | |
| Template Revision | Number | Y | |
| Prepared By | Lookup (Stakeholder User) | Y | Coordinator or Manager |
| Prepared Date | Date | Y | |
| Overall Result | Dropdown | Y | Pass / Fail / Rework |
| Remarks | Multi-line |  | |
| Digital Signature | File Upload | C | Required if template demands |
| Distribution List | Multi-select Lookup (Stakeholder User) |  | |
| Attachments | File Upload |  | Final COA |

### Counter Sample Register
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Sample ID | Auto Number | Y | |
| QC Request | Lookup (QC Request) | Y | |
| Storage Location | Dropdown | Y | Warehouse / QC Lab |
| Shelf | Single Line |  | |
| Bin | Single Line |  | |
| Issued To | Lookup (Stakeholder User) |  | |
| Issue Date | Date |  | |
| Expected Return Date | Date |  | |
| Actual Return Date | Date |  | |
| Reminder Sent | Checkbox |  | Auto-reminder |
| Disposal Date | Date |  | |
| Disposal Approved By | Lookup (Stakeholder User) |  | |

---
## 6. Inventory, Logistics & Returns

### Inventory Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger Entry ID | Auto Number | Y | |
| Transaction Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Godown | Dropdown | Y | |
| Product | Lookup (Product) | Y | |
| Batch | Single Line |  | |
| Quantity In | Decimal |  | |
| Quantity Out | Decimal |  | |
| UOM | Dropdown | Y | |
| Transaction Type | Dropdown | Y | Receipt / Issue / Transfer / Adjustment / Dispatch |
| Source Document | Lookup (Varies) | Y | |
| Cost | Currency |  | |
| Status | Dropdown | Y | Available / In Transit / Reserved |
| FIFO Layer ID | Single Line |  | Valuation |
| Remarks | Multi-line |  | |

### Stock Transfer DC
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Transfer No. | Auto Number | Y | |
| Created Date | Date | Y | |
| From Warehouse | Lookup (Warehouse) | Y | |
| To Warehouse | Lookup (Warehouse) | Y | |
| Dispatch Date | Date |  | |
| Transporter | Lookup (Transporter) |  | |
| Freight Terms | Dropdown | Y | |
| Loading Wages | Currency |  | |
| Freight Amount | Currency |  | |
| Transfer Lines | Subform | Y | Products |
| Status | Dropdown | Y | Draft / In Transit / Received / Closed |
| Documents | File Upload |  | DC |

#### Transfer Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line | C | |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |
| Source Godown | Dropdown | Y | |
| Destination Godown | Dropdown | Y | |

### Stock Transfer Receipt
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Receipt No. | Auto Number | Y | |
| Receipt Date | Date | Y | |
| From Warehouse | Lookup (Warehouse) | Y | |
| To Warehouse | Lookup (Warehouse) | Y | |
| Linked Transfer | Lookup (Stock Transfer DC) | Y | |
| Received By | Lookup (Stakeholder User) | Y | |
| Receipt Lines | Subform | Y | |
| QC Result | Dropdown |  | Pass / Fail |
| Variance Notes | Multi-line |  | |
| Freight Details | Subform |  | Local drayage |
| Loading Unloading Wages | Subform |  | |
| Status | Dropdown | Y | Draft / Completed |

#### Receipt Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line |  | |
| Quantity Dispatched | Decimal | Y | |
| Quantity Received | Decimal | Y | |
| UOM | Dropdown | Y | |
| Received Godown | Dropdown | Y | |
| Condition | Dropdown |  | Good / Damaged |

### Warehouse Shifting
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Shifting No. | Auto Number | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Request Date | Date | Y | |
| From Godown | Dropdown | Y | |
| To Godown | Dropdown | Y | |
| Reason Code | Dropdown | Y | Damage / Space Optimisation / Audit / Other |
| Other Reason | Multi-line | C | Mandatory when Reason = Other |
| Products | Subform | Y | |
| Freight/Wage Drafts | Subform |  | |
| Status | Dropdown | Y | Draft / Pending Approval / Approved / Completed |
| In-Transit Flag | Checkbox |  | |
| Attachments | File Upload |  | Evidence |

#### Products (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line |  | |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |

#### Freight/Wage Drafts (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Expense Type | Dropdown | Y | Freight / Loading / Unloading |
| Vendor | Lookup (Vendor/Transporter) | C | Mandatory when payable by company |
| Amount | Currency | Y | |
| Payable By | Dropdown | Y | Sending Warehouse / Receiving Warehouse |
| Approval Status | Dropdown | Y | Draft / Pending / Approved |

### Job Work Order
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Order No. | Auto Number | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Template | Lookup (Template Library) | Y | |
| Template Revision | Number | Y | |
| Start Date | Date | Y | |
| Expected Completion Date | Date |  | From template |
| Turnaround Threshold | Number |  | For alerts |
| Materials Supplied | Subform | Y | |
| Outputs Expected | Subform | Y | |
| Freight Terms | Dropdown | Y | |
| Status | Dropdown | Y | Draft / In Progress / Completed |
| Alerts Enabled | Checkbox |  | Trigger overdue reminders |

#### Materials Supplied (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Material Type | Dropdown | Y | RM / PM / Machine |
| Product/Machine | Lookup (Product or Machine) | Y | |
| Batch | Single Line |  | |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |

#### Outputs Expected (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Expected Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |
| Expected Batch Suffix | Single Line |  | For tracking |

### Job Work DC
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| JW DC No. | Auto Number | Y | |
| Job Work Order | Lookup (Job Work Order) | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Dispatch Date | Date | Y | |
| Transporter | Lookup (Transporter) |  | |
| Freight Terms | Dropdown | Y | |
| Issued Materials | Subform | Y | |
| Documents | File Upload |  | DC, challan |
| Status | Dropdown | Y | Draft / Dispatched / Completed |

#### Issued Materials (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Material Type | Dropdown | Y | RM / PM / Machine |
| Product/Machine | Lookup (Product or Machine) | Y | |
| Batch | Single Line |  | |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |
| Expected Return Date | Date |  | |

### Job Work Receipt
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Receipt No. | Auto Number | Y | |
| Receipt Date | Date | Y | |
| Job Work Order | Lookup (Job Work Order) | Y | |
| JW DC Reference | Lookup (Job Work DC) | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Returned Goods | Subform | Y | |
| New Batch ID | Single Line |  | Distinct batch |
| QC Result | Dropdown |  | Pass / Fail |
| Pending Quantity | Decimal | Y | |
| Charges | Subform |  | Job work + freight |
| Status | Dropdown | Y | Draft / Completed |

#### Returned Goods (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line | Y | |
| Quantity Received | Decimal | Y | |
| UOM | Dropdown | Y | |
| Viability | Dropdown |  | Resaleable / Reformulate / Scrap |

#### Charges (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Charge Type | Dropdown | Y | Job Work / Freight / Loading / Unloading |
| Amount | Currency | Y | |
| TDS % | Decimal |  | Separate rates |
| Payable By | Dropdown | Y | Company / Vendor |

### Sales Return Advice
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Return No. | Auto Number | Y | |
| Return Date | Date | Y | |
| Customer | Lookup (Customer) | Y | |
| Original Invoice | Lookup (Sales Invoice Check) | Y | |
| Returned By | Single Line |  | Customer contact |
| Received Warehouse | Lookup (Warehouse) | Y | |
| Return Lines | Subform | Y | |
| Freight Terms | Dropdown | Y | |
| Freight Charges | Subform |  | |
| Loading/Unloading Charges | Subform |  | |
| QC Requirement | Dropdown | Y | Required / Optional |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approval Trail | Subform |  | |
| Remarks | Multi-line |  | |

#### Return Lines (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product | Lookup (Product) | Y | |
| Batch | Single Line |  | |
| Quantity Returned | Decimal | Y | |
| UOM | Dropdown | Y | |
| Condition | Dropdown | Y | Resaleable / Reformulate / Scrap |
| Viability Notes | Multi-line |  | |
| Packing Material Captured | Lookup (Product) |  | |

#### Freight Charges (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Freight Type | Dropdown | Y | Local Drayage / Linehaul |
| Transporter | Lookup (Transporter) |  | |
| Amount | Currency | Y | |
| Discount | Currency |  | |
| Payable By | Dropdown | Y | Company / Customer |

#### Loading/Unloading Charges (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Charge Type | Dropdown | Y | Loading / Unloading |
| Contractor Vendor | Lookup (Vendor) |  | |
| Amount | Currency | Y | |
| TDS % | Decimal |  | |
| Payable By | Dropdown | Y | Company / Customer |

### Stock Adjustment
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Adjustment No. | Auto Number | Y | |
| Adjustment Date | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Godown | Dropdown | Y | |
| Product | Lookup (Product) | Y | |
| Batch | Single Line |  | |
| Adjustment Type | Dropdown | Y | Positive / Negative |
| Quantity | Decimal | Y | |
| UOM | Dropdown | Y | |
| Reason Code | Dropdown | Y | Damage / Expiry / Shortage / Surplus / Audit Correction / Others |
| Other Reason | Multi-line | C | Mandatory if Others |
| Evidence Attachments | File Upload | Y | Photos, documents |
| Value Impact | Currency | Y | Auto-calculated |
| Finance Review Required | Checkbox | Y | Auto flag if value > ₹25,000 |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | Lookup (Stakeholder User) |  | |
| Approval Date | Date-Time |  | |
| Notified To | Multi-select Lookup (Stakeholder User) |  | Office Manager notification |
| Notes | Multi-line |  | |

---
## 7. Finance Module

### Vendor Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger ID | Auto Number | Y | |
| Vendor | Lookup (Vendor) | Y | |
| Document Type | Dropdown | Y | PO / Receipt / Invoice / Freight / Wage / Credit Note |
| Document Reference | Lookup (Varies) | Y | |
| Document Date | Date | Y | |
| Debit Amount | Currency |  | |
| Credit Amount | Currency |  | |
| Tax Breakdown | Subform |  | |
| Due Date | Date |  | |
| Payment Status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Ageing Bucket | Dropdown |  | 0-30 / 31-60 / >60 |
| Notes | Multi-line |  | |

#### Tax Breakdown (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Tax Type | Dropdown | Y | GST / TDS / TCS |
| Rate % | Decimal | Y | |
| Amount | Currency | Y | |

### Payment Advice Workflow
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Advice No. | Auto Number | Y | |
| Beneficiary Type | Dropdown | Y | Vendor / Transporter / Contractor |
| Beneficiary | Lookup (Vendor/Transporter) | Y | |
| Source Document | Lookup (Varies) | Y | |
| Amount | Currency | Y | |
| TDS/TCS Details | Subform |  | |
| Due Date | Date | Y | |
| Payment Method | Dropdown | Y | Bank Transfer / Cash / Cheque / UPI |
| Bank Account | Lookup (Vendor Bank Details) | C | Required for bank transfer |
| Prepared By | Lookup (Stakeholder User) | Y | |
| Prepared Date | Date | Y | |
| Finance Manager Approval | Subform | Y | Stage 1 |
| Office Manager Authorization | Subform | Y | Stage 2 |
| Payment Status | Dropdown | Y | Draft / Pending Finance / Pending Authorization / Approved / Paid |
| Payment Reference | Single Line |  | Bank txn |
| Attachments | File Upload |  | Bank proof |

#### TDS/TCS Details (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Tax Type | Dropdown | Y | TDS / TCS |
| Section | Single Line |  | |
| Rate % | Decimal | Y | |
| Amount | Currency | Y | |

#### Finance Manager Approval (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Approved By | Lookup (Stakeholder User) | Y | |
| Approval Date | Date-Time | Y | |
| Remarks | Multi-line |  | |

#### Office Manager Authorization (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Authorized By | Lookup (Stakeholder User) | Y | |
| Authorization Date | Date-Time | Y | |
| Remarks | Multi-line |  | |

### Bank Statement Upload
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Upload ID | Auto Number | Y | |
| Bank Account | Dropdown | Y | |
| Statement Period Start | Date | Y | |
| Statement Period End | Date | Y | |
| Upload Date | Date | Y | |
| Statement File | File Upload | Y | PDF/CSV |
| Parsing Status | Dropdown | Y | Pending / Parsed / Error |
| Auto-Matched Entries | Subform |  | |
| Exceptions | Subform |  | |
| Remarks | Multi-line |  | |

#### Auto-Matched Entries (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Statement Line ID | Single Line | Y | |
| Match Type | Dropdown | Y | Payable / Receivable |
| Linked Document | Lookup (Vendor Ledger / Customer Ledger) | Y | |
| Amount | Currency | Y | |
| Status | Dropdown | Y | Confirmed / Pending |

#### Exceptions (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Statement Line ID | Single Line | Y | |
| Transaction Date | Date | Y | |
| Amount | Currency | Y | |
| Suggested Match | Lookup (Ledger) |  | |
| Exception Notes | Multi-line |  | |
| Resolution Status | Dropdown | Y | Open / Resolved |

### Customer Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger ID | Auto Number | Y | |
| Customer | Lookup (Customer) | Y | |
| Document Type | Dropdown | Y | Invoice / Receipt / Credit Note |
| Document Reference | Lookup (Sales Invoice Check / Receipts) | Y | |
| Document Date | Date | Y | |
| Debit Amount | Currency |  | |
| Credit Amount | Currency |  | |
| Due Date | Date |  | |
| Payment Status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Reminder Sent Flags | Subform |  | |
| Notes | Multi-line |  | |

### Freight Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger ID | Auto Number | Y | |
| Direction | Dropdown | Y | Inbound / Outbound / Transfer |
| Transporter | Lookup (Transporter) | Y | |
| Freight Advice | Lookup (Freight Advice) | Y | |
| Amount | Currency | Y | |
| Discount | Currency |  | |
| Payment Schedule | Subform |  | |
| Amount Paid | Currency |  | |
| Balance | Currency | Y | |
| Reminder Flag | Checkbox |  | Auto reminder on due date |
| Notes | Multi-line |  | |

### Wage Ledger
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Ledger ID | Auto Number | Y | |
| Wage Voucher | Lookup (Wage Voucher) | Y | |
| Contractor/Staff Group | Lookup (Vendor or Staff) | Y | |
| Amount | Currency | Y | |
| TDS % | Decimal |  | |
| Payment Week | Date | Y | Week ending date |
| Approval Status | Dropdown | Y | Draft / Pending / Approved / Paid |
| Settlement Method | Dropdown | Y | Bank Transfer / Cash |
| Notes | Multi-line |  | |

### Credit/Debit Note
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Note No. | Auto Number | Y | |
| Note Type | Dropdown | Y | Credit / Debit |
| Vendor/Customer | Lookup (Vendor or Customer) | Y | |
| Source Document | Lookup (PO / Invoice / Sales Invoice Check) | Y | |
| Amount | Currency | Y | |
| Tax | Currency |  | |
| Reason | Multi-line | Y | |
| Approval Status | Dropdown | Y | Draft / Pending / Approved |
| Approved By | Lookup (Stakeholder User) |  | |
| Approval Date | Date-Time |  | |
| Ledger Posting Reference | Lookup (Ledger) |  | |

### GST Reconciliation Report
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Report ID | Auto Number | Y | |
| Reporting Period | Date Range | Y | Month/Quarter |
| Data Source | Dropdown | Y | Creator / GSTR-2B / GSTR-1 |
| Variance Summary | Multi-line |  | |
| Adjustments | Subform |  | |
| Export File | File Upload |  | CSV for Tally |

#### Adjustments (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Adjustment Type | Dropdown | Y | ITC Reversal / Additional Claim |
| Amount | Currency | Y | |
| Notes | Multi-line |  | |
| Approved By | Lookup (Stakeholder User) |  | |

### Petty Cash Register
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Register ID | Auto Number | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Coordinator | Lookup (Stakeholder User) | Y | |
| Opening Balance | Currency | Y | |
| Transactions | Subform | Y | |
| Current Balance | Currency | Y | Auto-calculated |
| Last Reconciled Date | Date |  | |

#### Transactions (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Transaction Date | Date | Y | |
| Voucher Reference | Lookup (Payment Advice / Wage Voucher) | Y | |
| Amount | Currency | Y | |
| Type | Dropdown | Y | Advance / Settlement |
| Notes | Multi-line |  | |

---

## 8. Attendance & HR Module

### Shift Definition
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Shift Code | Single Line | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Shift Name | Single Line | Y | |
| Start Time | Time | Y | |
| End Time | Time | Y | |
| Break Duration (mins) | Number |  | |
| Overtime Eligibility | Checkbox |  | |
| Attendance Calculation Rule | Dropdown | Y | 8-hour / Custom |
| Grace Period Minutes | Number |  | |
| Approval Required | Checkbox |  | |

### Attendance Capture
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Record ID | Auto Number | Y | |
| Staff | Lookup (Staff) | Y | |
| Date | Date | Y | |
| Check-in Time | Date-Time | Y | |
| Check-out Time | Date-Time |  | |
| Entry Photo | Image Upload | Y | Retained 7 days |
| Exit Photo | Image Upload |  | Retained 7 days |
| Geo Latitude | Decimal | Y | Must fall within warehouse geofence |
| Geo Longitude | Decimal | Y | |
| Face Match Confidence | Decimal | Y | From external API |
| Device ID | Single Line | Y | HR device |
| Shift | Lookup (Shift Definition) | Y | |
| Attendance Status | Dropdown | Y | Present / Absent / Half Day / Permission |
| Overtime Hours | Decimal |  | |
| Notes | Multi-line |  | |

### Leave Request
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Request No. | Auto Number | Y | |
| Staff | Lookup (Staff) | Y | |
| Leave Type | Dropdown | Y | Full Day / Half Day / Permission |
| Start Date | Date | Y | |
| End Date | Date | C | Required when full-day leave |
| Duration (Hours) | Decimal | C | Required for permission |
| Reason | Multi-line | Y | |
| Attachment | File Upload |  | Medical proof |
| Status | Dropdown | Y | Pending / Approved / Rejected |
| Approver | Lookup (Stakeholder User) |  | |
| Approval Date | Date-Time |  | |

### Overtime Request
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Request No. | Auto Number | Y | |
| Staff | Lookup (Staff) | Y | |
| Date | Date | Y | |
| Shift | Lookup (Shift Definition) |  | |
| Hours Worked | Decimal | Y | |
| Task Description | Multi-line | Y | |
| Supporting Evidence | File Upload |  | |
| Approval Status | Dropdown | Y | Pending / Approved / Rejected |
| Approved By | Lookup (Stakeholder User) |  | Warehouse Coordinator (Office) |
| Wage Integration Flag | Checkbox |  | Creates wage voucher |

### Payroll Export
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Export ID | Auto Number | Y | |
| Period Start | Date | Y | |
| Period End | Date | Y | |
| Warehouse | Lookup (Warehouse) | Y | |
| Staff Summary | Subform | Y | |
| Attendance Metrics | Multi-line |  | |
| Overtime Hours Total | Decimal |  | |
| Exceptions | Multi-line |  | |
| Export File | File Upload |  | CSV for payroll |

#### Staff Summary (subform)
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Staff | Lookup (Staff) | Y | |
| Present Days | Number | Y | |
| Absent Days | Number | Y | |
| Overtime Hours | Decimal |  | |
| Wages Amount | Currency |  | |

### Attendance Device Log
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Log ID | Auto Number | Y | |
| Device ID | Single Line | Y | |
| Event Time | Date-Time | Y | |
| Event Type | Dropdown | Y | Capture / Sync |
| Status | Dropdown | Y | Success / Failed |
| Error Message | Multi-line |  | |

---

## 9. Configuration & Audit

### System Parameters
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter Name | Single Line | Y | |
| Parameter Value | Single Line | Y | |
| Module Scope | Dropdown | Y | Purchase / Sales / Inventory / Finance / Attendance |
| Description | Multi-line |  | |
| Last Updated By | Lookup (Stakeholder User) | Y | |
| Effective Date | Date | Y | |

### Decision Log
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Decision ID | Auto Number | Y | |
| Topic | Single Line | Y | |
| Stakeholders | Multi-select Lookup (Stakeholder User) | Y | |
| Decision Details | Multi-line | Y | |
| Decision Date | Date | Y | |
| Follow-up Actions | Multi-line |  | |

### Audit Trail
| Field | Type | Req. | Notes |
| --- | --- | --- | --- |
| Audit ID | Auto Number | Y | |
| Module | Dropdown | Y | |
| Record ID | Single Line | Y | |
| Action | Dropdown | Y | Create / Update / Delete / Approve |
| User | Lookup (Stakeholder User) | Y | |
| Timestamp | Date-Time | Y | |
| Before Snapshot | File Upload |  | JSON export |
| After Snapshot | File Upload |  | JSON export |
| Remarks | Multi-line |  | |

Use this catalogue with the ERD and flowchart libraries to ensure every workflow, approval, and integration touchpoint is fully supported by the underlying data structures.
