# Security Model Build Playbook

This playbook details the sequential activities required to implement the Zoho Creator ERP security model, covering access segmentation, role provisioning, record-sharing automation, and ongoing governance.

## Step 1: Confirm Security Scope & Stakeholders
1. IT Admin schedules a workshop with Office Manager, Warehouse Coordinator at Office, Finance Manager, HR Coordinator at Office, and Process Owners to reconfirm security objectives (least privilege, warehouse scoping, audit traceability).
2. Catalogue all stakeholder personas from the ERP Structure document, including composite roles (e.g., Purchase Manager + Warehouse Coordinator).
3. Validate regulatory requirements (GST, wage data privacy, attendance biometrics) and document any segregation-of-duty constraints.
4. Produce a responsibility matrix showing which module/forms each persona must access and whether they require create/read/update/delete rights.

## Step 2: Define Role Hierarchy & Permission Bundles
1. Map Creator "Profiles" to top-level personas (Head Office roles vs warehouse roles) and "Roles" to reporting hierarchy for record sharing.
2. Break down each module into functional bundles (e.g., Purchase Request Intake, RFQ Processing, Freight Advice Approval) and align them to one or more roles.
3. Document field-level visibility needs (e.g., financial terms visible only to Finance roles, QC results restricted to QC hierarchy) and mark sensitive fields for masking or read-only.
4. Validate cross-role combinations to ensure composite users inherit additive permissions without conflicts.

## Step 3: Model Data Access Rules
1. Identify forms that require row-level security (Warehouse-scoped data, Company-specific ledgers) and define filter logic (e.g., `Warehouse = CurrentUser.WarehouseScope`).
2. For shared masters (Products, Services, Transporters), determine if global read access suffices or if edit rights must be constrained to IT Admin.
3. Design Creator sharing rules for transactional records triggered by workflows (e.g., auto-share Purchase Requests with approvers, auto-share DC with assigned warehouse team).
4. Define exception handling for cross-warehouse visibility (e.g., Head Office QA reviewing multiple warehouses) via explicit record sharing policies.

## Step 4: Configure Creator Roles & Permissions
1. Create Creator custom roles following the approved naming convention (`HO_Purchase_Manager`, `WH_Manager_<WarehouseCode>`).
2. Assign module/page/form access according to the permission bundles, enabling only necessary actions per role.
3. Configure profile-based restrictions for file downloads, export capabilities, and API access for sensitive modules.
4. Establish delegation rules (temporary access) for leaves or escalations using Creator's role assignment scheduling.

## Step 5: Implement Record Sharing Automations
1. Update workflow scripts in each module to auto-share newly created records with required approvers based on lookup fields (e.g., Warehouse Manager on Purchase Request).
2. Configure conditional sharing for multi-step approvals (e.g., once Purchase Manager approves RFQ, share PO with Finance Manager for payment readiness).
3. Implement revocation routines that remove access after approval completion or rejection to maintain least privilege.
4. Document all automation scripts, including trigger points and access scopes, in the security runbook for audit.

## Step 6: Provision Users & Assign Roles
1. Sync Zoho Portal Users with Creator, ensuring email verification and mapping to employee master records.
2. Assign primary roles per stakeholder; for composite responsibilities, add secondary roles explicitly and document approvals.
3. Configure default warehouse/company scope for each warehouse-facing user via role parameters or user preference forms.
4. Test login for a sample user in each persona to confirm access boundaries and module visibility.

## Step 7: Validate & Harden Security Controls
1. Execute role-based test scripts covering create/read/update/delete scenarios per module to confirm expected access and restrictions.
2. Conduct negative testing (attempting cross-warehouse data access, editing locked fields) and log outcomes.
3. Enable Creator audit trails and schedule weekly reviews of critical modules (Finance, Payroll, QC) for anomalous access.
4. Finalise security documentation: access matrix, workflow sharing diagram, user provisioning SOP, and approval logs.

## Step 8: Operationalise Ongoing Governance
1. Establish monthly access review cadence with HR Coordinator at Office and Process Owners to reconcile role changes with staffing updates.
2. Define onboarding/offboarding checklist to ensure timely role assignment and revocation.
3. Set up automated notifications to IT Admin when new warehouses/companies are created so related warehouse roles can be cloned.
4. Integrate security change requests into the Change Enablement process with documented approvals and rollback plans.
