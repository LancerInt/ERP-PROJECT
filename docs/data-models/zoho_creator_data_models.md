# Zoho Creator ERP Data Models

This catalogue enumerates every Zoho Creator form, subform, and lookup that powers the ERP. Each section lists all fields
required by the business requirements, grouped by module. Use these definitions when building forms, importing legacy data,
and configuring automation.

**Field Legend**

* **Link Name** – Internal Zoho Creator variable/field link name generated in snake_case.
* **Type** – Suggested Zoho Creator field type (Single Line, Dropdown, Date-Time, Lookup, File Upload, Subform, etc.).
* **Req.** – `Y` if mandatory at record creation, `C` if conditionally mandatory, blank otherwise.
* **Notes** – Validation, defaulting, lookup behaviour, automation hooks.

---

## 1. Core & Shared Masters

### Company
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Company Code | company_code | Single Line (Unique) | Y | Short code used across modules and exports |
| Legal Name | legal_name | Single Line | Y | Registered legal entity name |
| Trade Name | trade_name | Single Line |  | Optional doing-business-as name |
| GSTIN | gstin | Single Line | Y | GST registration; validate 15-character format |
| PAN | pan | Single Line |  | For TDS/TCS calculations |
| CIN | cin | Single Line |  | Corporate Identification Number |
| Registered Address | registered_address | Address | Y | Multi-line address |
| Billing Address | billing_address | Address | Y | Defaults on invoices |
| Contact Email | contact_email | Email |  | Finance escalation |
| Contact Phone | contact_phone | Phone |  |  |
| Default Currency | default_currency | Dropdown | Y | Values maintained in system parameters |
| Books Export Flag | books_export_flag | Checkbox |  | Toggle for Tally integration |
| Active From | active_from | Date | Y | Effective start date |
| Active To | active_to | Date |  | Optional sunset |
| Notes | notes | Multi-line |  | Additional remarks |

### Warehouse
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Warehouse Code | warehouse_code | Single Line (Unique) | Y | Used in stock and logistics documents |
| Company | company | Lookup (Company) | Y | Owning entity |
| Name | name | Single Line | Y | Display name |
| Warehouse Type | warehouse_type | Dropdown | Y | Head Office / Factory / Job Work Partner |
| Address | address | Address | Y | Physical location |
| City | city | Single Line | Y |  |
| State | state | Dropdown | Y | For GST place of supply |
| Country | country | Dropdown | Y |  |
| Pincode | pincode | Single Line | Y |  |
| Geo Latitude | geo_latitude | Decimal | Y | Attendance geofence |
| Geo Longitude | geo_longitude | Decimal | Y | Attendance geofence |
| Time Zone | time_zone | Dropdown | Y | For SLA calculations |
| Default Currency | default_currency | Dropdown | Y | Inherits from company by default |
| Warehouse Coordinator (Office) | warehouse_coordinator_office | Lookup (Stakeholder User) | C | Required for warehouses |
| Warehouse HR Coordinator | warehouse_hr_coordinator | Lookup (Stakeholder User) |  | Optional |
| Warehouse Manager(s) | warehouse_managers | Multi-select Lookup (Stakeholder User) |  |  |
| Warehouse Coordinator(s) | warehouse_coordinators | Multi-select Lookup (Stakeholder User) |  |  |
| Warehouse Supervisor(s) | warehouse_supervisors | Multi-select Lookup (Stakeholder User) |  |  |
| Godown List | godown_list | Subform | Y | Contains godown level stock segregation |
| Active Flag | active_flag | Checkbox | Y | Deactivate to hide from new transactions |
| Notes | notes | Multi-line |  |  |

#### Godown (subform)
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Godown Code | godown_code | Single Line | Y | Unique within warehouse |
| Godown Name | godown_name | Single Line | Y |  |
| Storage Condition | storage_condition | Dropdown |  | Ambient / Cold / Hazardous |
| Capacity UOM | capacity_uom | Dropdown |  |  |
| Capacity Value | capacity_value | Decimal |  | Max storage |
| Batch Tracking Enabled | batch_tracking_enabled | Checkbox | Y | Controls batch-level location |
| Default QC Hold Area | default_qc_hold_area | Checkbox |  | Flags quarantine |
| Machinery List | machinery_list | Subform |  | Equipment housed in the godown |

#### Machinery (Godown subform)
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Machine ID | machine_id | Single Line | Y | Unique equipment identifier |
| Machine Name | machine_name | Single Line | Y |  |
| Category | category | Dropdown | Y | Capital Goods / Machine Spares / Production Line |
| Commission Date | commission_date | Date |  |  |
| Maintenance Vendor | maintenance_vendor | Lookup (Vendor) |  | For service/job work |
| Next Service Due | next_service_due | Date |  |  |
| Status | status | Dropdown | Y | Active / Under Maintenance / Retired |

### Role Definition
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Role Code | role_code | Single Line | Y | Unique role identifier |
| Role Name | role_name | Single Line | Y |  |
| Module Permissions | module_permissions | Multi-line JSON | Y | CRUD/approval rights per module |
| Data Scope | data_scope | Dropdown | Y | Global / Company / Warehouse |
| Approval Levels | approval_levels | Subform |  | Specifies approvals handled |
| Default Share Rules | default_share_rules | Multi-line |  | Creator share settings template |
| Active Flag | active_flag | Checkbox | Y |  |

#### Approval Levels (subform)
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Module | module | Dropdown | Y | Purchase / Sales / Production / etc. |
| Stage | stage | Dropdown | Y | Request / Evaluation / Payment |
| Min Amount | min_amount | Currency |  | Threshold |
| Max Amount | max_amount | Currency |  |  |

### Stakeholder User
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Portal User ID | portal_user_id | Single Line | Y | Zoho portal identifier |
| Employee Record | employee_record | Lookup (Staff Master) | Y | Links to staff |
| Primary Email | primary_email | Email | Y |  |
| Mobile | mobile | Phone |  |  |
| Assigned Roles | assigned_roles | Multi-select Lookup (Role Definition) | Y | Supports multi-role users |
| Default Warehouse | default_warehouse | Lookup (Warehouse) |  |  |
| Warehouse Scope | warehouse_scope | Multi-select Lookup (Warehouse) |  | Overrides default |
| Status | status | Dropdown | Y | Active / Suspended |
| Last Accessed | last_accessed | Date-Time |  |  |
| Notes | notes | Multi-line |  |  |

### Staff Master (Employees & Staff)
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Staff ID | staff_id | Single Line (Unique) | Y | Official staff number |
| Staff Type | staff_type | Dropdown | Y | Employee (Stakeholder) / Staff |
| First Name | first_name | Single Line | Y |  |
| Last Name | last_name | Single Line |  |  |
| Gender | gender | Dropdown |  |  |
| Date of Birth | date_of_birth | Date |  |  |
| Company | company | Lookup (Company) | Y | Employer entity |
| Primary Location | primary_location | Lookup (Warehouse) | Y | For attendance |
| Department | department | Dropdown |  |  |
| Designation | designation | Single Line | Y |  |
| Employment Start Date | employment_start_date | Date | Y |  |
| Employment End Date | employment_end_date | Date |  |  |
| Employment Status | employment_status | Dropdown | Y | Active / On Leave / Resigned |
| HR Owner | hr_owner | Lookup (Stakeholder User) | Y | Controls approvals |
| Shift Assignment | shift_assignment | Lookup (Shift Definition) |  | Defaults attendance |
| Overtime Eligible | overtime_eligible | Checkbox |  |  |
| Contractor Flag | contractor_flag | Checkbox |  | For wages via vendor |
| Contractor Vendor | contractor_vendor | Lookup (Vendor) | C | Mandatory if contractor flag checked |
| Bank Account | bank_account | Subform |  | Payment details |
| ID Proofs | id_proofs | Subform |  | Attachments |
| Face Template ID | face_template_id | Single Line | Y | External face recognition ID |
| Photo Reference | photo_reference | Image Upload | Y | Stored for 7 days |
| Contact Number | contact_number | Phone |  |  |
| Emergency Contact | emergency_contact | Phone |  |  |
| Address | address | Address |  |  |
| Remarks | remarks | Multi-line |  |  |

#### Bank Account (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Account Holder | account_holder | Single Line | Y |  |
| Bank Name | bank_name | Single Line | Y |  |
| IFSC Code | ifsc_code | Single Line | Y | Validate format |
| Account Number | account_number | Single Line | Y | Mask display |
| Account Type | account_type | Dropdown |  |  |

#### ID Proofs (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Document Type | document_type | Dropdown | Y | Aadhaar / PAN / License / Other |
| Document Number | document_number | Single Line | Y |  |
| Expiry Date | expiry_date | Date |  |  |
| Attachment | attachment | File Upload | Y |  |

### Product Master
| Field Name | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| SKU Code | sku_code | Single Line (Unique) | Y | Cross-module identifier |
| Product Name | product_name | Single Line | Y |  |
| Product Type | product_type | Dropdown | Y | Goods / Services |
| Goods Sub-Type | goods_sub_type | Dropdown | C | RAW_MATERIAL / PACKING_MATERIAL / FINISHED_GOOD / SEMI_FINISHED / TRADED_PRODUCTS / CAPITAL_GOOD / MACHINE_SPARES / CONSUMABLES |
| Service Sub-Type | service_sub_type | Dropdown | C | Warehouse Expense / Wages / Freight / Miscellaneous / Staff Welfare / Vehicle / Custom |
| Custom Service Category | custom_service_category | Lookup (Service Catalogue) | C | For IT-admin defined services |
| Description | description | Multi-line |  |  |
| Batch Tracking Required | batch_tracking_required | Checkbox | C | Required for goods |
| Shelf Life (Days) | shelf_life_days | Number |  | For expiry |
| QC Responsibility | qc_responsibility | Dropdown |  | Warehouse Coordinator / QC Coordinator / QC Manager |
| QC Template | qc_template | Lookup (Template Library) |  | Default QC parameters |
| UOM | uom | Dropdown | Y | Base unit |
| Secondary UOMs | secondary_uoms | Subform |  | For conversions |
| Specific Gravity | specific_gravity | Decimal |  | Used for kg ↔ litre |
| Conversion Notes | conversion_notes | Multi-line |  |  |
| Packing Material Default | packing_material_default | Lookup (Product) |  | Default packaging |
| Yield Tracking Required | yield_tracking_required | Checkbox |  |  |
| Yield Parameters | yield_parameters | Multi-select |  | Physical Qty / Purity % / AI Content |
| Wage Method | wage_method | Dropdown |  | Template Rate / Headcount / None |
| Freight Class | freight_class | Dropdown |  | Logistics reference |
| Active Flag | active_flag | Checkbox | Y |  |
| Created By | created_by | Lookup (Stakeholder User) | Y |  |
| Created Date | created_date | Date-Time | Y |  |
| Last Modified By | last_modified_by | Lookup (Stakeholder User) |  |  |
| Last Modified Date | last_modified_date | Date-Time |  |  |

#### Secondary UOMs (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| To UOM | to_uom | Dropdown | Y |  |
| Conversion Factor | conversion_factor | Decimal | Y | Base to secondary |
| Specific Gravity Override | specific_gravity_override | Decimal |  | Optional |
| Valid From | valid_from | Date |  |  |
| Valid To | valid_to | Date |  |  |

### Service Catalogue
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Service Code | service_code | Single Line | Y |  |
| Name | name | Single Line | Y |  |
| Category | category | Dropdown | Y | Warehouse Expense / Wages / Freight / Misc / Custom |
| Direction | direction | Dropdown | Y | Inbound / Outbound / Both |
| Default TDS % | default_tds | Decimal |  |  |
| Default TCS % | default_tcs | Decimal |  |  |
| Warehouse Availability | warehouse_availability | Multi-select Lookup (Warehouse) |  |  |
| Description | description | Multi-line |  |  |
| Active Flag | active_flag | Checkbox | Y |  |

### Vendor
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Vendor Code | vendor_code | Single Line | Y |  |
| Vendor Name | vendor_name | Single Line | Y |  |
| Vendor Type | vendor_type | Multi-select Dropdown | Y | Material / Service / Freight / Wages / Job Work / Contractor |
| Company | company | Lookup (Company) | Y |  |
| GSTIN | gstin | Single Line | C | Mandatory if taxable |
| PAN | pan | Single Line | Y |  |
| Address | address | Address | Y |  |
| City | city | Single Line | Y |  |
| State | state | Dropdown | Y |  |
| Country | country | Dropdown | Y |  |
| Pincode | pincode | Single Line | Y |  |
| Contact Person | contact_person | Single Line |  |  |
| Contact Email | contact_email | Email |  |  |
| Contact Phone | contact_phone | Phone |  |  |
| Payment Terms | payment_terms | Dropdown | Y | Net 15 / Net 30 / Custom |
| Custom Payment Days | custom_payment_days | Number | C | Mandatory when Payment Terms = Custom |
| Freight Terms | freight_terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Freight Split Notes | freight_split_notes | Multi-line |  |  |
| Credit Limit | credit_limit | Currency |  |  |
| Credit Days | credit_days | Number |  |  |
| TDS Rate % | tds_rate | Decimal |  |  |
| TCS Rate % | tcs_rate | Decimal |  |  |
| Bank Details | bank_details | Subform |  | Multiple accounts |
| Preferred Transporters | preferred_transporters | Multi-select Lookup (Transporter) |  |  |
| Allowed Warehouses | allowed_warehouses | Multi-select Lookup (Warehouse) |  |  |
| Attachments | attachments | File Upload |  | Agreements |
| Active Flag | active_flag | Checkbox | Y |  |
| Created Date | created_date | Date-Time | Y |  |

#### Vendor Bank Details (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Account Nickname | account_nickname | Single Line | Y |  |
| Bank Name | bank_name | Single Line | Y |  |
| Branch | branch | Single Line |  |  |
| IFSC | ifsc | Single Line | Y |  |
| Account Number | account_number | Single Line | Y |  |
| Payment Method | payment_method | Dropdown |  | NEFT / RTGS / Cheque / UPI |

### Customer
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Customer Code | customer_code | Single Line | Y |  |
| Customer Name | customer_name | Single Line | Y |  |
| Company | company | Lookup (Company) | Y |  |
| GSTIN | gstin | Single Line | C | Mandatory if taxable |
| PAN | pan | Single Line |  |  |
| Billing Address | billing_address | Address | Y |  |
| Shipping Addresses | shipping_addresses | Subform | Y | Supports multiple |
| Credit Terms | credit_terms | Dropdown | Y | Net 15 / Net 30 / Net 45 / Custom |
| Custom Credit Days | custom_credit_days | Number | C | Mandatory when Credit Terms = Custom |
| Freight Terms | freight_terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Freight Split Notes | freight_split_notes | Multi-line |  |  |
| Allowed Price Lists | allowed_price_lists | Multi-select Lookup (Price List) | Y |  |
| Default Warehouse | default_warehouse | Lookup (Warehouse) | Y |  |
| Overdue Notification Recipients | overdue_notification_recipients | Multi-select Lookup (Stakeholder User) |  |  |
| Contact Person | contact_person | Single Line |  |  |
| Contact Email | contact_email | Email |  |  |
| Contact Phone | contact_phone | Phone |  |  |
| Documents | documents | File Upload |  | Contracts |
| Active Flag | active_flag | Checkbox | Y |  |

#### Shipping Address (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Address Label | address_label | Single Line | Y |  |
| Address | address | Address | Y |  |
| Delivery Region | delivery_region | Dropdown | Y | For price list mapping |
| Default Price List | default_price_list | Lookup (Price List) |  | Auto-selection |
| Contact Person | contact_person | Single Line |  |  |
| Contact Phone | contact_phone | Phone |  |  |

### Transporter
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Transporter Code | transporter_code | Single Line | Y |  |
| Name | name | Single Line | Y |  |
| GSTIN | gstin | Single Line |  |  |
| Contact Person | contact_person | Single Line |  |  |
| Contact Email | contact_email | Email |  |  |
| Contact Phone | contact_phone | Phone |  |  |
| Freight Modes | freight_modes | Multi-select Dropdown | Y | Local Drayage / Linehaul |
| Coverage Routes | coverage_routes | Multi-line |  |  |
| TDS Rate % | tds_rate | Decimal |  |  |
| Payment Terms | payment_terms | Dropdown |  |  |
| Rating | rating | Number (1-5) |  |  |
| Documents | documents | File Upload |  | Insurance |
| Active Flag | active_flag | Checkbox | Y |  |

### Price List
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Price List ID | price_list_id | Single Line | Y |  |
| Company | company | Lookup (Company) | Y |  |
| Customer | customer | Lookup (Customer) |  | Optional if customer-specific |
| Delivery Region | delivery_region | Dropdown |  | For auto-selection |
| Currency | currency | Dropdown | Y |  |
| Effective From | effective_from | Date | Y |  |
| Effective To | effective_to | Date |  |  |
| Default Freight Terms | default_freight_terms | Dropdown |  | Overrides customer |
| Status | status | Dropdown | Y | Draft / Active / Archived |
| Price Lines | price_lines | Subform | Y | Product level rates |
| Notes | notes | Multi-line |  |  |

#### Price Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| UOM | uom | Dropdown | Y |  |
| Rate | rate | Currency | Y |  |
| Discount % | discount | Decimal |  |  |
| GST % | gst | Decimal | Y |  |
| Freight Component | freight_component | Currency |  | Optional |
| Valid From | valid_from | Date |  |  |
| Valid To | valid_to | Date |  |  |

### Tax Master
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Tax Type | tax_type | Dropdown | Y | GST / TDS / TCS |
| Section Reference | section_reference | Single Line |  |  |
| Rate % | rate | Decimal | Y |  |
| Effective From | effective_from | Date | Y |  |
| Effective To | effective_to | Date |  |  |
| Applicable On | applicable_on | Multi-select Dropdown | Y | Product / Service / Freight / Wage |
| Threshold Amount | threshold_amount | Currency |  |  |
| Company Scope | company_scope | Lookup (Company) | Y |  |
| Notes | notes | Multi-line |  |  |

### Template Library
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Template ID | template_id | Single Line | Y |  |
| Template Type | template_type | Dropdown | Y | Production / QC Report / Job Work / Packing / Invoice |
| Name | name | Single Line | Y |  |
| Warehouse Scope | warehouse_scope | Multi-select Lookup (Warehouse) | Y |  |
| Revision No. | revision_no | Number | Y | Rev 1, Rev 2, etc. |
| Effective From | effective_from | Date | Y |  |
| Effective To | effective_to | Date |  |  |
| Layout JSON/XML | layout_json_xml | Multi-line | Y | Stores dynamic layout |
| Requires Digital Signature | requires_digital_signature | Checkbox |  |  |
| Created By | created_by | Lookup (Stakeholder User) | Y |  |
| Approval Log | approval_log | Subform |  |  |
| Status | status | Dropdown | Y | Draft / Active / Retired |

#### Approval Log (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Approved By | approved_by | Lookup (Stakeholder User) | Y |  |
| Approval Date | approval_date | Date-Time | Y |  |
| Remarks | remarks | Multi-line |  |  |

---

## 2. Purchase Module

### Purchase Request (PR)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| PR No. | pr_no | Auto Number | Y |  |
| Request Date | request_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y | Visibility restricted |
| Godown | godown | Dropdown (filtered) | C | Required for stock items |
| Requested By | requested_by | Lookup (Stakeholder User) | Y |  |
| Requestor Role | requestor_role | Dropdown | Y | Warehouse Manager / Coordinator |
| Requirement Type | requirement_type | Dropdown | Y | Goods / Services / Machinery |
| Lines | lines | Subform | Y | Detailed requirements |
| Priority | priority | Dropdown |  | Low / Medium / High |
| Required By Date | required_by_date | Date | C | Mandatory when Requirement Type = Goods |
| Justification | justification | Multi-line |  |  |
| Attachments | attachments | File Upload |  | Specs, photos |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Rejected / Partially Approved |
| Approval Trail | approval_trail | Subform |  | Audit |
| Visibility Scope | visibility_scope | Multi-select Lookup (Stakeholder User / Role) |  | Auto-share |
| Created From BOM Request | created_from_bom_request | Lookup (BOM Request) |  | Traceability |
| Notes | notes | Multi-line |  |  |

#### PR Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Line No. | line_no | Number | Y |  |
| Product/Service | product_service | Lookup (Product) | Y |  |
| Description Override | description_override | Multi-line |  |  |
| Quantity Requested | quantity_requested | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Required Date | required_date | Date |  |  |
| Purpose | purpose | Dropdown |  | Production / Maintenance / Consumable |
| Machine Reference | machine_reference | Lookup (Machine) |  | For spares/job work |
| Allow RFQ Skip | allow_rfq_skip | Checkbox |  | Requires approval |
| Attachments | attachments | File Upload |  | Photos |
| Status | status | Dropdown | Y | Pending / Approved / Rejected / Fulfilled |
| Approved Quantity | approved_quantity | Decimal |  | For partial approval |

#### Approval Trail (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Action | action | Dropdown | Y | Approved / Rejected / Partial |
| Actor | actor | Lookup (Stakeholder User) | Y |  |
| Action Date | action_date | Date-Time | Y |  |
| Remarks | remarks | Multi-line |  |  |

### RFQ Header
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| RFQ No. | rfq_no | Auto Number | Y |  |
| Linked PRs | linked_prs | Multi-select Lookup (Purchase Request) | Y |  |
| Created By | created_by | Lookup (Stakeholder User) | Y |  |
| Creation Date | creation_date | Date | Y |  |
| RFQ Mode | rfq_mode | Dropdown | Y | Email / Portal / Phone |
| RFQ Documents | rfq_documents | File Upload |  | Specs |
| RFQ Status | rfq_status | Dropdown | Y | Open / Closed / Cancelled |
| Quote Count Expected | quote_count_expected | Number |  | Typically 3 |
| Skip RFQ Flag | skip_rfq_flag | Checkbox |  | Requires purchase manager approval |
| Skip RFQ Justification | skip_rfq_justification | Multi-line | C | Mandatory when skip flag = true |
| Purchase Manager Approval | purchase_manager_approval | Lookup (Stakeholder User) |  |  |
| Approval Attachment | approval_attachment | File Upload |  |  |
| Dispatch ETA Updates | dispatch_eta_updates | Subform |  | Anticipated arrival |

#### Dispatch ETA Updates (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Update Date | update_date | Date-Time | Y |  |
| Updated By | updated_by | Lookup (Stakeholder User) | Y |  |
| Expected Arrival | expected_arrival | Date | Y |  |
| Remarks | remarks | Multi-line |  |  |

### Quote Response
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Quote ID | quote_id | Auto Number | Y |  |
| RFQ | rfq | Lookup (RFQ Header) | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Quote Date | quote_date | Date | Y |  |
| Price Valid Till | price_valid_till | Date |  |  |
| Currency | currency | Dropdown | Y |  |
| Quote Lines | quote_lines | Subform | Y |  |
| Freight Terms | freight_terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Payment Terms | payment_terms | Dropdown | Y | Inherit from vendor but editable |
| Delivery Terms | delivery_terms | Multi-line |  |  |
| Lead Time (Days) | lead_time_days | Number |  |  |
| Attachments | attachments | File Upload |  | Vendor quote |
| Remarks | remarks | Multi-line |  |  |
| Evaluation Score | evaluation_score | Decimal |  | Computed |
| Chosen Flag | chosen_flag | Checkbox |  |  |

#### Quote Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| PR Line | pr_line | Lookup (PR Line) | Y |  |
| Product/Service | product_service | Lookup (Product) | Y |  |
| Specification | specification | Multi-line |  |  |
| Quantity Offered | quantity_offered | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Unit Price | unit_price | Currency | Y |  |
| Discount % | discount | Decimal |  |  |
| GST % | gst | Decimal | Y |  |
| Freight Charge | freight_charge | Currency |  |  |
| Delivery Timeline | delivery_timeline | Number |  | Days |

### Quote Evaluation
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Evaluation ID | evaluation_id | Auto Number | Y |  |
| RFQ | rfq | Lookup (RFQ Header) | Y |  |
| Evaluation Date | evaluation_date | Date | Y |  |
| Evaluated By | evaluated_by | Lookup (Stakeholder User) | Y |  |
| Comparison Table | comparison_table | Subform | Y | Vendor comparisons |
| Best Quote Flag | best_quote_flag | Checkbox |  |  |
| Recommended Vendor | recommended_vendor | Lookup (Vendor) |  |  |
| Justification Notes | justification_notes | Multi-line | C | Mandatory when best quote not chosen |
| Approval Status | approval_status | Dropdown | Y | Pending / Approved / Rejected |
| Approval Trail | approval_trail | Subform |  | Purchase Manager approval |

#### Comparison Table (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Total Cost | total_cost | Currency | Y | Sum of lines |
| Lead Time | lead_time | Number |  |  |
| Freight Terms | freight_terms | Dropdown |  |  |
| Payment Terms | payment_terms | Dropdown |  |  |
| Score | score | Decimal |  | Weighted |
| Remarks | remarks | Multi-line |  |  |

### Purchase Order (PO)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| PO No. | po_no | Auto Number | Y |  |
| Revision No. | revision_no | Number | Y | Rev 0 default |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Company | company | Lookup (Company) | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Linked PRs | linked_prs | Multi-select Lookup (Purchase Request) | Y |  |
| Linked RFQ | linked_rfq | Lookup (RFQ Header) |  |  |
| PO Date | po_date | Date | Y |  |
| Expected Delivery Start | expected_delivery_start | Date |  |  |
| Expected Delivery End | expected_delivery_end | Date |  |  |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Payment Terms | payment_terms | Dropdown | Y |  |
| Currency | currency | Dropdown | Y |  |
| PO Lines | po_lines | Subform | Y |  |
| Attachments | attachments | File Upload |  | Signed PO |
| Terms & Conditions | terms_and_conditions | Multi-line |  |  |
| Approval Trail | approval_trail | Subform |  |  |
| Status | status | Dropdown | Y | Draft / Approved / Issued / Closed / Cancelled |
| Partial Receipt Flag | partial_receipt_flag | Checkbox |  |  |

#### PO Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Line No. | line_no | Number | Y |  |
| Product/Service | product_service | Lookup (Product) | Y |  |
| Description | description | Multi-line |  |  |
| Quantity Ordered | quantity_ordered | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Unit Price | unit_price | Currency | Y |  |
| Discount % | discount | Decimal |  |  |
| GST % | gst | Decimal | Y |  |
| Extra Commission | extra_commission | Currency |  | Applied for select products; included in landed cost |
| Agent Commission | agent_commission | Currency |  | Commission payable to external agents; included in landed cost |
| Freight Estimate | freight_estimate | Currency |  | Tentative freight |
| Delivery Schedule | delivery_schedule | Date |  |  |
| Linked PR Line | linked_pr_line | Lookup (PR Line) |  |  |
| Linked RFQ Line | linked_rfq_line | Lookup (Quote Line) |  |  |
| Batch Requirement Notes | batch_requirement_notes | Multi-line |  |  |

### PO ETA Update (Anticipated Arrival)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Update ID | update_id | Auto Number | Y |  |
| PO | po | Lookup (Purchase Order) | Y |  |
| Update Date | update_date | Date-Time | Y |  |
| Updated By | updated_by | Lookup (Stakeholder User) | Y | Purchase Coordinator or Warehouse Coordinator |
| Expected Arrival Date | expected_arrival_date | Date | Y |  |
| Status | status | Dropdown | Y | Pending / Updated |
| Remarks | remarks | Multi-line |  |  |

### Receipt Advice (Inbound)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Receipt Advice No. | receipt_advice_no | Auto Number | Y |  |
| Receipt Date | receipt_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Godown | godown | Dropdown | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Linked PO(s) | linked_pos | Multi-select Lookup (Purchase Order) | Y |  |
| Vehicle Number | vehicle_number | Single Line |  |  |
| Driver Name | driver_name | Single Line |  |  |
| Invoice Upload | invoice_upload | File Upload | Y | Vendor invoice |
| Packing List Upload | packing_list_upload | File Upload |  |  |
| Receipt Lines | receipt_lines | Subform | Y | Products received |
| Packing Material Lines | packing_material_lines | Subform |  | Packaging capture |
| Freight Details | freight_details | Subform |  | Local/Linehaul |
| Loading Unloading Wages | loading_unloading_wages | Subform |  |  |
| QC Routing | qc_routing | Dropdown | Y | Warehouse / QC Coordinator / QC Manager |
| QC Status | qc_status | Dropdown | Y | Pending / Pass / Fail / Hold |
| Partial Receipt Flag | partial_receipt_flag | Checkbox |  |  |
| Remarks | remarks | Multi-line |  |  |
| Created By | created_by | Lookup (Stakeholder User) | Y |  |
| Created Time | created_time | Date-Time | Y |  |

#### Receipt Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Line No. | line_no | Number | Y |  |
| PO Line | po_line | Lookup (PO Line) | Y |  |
| Product | product | Lookup (Product) | Y |  |
| Batch No. | batch_no | Single Line | C | Mandatory when batch tracking enabled |
| Expiry Date | expiry_date | Date |  |  |
| Quantity Received | quantity_received | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Extra Commission | extra_commission | Currency |  | Capture actual commission incurred |
| Agent Commission | agent_commission | Currency |  | Capture agent payouts associated with the receipt |
| Quantity Accepted | quantity_accepted | Decimal |  | Post QC |
| Quantity Rejected | quantity_rejected | Decimal |  |  |
| Godown Location | godown_location | Dropdown | Y | Filters by warehouse |
| Remarks | remarks | Multi-line |  |  |

#### Packing Material Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Packaging SKU | packaging_sku | Lookup (Product) | Y | Must be PACKING_MATERIAL |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Condition | condition | Dropdown |  | New / Damaged |

#### Freight Details (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Freight Type | freight_type | Dropdown | Y | Local Drayage / Linehaul |
| Transporter | transporter | Lookup (Transporter) | C | Required when company pays |
| Freight Terms | freight_terms | Dropdown | Y | Paid / To_Pay / Mixed |
| Tentative Charge | tentative_charge | Currency |  | Pre-filled from PO |
| Discount | discount | Currency |  | Optional |
| Payable By | payable_by | Dropdown | Y | Company / Vendor |
| Quantity Basis | quantity_basis | Decimal |  | Total shipment quantity for cost-per-unit reporting |
| Quantity UOM | quantity_uom | Dropdown |  | Tonnes / KG / KL / Units |
| Destination State | destination_state | Dropdown |  | Auto-populated from receiving warehouse |
| Cost Per Unit (Calc) | cost_per_unit_calc | Decimal (Formula) |  | Tentative charge minus discount divided by quantity basis |
| Payment Schedule | payment_schedule | Subform |  | Instalments |

#### Loading Unloading Wages (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Wage Type | wage_type | Dropdown | Y | Loading / Unloading |
| Contractor Vendor | contractor_vendor | Lookup (Vendor) | C | Mandatory if payable by company |
| Amount | amount | Currency | Y | Includes product value plus extra/agent commissions when applicable |
| TDS Applicable % | tds_applicable | Decimal |  |  |
| Payable By | payable_by | Dropdown | Y | Company / Vendor |
| Remarks | remarks | Multi-line |  |  |

#### Payment Schedule (nested subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Due Date | due_date | Date | Y |  |
| Amount | amount | Currency | Y |  |
| TDS % | tds | Decimal |  |  |
| Reminder Flag | reminder_flag | Checkbox |  | Triggers auto reminders |

### Freight Advice (Inbound)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Advice No. | advice_no | Auto Number | Y |  |
| Direction | direction | Dropdown | Y | Inbound |
| Receipt Advice | receipt_advice | Lookup (Receipt Advice) | Y |  |
| Transporter | transporter | Lookup (Transporter) | Y |  |
| Freight Type | freight_type | Dropdown | Y | Local Drayage / Linehaul |
| Created By | created_by | Lookup (Stakeholder User) | Y | Freight Coordinator originator |
| Created Date | created_date | Date | Y |  |
| Base Amount | base_amount | Currency | Y |  |
| Discount | discount | Currency |  |  |
| Loading Wages Amount | loading_wages_amount | Currency |  |  |
| Unloading Wages Amount | unloading_wages_amount | Currency |  |  |
| Quantity Basis | quantity_basis | Decimal |  | Total quantity covered by the advice |
| Quantity UOM | quantity_uom | Dropdown |  | Tonnes / KG / KL / Units |
| Cost Per Unit (Calc) | cost_per_unit_calc | Decimal (Formula) |  | Payable amount divided by quantity basis |
| Destination State | destination_state | Dropdown |  | Auto-derived from receiving warehouse |
| Payable Amount | payable_amount | Currency | Y | Base - discount + wages |
| Payment Schedule | payment_schedule | Subform |  |  |
| Approval Workflow | approval_workflow | Subform |  | Freight Coordinator → Finance Manager |
| Status | status | Dropdown | Y | Draft / Pending Approval / Approved / Paid |

### Vendor Payment Advice
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Advice No. | advice_no | Auto Number | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Source Document Type | source_document_type | Dropdown | Y | PO / Receipt / Freight / Wage / Credit Note |
| Source Document | source_document | Lookup (Varies) | Y | Dynamic lookup |
| Amount | amount | Currency | Y |  |
| Tax Components | tax_components | Subform |  | TDS/TCS |
| Due Date | due_date | Date | Y |  |
| Payment Method | payment_method | Dropdown | Y | Bank Transfer / Cash / Cheque / UPI |
| Prepared By | prepared_by | Lookup (Stakeholder User) | Y | Warehouse Coordinator (Office) originator |
| Approval Workflow | approval_workflow | Subform | Y | Finance Manager → Office Manager |
| Status | status | Dropdown | Y | Draft / Pending / Approved / Paid / On Hold |
| Notes | notes | Multi-line |  |  |

#### Tax Components (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Tax Type | tax_type | Dropdown | Y | TDS / TCS |
| Rate % | rate | Decimal | Y |  |
| Amount | amount | Currency | Y |  |

---

## 3. Sales Module

### Customer PO Upload
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Upload ID | upload_id | Auto Number | Y |  |
| Customer | customer | Lookup (Customer) | Y |  |
| Upload Date | upload_date | Date-Time | Y |  |
| PO File | po_file | File Upload | Y | PDF |
| AI Parser Confidence | ai_parser_confidence | Decimal | Y |  |
| Parsed PO Number | parsed_po_number | Single Line |  |  |
| Parsed PO Date | parsed_po_date | Date |  |  |
| Delivery Location | delivery_location | Dropdown |  | Suggest price list |
| Parsed Lines | parsed_lines | Subform |  | Output of parser |
| Manual Review Required | manual_review_required | Checkbox |  | Auto checked if confidence < threshold |
| Review Comments | review_comments | Multi-line |  |  |
| Status | status | Dropdown | Y | Uploaded / Parsed / Converted / Archived |
| Linked Sales Order | linked_sales_order | Lookup (Sales Order) |  |  |

#### Parsed Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product Description | product_description | Single Line |  |  |
| Quantity | quantity | Decimal |  |  |
| UOM | uom | Dropdown |  |  |
| Price | price | Currency |  |  |
| Parsed SKU | parsed_sku | Lookup (Product) |  | Auto-mapped |
| Confidence % | confidence | Decimal |  |  |

### Sales Order (SO)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| SO No. | so_no | Auto Number | Y |  |
| Customer | customer | Lookup (Customer) | Y |  |
| Company | company | Lookup (Company) | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Price List | price_list | Lookup (Price List) | Y | Filter by customer |
| Credit Terms | credit_terms | Dropdown | Y | Inherit from customer |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Customer PO Reference | customer_po_reference | Lookup (Customer PO Upload) |  |  |
| SO Date | so_date | Date | Y |  |
| Required Ship Date | required_ship_date | Date |  |  |
| Lines | lines | Subform | Y |  |
| Remarks | remarks | Multi-line |  |  |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |
| Approval Date | approval_date | Date-Time |  |  |
| Assigned Warehouse Stakeholders | assigned_warehouse_stakeholders | Multi-select Lookup (Stakeholder User) |  | Auto-share |

#### SO Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Line No. | line_no | Number | Y |  |
| Product | product | Lookup (Product) | Y | Must exist in price list |
| Batch Preference | batch_preference | Single Line |  |  |
| Quantity Ordered | quantity_ordered | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Unit Price | unit_price | Currency | Y | From price list |
| Discount % | discount | Decimal |  |  |
| GST % | gst | Decimal | Y |  |
| Delivery Schedule Date | delivery_schedule_date | Date |  |  |
| Remarks | remarks | Multi-line |  |  |
| Reserved Qty | reserved_qty | Decimal |  | Updated at dispatch |

### Dispatch Challan (DC)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| DC No. | dc_no | Auto Number | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Dispatch Date | dispatch_date | Date | Y |  |
| Transporter | transporter | Lookup (Transporter) |  |  |
| Freight Rate Type | freight_rate_type | Dropdown |  | Per km / Flat |
| Freight Rate Value | freight_rate_value | Currency |  |  |
| Freight Amount Total | freight_amount_total | Currency |  |  |
| Lorry No. | lorry_no | Single Line |  |  |
| Driver Contact | driver_contact | Phone |  |  |
| Linked SO Lines | linked_so_lines | Multi-select Lookup (SO Line) | Y |  |
| DC Lines | dc_lines | Subform | Y | Consolidated products |
| Delivery Locations | delivery_locations | Subform |  | For multi-drop |
| Documents | documents | File Upload |  | DC PDF |
| Status | status | Dropdown | Y | Draft / Released / Delivered / Closed |
| Created By | created_by | Lookup (Stakeholder User) | Y |  |
| Freight Advice Link | freight_advice_link | Lookup (Freight Advice) |  | Outbound |

#### DC Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line | C | Required if batch tracking |
| Quantity Dispatched | quantity_dispatched | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Linked SO Line | linked_so_line | Lookup (SO Line) | Y |  |
| Weight | weight | Decimal |  | Optional for weighment |

#### Delivery Locations (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Sequence | sequence | Number | Y |  |
| Shipping Address | shipping_address | Lookup (Customer Shipping Address) | Y |  |
| Quantity for Location | quantity_for_location | Decimal | Y |  |
| Estimated Arrival | estimated_arrival | Date |  |  |

### Sales Invoice Check
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Invoice Check ID | invoice_check_id | Auto Number | Y |  |
| DC Reference | dc_reference | Lookup (Dispatch Challan) | Y |  |
| Statutory Invoice Upload | statutory_invoice_upload | File Upload | Y | External invoice |
| Invoice Number | invoice_number | Single Line | Y |  |
| Invoice Date | invoice_date | Date | Y |  |
| Total Value (Upload) | total_value_upload | Currency | Y | Parsed |
| Total Value (SO) | total_value_so | Currency | Y | Computed |
| Variance Amount | variance_amount | Currency | Y |  |
| Variance Flag | variance_flag | Dropdown | Y | Within Tolerance / Requires Review |
| Remarks | remarks | Multi-line |  |  |
| Acceptance Timestamp | acceptance_timestamp | Date-Time |  |  |
| Accepted By | accepted_by | Lookup (Stakeholder User) |  |  |

### Freight Advice (Outbound)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Advice No. | advice_no | Auto Number | Y |  |
| Direction | direction | Dropdown | Y | Outbound |
| Dispatch Challan | dispatch_challan | Lookup (Dispatch Challan) | Y |  |
| Transporter | transporter | Lookup (Transporter) | Y |  |
| Freight Type | freight_type | Dropdown | Y | Local Drayage / Linehaul |
| Created By | created_by | Lookup (Stakeholder User) | Y | Freight Coordinator originator |
| Created Date | created_date | Date | Y |  |
| Base Amount | base_amount | Currency | Y |  |
| Discount | discount | Currency |  |  |
| Loading Wages Amount | loading_wages_amount | Currency |  |  |
| Unloading Wages Amount | unloading_wages_amount | Currency |  |  |
| Shipment Quantity | shipment_quantity | Decimal |  | Total quantity dispatched |
| Quantity UOM | quantity_uom | Dropdown |  | Tonnes / KG / KL / Units |
| Cost Per Unit (Calc) | cost_per_unit_calc | Decimal (Formula) |  | Payable amount divided by shipment quantity |
| Destination State | destination_state | Dropdown |  | Auto-populated from delivery address |
| Payable Amount | payable_amount | Currency | Y |  |
| Payment Schedule | payment_schedule | Subform |  |  |
| Approval Workflow | approval_workflow | Subform |  | Freight Coordinator → Finance Manager |
| Status | status | Dropdown | Y | Draft / Pending Approval / Approved / Paid |

### Receivable Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger ID | ledger_id | Auto Number | Y |  |
| Customer | customer | Lookup (Customer) | Y |  |
| Invoice Reference | invoice_reference | Lookup (Sales Invoice Check) | Y |  |
| Invoice Date | invoice_date | Date | Y |  |
| Due Date | due_date | Date | Y |  |
| Amount | amount | Currency | Y |  |
| Amount Paid | amount_paid | Currency |  |  |
| Balance | balance | Currency | Y |  |
| Payment Status | payment_status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Reminder Dates | reminder_dates | Subform |  | Auto reminders |
| Escalation Flag | escalation_flag | Checkbox |  | Trigger after 2 weeks |
| Notes | notes | Multi-line |  |  |

#### Reminder Dates (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Reminder Date | reminder_date | Date | Y |  |
| Reminder Sent By | reminder_sent_by | Lookup (Stakeholder User) |  |  |
| Reminder Method | reminder_method | Dropdown |  | Email / Call |

---

## 4. Production Module

### BOM Request
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Request No. | request_no | Auto Number | Y |  |
| Request Date | request_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Requested By | requested_by | Lookup (Stakeholder User) | Y | Warehouse Coordinator |
| Production Template | production_template | Lookup (Template Library) | Y |  |
| Output Product | output_product | Lookup (Product) | Y |  |
| Output Quantity | output_quantity | Decimal | Y |  |
| Required Completion Date | required_completion_date | Date |  |  |
| Auto-calculated Inputs | auto_calculated_inputs | Subform | Y | Computed from template |
| Shortfall Summary | shortfall_summary | Multi-line |  |  |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |
| Approved Date | approved_date | Date-Time |  |  |
| Excel Export Link | excel_export_link | URL |  | Download BOM |
| Notes | notes | Multi-line |  |  |

#### Auto-calculated Inputs (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Required Qty | required_qty | Decimal | Y |  |
| Available Qty | available_qty | Decimal | Y | From stock |
| Shortfall Qty | shortfall_qty | Decimal | Y | Negative allowed |
| Purpose | purpose | Dropdown | Y | RM / PM / Wage |

### Material Issue
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Issue No. | issue_no | Auto Number | Y |  |
| Issue Date | issue_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Work Order | work_order | Lookup (Work Order) | Y |  |
| Issued By | issued_by | Lookup (Stakeholder User) | Y |  |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |
| Issue Lines | issue_lines | Subform | Y |  |
| Remarks | remarks | Multi-line |  |  |

#### Issue Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch Out | batch_out | Single Line | C | Required when batch tracking |
| Godown | godown | Dropdown | Y |  |
| Quantity Issued | quantity_issued | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Reserved for Template | reserved_for_template | Checkbox |  | Packing material reservation |

### Work Order / Production Batch
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Batch ID | batch_id | Auto Number | Y |  |
| Work Order No. | work_order_no | Single Line | Y | Display |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Production Template | production_template | Lookup (Template Library) | Y | Includes revision |
| Template Revision | template_revision | Number | Y |  |
| Linked Sales Order | linked_sales_order | Lookup (Sales Order) |  |  |
| Linked Dispatch Challan | linked_dispatch_challan | Lookup (Dispatch Challan) |  |  |
| Planned Start Date | planned_start_date | Date | Y |  |
| Planned End Date | planned_end_date | Date |  |  |
| Actual Start Date | actual_start_date | Date |  |  |
| Actual End Date | actual_end_date | Date |  |  |
| Stage Status | stage_status | Dropdown | Y | Material Issue / Mixing / Packing / QC / Closed |
| Input Consumption | input_consumption | Subform | Y | Actual usage |
| Output Products | output_products | Subform | Y | Manufactured goods |
| Damage Report | damage_report | Subform |  | Damage / scrap |
| QC Request | qc_request | Lookup (QC Request) |  |  |
| Wage Method | wage_method | Dropdown |  | Template Rate / Headcount |
| Wage Vouchers | wage_vouchers | Subform |  | Linked vouchers |
| Yield Log Reference | yield_log_reference | Lookup (Production Yield Log) |  |  |
| Rework Flag | rework_flag | Checkbox |  | For reformulation |
| Parent Batch | parent_batch | Lookup (Work Order) |  | For rework linkage |
| Notes | notes | Multi-line |  |  |

#### Input Consumption (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Planned Qty | planned_qty | Decimal | Y | From template |
| Actual Qty | actual_qty | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Batch Used | batch_used | Single Line | C |  |
| Godown | godown | Dropdown | Y |  |
| Yield Loss % | yield_loss | Decimal |  | Capture deviations |

#### Output Products (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch ID | batch_id | Single Line | Y | Auto-generated |
| Quantity Produced | quantity_produced | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Purity % | purity | Decimal | C | Required when yield tracking includes purity |
| AI Content | ai_content | Decimal | C | Required when tracked |
| QC Status | qc_status | Dropdown | Y | Pending / Pass / Fail / Hold |

#### Damage Report (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Stage | stage | Dropdown | Y | Mixing / Packing / QC |
| Description | description | Multi-line | Y |  |
| Quantity Lost | quantity_lost | Decimal |  |  |
| UOM | uom | Dropdown |  |  |
| Handling Action | handling_action | Dropdown |  | Scrap / Rework |

#### Wage Vouchers (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Wage Voucher | wage_voucher | Lookup (Wage Voucher) | Y |  |
| Amount | amount | Currency | Y |  |

### Wage Voucher (Production)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Voucher No. | voucher_no | Auto Number | Y |  |
| Work Order | work_order | Lookup (Work Order) | Y |  |
| Wage Type | wage_type | Dropdown | Y | Template Rate / Headcount |
| Contractor Vendor | contractor_vendor | Lookup (Vendor) | C | Mandatory for contractor |
| Staff Group | staff_group | Multi-select Lookup (Staff) | C | Mandatory for headcount |
| Hours / Tasks | hours_tasks | Subform | Y |  |
| Amount | amount | Currency | Y |  |
| TDS % | tds | Decimal |  |  |
| Prepared By | prepared_by | Lookup (Stakeholder User) | Y | Warehouse Coordinator (Office) originator |
| Prepared Date | prepared_date | Date | Y |  |
| Approval Workflow | approval_workflow | Subform | Y | Warehouse Coordinator (Office) → Finance Manager |
| Status | status | Dropdown | Y | Draft / Pending / Approved / Paid |
| Remarks | remarks | Multi-line |  |  |

#### Hours / Tasks (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Staff | staff | Lookup (Staff) |  | Required for headcount |
| Task Description | task_description | Multi-line | Y |  |
| Hours Worked | hours_worked | Decimal |  |  |
| Quantity Produced | quantity_produced | Decimal |  | For incentive |

### Production Yield Log
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Log ID | log_id | Auto Number | Y |  |
| Work Order | work_order | Lookup (Work Order) | Y |  |
| Product | product | Lookup (Product) | Y |  |
| Planned Yield % | planned_yield | Decimal |  |  |
| Actual Output Qty | actual_output_qty | Decimal | Y |  |
| Purity % | purity | Decimal | C |  |
| AI Content | ai_content | Decimal | C |  |
| Variance % | variance | Decimal | Y |  |
| Remarks | remarks | Multi-line |  |  |
| Report Date | report_date | Date | Y |  |

---

## 5. Quality Control Module

### QC Parameter Library
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Parameter Code | parameter_code | Single Line | Y |  |
| Parameter Name | parameter_name | Single Line | Y |  |
| Unit | unit | Single Line |  |  |
| Applicable Template | applicable_template | Lookup (Template Library) |  |  |
| Applicable Product | applicable_product | Lookup (Product) |  |  |
| Acceptable Min | acceptable_min | Decimal |  |  |
| Acceptable Max | acceptable_max | Decimal |  |  |
| Critical Flag | critical_flag | Checkbox |  |  |
| Notes | notes | Multi-line |  |  |

### QC Request
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Request No. | request_no | Auto Number | Y |  |
| Request Date | request_date | Date | Y |  |
| Requested By | requested_by | Lookup (Stakeholder User) | Y | Warehouse roles |
| Requestor Role | requestor_role | Dropdown | Y | Warehouse Supervisor / Coordinator / Manager |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line | C |  |
| Stage | stage | Dropdown | Y | Receipt / In-Process / Finished / Sales Return |
| QC Template | qc_template | Lookup (Template Library) | Y |  |
| Selected Parameters | selected_parameters | Subform |  | Optional overrides |
| Sample Photo | sample_photo | Image Upload | Y |  |
| Sample Qty | sample_qty | Decimal |  |  |
| Priority | priority | Dropdown |  | Normal / Urgent |
| Remarks | remarks | Multi-line |  |  |
| Status | status | Dropdown | Y | Requested / In Progress / Completed |
| Lab Code | lab_code | Single Line |  | Generated by coordinator |
| Counter Sample Required | counter_sample_required | Checkbox |  |  |

#### Selected Parameters (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Parameter | parameter | Lookup (QC Parameter Library) | Y |  |
| Override Range Min | override_range_min | Decimal |  |  |
| Override Range Max | override_range_max | Decimal |  |  |
| Notes | notes | Multi-line |  |  |

### QC Lab Job
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Job No. | job_no | Auto Number | Y |  |
| QC Request | qc_request | Lookup (QC Request) | Y |  |
| Analyst | analyst | Lookup (Stakeholder User) | Y |  |
| Assigned Parameters | assigned_parameters | Subform | Y |  |
| Sample Received Date | sample_received_date | Date | Y |  |
| Results Attachment | results_attachment | File Upload |  | Raw data |
| Comments | comments | Multi-line |  |  |
| Status | status | Dropdown | Y | Assigned / In Progress / Completed |

#### Assigned Parameters (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Parameter | parameter | Lookup (QC Parameter Library) | Y |  |
| Result Value | result_value | Decimal |  |  |
| Result Text | result_text | Multi-line |  |  |
| Result Photo | result_photo | Image Upload |  |  |
| Pass/Fail | pass_fail | Dropdown |  |  |

### QC Final Report
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Report No. | report_no | Auto Number | Y |  |
| QC Request | qc_request | Lookup (QC Request) | Y |  |
| Template Revision | template_revision | Number | Y |  |
| Prepared By | prepared_by | Lookup (Stakeholder User) | Y | Coordinator or Manager |
| Prepared Date | prepared_date | Date | Y |  |
| Overall Result | overall_result | Dropdown | Y | Pass / Fail / Rework |
| Remarks | remarks | Multi-line |  |  |
| Digital Signature | digital_signature | File Upload | C | Required if template demands |
| Distribution List | distribution_list | Multi-select Lookup (Stakeholder User) |  |  |
| Attachments | attachments | File Upload |  | Final COA |

### Counter Sample Register
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Sample ID | sample_id | Auto Number | Y |  |
| QC Request | qc_request | Lookup (QC Request) | Y |  |
| Storage Location | storage_location | Dropdown | Y | Warehouse / QC Lab |
| Shelf | shelf | Single Line |  |  |
| Bin | bin | Single Line |  |  |
| Issued To | issued_to | Lookup (Stakeholder User) |  |  |
| Issue Date | issue_date | Date |  |  |
| Expected Return Date | expected_return_date | Date |  |  |
| Actual Return Date | actual_return_date | Date |  |  |
| Reminder Sent | reminder_sent | Checkbox |  | Auto-reminder |
| Disposal Date | disposal_date | Date |  |  |
| Disposal Approved By | disposal_approved_by | Lookup (Stakeholder User) |  |  |

---

## 6. Inventory, Logistics & Returns

### Inventory Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger Entry ID | ledger_entry_id | Auto Number | Y |  |
| Transaction Date | transaction_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Godown | godown | Dropdown | Y |  |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity In | quantity_in | Decimal |  |  |
| Quantity Out | quantity_out | Decimal |  |  |
| UOM | uom | Dropdown | Y |  |
| Transaction Type | transaction_type | Dropdown | Y | Receipt / Issue / Transfer / Adjustment / Dispatch |
| Source Document | source_document | Lookup (Varies) | Y |  |
| Cost | cost | Currency |  |  |
| Status | status | Dropdown | Y | Available / In Transit / Reserved |
| FIFO Layer ID | fifo_layer_id | Single Line |  | Valuation |
| Remarks | remarks | Multi-line |  |  |

### Stock Transfer DC
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Transfer No. | transfer_no | Auto Number | Y |  |
| Created Date | created_date | Date | Y |  |
| From Warehouse | from_warehouse | Lookup (Warehouse) | Y |  |
| To Warehouse | to_warehouse | Lookup (Warehouse) | Y |  |
| Dispatch Date | dispatch_date | Date |  |  |
| Transporter | transporter | Lookup (Transporter) |  |  |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Loading Wages | loading_wages | Currency |  |  |
| Freight Amount | freight_amount | Currency |  |  |
| Transfer Lines | transfer_lines | Subform | Y | Products |
| Status | status | Dropdown | Y | Draft / In Transit / Received / Closed |
| Documents | documents | File Upload |  | DC |

#### Transfer Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line | C |  |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Source Godown | source_godown | Dropdown | Y |  |
| Destination Godown | destination_godown | Dropdown | Y |  |

### Stock Transfer Receipt
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Receipt No. | receipt_no | Auto Number | Y |  |
| Receipt Date | receipt_date | Date | Y |  |
| From Warehouse | from_warehouse | Lookup (Warehouse) | Y |  |
| To Warehouse | to_warehouse | Lookup (Warehouse) | Y |  |
| Linked Transfer | linked_transfer | Lookup (Stock Transfer DC) | Y |  |
| Received By | received_by | Lookup (Stakeholder User) | Y |  |
| Receipt Lines | receipt_lines | Subform | Y |  |
| QC Result | qc_result | Dropdown |  | Pass / Fail |
| Variance Notes | variance_notes | Multi-line |  |  |
| Freight Details | freight_details | Subform |  | Local drayage |
| Loading Unloading Wages | loading_unloading_wages | Subform |  |  |
| Status | status | Dropdown | Y | Draft / Completed |

#### Receipt Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity Dispatched | quantity_dispatched | Decimal | Y |  |
| Quantity Received | quantity_received | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Received Godown | received_godown | Dropdown | Y |  |
| Condition | condition | Dropdown |  | Good / Damaged |

### Warehouse Shifting
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Shifting No. | shifting_no | Auto Number | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Request Date | request_date | Date | Y |  |
| From Godown | from_godown | Dropdown | Y |  |
| To Godown | to_godown | Dropdown | Y |  |
| Reason Code | reason_code | Dropdown | Y | Damage / Space Optimisation / Audit / Other |
| Other Reason | other_reason | Multi-line | C | Mandatory when Reason = Other |
| Products | products | Subform | Y |  |
| Freight/Wage Drafts | freight_wage_drafts | Subform |  |  |
| Status | status | Dropdown | Y | Draft / Pending Approval / Approved / Completed |
| In-Transit Flag | in_transit_flag | Checkbox |  |  |
| Attachments | attachments | File Upload |  | Evidence |

#### Products (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |

#### Freight/Wage Drafts (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Expense Type | expense_type | Dropdown | Y | Freight / Loading / Unloading |
| Vendor | vendor | Lookup (Vendor/Transporter) | C | Mandatory when payable by company |
| Amount | amount | Currency | Y |  |
| Payable By | payable_by | Dropdown | Y | Sending Warehouse / Receiving Warehouse |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved |

### Job Work Order
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Order No. | order_no | Auto Number | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Template | template | Lookup (Template Library) | Y |  |
| Template Revision | template_revision | Number | Y |  |
| Start Date | start_date | Date | Y |  |
| Expected Completion Date | expected_completion_date | Date |  | From template |
| Turnaround Threshold | turnaround_threshold | Number |  | For alerts |
| Materials Supplied | materials_supplied | Subform | Y |  |
| Outputs Expected | outputs_expected | Subform | Y |  |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Status | status | Dropdown | Y | Draft / In Progress / Completed |
| Alerts Enabled | alerts_enabled | Checkbox |  | Trigger overdue reminders |

#### Materials Supplied (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Material Type | material_type | Dropdown | Y | RM / PM / Machine |
| Product/Machine | product_machine | Lookup (Product or Machine) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |

#### Outputs Expected (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Expected Quantity | expected_quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Expected Batch Suffix | expected_batch_suffix | Single Line |  | For tracking |

### Job Work DC
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| JW DC No. | jw_dc_no | Auto Number | Y |  |
| Job Work Order | job_work_order | Lookup (Job Work Order) | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Dispatch Date | dispatch_date | Date | Y |  |
| Transporter | transporter | Lookup (Transporter) |  |  |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Issued Materials | issued_materials | Subform | Y |  |
| Documents | documents | File Upload |  | DC, challan |
| Status | status | Dropdown | Y | Draft / Dispatched / Completed |

#### Issued Materials (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Material Type | material_type | Dropdown | Y | RM / PM / Machine |
| Product/Machine | product_machine | Lookup (Product or Machine) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Expected Return Date | expected_return_date | Date |  |  |

### Job Work Receipt
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Receipt No. | receipt_no | Auto Number | Y |  |
| Receipt Date | receipt_date | Date | Y |  |
| Job Work Order | job_work_order | Lookup (Job Work Order) | Y |  |
| JW DC Reference | jw_dc_reference | Lookup (Job Work DC) | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Returned Goods | returned_goods | Subform | Y |  |
| New Batch ID | new_batch_id | Single Line |  | Distinct batch |
| QC Result | qc_result | Dropdown |  | Pass / Fail |
| Pending Quantity | pending_quantity | Decimal | Y |  |
| Charges | charges | Subform |  | Job work + freight |
| Status | status | Dropdown | Y | Draft / Completed |

#### Returned Goods (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line | Y |  |
| Quantity Received | quantity_received | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Viability | viability | Dropdown |  | Resaleable / Reformulate / Scrap |

#### Charges (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Charge Type | charge_type | Dropdown | Y | Job Work / Freight / Loading / Unloading |
| Amount | amount | Currency | Y |  |
| TDS % | tds | Decimal |  | Separate rates |
| Payable By | payable_by | Dropdown | Y | Company / Vendor |

### Sales Return Advice
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Return No. | return_no | Auto Number | Y |  |
| Return Date | return_date | Date | Y |  |
| Customer | customer | Lookup (Customer) | Y |  |
| Original Invoice | original_invoice | Lookup (Sales Invoice Check) | Y |  |
| Returned By | returned_by | Single Line |  | Customer contact |
| Received Warehouse | received_warehouse | Lookup (Warehouse) | Y |  |
| Return Lines | return_lines | Subform | Y |  |
| Freight Terms | freight_terms | Dropdown | Y |  |
| Freight Charges | freight_charges | Subform |  |  |
| Loading/Unloading Charges | loading_unloading_charges | Subform |  |  |
| QC Requirement | qc_requirement | Dropdown | Y | Required / Optional |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approval Trail | approval_trail | Subform |  |  |
| Remarks | remarks | Multi-line |  |  |

#### Return Lines (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line |  |  |
| Quantity Returned | quantity_returned | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Condition | condition | Dropdown | Y | Resaleable / Reformulate / Scrap |
| Viability Notes | viability_notes | Multi-line |  |  |
| Packing Material Captured | packing_material_captured | Lookup (Product) |  |  |

#### Freight Charges (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Freight Type | freight_type | Dropdown | Y | Local Drayage / Linehaul |
| Transporter | transporter | Lookup (Transporter) |  |  |
| Amount | amount | Currency | Y |  |
| Discount | discount | Currency |  |  |
| Payable By | payable_by | Dropdown | Y | Company / Customer |

#### Loading/Unloading Charges (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Charge Type | charge_type | Dropdown | Y | Loading / Unloading |
| Contractor Vendor | contractor_vendor | Lookup (Vendor) |  |  |
| Amount | amount | Currency | Y |  |
| TDS % | tds | Decimal |  |  |
| Payable By | payable_by | Dropdown | Y | Company / Customer |

### Stock Adjustment
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Adjustment No. | adjustment_no | Auto Number | Y |  |
| Adjustment Date | adjustment_date | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Godown | godown | Dropdown | Y |  |
| Product | product | Lookup (Product) | Y |  |
| Batch | batch | Single Line |  |  |
| Adjustment Type | adjustment_type | Dropdown | Y | Positive / Negative |
| Quantity | quantity | Decimal | Y |  |
| UOM | uom | Dropdown | Y |  |
| Reason Code | reason_code | Dropdown | Y | Damage / Expiry / Shortage / Surplus / Audit Correction / Others |
| Other Reason | other_reason | Multi-line | C | Mandatory if Others |
| Evidence Attachments | evidence_attachments | File Upload | Y | Photos, documents |
| Value Impact | value_impact | Currency | Y | Auto-calculated |
| Finance Review Required | finance_review_required | Checkbox | Y | Auto flag if value > ₹25,000 |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Rejected |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |
| Approval Date | approval_date | Date-Time |  |  |
| Notified To | notified_to | Multi-select Lookup (Stakeholder User) |  | Office Manager notification |
| Notes | notes | Multi-line |  |  |

---

## 7. Finance Module

### Vendor Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger ID | ledger_id | Auto Number | Y |  |
| Vendor | vendor | Lookup (Vendor) | Y |  |
| Document Type | document_type | Dropdown | Y | PO / Receipt / Invoice / Freight / Wage / Credit Note |
| Document Reference | document_reference | Lookup (Varies) | Y |  |
| Document Date | document_date | Date | Y |  |
| Debit Amount | debit_amount | Currency |  |  |
| Credit Amount | credit_amount | Currency |  |  |
| Tax Breakdown | tax_breakdown | Subform |  |  |
| Due Date | due_date | Date |  |  |
| Payment Status | payment_status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Ageing Bucket | ageing_bucket | Dropdown |  | 0-30 / 31-60 / >60 |
| Notes | notes | Multi-line |  |  |

#### Tax Breakdown (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Tax Type | tax_type | Dropdown | Y | GST / TDS / TCS |
| Rate % | rate | Decimal | Y |  |
| Amount | amount | Currency | Y |  |

### Payment Advice Workflow
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Advice No. | advice_no | Auto Number | Y |  |
| Beneficiary Type | beneficiary_type | Dropdown | Y | Vendor / Transporter / Contractor |
| Beneficiary | beneficiary | Lookup (Vendor/Transporter) | Y |  |
| Source Document | source_document | Lookup (Varies) | Y |  |
| Amount | amount | Currency | Y |  |
| TDS/TCS Details | tds_tcs_details | Subform |  |  |
| Due Date | due_date | Date | Y |  |
| Payment Method | payment_method | Dropdown | Y | Bank Transfer / Cash / Cheque / UPI |
| Bank Account | bank_account | Lookup (Vendor Bank Details) | C | Required for bank transfer |
| Prepared By | prepared_by | Lookup (Stakeholder User) | Y |  |
| Prepared Date | prepared_date | Date | Y |  |
| Finance Manager Approval | finance_manager_approval | Subform | Y | Stage 1 |
| Office Manager Authorization | office_manager_authorization | Subform | Y | Stage 2 |
| Payment Status | payment_status | Dropdown | Y | Draft / Pending Finance / Pending Authorization / Approved / Paid |
| Payment Reference | payment_reference | Single Line |  | Bank txn |
| Attachments | attachments | File Upload |  | Bank proof |

#### TDS/TCS Details (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Tax Type | tax_type | Dropdown | Y | TDS / TCS |
| Section | section | Single Line |  |  |
| Rate % | rate | Decimal | Y |  |
| Amount | amount | Currency | Y |  |

#### Finance Manager Approval (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Approved By | approved_by | Lookup (Stakeholder User) | Y |  |
| Approval Date | approval_date | Date-Time | Y |  |
| Remarks | remarks | Multi-line |  |  |

#### Office Manager Authorization (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Authorized By | authorized_by | Lookup (Stakeholder User) | Y |  |
| Authorization Date | authorization_date | Date-Time | Y |  |
| Remarks | remarks | Multi-line |  |  |

### Bank Statement Upload
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Upload ID | upload_id | Auto Number | Y |  |
| Bank Account | bank_account | Dropdown | Y |  |
| Statement Period Start | statement_period_start | Date | Y |  |
| Statement Period End | statement_period_end | Date | Y |  |
| Upload Date | upload_date | Date | Y |  |
| Statement File | statement_file | File Upload | Y | PDF/CSV |
| Parsing Status | parsing_status | Dropdown | Y | Pending / Parsed / Error |
| Auto-Matched Entries | auto_matched_entries | Subform |  |  |
| Exceptions | exceptions | Subform |  |  |
| Remarks | remarks | Multi-line |  |  |

#### Auto-Matched Entries (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Statement Line ID | statement_line_id | Single Line | Y |  |
| Match Type | match_type | Dropdown | Y | Payable / Receivable |
| Linked Document | linked_document | Lookup (Vendor Ledger / Customer Ledger) | Y |  |
| Amount | amount | Currency | Y |  |
| Status | status | Dropdown | Y | Confirmed / Pending |

#### Exceptions (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Statement Line ID | statement_line_id | Single Line | Y |  |
| Transaction Date | transaction_date | Date | Y |  |
| Amount | amount | Currency | Y |  |
| Suggested Match | suggested_match | Lookup (Ledger) |  |  |
| Exception Notes | exception_notes | Multi-line |  |  |
| Resolution Status | resolution_status | Dropdown | Y | Open / Resolved |

### Customer Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger ID | ledger_id | Auto Number | Y |  |
| Customer | customer | Lookup (Customer) | Y |  |
| Document Type | document_type | Dropdown | Y | Invoice / Receipt / Credit Note |
| Document Reference | document_reference | Lookup (Sales Invoice Check / Receipts) | Y |  |
| Document Date | document_date | Date | Y |  |
| Debit Amount | debit_amount | Currency |  |  |
| Credit Amount | credit_amount | Currency |  |  |
| Due Date | due_date | Date |  |  |
| Payment Status | payment_status | Dropdown | Y | Not Due / Partially Paid / Paid / Overdue |
| Reminder Sent Flags | reminder_sent_flags | Subform |  |  |
| Notes | notes | Multi-line |  |  |

### Freight Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger ID | ledger_id | Auto Number | Y |  |
| Direction | direction | Dropdown | Y | Inbound / Outbound / Transfer |
| Transporter | transporter | Lookup (Transporter) | Y |  |
| Freight Advice | freight_advice | Lookup (Freight Advice) | Y |  |
| Amount | amount | Currency | Y |  |
| Discount | discount | Currency |  |  |
| Shipment Quantity | shipment_quantity | Decimal |  | Pulled from freight advice |
| Quantity UOM | quantity_uom | Dropdown |  |  |
| Cost Per Unit | cost_per_unit | Decimal |  | Stored for reporting |
| Destination State | destination_state | Dropdown |  | Enables cost-per-destination analytics |
| Payment Schedule | payment_schedule | Subform |  |  |
| Amount Paid | amount_paid | Currency |  |  |
| Balance | balance | Currency | Y |  |
| Reminder Flag | reminder_flag | Checkbox |  | Auto reminder on due date |
| Notes | notes | Multi-line |  |  |

### Wage Ledger
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Ledger ID | ledger_id | Auto Number | Y |  |
| Wage Voucher | wage_voucher | Lookup (Wage Voucher) | Y |  |
| Contractor/Staff Group | contractor_staff_group | Lookup (Vendor or Staff) | Y |  |
| Amount | amount | Currency | Y |  |
| TDS % | tds | Decimal |  |  |
| Payment Week | payment_week | Date | Y | Week ending date |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved / Paid |
| Settlement Method | settlement_method | Dropdown | Y | Bank Transfer / Cash |
| Notes | notes | Multi-line |  |  |

### Credit/Debit Note
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Note No. | note_no | Auto Number | Y |  |
| Note Type | note_type | Dropdown | Y | Credit / Debit |
| Vendor/Customer | vendor_customer | Lookup (Vendor or Customer) | Y |  |
| Source Document | source_document | Lookup (PO / Invoice / Sales Invoice Check) | Y |  |
| Amount | amount | Currency | Y |  |
| Tax | tax | Currency |  |  |
| Reason | reason | Multi-line | Y |  |
| Approval Status | approval_status | Dropdown | Y | Draft / Pending / Approved |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |
| Approval Date | approval_date | Date-Time |  |  |
| Ledger Posting Reference | ledger_posting_reference | Lookup (Ledger) |  |  |

### GST Reconciliation Report
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Report ID | report_id | Auto Number | Y |  |
| Reporting Period | reporting_period | Date Range | Y | Month/Quarter |
| Data Source | data_source | Dropdown | Y | Creator / GSTR-2B / GSTR-1 |
| Variance Summary | variance_summary | Multi-line |  |  |
| Adjustments | adjustments | Subform |  |  |
| Export File | export_file | File Upload |  | CSV for Tally |

#### Adjustments (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Adjustment Type | adjustment_type | Dropdown | Y | ITC Reversal / Additional Claim |
| Amount | amount | Currency | Y |  |
| Notes | notes | Multi-line |  |  |
| Approved By | approved_by | Lookup (Stakeholder User) |  |  |

### Petty Cash Register
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Register ID | register_id | Auto Number | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Coordinator | coordinator | Lookup (Stakeholder User) | Y |  |
| Opening Balance | opening_balance | Currency | Y |  |
| Transactions | transactions | Subform | Y |  |
| Current Balance | current_balance | Currency | Y | Auto-calculated |
| Last Reconciled Date | last_reconciled_date | Date |  |  |

#### Transactions (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Transaction Date | transaction_date | Date | Y |  |
| Voucher Reference | voucher_reference | Lookup (Payment Advice / Wage Voucher) | Y |  |
| Amount | amount | Currency | Y |  |
| Type | type | Dropdown | Y | Advance / Settlement |
| Notes | notes | Multi-line |  |  |

---

## 8. Attendance & HR Module

### Shift Definition
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Shift Code | shift_code | Single Line | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Shift Name | shift_name | Single Line | Y |  |
| Start Time | start_time | Time | Y |  |
| End Time | end_time | Time | Y |  |
| Break Duration (mins) | break_duration_mins | Number |  |  |
| Overtime Eligibility | overtime_eligibility | Checkbox |  |  |
| Attendance Calculation Rule | attendance_calculation_rule | Dropdown | Y | 8-hour / Custom |
| Grace Period Minutes | grace_period_minutes | Number |  |  |
| Approval Required | approval_required | Checkbox |  |  |

### Attendance Capture
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Record ID | record_id | Auto Number | Y |  |
| Staff | staff | Lookup (Staff) | Y |  |
| Date | date | Date | Y |  |
| Check-in Time | check_in_time | Date-Time | Y |  |
| Check-out Time | check_out_time | Date-Time |  |  |
| Entry Photo | entry_photo | Image Upload | Y | Retained 7 days |
| Exit Photo | exit_photo | Image Upload |  | Retained 7 days |
| Geo Latitude | geo_latitude | Decimal | Y | Must fall within warehouse geofence |
| Geo Longitude | geo_longitude | Decimal | Y |  |
| Face Match Confidence | face_match_confidence | Decimal | Y | From external API |
| Device ID | device_id | Single Line | Y | HR device |
| Shift | shift | Lookup (Shift Definition) | Y |  |
| Attendance Status | attendance_status | Dropdown | Y | Present / Absent / Half Day / Permission |
| Overtime Hours | overtime_hours | Decimal |  |  |
| Notes | notes | Multi-line |  |  |

### Leave Request
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Request No. | request_no | Auto Number | Y |  |
| Staff | staff | Lookup (Staff) | Y |  |
| Leave Type | leave_type | Dropdown | Y | Full Day / Half Day / Permission |
| Start Date | start_date | Date | Y |  |
| End Date | end_date | Date | C | Required when full-day leave |
| Duration (Hours) | duration_hours | Decimal | C | Required for permission |
| Reason | reason | Multi-line | Y |  |
| Attachment | attachment | File Upload |  | Medical proof |
| Status | status | Dropdown | Y | Pending / Approved / Rejected |
| Approver | approver | Lookup (Stakeholder User) |  |  |
| Approval Date | approval_date | Date-Time |  |  |

### Overtime Request
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Request No. | request_no | Auto Number | Y |  |
| Staff | staff | Lookup (Staff) | Y |  |
| Date | date | Date | Y |  |
| Shift | shift | Lookup (Shift Definition) |  |  |
| Hours Worked | hours_worked | Decimal | Y |  |
| Task Description | task_description | Multi-line | Y |  |
| Supporting Evidence | supporting_evidence | File Upload |  |  |
| Approval Status | approval_status | Dropdown | Y | Pending / Approved / Rejected |
| Approved By | approved_by | Lookup (Stakeholder User) |  | Warehouse Coordinator (Office) |
| Wage Integration Flag | wage_integration_flag | Checkbox |  | Creates wage voucher |

### Payroll Export
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Export ID | export_id | Auto Number | Y |  |
| Period Start | period_start | Date | Y |  |
| Period End | period_end | Date | Y |  |
| Warehouse | warehouse | Lookup (Warehouse) | Y |  |
| Staff Summary | staff_summary | Subform | Y |  |
| Attendance Metrics | attendance_metrics | Multi-line |  |  |
| Overtime Hours Total | overtime_hours_total | Decimal |  |  |
| Exceptions | exceptions | Multi-line |  |  |
| Export File | export_file | File Upload |  | CSV for payroll |

#### Staff Summary (subform)
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Staff | staff | Lookup (Staff) | Y |  |
| Present Days | present_days | Number | Y |  |
| Absent Days | absent_days | Number | Y |  |
| Overtime Hours | overtime_hours | Decimal |  |  |
| Wages Amount | wages_amount | Currency |  |  |

### Attendance Device Log
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Log ID | log_id | Auto Number | Y |  |
| Device ID | device_id | Single Line | Y |  |
| Event Time | event_time | Date-Time | Y |  |
| Event Type | event_type | Dropdown | Y | Capture / Sync |
| Status | status | Dropdown | Y | Success / Failed |
| Error Message | error_message | Multi-line |  |  |

---

## 9. Configuration & Audit

### System Parameters
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Parameter Name | parameter_name | Single Line | Y |  |
| Parameter Value | parameter_value | Single Line | Y |  |
| Module Scope | module_scope | Dropdown | Y | Purchase / Sales / Inventory / Finance / Attendance |
| Description | description | Multi-line |  |  |
| Last Updated By | last_updated_by | Lookup (Stakeholder User) | Y |  |
| Effective Date | effective_date | Date | Y |  |

### Decision Log
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Decision ID | decision_id | Auto Number | Y |  |
| Topic | topic | Single Line | Y |  |
| Stakeholders | stakeholders | Multi-select Lookup (Stakeholder User) | Y |  |
| Decision Details | decision_details | Multi-line | Y |  |
| Decision Date | decision_date | Date | Y |  |
| Follow-up Actions | follow_up_actions | Multi-line |  |  |

### Audit Trail
| Field | Link Name | Type | Req. | Notes |
| --- | --- | --- | --- | --- |
| Audit ID | audit_id | Auto Number | Y |  |
| Module | module | Dropdown | Y |  |
| Record ID | record_id | Single Line | Y |  |
| Action | action | Dropdown | Y | Create / Update / Delete / Approve |
| User | user | Lookup (Stakeholder User) | Y |  |
| Timestamp | timestamp | Date-Time | Y |  |
| Before Snapshot | before_snapshot | File Upload |  | JSON export |
| After Snapshot | after_snapshot | File Upload |  | JSON export |
| Remarks | remarks | Multi-line |  |  |

Use this catalogue with the ERD and flowchart libraries to ensure every workflow, approval, and integration touchpoint is fully supported by the underlying data structures.
