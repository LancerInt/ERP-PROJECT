# Zoho Zia Master Form Prompts

Run each prompt separately inside Zoho Zia in the listed order so lookup dependencies resolve correctly.

## Prompt 1

Create form "Company Master" (link name company_master). Purpose: Stores legal entities that participate in purchase, sales, finance and compliance.
Category: Core master.
Fields:
- Auto-number field "Company ID" (link name company_id) with prefix "COMP", 5-digit padding; required; unique
- Single-line text field "Company Name" (link name company_name); required; unique
- Single-line text field "Legal Name" (link name legal_name); required
- Single-line text field "CIN" (link name cin)
- Single-line text field "GSTIN" (link name gstin); required
- Single-line text field "PAN" (link name pan)
- Single-line text field "TAN" (link name tan)
- Single-line text field "Billing Address Line 1" (link name billing_address_line1); required
- Single-line text field "Billing Address Line 2" (link name billing_address_line2)
- Single-line text field "City" (link name billing_city); required
- Dropdown field "State" (link name billing_state); Choices: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry
- Single-line text field "Postal Code" (link name billing_postal_code); required
- Single-line text field "Country" (link name billing_country); default 'India'
- Single-line text field "Finance Contact Name" (link name finance_contact_name)
- Email field "Finance Contact Email" (link name finance_contact_email)
- Phone field "Finance Contact Phone" (link name finance_contact_phone)
- Dropdown field "Default Currency" (link name default_currency); default 'INR'; Choices: INR, USD
- Dropdown field "Accounting System" (link name books_system); default 'Tally'; Choices: Zoho Books, Tally, Other
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive
- Multi-line text field "Notes" (link name notes)


Create form "Role Master" (link name role_master). Purpose: Defines system roles and governance metadata for access control.
Category: Security master.
Fields:
- Auto-number field "Role ID" (link name role_id) with prefix "ROLE", 4-digit padding; required; unique
- Single-line text field "Role Name" (link name role_name); required; unique
- Dropdown field "Scope" (link name scope); Choices: Head Office, Warehouse, All
- Multi-line text field "Description" (link name description)
- Single-line text field "Default Page" (link name default_page)
- Checkbox field "Active" (link name is_active); default True

## Prompt 2

Create form "Tax Master" (link name tax_master). Purpose: Captures GST, TDS and TCS rates with validity periods.
Category: Finance master.
Fields:
- Auto-number field "Tax ID" (link name tax_id) with prefix "TAX", 4-digit padding; required; unique
- Single-line text field "Tax Name" (link name tax_name); required
- Dropdown field "Tax Type" (link name tax_type); required; Choices: GST, TDS, TCS
- Single-line text field "Section/Rule" (link name section)
- Decimal field "Rate (%)" (link name rate_percent) with precision 5, scale 2; required
- Currency field "Threshold Amount" (link name threshold_amount) with precision 12, scale 2
- Dropdown field "Applicable On" (link name applicable_on); Choices: Product, Freight, Wages, Service, All
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive


Create form "Payment Terms Master" (link name payment_terms_master). Purpose: Standard payment term definitions for vendors, customers and contractors.
Category: Finance master.
Fields:
- Auto-number field "Payment Term ID" (link name payment_terms_id) with prefix "PT", 4-digit padding; required; unique
- Single-line text field "Name" (link name name); required; unique
- Multi-line text field "Description" (link name description)
- Number field "Due in Days" (link name due_in_days); required
- Decimal field "Early Payment Discount (%)" (link name early_payment_discount_percent) with precision 5, scale 2
- Number field "Discount Window (Days)" (link name early_payment_window_days)
- Checkbox field "Apply TCS" (link name apply_tcs); default False
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive


Create form "Freight Terms Master" (link name freight_terms_master). Purpose: Defines inbound and outbound freight responsibilities and approvals.
Category: Logistics master.
Fields:
- Auto-number field "Freight Term ID" (link name freight_term_id) with prefix "FT", 4-digit padding; required; unique
- Single-line text field "Name" (link name name); required; unique
- Dropdown field "Direction" (link name direction); required; Choices: Inbound, Outbound, Both
- Dropdown field "Default Payer" (link name payer); required; Choices: Company, Vendor/Customer, Split
- Checkbox field "Includes Loading" (link name includes_loading); default False
- Checkbox field "Includes Unloading" (link name includes_unloading); default False
- Checkbox field "Requires Approval" (link name requires_freight_approval); default True
- Multi-line text field "Notes" (link name notes)

## Prompt 3

Create form "Transporter Master" (link name transporter_master). Purpose: Transport partners for inbound, outbound, stock transfer and job work movements.
Category: Logistics master.
Fields:
- Auto-number field "Transporter ID" (link name transporter_id) with prefix "TRN", 5-digit padding; required; unique
- Single-line text field "Transporter Name" (link name transporter_name); required
- Single-line text field "Code" (link name transporter_code); unique
- Single-line text field "GSTIN" (link name gstin)
- Single-line text field "PAN" (link name pan)
- Single-line text field "Contact Name" (link name contact_name)
- Phone field "Contact Phone" (link name contact_phone)
- Email field "Contact Email" (link name contact_email)
- Multi-select dropdown "Freight Directions" (link name freight_directions); Choices: Inbound, Outbound, Stock Transfer, Job Work
- Multi-select dropdown "States Served" (link name states_served); Choices: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry
- Checkbox field "Preferred" (link name preferred); default False
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive
- Multi-line text field "Remarks" (link name remarks)


Create form "UOM Master" (link name uom_master). Purpose: Standard unit of measure definitions including base conversions.
Category: Inventory master.
Fields:
- Auto-number field "UOM ID" (link name uom_id) with prefix "UOM", 4-digit padding; required; unique
- Single-line text field "Unit Name" (link name uom_name); required
- Single-line text field "Symbol" (link name symbol)
- Dropdown field "Category" (link name category); Choices: Weight, Volume, Count, Length, Area, Time
- Checkbox field "Base Unit" (link name base_unit); default False
- Lookup field "Base Reference" (link name base_reference) pointing to uom_master
- Decimal field "Conversion Factor" (link name conversion_factor) with precision 12, scale 6
- Checkbox field "Specific Gravity Applicable" (link name specific_gravity_applicable); default False
- Multi-line text field "Notes" (link name notes)


Create form "Integration Config" (link name integration_config). Purpose: Stores configuration values for AI parsers, attendance recognition and accounting connectors.
Category: IT Governance master.
Fields:
- Auto-number field "Config ID" (link name config_id) with prefix "CFG", 4-digit padding; required; unique
- Dropdown field "Category" (link name config_category); required; Choices: AI_PO_PARSER, FACE_RECOGNITION, BANK_RECON, ACCOUNTING, OTHERS
- Single-line text field "Key" (link name key); required
- Single-line text field "Value" (link name value); required
- Multi-line text field "Description" (link name description)
- Checkbox field "Active" (link name active); default True

## Prompt 4

Create form "Stock Adjustment Reasons" (link name stock_adjustment_reasons). Purpose: Controlled vocabulary for stock adjustment justifications.
Category: Inventory master.
Fields:
- Auto-number field "Reason ID" (link name reason_id) with prefix "SAR", 4-digit padding; required; unique
- Single-line text field "Reason Code" (link name reason_code); required; unique
- Single-line text field "Reason Label" (link name reason_label); required
- Dropdown field "Category" (link name reason_category); Choices: Damage, Expiry, Shortage, Surplus, Audit Correction, Other
- Checkbox field "Needs Secondary Approval" (link name requires_secondary_approval); default False
- Checkbox field "Active" (link name active); default True


Create form "Inter-Warehouse Shift Reasons" (link name inter_warehouse_shift_reasons). Purpose: Reason codes for intra-warehouse shifting operations.
Category: Inventory master.
Fields:
- Auto-number field "Reason ID" (link name reason_id) with prefix "IWSR", 4-digit padding; required; unique
- Single-line text field "Reason Name" (link name reason_name); required
- Checkbox field "Requires Comment" (link name requires_comment); default False
- Checkbox field "Active" (link name active); default True


Create form "ERP User Master" (link name user_master). Purpose: Stores stakeholders who access the ERP with role assignments.
Category: Security master.
Fields:
- Auto-number field "User ID" (link name user_id) with prefix "USR", 5-digit padding; required; unique
- Single-line text field "Full Name" (link name user_full_name); required
- Email field "Email" (link name email); required; unique
- Phone field "Phone" (link name phone)
- Multi-select dropdown "Stakeholder Roles" (link name stakeholder_roles); Choices: Office Manager, Purchase Manager, Purchase Coordinator, Sales Manager, Sales Coordinator, Finance Manager, Accounts Manager, Freight Coordinator, QC Manager, QC Coordinator, QC Analyst, Warehouse Coordinator (Office), HR Coordinator (Office), IT Admin, Warehouse Manager, Warehouse Coordinator, Warehouse Supervisor, Warehouse HR Coordinator, Employee
- Checkbox field "Active" (link name is_active); default True
- Multi-line text field "Remarks" (link name remarks)
Add the following lookup fields after their target form exists: Default Warehouse.

## Prompt 5

Create form "Warehouse Master" (link name warehouse_master). Purpose: Defines physical warehouses managed by the organisation.
Category: Core master.
Fields:
- Auto-number field "Warehouse ID" (link name warehouse_id) with prefix "WH", 5-digit padding; required; unique
- Single-line text field "Warehouse Name" (link name warehouse_name); required
- Single-line text field "Warehouse Code" (link name warehouse_code); required; unique
- Lookup field "Company" (link name company) pointing to company_master; required
- Single-line text field "Address Line 1" (link name address_line1); required
- Single-line text field "Address Line 2" (link name address_line2)
- Single-line text field "City" (link name city); required
- Dropdown field "State" (link name state); Choices: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry
- Single-line text field "Postal Code" (link name postal_code); required
- Single-line text field "Country" (link name country); default 'India'
- Decimal field "Latitude" (link name latitude) with precision 8, scale 6
- Decimal field "Longitude" (link name longitude) with precision 9, scale 6
- Lookup field "Warehouse Manager" (link name warehouse_manager) pointing to user_master
- Lookup field "Warehouse HR Coordinator" (link name hr_coordinator) pointing to user_master
- Multi-line text field "Capacity Notes" (link name capacity_notes)
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive


Update form "ERP User Master" (link name user_master) to add these fields now that dependencies are ready:
- Lookup field "Default Warehouse" (link name default_warehouse) pointing to warehouse_master


Create form "Godown Master" (link name godown_master). Purpose: Defines storage godowns within a warehouse and the machinery allocated to them.
Category: Core master.
Fields:
- Auto-number field "Godown ID" (link name godown_id) with prefix "GD", 5-digit padding; required; unique
- Single-line text field "Godown Name" (link name godown_name); required
- Single-line text field "Godown Code" (link name godown_code); required; unique
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master; required
- Dropdown field "Storage Type" (link name storage_type); Choices: Ambient, Cold, Hazardous, Bulk, Finished Goods
- Single-line text field "Temperature Range" (link name temperature_range)
- Checkbox field "Humidity Control" (link name humidity_control); default False
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive

## Prompt 6

Create form "Service Catalog" (link name service_master). Purpose: Extensible list of services available per warehouse or centrally.
Category: Finance master.
Fields:
- Auto-number field "Service ID" (link name service_id) with prefix "SRV", 5-digit padding; required; unique
- Single-line text field "Service Name" (link name service_name); required
- Dropdown field "Service Category" (link name service_category); required; Choices: Warehouse Expense, Wages, Freight, Miscellaneous Expense, Staff Welfare, Vehicle, Custom
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master
- Multi-line text field "Description" (link name description)
- Checkbox field "Active" (link name is_active); default True


Create form "Shift Master" (link name attendance_shift_master). Purpose: Shift definitions for attendance capture with overtime policies.
Category: HR master.
Fields:
- Auto-number field "Shift ID" (link name shift_id) with prefix "SHIFT", 4-digit padding; required; unique
- Single-line text field "Shift Name" (link name shift_name); required
- Dropdown field "Location Type" (link name location_type); Choices: Head Office, Warehouse, Lab
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master
- Time field "Start Time" (link name start_time); required
- Time field "End Time" (link name end_time); required
- Number field "Break Minutes" (link name break_minutes); default 0
- Checkbox field "Overtime Applicable" (link name overtime_applicable); default False
- Dropdown field "OT Rate Type" (link name overtime_rate_type); show when overtime_applicable; Choices: Multiplier, Fixed
- Decimal field "OT Rate Value" (link name overtime_rate_value) with precision 6, scale 2; show when overtime_applicable
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Dropdown field "Status" (link name status); default 'Active'; Choices: Draft, Active, Inactive

## Prompt 7

Create form "Product Master" (link name product_master). Purpose: Catalogue of goods and services with QC, taxation and conversion metadata.
Category: Inventory master.
Fields:
- Auto-number field "Product ID" (link name product_id) with prefix "PRD", 5-digit padding; required; unique
- Single-line text field "Product Name" (link name product_name); required
- Single-line text field "SKU Code" (link name sku_code); required; unique
- Dropdown field "Product Type" (link name product_type); required; Choices: Goods, Service
- Dropdown field "Goods Type" (link name goods_type); show when product_type == 'Goods'; Choices: RAW_MATERIAL, PACKING_MATERIAL, FINISHED_GOOD, SEMI_FINISHED, TRADED_PRODUCT, CAPITAL_GOOD, MACHINE_SPARE, CONSUMABLE
- Dropdown field "Service Type" (link name service_type); show when product_type == 'Service'; Choices: Warehouse Expense, Wages, Freight, Miscellaneous Expense, Staff Welfare, Vehicle, Custom
- Single-line text field "Custom Service Category" (link name custom_service_category); show when service_type == 'Custom'
- Lookup field "Base UOM" (link name base_uom) pointing to uom_master; required
- Decimal field "Specific Gravity" (link name specific_gravity) with precision 6, scale 3
- Checkbox field "Batch Tracking Required" (link name batch_tracking_required); default True
- Checkbox field "Expiry Tracking Required" (link name expiry_required); default False
- Dropdown field "QC Routing" (link name qc_routing); default 'Warehouse Coordinator'; Choices: Warehouse Coordinator, QC Coordinator, QC Manager
- Dropdown field "Yield Tracking Mode" (link name yield_tracking_mode); default 'None'; Choices: None, Physical Quantity, Physical + Purity, Physical + Purity + AI
- Checkbox field "Capture Received Packing" (link name packing_capture_required); default False
- Checkbox field "Allow Reformulation" (link name reformulation_allowed); default False
- Checkbox field "Active" (link name active); default True
- Multi-line text field "Remarks" (link name remarks)


Create form "Price List Master" (link name price_list_master). Purpose: Stores price policies per customer, region, and product.
Category: Sales master.
Fields:
- Auto-number field "Price List ID" (link name price_list_id) with prefix "PL", 5-digit padding; required; unique
- Single-line text field "Price List Name" (link name price_list_name); required
- Single-line text field "Code" (link name price_list_code); unique
- Lookup field "Company" (link name company) pointing to company_master
- Single-line text field "Region" (link name region)
- Dropdown field "Currency" (link name currency); default 'INR'; Choices: INR, USD
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Lookup field "Freight Term Override" (link name freight_term_override) pointing to freight_terms_master
- Dropdown field "Status" (link name status); default 'Draft'; Choices: Draft, Active, Expired

## Prompt 8

Create form "Vendor Master" (link name vendor_master). Purpose: Maintains vendor identities, compliance data and credit terms.
Category: Procurement master.
Fields:
- Auto-number field "Vendor ID" (link name vendor_id) with prefix "VND", 5-digit padding; required; unique
- Single-line text field "Vendor Name" (link name vendor_name); required
- Single-line text field "Vendor Code" (link name vendor_code); unique
- Dropdown field "Vendor Type" (link name vendor_type); Choices: Raw Material, Packing Material, Machinery, Service, Job Work, Other
- Single-line text field "GSTIN" (link name gstin)
- Single-line text field "PAN" (link name pan)
- Single-line text field "Primary Contact" (link name primary_contact_name)
- Email field "Primary Email" (link name primary_email)
- Phone field "Primary Phone" (link name primary_phone)
- Currency field "Credit Limit" (link name credit_limit) with precision 12, scale 2
- Lookup field "Payment Terms" (link name payment_terms) pointing to payment_terms_master
- Lookup field "Freight Terms" (link name freight_terms) pointing to freight_terms_master
- Lookup field "TDS Profile" (link name tds_profile) pointing to tax_master
- Checkbox field "Wage Contractor" (link name wage_vendor); default False
- Multi-line text field "Notes" (link name notes)
- Checkbox field "Active" (link name active); default True


Create form "Customer Master" (link name customer_master). Purpose: Customer registry with credit terms, freight agreements and price list mapping.
Category: Sales master.
Fields:
- Auto-number field "Customer ID" (link name customer_id) with prefix "CUS", 5-digit padding; required; unique
- Single-line text field "Customer Name" (link name customer_name); required
- Single-line text field "Customer Code" (link name customer_code); unique
- Single-line text field "GSTIN" (link name gstin)
- Single-line text field "PAN" (link name pan)
- Currency field "Credit Limit" (link name credit_limit) with precision 12, scale 2
- Lookup field "Credit Terms" (link name credit_terms) pointing to payment_terms_master
- Lookup field "Freight Terms" (link name freight_terms) pointing to freight_terms_master
- Lookup field "Default Price Policy" (link name price_policy) pointing to price_list_master
- Single-line text field "Primary Contact" (link name primary_contact_name)
- Email field "Primary Email" (link name primary_email)
- Phone field "Primary Phone" (link name primary_phone)
- Checkbox field "Notify on Overdue" (link name notify_on_overdue); default True
- Checkbox field "Active" (link name active); default True

## Prompt 9

Create form "Bank Account Master" (link name bank_account_master). Purpose: Company bank accounts used for receivables and payables processing.
Category: Finance master.
Fields:
- Auto-number field "Bank Account ID" (link name bank_account_id) with prefix "BANK", 4-digit padding; required; unique
- Lookup field "Company" (link name company) pointing to company_master; required
- Single-line text field "Bank Name" (link name bank_name); required
- Single-line text field "Branch" (link name branch)
- Single-line text field "Account Number" (link name account_number); required
- Single-line text field "IFSC" (link name ifsc); required
- Dropdown field "Account Type" (link name account_type); Choices: Current, Savings, Cash Credit, Overdraft
- Dropdown field "Currency" (link name currency); default 'INR'; Choices: INR, USD
- Multi-select dropdown "Usage" (link name usage); Choices: Payables, Receivables, Payroll, Petty Cash
- Checkbox field "Active" (link name is_active); default True


Create form "Staff Master" (link name staff_master). Purpose: Maintains staffing data for attendance, wage, and shift assignment workflows.
Category: HR master.
Fields:
- Auto-number field "Staff ID" (link name staff_id) with prefix "STF", 5-digit padding; required; unique
- Single-line text field "Staff Code" (link name staff_code); required; unique
- Single-line text field "First Name" (link name first_name); required
- Single-line text field "Last Name" (link name last_name)
- Dropdown field "Employment Location" (link name employment_location); Choices: Head Office, Warehouse, Lab, QC
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master
- Single-line text field "Department" (link name department)
- Single-line text field "Designation" (link name designation)
- Dropdown field "Employment Type" (link name employment_type); Choices: Permanent, Contract, Apprentice
- Lookup field "Contractor Vendor" (link name contractor_vendor) pointing to vendor_master
- Date field "Date of Joining" (link name date_of_joining)
- Image upload field "Photo Reference" (link name photo_reference)
- Checkbox field "Active" (link name active); default True

## Prompt 10

Create form "Freight Rate Card" (link name freight_rate_card). Purpose: Baseline freight cost references to support per-unit reporting.
Category: Logistics master.
Fields:
- Auto-number field "Rate Card ID" (link name rate_card_id) with prefix "FRC", 5-digit padding; required; unique
- Lookup field "Transporter" (link name transporter) pointing to transporter_master; required
- Dropdown field "Origin State" (link name origin); Choices: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry
- Dropdown field "Destination State" (link name destination); required; Choices: Andhra Pradesh, Arunachal Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana, Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh, Maharashtra, Manipur, Meghalaya, Mizoram, Nagaland, Odisha, Punjab, Rajasthan, Sikkim, Tamil Nadu, Telangana, Tripura, Uttar Pradesh, Uttarakhand, West Bengal, Andaman and Nicobar Islands, Chandigarh, Dadra and Nagar Haveli and Daman and Diu, Delhi, Jammu and Kashmir, Ladakh, Lakshadweep, Puducherry
- Dropdown field "Freight Direction" (link name freight_direction); required; Choices: Inbound, Outbound, Stock Transfer, Job Work
- Lookup field "Rate UOM" (link name uom) pointing to uom_master; required
- Currency field "Rate per UOM" (link name rate_per_uom) with precision 12, scale 2; required
- Decimal field "Surcharge (%)" (link name surcharge_percent) with precision 5, scale 2
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Checkbox field "Active" (link name active); default True


Create form "Wage Rate Master" (link name wage_rate_master). Purpose: Reference wage rates for production and logistics contractors.
Category: Finance master.
Fields:
- Auto-number field "Wage Rate ID" (link name wage_rate_id) with prefix "WGR", 4-digit padding; required; unique
- Dropdown field "Wage Category" (link name wage_category); required; Choices: Loading, Unloading, Production, Headcount
- Lookup field "Contractor" (link name vendor) pointing to vendor_master
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master
- Dropdown field "Rate Basis" (link name rate_basis); Choices: Per Batch, Per MT, Per Hour, Headcount
- Lookup field "UOM" (link name uom) pointing to uom_master
- Currency field "Rate" (link name rate) with precision 12, scale 2; required
- Lookup field "TDS Profile" (link name tds_profile) pointing to tax_master
- Date field "Effective From" (link name effective_from); required
- Date field "Effective To" (link name effective_to)
- Checkbox field "Active" (link name active); default True

## Prompt 11

Create form "Petty Cash Master" (link name petty_cash_master). Purpose: Tracks authorised petty cash custodians per warehouse.
Category: Finance master.
Fields:
- Auto-number field "Petty Cash ID" (link name petty_cash_id) with prefix "PET", 4-digit padding; required; unique
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master; required
- Lookup field "Custodian" (link name custodian) pointing to user_master; required
- Currency field "Float Amount" (link name float_amount) with precision 12, scale 2; required
- Currency field "Replenishment Threshold" (link name replenishment_threshold) with precision 12, scale 2
- Dropdown field "Status" (link name status); default 'Active'; Choices: Active, Inactive


Create form "QC Report Templates" (link name qc_report_templates). Purpose: Controls final QC report formats per product and revision.
Category: Quality master.
Fields:
- Auto-number field "Template ID" (link name template_id) with prefix "QCT", 4-digit padding; required; unique
- Single-line text field "Template Name" (link name template_name); required
- Lookup field "Product" (link name product) pointing to product_master
- Single-line text field "Revision" (link name revision); required
- Checkbox field "Digital Signature Required" (link name requires_digital_signature); default True
- Checkbox field "Active" (link name active); default True


Create form "Production Templates" (link name production_template_master). Purpose: Master data for production recipes with version control and yield settings.
Category: Production master.
Fields:
- Auto-number field "Template ID" (link name template_id) with prefix "BOM", 5-digit padding; required; unique
- Single-line text field "Template Name" (link name template_name); required
- Lookup field "Warehouse" (link name warehouse) pointing to warehouse_master; required
- Lookup field "Output Product" (link name output_product) pointing to product_master; required
- Single-line text field "Revision" (link name revision); required
- Decimal field "Expected Yield Loss (%)" (link name yield_loss_percent) with precision 5, scale 2
- Checkbox field "Wage Template" (link name wage_template); default False
- Checkbox field "Active" (link name active); default True
