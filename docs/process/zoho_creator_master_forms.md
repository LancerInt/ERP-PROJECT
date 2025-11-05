# Zoho Creator Master Forms

This guide enumerates every master form that must be configured in Zoho Creator before
transactional modules go live. These forms provide the foundational reference data used
across purchase, sales, production, logistics, finance, QC, and attendance workflows.
For each form you will find the business purpose, creation guidance, and a complete
field map (mirroring the authoritative data model catalogue).

> **Tip:** Build masters in the order presented so that lookups and approval flows have
> valid targets when you start configuring transactional forms.

---

## 1. Organisational Masters

### 1.1 Company Master
**Purpose:** Register each legal entity that participates in purchasing, sales,
finance, or compliance. Required before warehouses, vendors, or customers can be
associated with a company.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Company Code | Single Line (Unique) | Y | Short code used across modules and exports |
| Legal Name | Single Line | Y | Registered legal entity name |
| Trade Name | Single Line |  | Optional doing-business-as name |
| GSTIN | Single Line | Y | Validate 15-character GST format |
| PAN | Single Line |  | Required for TDS/TCS |
| CIN | Single Line |  | Corporate Identification Number |
| Registered Address | Address | Y | Multi-line address |
| Billing Address | Address | Y | Defaults onto invoices |
| Contact Email | Email |  | Finance escalation |
| Contact Phone | Phone |  | |
| Default Currency | Dropdown | Y | Seed from System Parameters |
| Books Export Flag | Checkbox |  | Toggle for Tally integration |
| Active From | Date | Y | Effective start date |
| Active To | Date |  | Optional sunset |
| Notes | Multi-line |  | |

### 1.2 Warehouse Master
**Purpose:** Capture warehouse profile and governance roles. Godowns and machinery are
maintained via dedicated masters that reference the warehouse record.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Warehouse Code | Single Line (Unique) | Y | Used in stock and logistics documents |
| Company | Lookup (Company) | Y | Owning entity |
| Name | Single Line | Y | Display name |
| Warehouse Type | Dropdown | Y | Head Office / Factory / Job Work Partner |
| Address | Address | Y | Physical location |
| City | Single Line | Y | |
| State | Dropdown | Y | GST place of supply |
| Country | Dropdown | Y | |
| Pincode | Single Line | Y | |
| Geo Latitude | Decimal | Y | Attendance geofence |
| Geo Longitude | Decimal | Y | Attendance geofence |
| Time Zone | Dropdown | Y | SLA calculations |
| Default Currency | Dropdown | Y | Inherits from company by default |
| Warehouse Coordinator (Office) | Lookup (Stakeholder User) | C | Mandatory for active warehouses |
| Warehouse HR Coordinator | Lookup (Stakeholder User) |  | |
| Warehouse Manager(s) | Multi-select Lookup (Stakeholder User) |  | |
| Warehouse Coordinator(s) | Multi-select Lookup (Stakeholder User) |  | |
| Warehouse Supervisor(s) | Multi-select Lookup (Stakeholder User) |  | |
| Active Flag | Checkbox | Y | Deactivate to hide from new transactions |
| Notes | Multi-line |  | |

### 1.3 Godown Master
**Purpose:** Manage individual storage zones within a warehouse so stock, QC, and
production flows can reference the precise location.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Godown Code | Single Line (Unique) | Y | Unique within the owning company |
| Warehouse | Lookup (Warehouse) | Y | Owning warehouse |
| Godown Name | Single Line | Y | Display name |
| Storage Condition | Dropdown |  | Ambient / Cold / Hazardous |
| Capacity UOM | Dropdown |  | |
| Capacity Value | Decimal |  | Maximum storage capacity |
| Batch Tracking Enabled | Checkbox | Y | Controls batch-level location |
| Default QC Hold Area | Checkbox |  | Flags quarantine |
| Active Flag | Checkbox | Y | Hide from selection when inactive |
| Notes | Multi-line |  | |

### 1.4 Machinery Master
**Purpose:** Register machinery located in each godown for maintenance tracking, job
work, and production allocation.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Machine ID | Single Line (Unique) | Y | Unique equipment identifier |
| Warehouse | Lookup (Warehouse) | Y | Auto-populated from the selected godown |
| Godown | Lookup (Godown) | Y | Location of the machine |
| Machine Name | Single Line | Y | Display name |
| Category | Dropdown | Y | Capital Goods / Machine Spares / Production Line |
| Commission Date | Date |  | |
| Maintenance Vendor | Lookup (Vendor) |  | For service/job work |
| Next Service Due | Date |  | |
| Status | Dropdown | Y | Active / Under Maintenance / Retired |
| Notes | Multi-line |  | |

### 1.5 Role Definition
**Purpose:** Define composite permission bundles that control record creation,
approval, and sharing.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Role Code | Single Line | Y | Unique role identifier |
| Role Name | Single Line | Y | |
| Module Permissions | Multi-line JSON | Y | CRUD/approval rights per module |
| Data Scope | Dropdown | Y | Global / Company / Warehouse |
| Approval Levels | Subform |  | Configure amount thresholds |
| Default Share Rules | Multi-line |  | Creator share settings template |
| Active Flag | Checkbox | Y | |

#### Approval Levels Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Module | Dropdown | Y | Purchase / Sales / Production / etc. |
| Stage | Dropdown | Y | Request / Evaluation / Payment |
| Min Amount | Currency |  | Threshold |
| Max Amount | Currency |  | |

### 1.6 Stakeholder User
**Purpose:** Map Zoho portal users to ERP stakeholder roles and warehouse scopes.

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

### 1.7 Staff Master
**Purpose:** Maintain the complete roster of staff (office and warehouse) for
attendance, HR, and wage integration.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Staff ID | Single Line (Unique) | Y | Official staff number |
| Full Name | Single Line | Y | |
| Gender | Dropdown |  | |
| Date of Birth | Date |  | |
| Employment Type | Dropdown | Y | Permanent / Contract / Trainee |
| Employment Location | Dropdown | Y | Office / Warehouse / Lab / etc. |
| Warehouse / Office | Lookup (Warehouse) | C | Mandatory for warehouse-based staff |
| Department | Dropdown |  | |
| Designation | Single Line |  | |
| Date of Joining | Date | Y | |
| Reporting Manager | Lookup (Staff Master) |  | Self-reference |
| Active Status | Dropdown | Y | Active / On Notice / Relieved |
| Attendance Shift | Lookup (Shift Definition) |  | Default shift |
| Overtime Eligible | Checkbox |  | |
| Photo | Image | Y | Used for face recognition |
| Aadhaar Number | Single Line |  | Mask on display |
| PAN Number | Single Line |  | |
| Address | Address |  | |
| Emergency Contact | Phone |  | |
| Bank Accounts | Subform |  | Multiple salary accounts |
| ID Proofs | Subform |  | Documents |
| Notes | Multi-line |  | |

#### Bank Account Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Bank Name | Single Line | Y | |
| Account Number | Single Line | Y | Mask when displayed |
| IFSC | Single Line | Y | Validate pattern |
| Account Type | Dropdown |  | Savings / Current |
| Primary Account | Checkbox |  | |

#### ID Proofs Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Proof Type | Dropdown | Y | Aadhaar / PAN / License |
| Proof Number | Single Line | Y | |
| Proof File | File Upload | Y | |
| Expiry Date | Date |  | Mandatory for expiring proofs |

### 1.8 Shift Definition
**Purpose:** Preconfigure shift timings, allowances, and overtime policies for
attendance automation.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Shift Code | Single Line (Unique) | Y | |
| Shift Name | Single Line | Y | |
| Location Scope | Dropdown | Y | Office / Warehouse specific |
| Warehouse | Lookup (Warehouse) | C | Required for warehouse shifts |
| Start Time | Time | Y | |
| End Time | Time | Y | |
| Break Minutes | Number |  | |
| Working Hours | Decimal | Y | Auto-calc or manual |
| Overtime Threshold (hrs) | Decimal |  | |
| Attendance Window Start | Time | Y | Earliest check-in |
| Attendance Window End | Time | Y | Latest check-in |
| Notes | Multi-line |  | |

---

## 2. Product & Service Catalogue Masters

### 2.1 Product Master
**Purpose:** Maintain all goods tracked in stock, production, purchase, and sales,
inclusive of unit conversions and QC flags.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Product Code | Single Line (Unique) | Y | SKU identifier |
| Product Name | Single Line | Y | |
| Product Type | Dropdown | Y | Goods / Service |
| Goods Category | Dropdown | C | RAW_MATERIAL / PACKING_MATERIAL / etc. |
| Service Category | Dropdown | C | Only when Product Type = Service |
| Specific Gravity | Decimal |  | For unit conversion |
| Primary UOM | Dropdown | Y | |
| Secondary UOMs | Subform |  | Unit conversion pairs |
| Batch Tracking Required | Checkbox |  | |
| QC Required | Checkbox |  | |
| QC Performed By | Dropdown | C | Warehouse Coordinator / QC Team |
| Expiry Tracking | Checkbox |  | |
| Shelf Life (Days) | Number | C | Required when expiry tracking |
| Reorder Level | Number |  | For alerts |
| HSN/SAC Code | Single Line |  | Tax integration |
| GST Rate | Decimal |  | Default tax |
| Default Company | Lookup (Company) |  | Used for variance checks |
| Default Warehouse | Lookup (Warehouse) |  | |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

#### Secondary UOMs Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Alternate UOM | Dropdown | Y | |
| Conversion Factor | Decimal | Y | Multiply primary to get alternate |
| Basis | Dropdown |  | Weight / Volume / Count |

### 2.2 Service Catalogue
**Purpose:** Register non-stock services (e.g., freight, wages) with tax rules
and warehouse availability.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Service Code | Single Line (Unique) | Y | |
| Service Name | Single Line | Y | |
| Service Type | Dropdown | Y | Warehouse Expense / Wages / etc. |
| Warehouse Scope | Multi-select Lookup (Warehouse) |  | Limit availability |
| GST Applicability | Dropdown | Y | Taxable / Exempt |
| GST Rate | Decimal | C | When taxable |
| TDS Section | Dropdown |  | Needed for wages |
| Default Ledger | Dropdown | Y | Finance mapping |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

### 2.3 Template Library
**Purpose:** Store reusable templates for production, QC reports, job work,
and document generation with version control.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Template Code | Single Line (Unique) | Y | |
| Template Name | Single Line | Y | |
| Template Type | Dropdown | Y | Production / QC Report / Job Work / Document |
| Revision Number | Single Line | Y | e.g., Rev 1 |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Warehouse Scope | Multi-select Lookup (Warehouse) |  | |
| JSON Definition | Multi-line JSON | Y | Structured template payload |
| Approval Log | Subform |  | Audit trail |
| Notes | Multi-line |  | |

#### Approval Log Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Approved By | Lookup (Stakeholder User) | Y | |
| Approved On | Date-Time | Y | |
| Remarks | Multi-line |  | |

### 2.4 QC Parameter Library
**Purpose:** Maintain parameter definitions used when configuring QC templates
and recording lab results.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter Code | Single Line (Unique) | Y | |
| Parameter Name | Single Line | Y | |
| Parameter Type | Dropdown | Y | Physical / Chemical / Microbial |
| Unit | Dropdown |  | |
| Min Spec | Decimal |  | |
| Max Spec | Decimal |  | |
| Default Method | Single Line |  | |
| Result Format | Dropdown | Y | Numeric / Text / Pass-Fail |
| Attachments Required | Checkbox |  | |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

---

## 3. Partner, Pricing & Tax Masters

### 3.1 Vendor Master
**Purpose:** Capture vendor identities, payment terms, tax compliance, and
banking for purchase and job work operations.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Vendor Code | Single Line (Unique) | Y | |
| Legal Name | Single Line | Y | |
| Trade Name | Single Line |  | |
| Vendor Type | Dropdown | Y | Goods Supplier / Service / Job Work / Contractor |
| GSTIN | Single Line | C | Mandatory when taxable |
| PAN | Single Line |  | |
| Address | Address | Y | |
| City | Single Line | Y | |
| State | Dropdown | Y | |
| Country | Dropdown | Y | |
| Pincode | Single Line | Y | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Payment Terms | Dropdown | Y | Net 15 / Net 30 / Custom |
| Credit Limit | Currency |  | |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Default Currency | Dropdown | Y | |
| TDS Section | Dropdown |  | |
| MSME Category | Dropdown |  | |
| Vendor Bank Details | Subform |  | Multiple accounts |
| Documents | File Upload (Multi) |  | Contracts, certifications |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

#### Vendor Bank Details Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Bank Name | Single Line | Y | |
| Branch | Single Line |  | |
| Account Number | Single Line | Y | Mask when displayed |
| IFSC | Single Line | Y | |
| Account Type | Dropdown |  | Savings / Current |
| Is Primary | Checkbox |  | |

### 3.2 Customer Master
**Purpose:** Maintain customer billing and shipping profiles, credit terms, and
price list assignments.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Customer Code | Single Line (Unique) | Y | |
| Legal Name | Single Line | Y | |
| Trade Name | Single Line |  | |
| Customer Type | Dropdown | Y | Domestic / Export |
| GSTIN | Single Line | C | Mandatory for domestic taxable |
| PAN | Single Line |  | |
| Billing Address | Address | Y | |
| Billing City | Single Line | Y | |
| Billing State | Dropdown | Y | |
| Billing Country | Dropdown | Y | |
| Billing Pincode | Single Line | Y | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Payment Terms | Dropdown | Y | Net 15 / Net 30 / etc. |
| Credit Limit | Currency |  | |
| Freight Terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Default Currency | Dropdown | Y | |
| Price Lists | Multi-select Lookup (Price List) |  | Allow multi-region pricing |
| Shipping Address | Subform |  | Location-wise details |
| Documents | File Upload (Multi) |  | Contracts |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

#### Shipping Address Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Location Name | Single Line | Y | |
| Address | Address | Y | |
| City | Single Line | Y | |
| State | Dropdown | Y | |
| Country | Dropdown | Y | |
| Pincode | Single Line | Y | |
| Price List | Lookup (Price List) |  | Default per location |
| Freight Terms Override | Dropdown |  | Optional per location |

### 3.3 Transporter Master
**Purpose:** Register transport partners for inbound/outbound freight,
including payment preferences for drayage and linehaul.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Transporter Code | Single Line (Unique) | Y | |
| Transporter Name | Single Line | Y | |
| GSTIN | Single Line |  | |
| PAN | Single Line |  | |
| Address | Address | Y | |
| Contact Person | Single Line |  | |
| Contact Email | Email |  | |
| Contact Phone | Phone |  | |
| Service Regions | Multi-select Dropdown |  | States / Zones |
| Payment Terms | Dropdown | Y | Immediate / Weekly / Monthly |
| Freight Type | Multi-select Dropdown | Y | Local Drayage / Linehaul |
| Preferred Payment Mode | Dropdown |  | Bank / Cash / UPI |
| Active Flag | Checkbox | Y | |
| Notes | Multi-line |  | |

### 3.4 Price List Master
**Purpose:** Configure customer-specific price catalogues with effective periods
and multiple revision lines.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Price List Code | Single Line (Unique) | Y | |
| Price List Name | Single Line | Y | |
| Customer | Lookup (Customer) |  | Optional master without direct assignment |
| Region | Dropdown |  | |
| Currency | Dropdown | Y | |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Default Freight Terms | Dropdown |  | |
| Active Flag | Checkbox | Y | |
| Price Lines | Subform |  | Define product/service rates |
| Notes | Multi-line |  | |

#### Price Lines Subform
| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Item | Lookup (Product Master / Service Catalogue) | Y | |
| UOM | Dropdown | Y | |
| Unit Price | Currency | Y | |
| Minimum Order Qty | Decimal |  | |
| Discount % | Decimal |  | |
| Freight Inclusion Flag | Checkbox |  | For bundled freight |

### 3.5 Tax Master
**Purpose:** Centralise GST, TDS, and TCS rates for automated calculations in
purchase, sales, and finance modules.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Tax Code | Single Line (Unique) | Y | |
| Tax Type | Dropdown | Y | GST / TDS / TCS |
| Description | Single Line | Y | |
| Rate (%) | Decimal | Y | |
| Applicable From | Date | Y | |
| Applicable To | Date |  | |
| Ledger Mapping | Dropdown |  | Finance integration |
| Notes | Multi-line |  | |

---

## 4. Configuration & Governance Masters

### 4.1 System Parameters
**Purpose:** Maintain configurable lists (currencies, UOMs, thresholds, alert
frequencies) consumed across modules.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Parameter Code | Single Line (Unique) | Y | |
| Parameter Group | Dropdown | Y | Currency / UOM / Threshold / Alert |
| Parameter Name | Single Line | Y | |
| Value | Multi-line | Y | JSON or delimited list |
| Effective From | Date | Y | |
| Effective To | Date |  | |
| Notes | Multi-line |  | |

### 4.2 Decision Log
**Purpose:** Track strategic and configuration decisions (e.g., AI services,
thresholds) for auditability and onboarding.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Decision ID | Single Line (Unique) | Y | |
| Decision Date | Date | Y | |
| Owner | Lookup (Stakeholder User) | Y | |
| Topic | Dropdown | Y | Integration / Finance / Process |
| Summary | Multi-line | Y | |
| Impacted Modules | Multi-select Dropdown |  | |
| Follow-up Actions | Multi-line |  | |
| Status | Dropdown | Y | Proposed / Approved / Implemented |

### 4.3 Audit Trail
**Purpose:** Log structural changes to masters (field additions, workflow
updates) for compliance. Populate automatically via Deluge scripts/triggers.

| Field Name | Type | Req. | Notes |
| --- | --- | --- | --- |
| Audit ID | Single Line (Unique) | Y | |
| Module | Dropdown | Y | Master module name |
| Record Reference | Lookup (Dynamic) | Y | Link to impacted record |
| Change Type | Dropdown | Y | Create / Update / Delete |
| Changed By | Lookup (Stakeholder User) | Y | |
| Change Timestamp | Date-Time | Y | |
| Change Summary | Multi-line | Y | |
| Attachment | File Upload |  | Optional evidence |

---

## 5. Implementation Checklist

Use this quick checklist when creating masters inside Zoho Creator:

1. **Seed System Parameters** – currencies, UOMs, state lists, alert thresholds.
2. **Create Companies** – load all legal entities and validate GSTIN/PAN formats.
3. **Onboard Warehouses** – ensure godown and machinery subforms are populated.
4. **Define Roles** – capture approval levels and share rules before user mapping.
5. **Load Staff & Stakeholders** – upload staff roster, then link portal users.
6. **Configure Shifts** – assign default shifts for attendance automation.
7. **Catalogue Products & Services** – include conversion factors and QC flags.
8. **Load Vendors, Customers, Transporters** – verify payment and freight terms.
9. **Publish Price Lists** – map to customers and shipping locations as needed.
10. **Upload Template/QC Libraries** – align with production and QC processes.
11. **Set Tax Rates** – GST, TDS, TCS for transactions and wage calculations.
12. **Record Decisions & Audit Hooks** – keep governance log current.

Completing these forms ensures every downstream workflow (purchase requests,
production batches, freight advice, wage approvals, etc.) has valid reference
data and can enforce the governance model described in the broader ERP blueprint.
