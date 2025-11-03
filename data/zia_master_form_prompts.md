# Zoho Zia Master Form Prompts

Run each prompt separately inside Zoho Zia in the listed order so lookup dependencies resolve correctly.

## Prompt 1

Create form "Company Master" (link name company_master). Purpose: Register each legal entity participating in procurement, sales, finance, and compliance.
Category: Core master.
Fields:
- Single-line (Unique) field "Company Code" (link name company_code); required; Short code used across modules and exports
- Single-line field "Legal Name" (link name legal_name); required; Registered legal entity name
- Single-line field "Trade Name" (link name trade_name); Optional doing-business-as name
- Single-line field "GSTIN" (link name gstin); required; GST registration; validate 15-character format
- Single-line field "PAN" (link name pan); For TDS/TCS calculations
- Single-line field "CIN" (link name cin); Corporate Identification Number
- Address field "Registered Address" (link name registered_address); required; Multi-line address
- Address field "Billing Address" (link name billing_address); required; Defaults on invoices
- Email field "Contact Email" (link name contact_email); Finance escalation
- Phone field "Contact Phone" (link name contact_phone)
- Dropdown field "Default Currency" (link name default_currency); required; Values maintained in system parameters
- Checkbox field "Books Export Flag" (link name books_export_flag); Toggle for Tally integration
- Date field "Active From" (link name active_from); required; Effective start date
- Date field "Active To" (link name active_to); Optional sunset
- Multi-line field "Notes" (link name notes); Additional remarks

## Prompt 2

Create form "Warehouse Master" (link name warehouse_master). Purpose: Define warehouses along with their godown and machinery inventories.
Category: Core master.
Fields:
- Single-line (Unique) field "Warehouse Code" (link name warehouse_code); required; Used in stock and logistics documents
- Lookup (Company) field "Company" (link name company); required; Owning entity
- Single-line field "Name" (link name name); required; Display name
- Dropdown field "Warehouse Type" (link name warehouse_type); required; Head Office / Factory / Job Work Partner
- Address field "Address" (link name address); required; Physical location
- Single-line field "City" (link name city); required
- Dropdown field "State" (link name state); required; For GST place of supply
- Dropdown field "Country" (link name country); required
- Single-line field "Pincode" (link name pincode); required
- Decimal field "Geo Latitude" (link name geo_latitude); required; Attendance geofence
- Decimal field "Geo Longitude" (link name geo_longitude); required; Attendance geofence
- Dropdown field "Time Zone" (link name time_zone); required; For SLA calculations
- Dropdown field "Default Currency" (link name default_currency); required; Inherits from company by default
- Lookup (Stakeholder User) field "Warehouse Coordinator (Office)" (link name warehouse_coordinator_office); conditionally required; Required for warehouses
- Lookup (Stakeholder User) field "Warehouse HR Coordinator" (link name warehouse_hr_coordinator); Optional
- Multi-select Lookup (Stakeholder User) field "Warehouse Manager(s)" (link name warehouse_managers)
- Multi-select Lookup (Stakeholder User) field "Warehouse Coordinator(s)" (link name warehouse_coordinators)
- Multi-select Lookup (Stakeholder User) field "Warehouse Supervisor(s)" (link name warehouse_supervisors)
- Subform field "Godown List" (link name godown_list); required; Contains godown level stock segregation
- Checkbox field "Active Flag" (link name active_flag); required; Deactivate to hide from new transactions
- Multi-line field "Notes" (link name notes)

Subform "Godown (subform)" fields:
- Single-line field "Godown Code" (link name godown_code); required; Unique within warehouse
- Single-line field "Godown Name" (link name godown_name); required
- Dropdown field "Storage Condition" (link name storage_condition); Ambient / Cold / Hazardous
- Dropdown field "Capacity UOM" (link name capacity_uom)
- Decimal field "Capacity Value" (link name capacity_value); Max storage
- Checkbox field "Batch Tracking Enabled" (link name batch_tracking_enabled); required; Controls batch-level location
- Checkbox field "Default QC Hold Area" (link name default_qc_hold_area); Flags quarantine
- Subform field "Machinery List" (link name machinery_list); Equipment housed in the godown

Subform "Machinery (Godown subform)" fields:
- Single-line field "Machine ID" (link name machine_id); required; Unique equipment identifier
- Single-line field "Machine Name" (link name machine_name); required
- Dropdown field "Category" (link name category); required; Capital Goods / Machine Spares / Production Line
- Date field "Commission Date" (link name commission_date)
- Lookup (Vendor) field "Maintenance Vendor" (link name maintenance_vendor); For service/job work
- Date field "Next Service Due" (link name next_service_due)
- Dropdown field "Status" (link name status); required; Active / Under Maintenance / Retired

Note: If Zoho Zia requires the Stakeholder User form to exist before adding the stakeholder lookup fields, revisit this form after Prompt 6 to add those lookups.

## Prompt 3

Create form "Role Definition" (link name role_definition). Purpose: Bundle permissions and approval thresholds for Zoho Creator sharing.
Category: Security master.
Fields:
- Single-line field "Role Code" (link name role_code); required; Unique role identifier
- Single-line field "Role Name" (link name role_name); required
- Multi-line JSON field "Module Permissions" (link name module_permissions); required; CRUD/approval rights per module
- Dropdown field "Data Scope" (link name data_scope); required; Global / Company / Warehouse
- Subform field "Approval Levels" (link name approval_levels); Specifies approvals handled
- Multi-line field "Default Share Rules" (link name default_share_rules); Creator share settings template
- Checkbox field "Active Flag" (link name active_flag); required

Subform "Approval Levels (subform)" fields:
- Dropdown field "Module" (link name module); required; Purchase / Sales / Production / etc.
- Dropdown field "Stage" (link name stage); required; Request / Evaluation / Payment
- Currency field "Min Amount" (link name min_amount); Threshold
- Currency field "Max Amount" (link name max_amount)

## Prompt 4

Create form "Shift Definition" (link name shift_definition). Purpose: Configure standard shifts and attendance calculation rules.
Category: HR master.
Fields:
- Single-line field "Shift Code" (link name shift_code); required
- Lookup (Warehouse) field "Warehouse" (link name warehouse); required
- Single-line field "Shift Name" (link name shift_name); required
- Time field "Start Time" (link name start_time); required
- Time field "End Time" (link name end_time); required
- Number field "Break Duration (mins)" (link name break_duration_mins)
- Checkbox field "Overtime Eligibility" (link name overtime_eligibility)
- Dropdown field "Attendance Calculation Rule" (link name attendance_calculation_rule); required; 8-hour / Custom
- Number field "Grace Period Minutes" (link name grace_period_minutes)
- Checkbox field "Approval Required" (link name approval_required)

## Prompt 5

Create form "Staff Master" (link name staff_master). Purpose: Maintain the complete roster of staff for attendance, HR, and wage processing.
Category: HR master.
Fields:
- Single-line (Unique) field "Staff ID" (link name staff_id); required; Official staff number
- Dropdown field "Staff Type" (link name staff_type); required; Employee (Stakeholder) / Staff
- Single-line field "First Name" (link name first_name); required
- Single-line field "Last Name" (link name last_name)
- Dropdown field "Gender" (link name gender)
- Date field "Date of Birth" (link name date_of_birth)
- Lookup (Company) field "Company" (link name company); required; Employer entity
- Lookup (Warehouse) field "Primary Location" (link name primary_location); required; For attendance
- Dropdown field "Department" (link name department)
- Single-line field "Designation" (link name designation); required
- Date field "Employment Start Date" (link name employment_start_date); required
- Date field "Employment End Date" (link name employment_end_date)
- Dropdown field "Employment Status" (link name employment_status); required; Active / On Leave / Resigned
- Lookup (Stakeholder User) field "HR Owner" (link name hr_owner); required; Controls approvals
- Lookup (Shift Definition) field "Shift Assignment" (link name shift_assignment); Defaults attendance
- Checkbox field "Overtime Eligible" (link name overtime_eligible)
- Checkbox field "Contractor Flag" (link name contractor_flag); For wages via vendor
- Lookup (Vendor) field "Contractor Vendor" (link name contractor_vendor); conditionally required; Mandatory if contractor flag checked
- Subform field "Bank Account" (link name bank_account); Payment details
- Subform field "ID Proofs" (link name id_proofs); Attachments
- Single-line field "Face Template ID" (link name face_template_id); required; External face recognition ID
- Image Upload field "Photo Reference" (link name photo_reference); required; Stored for 7 days
- Phone field "Contact Number" (link name contact_number)
- Phone field "Emergency Contact" (link name emergency_contact)
- Address field "Address" (link name address)
- Multi-line field "Remarks" (link name remarks)

Subform "Bank Account (subform)" fields:
- Single-line field "Account Holder" (link name account_holder); required
- Single-line field "Bank Name" (link name bank_name); required
- Single-line field "IFSC Code" (link name ifsc_code); required; Validate format
- Single-line field "Account Number" (link name account_number); required; Mask display
- Dropdown field "Account Type" (link name account_type)

Subform "ID Proofs (subform)" fields:
- Dropdown field "Document Type" (link name document_type); required; Aadhaar / PAN / License / Other
- Single-line field "Document Number" (link name document_number); required
- Date field "Expiry Date" (link name expiry_date)
- File Upload field "Attachment" (link name attachment); required

Note: If the HR Owner lookup cannot be created yet, add it after the Stakeholder User form (Prompt 6).

Note: Add the Contractor Vendor lookup once the Vendor Master (Prompt 12) exists if required.

## Prompt 6

Create form "Stakeholder User" (link name stakeholder_user). Purpose: Map portal users to stakeholder roles and warehouse scopes.
Category: Security master.
Fields:
- Single-line field "Portal User ID" (link name portal_user_id); required; Zoho portal identifier
- Lookup (Staff Master) field "Employee Record" (link name employee_record); required; Links to staff
- Email field "Primary Email" (link name primary_email); required
- Phone field "Mobile" (link name mobile)
- Multi-select Lookup (Role Definition) field "Assigned Roles" (link name assigned_roles); required; Supports multi-role users
- Lookup (Warehouse) field "Default Warehouse" (link name default_warehouse)
- Multi-select Lookup (Warehouse) field "Warehouse Scope" (link name warehouse_scope); Overrides default
- Dropdown field "Status" (link name status); required; Active / Suspended
- Date-time field "Last Accessed" (link name last_accessed)
- Multi-line field "Notes" (link name notes)

## Prompt 7

Create form "Service Catalogue" (link name service_catalogue). Purpose: Register services with tax and warehouse applicability.
Category: Service master.
Fields:
- Single-line field "Service Code" (link name service_code); required
- Single-line field "Name" (link name name); required
- Dropdown field "Category" (link name category); required; Warehouse Expense / Wages / Freight / Misc / Custom
- Dropdown field "Direction" (link name direction); required; Inbound / Outbound / Both
- Decimal field "Default TDS %" (link name default_tds)
- Decimal field "Default TCS %" (link name default_tcs)
- Multi-select Lookup (Warehouse) field "Warehouse Availability" (link name warehouse_availability)
- Multi-line field "Description" (link name description)
- Checkbox field "Active Flag" (link name active_flag); required

## Prompt 8

Create form "Template Library" (link name template_library). Purpose: Store reusable production, QC, job work, and document templates.
Category: Configuration master.
Fields:
- Single-line field "Template ID" (link name template_id); required
- Dropdown field "Template Type" (link name template_type); required; Production / QC Report / Job Work / Packing / Invoice
- Single-line field "Name" (link name name); required
- Multi-select Lookup (Warehouse) field "Warehouse Scope" (link name warehouse_scope); required
- Number field "Revision No." (link name revision_no); required; Rev 1, Rev 2, etc.
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Multi-line field "Layout JSON/XML" (link name layout_json_xml); required; Stores dynamic layout
- Checkbox field "Requires Digital Signature" (link name requires_digital_signature)
- Lookup (Stakeholder User) field "Created By" (link name created_by); required
- Subform field "Approval Log" (link name approval_log)
- Dropdown field "Status" (link name status); required; Draft / Active / Retired

Subform "Approval Log (subform)" fields:
- Lookup (Stakeholder User) field "Approved By" (link name approved_by); required
- Date-time field "Approval Date" (link name approval_date); required
- Multi-line field "Remarks" (link name remarks)

## Prompt 9

Create form "QC Parameter Library" (link name qc_parameter_library). Purpose: Maintain QC parameter definitions for lab testing and templates.
Category: QC master.
Fields:
- Single-line field "Parameter Code" (link name parameter_code); required
- Single-line field "Parameter Name" (link name parameter_name); required
- Single-line field "Unit" (link name unit)
- Lookup (Template Library) field "Applicable Template" (link name applicable_template)
- Lookup (Product) field "Applicable Product" (link name applicable_product)
- Decimal field "Acceptable Min" (link name acceptable_min)
- Decimal field "Acceptable Max" (link name acceptable_max)
- Checkbox field "Critical Flag" (link name critical_flag)
- Multi-line field "Notes" (link name notes)

## Prompt 10

Create form "Product Master" (link name product_master). Purpose: Catalogue all goods used in stock, production, purchasing, and sales.
Category: Product master.
Fields:
- Single-line (Unique) field "SKU Code" (link name sku_code); required; Cross-module identifier
- Single-line field "Product Name" (link name product_name); required
- Dropdown field "Product Type" (link name product_type); required; Goods / Services
- Dropdown field "Goods Sub-Type" (link name goods_sub_type); conditionally required; RAW_MATERIAL / PACKING_MATERIAL / FINISHED_GOOD / SEMI_FINISHED / TRADED_PRODUCTS / CAPITAL_GOOD / MACHINE_SPARES / CONSUMABLES
- Dropdown field "Service Sub-Type" (link name service_sub_type); conditionally required; Warehouse Expense / Wages / Freight / Miscellaneous / Staff Welfare / Vehicle / Custom
- Lookup (Service Catalogue) field "Custom Service Category" (link name custom_service_category); conditionally required; For IT-admin defined services
- Multi-line field "Description" (link name description)
- Checkbox field "Batch Tracking Required" (link name batch_tracking_required); conditionally required; Required for goods
- Number field "Shelf Life (Days)" (link name shelf_life_days); For expiry
- Dropdown field "QC Responsibility" (link name qc_responsibility); Warehouse Coordinator / QC Coordinator / QC Manager
- Lookup (Template Library) field "QC Template" (link name qc_template); Default QC parameters
- Dropdown field "UOM" (link name uom); required; Base unit
- Subform field "Secondary UOMs" (link name secondary_uoms); For conversions
- Decimal field "Specific Gravity" (link name specific_gravity); Used for kg ↔ litre
- Multi-line field "Conversion Notes" (link name conversion_notes)
- Lookup (Product) field "Packing Material Default" (link name packing_material_default); Default packaging
- Checkbox field "Yield Tracking Required" (link name yield_tracking_required)
- Multi-select field "Yield Parameters" (link name yield_parameters); Physical Qty / Purity % / AI Content
- Dropdown field "Wage Method" (link name wage_method); Template Rate / Headcount / None
- Dropdown field "Freight Class" (link name freight_class); Logistics reference
- Checkbox field "Active Flag" (link name active_flag); required
- Lookup (Stakeholder User) field "Created By" (link name created_by); required
- Date-time field "Created Date" (link name created_date); required
- Lookup (Stakeholder User) field "Last Modified By" (link name last_modified_by)
- Date-time field "Last Modified Date" (link name last_modified_date)

Subform "Secondary UOMs (subform)" fields:
- Dropdown field "To UOM" (link name to_uom); required
- Decimal field "Conversion Factor" (link name conversion_factor); required; Base to secondary
- Decimal field "Specific Gravity Override" (link name specific_gravity_override); Optional
- Date field "Valid From" (link name valid_from)
- Date field "Valid To" (link name valid_to)

## Prompt 11

Create form "Transporter Master" (link name transporter_master). Purpose: Register freight partners and payment preferences.
Category: Logistics master.
Fields:
- Single-line field "Transporter Code" (link name transporter_code); required
- Single-line field "Name" (link name name); required
- Single-line field "GSTIN" (link name gstin)
- Single-line field "Contact Person" (link name contact_person)
- Email field "Contact Email" (link name contact_email)
- Phone field "Contact Phone" (link name contact_phone)
- Multi-select Dropdown field "Freight Modes" (link name freight_modes); required; Local Drayage / Linehaul
- Multi-line field "Coverage Routes" (link name coverage_routes)
- Decimal field "TDS Rate %" (link name tds_rate)
- Dropdown field "Payment Terms" (link name payment_terms)
- Number (1-5) field "Rating" (link name rating)
- File Upload field "Documents" (link name documents); Insurance
- Checkbox field "Active Flag" (link name active_flag); required

## Prompt 12

Create form "Vendor Master" (link name vendor_master). Purpose: Capture vendor identities, compliance, payment, and logistics preferences.
Category: Partner master.
Fields:
- Single-line field "Vendor Code" (link name vendor_code); required
- Single-line field "Vendor Name" (link name vendor_name); required
- Multi-select Dropdown field "Vendor Type" (link name vendor_type); required; Material / Service / Freight / Wages / Job Work / Contractor
- Lookup (Company) field "Company" (link name company); required
- Single-line field "GSTIN" (link name gstin); conditionally required; Mandatory if taxable
- Single-line field "PAN" (link name pan); required
- Address field "Address" (link name address); required
- Single-line field "City" (link name city); required
- Dropdown field "State" (link name state); required
- Dropdown field "Country" (link name country); required
- Single-line field "Pincode" (link name pincode); required
- Single-line field "Contact Person" (link name contact_person)
- Email field "Contact Email" (link name contact_email)
- Phone field "Contact Phone" (link name contact_phone)
- Dropdown field "Payment Terms" (link name payment_terms); required; Net 15 / Net 30 / Custom
- Number field "Custom Payment Days" (link name custom_payment_days); conditionally required; Mandatory when Payment Terms = Custom
- Dropdown field "Freight Terms" (link name freight_terms); required; Paid / To_Pay / Mixed
- Multi-line field "Freight Split Notes" (link name freight_split_notes)
- Currency field "Credit Limit" (link name credit_limit)
- Number field "Credit Days" (link name credit_days)
- Decimal field "TDS Rate %" (link name tds_rate)
- Decimal field "TCS Rate %" (link name tcs_rate)
- Subform field "Bank Details" (link name bank_details); Multiple accounts
- Multi-select Lookup (Transporter) field "Preferred Transporters" (link name preferred_transporters)
- Multi-select Lookup (Warehouse) field "Allowed Warehouses" (link name allowed_warehouses)
- File Upload field "Attachments" (link name attachments); Agreements
- Checkbox field "Active Flag" (link name active_flag); required
- Date-time field "Created Date" (link name created_date); required

Subform "Vendor Bank Details (subform)" fields:
- Single-line field "Account Nickname" (link name account_nickname); required
- Single-line field "Bank Name" (link name bank_name); required
- Single-line field "Branch" (link name branch)
- Single-line field "IFSC" (link name ifsc); required
- Single-line field "Account Number" (link name account_number); required
- Dropdown field "Payment Method" (link name payment_method); NEFT / RTGS / Cheque / UPI

## Prompt 13

Create form "Price List Master" (link name price_list_master). Purpose: Define product/service rate cards with validity periods.
Category: Pricing master.
Fields:
- Single-line field "Price List ID" (link name price_list_id); required
- Lookup (Company) field "Company" (link name company); required
- Lookup (Customer) field "Customer" (link name customer); Optional if customer-specific
- Dropdown field "Delivery Region" (link name delivery_region); For auto-selection
- Dropdown field "Currency" (link name currency); required
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Dropdown field "Default Freight Terms" (link name default_freight_terms); Overrides customer
- Dropdown field "Status" (link name status); required; Draft / Active / Archived
- Subform field "Price Lines" (link name price_lines); required; Product level rates
- Multi-line field "Notes" (link name notes)

Subform "Price Lines (subform)" fields:
- Lookup (Product) field "Product" (link name product); required
- Dropdown field "UOM" (link name uom); required
- Currency field "Rate" (link name rate); required
- Decimal field "Discount %" (link name discount)
- Decimal field "GST %" (link name gst); required
- Currency field "Freight Component" (link name freight_component); Optional
- Date field "Valid From" (link name valid_from)
- Date field "Valid To" (link name valid_to)

Note: If the Customer lookup cannot be added immediately, return after creating Customer Master (Prompt 14).

## Prompt 14

Create form "Customer Master" (link name customer_master). Purpose: Maintain customer billing, shipping, credit, and price list data.
Category: Partner master.
Fields:
- Single-line field "Customer Code" (link name customer_code); required
- Single-line field "Customer Name" (link name customer_name); required
- Lookup (Company) field "Company" (link name company); required
- Single-line field "GSTIN" (link name gstin); conditionally required; Mandatory if taxable
- Single-line field "PAN" (link name pan)
- Address field "Billing Address" (link name billing_address); required
- Subform field "Shipping Addresses" (link name shipping_addresses); required; Supports multiple
- Dropdown field "Credit Terms" (link name credit_terms); required; Net 15 / Net 30 / Net 45 / Custom
- Number field "Custom Credit Days" (link name custom_credit_days); conditionally required; Mandatory when Credit Terms = Custom
- Dropdown field "Freight Terms" (link name freight_terms); required; Paid / To_Pay / Mixed
- Multi-line field "Freight Split Notes" (link name freight_split_notes)
- Multi-select Lookup (Price List) field "Allowed Price Lists" (link name allowed_price_lists); required
- Lookup (Warehouse) field "Default Warehouse" (link name default_warehouse); required
- Multi-select Lookup (Stakeholder User) field "Overdue Notification Recipients" (link name overdue_notification_recipients)
- Single-line field "Contact Person" (link name contact_person)
- Email field "Contact Email" (link name contact_email)
- Phone field "Contact Phone" (link name contact_phone)
- File Upload field "Documents" (link name documents); Contracts
- Checkbox field "Active Flag" (link name active_flag); required

Subform "Shipping Address (subform)" fields:
- Single-line field "Address Label" (link name address_label); required
- Address field "Address" (link name address); required
- Dropdown field "Delivery Region" (link name delivery_region); required; For price list mapping
- Lookup (Price List) field "Default Price List" (link name default_price_list); Auto-selection
- Single-line field "Contact Person" (link name contact_person)
- Phone field "Contact Phone" (link name contact_phone)

## Prompt 15

Create form "Tax Master" (link name tax_master). Purpose: Centralise GST, TDS, and TCS rates for financial transactions.
Category: Finance master.
Fields:
- Dropdown field "Tax Type" (link name tax_type); required; GST / TDS / TCS
- Single-line field "Section Reference" (link name section_reference)
- Decimal field "Rate %" (link name rate); required
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Multi-select Dropdown field "Applicable On" (link name applicable_on); required; Product / Service / Freight / Wage
- Currency field "Threshold Amount" (link name threshold_amount)
- Lookup (Company) field "Company Scope" (link name company_scope); required
- Multi-line field "Notes" (link name notes)

## Prompt 16

Create form "System Parameters" (link name system_parameters). Purpose: Store configurable values used across modules.
Category: Governance master.
Fields:
- Single-line field "Parameter Name" (link name parameter_name); required
- Single-line field "Parameter Value" (link name parameter_value); required
- Dropdown field "Module Scope" (link name module_scope); required; Purchase / Sales / Inventory / Finance / Attendance
- Multi-line field "Description" (link name description)
- Lookup (Stakeholder User) field "Last Updated By" (link name last_updated_by); required
- Date field "Effective Date" (link name effective_date); required

## Prompt 17

Create form "Decision Log" (link name decision_log). Purpose: Record key configuration decisions and stakeholders.
Category: Governance master.
Fields:
- Auto Number field "Decision ID" (link name decision_id); required
- Single-line field "Topic" (link name topic); required
- Multi-select Lookup (Stakeholder User) field "Stakeholders" (link name stakeholders); required
- Multi-line field "Decision Details" (link name decision_details); required
- Date field "Decision Date" (link name decision_date); required
- Multi-line field "Follow-up Actions" (link name follow_up_actions)

## Prompt 18

Create form "Audit Trail" (link name audit_trail). Purpose: Capture master data changes for compliance.
Category: Governance master.
Fields:
- Auto Number field "Audit ID" (link name audit_id); required
- Dropdown field "Module" (link name module); required
- Single-line field "Record ID" (link name record_id); required
- Dropdown field "Action" (link name action); required; Create / Update / Delete / Approve
- Lookup (Stakeholder User) field "User" (link name user); required
- Date-time field "Timestamp" (link name timestamp); required
- File Upload field "Before Snapshot" (link name before_snapshot); JSON export
- File Upload field "After Snapshot" (link name after_snapshot); JSON export
- Multi-line field "Remarks" (link name remarks)
