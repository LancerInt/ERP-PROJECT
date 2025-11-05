import re
import shutil
from pathlib import Path
from collections import defaultdict
import copy

DATA_MODEL_PATH = Path('docs/data-models/zoho_creator_data_models.md')
OUTPUT_ROOT = Path('forms/ds')
APP_SLUG = 'erp_creator_suite'
APP_DISPLAY_NAME = 'ERP Creator Suite'
UNMAPPED_LOOKUPS = defaultdict(list)

LOOKUP_ALIAS_MAP = {
    'approval workflow': ['approval_workflow'],
    'bank details': ['vendor_bank_details'],
    'customer shipping address': ['shipping_address'],
    'shipping addresses': ['shipping_address'],
    'invoice': ['sales_invoice_check'],
    'ledger': ['vendor_ledger', 'customer_ledger', 'freight_ledger', 'wage_ledger'],
    'lines': ['so_lines'],
    'machine': ['machinery'],
    'payment advice': ['vendor_payment_advice'],
    'payment schedule': ['freight_payment_schedule'],
    'po': ['purchase_order'],
    'po line': ['po_lines'],
    'pr line': ['pr_lines'],
    'product': ['product_master'],
    'product or machine': ['product_master', 'machinery'],
    'quote line': ['quote_lines'],
    'receipts': ['receipts'],
    'reminder sent flags': ['reminder_sent_flags'],
    'so line': ['so_lines'],
    'staff': ['staff_master'],
    'varies': ['purchase_order', 'receipt_advice', 'freight_advice', 'wage_voucher', 'credit_debit_note'],
    'work order': ['work_order_production_batch'],
}

EXTRA_FORMS = [
    {
        'module': 'Generated Utility Subforms',
        'name': 'Approval Workflow (subform)',
        'display_name': 'Approval Workflow (subform)',
        'slug': 'approval_workflow',
        'is_subform': True,
        'fields': [
            {'field_name': 'Stage', 'link_name': 'stage', 'type': 'Dropdown', 'required': 'Y', 'notes': 'Draft Review / Finance Manager Review / Office Manager Authorization'},
            {'field_name': 'Approver', 'link_name': 'approver', 'type': 'Lookup (Stakeholder User)', 'required': 'Y', 'notes': 'Approving stakeholder'},
            {'field_name': 'Decision', 'link_name': 'decision', 'type': 'Dropdown', 'required': 'Y', 'notes': 'Pending / Approved / Rejected'},
            {'field_name': 'Decision Date', 'link_name': 'decision_date', 'type': 'Date-Time', 'required': 'C', 'notes': 'Required when decision is approved/rejected'},
            {'field_name': 'Remarks', 'link_name': 'remarks', 'type': 'Multi-line', 'required': '', 'notes': 'Approval comments'},
        ],
    },
    {
        'module': 'Generated Utility Subforms',
        'name': 'Reminder Sent Flags (subform)',
        'display_name': 'Reminder Sent Flags (subform)',
        'slug': 'reminder_sent_flags',
        'is_subform': True,
        'fields': [
            {'field_name': 'Reminder Date', 'link_name': 'reminder_date', 'type': 'Date', 'required': 'Y', 'notes': ''},
            {'field_name': 'Reminder Method', 'link_name': 'reminder_method', 'type': 'Dropdown', 'required': '', 'notes': 'Email / Call / SMS'},
            {'field_name': 'Reminder Sent By', 'link_name': 'reminder_sent_by', 'type': 'Lookup (Stakeholder User)', 'required': '', 'notes': ''},
            {'field_name': 'Notes', 'link_name': 'notes', 'type': 'Multi-line', 'required': '', 'notes': ''},
        ],
    },
    {
        'module': 'Generated Utility Forms',
        'name': 'Receipts',
        'display_name': 'Receipts',
        'slug': 'receipts',
        'is_subform': False,
        'fields': [
            {'field_name': 'Receipt No.', 'link_name': 'receipt_no', 'type': 'Auto Number', 'required': 'Y', 'notes': ''},
            {'field_name': 'Customer', 'link_name': 'customer', 'type': 'Lookup (Customer)', 'required': 'Y', 'notes': ''},
            {'field_name': 'Receipt Date', 'link_name': 'receipt_date', 'type': 'Date', 'required': 'Y', 'notes': ''},
            {'field_name': 'Amount', 'link_name': 'amount', 'type': 'Currency', 'required': 'Y', 'notes': ''},
            {'field_name': 'Payment Method', 'link_name': 'payment_method', 'type': 'Dropdown', 'required': 'Y', 'notes': 'Bank Transfer / Cash / Cheque / UPI'},
            {'field_name': 'Reference Document', 'link_name': 'reference_document', 'type': 'Lookup (Sales Invoice Check)', 'required': '', 'notes': 'Original invoice reference'},
            {'field_name': 'Notes', 'link_name': 'notes', 'type': 'Multi-line', 'required': '', 'notes': ''},
        ],
    },
]


def slugify(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"[^0-9A-Za-z]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip('_').lower()


def module_slug(module: str) -> str:
    if not module:
        return 'general'
    module = re.sub(r"^[0-9.]+\s*", "", module)
    return slugify(module) or 'general'


def normalize_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\([^)]*\)", "", name)
    name = re.sub(r"[^0-9A-Za-z]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip().lower()


def parse_forms():
    text = DATA_MODEL_PATH.read_text()
    forms = []
    current_module = None
    current_form = None
    collecting = False
    rows = []

    def flush_rows():
        nonlocal rows, current_form
        if rows and current_form is not None:
            current_form['fields'].extend(rows)
            rows = []

    def flush_form():
        nonlocal current_form
        if current_form is not None:
            forms.append(current_form)
            current_form = None

    for line in text.splitlines():
        if line.startswith('## '):
            flush_rows()
            flush_form()
            current_module = line[3:].strip()
        elif line.startswith('### '):
            flush_rows()
            flush_form()
            name = line[4:].strip()
            current_form = {
                'module': current_module,
                'name': name,
                'display_name': name,
                'slug': slugify(name),
                'is_subform': False,
                'fields': []
            }
        elif line.startswith('#### '):
            flush_rows()
            flush_form()
            name = line[5:].strip()
            current_form = {
                'module': current_module,
                'name': name,
                'display_name': name,
                'slug': slugify(name),
                'is_subform': 'subform' in name.lower(),
                'fields': []
            }
        elif line.startswith('| Field Name |') or line.startswith('| Field |'):
            collecting = True
            rows = []
        elif collecting and line.startswith('| ---'):
            continue
        elif collecting and line.startswith('|'):
            cols = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cols) >= 5 and cols[0]:
                rows.append({
                    'field_name': cols[0],
                    'link_name': cols[1],
                    'type': cols[2],
                    'required': cols[3],
                    'notes': cols[4]
                })
        else:
            if collecting:
                flush_rows()
                collecting = False

    if collecting:
        flush_rows()
    flush_form()

    for extra in EXTRA_FORMS:
        forms.append(copy.deepcopy(extra))

    return forms


def ensure_unique_slugs(forms):
    seen = {}
    for form in forms:
        base = form['slug'] or slugify(form['name']) or 'form'
        slug_candidate = base
        index = 2
        while slug_candidate in seen:
            slug_candidate = f"{base}_{index}"
            index += 1
        form['slug'] = slug_candidate
        seen[slug_candidate] = form


def build_name_maps(forms):
    name_to_slug = defaultdict(list)
    for form in forms:
        norm = normalize_name(form['name'])
        name_to_slug[norm].append(form['slug'])
    return name_to_slug


def parse_lookup_targets(raw: str) -> list[str]:
    match = re.search(r'\((.*?)\)', raw)
    cleaned = match.group(1) if match else raw
    tokens = re.split(r"\s*/\s*|\s+or\s+|,", cleaned)
    return [t.strip() for t in tokens if t.strip()]


def map_lookup_target(target: str, name_map: dict, form=None, field=None):
    norm = normalize_name(target)
    if norm in LOOKUP_ALIAS_MAP:
        alias = LOOKUP_ALIAS_MAP[norm]
        if alias is None:
            return None
        if isinstance(alias, list):
            return alias
        return alias
    matches = name_map.get(norm)
    if not matches:
        UNMAPPED_LOOKUPS[norm].append(target)
        return None
    if isinstance(matches, list):
        if len(matches) == 1:
            return matches[0]
        if norm == 'freight advice' and form is not None:
            module_name = (form.get('module') or '').lower()
            field_notes = (field.get('notes') if field else '') or ''
            field_notes = field_notes.lower()
            form_name = form.get('name', '').lower()
            if 'finance' in module_name:
                return matches
            prefer_outbound = any(keyword in module_name for keyword in ('sales', 'inventory', 'logistics', 'return')) or 'outbound' in field_notes or 'dispatch' in form_name
            if prefer_outbound:
                for slug in matches:
                    if slug != matches[0]:
                        return slug
            return matches[0]
        return matches[0]
    return matches


def map_field_type(field, form, name_map):
    text = field['type'].strip()
    props: dict[str, object] = {}
    notes_lower = field['notes'].lower()
    if text.startswith('Single Line'):
        data_type = 'SingleLine'
        if 'unique' in text.lower():
            props['IsUnique'] = True
    elif text == 'Multi-line' or text == 'Multi-line JSON':
        data_type = 'MultiLine'
    elif text == 'Email':
        data_type = 'Email'
    elif text == 'Phone':
        data_type = 'Phone'
    elif text == 'Dropdown':
        data_type = 'Dropdown'
    elif text == 'Multi-select':
        data_type = 'MultiSelect'
    elif text == 'Multi-select Dropdown':
        data_type = 'MultiSelectDropdown'
    elif text == 'Checkbox':
        data_type = 'Checkbox'
    elif text == 'Date':
        data_type = 'Date'
    elif text == 'Date-Time':
        data_type = 'DateTime'
    elif text == 'Date Range':
        data_type = 'DateRange'
    elif text == 'Time':
        data_type = 'Time'
    elif text == 'Currency':
        data_type = 'Currency'
    elif text.startswith('Decimal'):
        data_type = 'Decimal'
        if 'formula' in text.lower():
            props['IsFormula'] = True
    elif text.startswith('Number'):
        data_type = 'Number'
    elif text == 'Address':
        data_type = 'Address'
    elif text == 'URL':
        data_type = 'URL'
    elif text == 'Image Upload':
        data_type = 'Image'
    elif text == 'File Upload':
        data_type = 'FileUpload'
    elif text == 'Auto Number':
        data_type = 'AutoNumber'
    elif text.startswith('Lookup'):
        data_type = 'Lookup'
        targets = parse_lookup_targets(field['type'])
        mapped = []
        for target in targets:
            mapped_slug = map_lookup_target(target, name_map, form, field)
            if isinstance(mapped_slug, list):
                mapped.extend(mapped_slug)
            elif mapped_slug:
                mapped.append(mapped_slug)
        if mapped:
            if 'multi-select' in text.lower():
                props['AllowMultiple'] = True
            deduped = []
            seen = set()
            for item in mapped:
                if item not in seen:
                    seen.add(item)
                    deduped.append(item)
            if len(deduped) == 1:
                props['RelatedFormLinkName'] = deduped[0]
            else:
                props['RelatedFormLinkNames'] = deduped
        else:
            if 'multi-select' in text.lower():
                props['AllowMultiple'] = True
            props['RelatedFormLinkName'] = None
    elif text == 'Subform':
        data_type = 'SubForm'
        subform_slug = map_lookup_target(field['field_name'], name_map, form, field)
        if isinstance(subform_slug, list):
            if subform_slug:
                props['SubFormLinkName'] = subform_slug[0]
        elif subform_slug:
            props['SubFormLinkName'] = subform_slug
    else:
        data_type = 'SingleLine'
    if 'multi-select lookup' in text.lower():
        props['AllowMultiple'] = True
    if data_type == 'Lookup' and 'AllowMultiple' not in props and 'Multi-select Lookup' in text:
        props['AllowMultiple'] = True
    return data_type, props


def format_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return '[' + ', '.join(f'"{v}"' for v in value) + ']'
    value = str(value).replace('"', '\\"')
    return f'"{value}"'


def render_form_lines(form, name_map):
    lines = []
    display_name = form['display_name']
    clean_display = re.sub(r"\s*\(subform\)", "", display_name, flags=re.IGNORECASE)
    lines.append(f"        // Module: {form['module'] or 'General'}")
    lines.append(f"        // Form: {clean_display}")
    lines.append(f"        form {form['slug']}")
    lines.append("        {")
    lines.append(f"            DisplayName = {format_value(clean_display)};")
    lines.append(f"            LinkName = {format_value(form['slug'])};")
    lines.append(f"            Module = {format_value(form['module'] or 'General')};")
    lines.append(f"            IsSubForm = {format_value(form['is_subform'])};")
    lines.append("")
    lines.append("            Sections")
    lines.append("            {")
    lines.append("                Section main")
    lines.append("                {")
    lines.append("                    DisplayName = \"Main\";")
    lines.append("                    Fields")
    lines.append("                    {")
    for field in form['fields']:
        field_name = field['link_name'] or slugify(field['field_name'])
        lines.append(f"                        Field {field_name}")
        lines.append("                        {")
        lines.append(f"                            DisplayName = {format_value(field['field_name'])};")
        lines.append(f"                            LinkName = {format_value(field_name)};")
        data_type, props = map_field_type(field, form, name_map)
        lines.append(f"                            DataType = {format_value(data_type)};")
        req = field['required'].strip().upper()
        if req == 'Y':
            lines.append("                            IsMandatory = true;")
        elif req == 'C':
            lines.append("                            ConditionalMandatory = true;")
        for key, value in props.items():
            lines.append(f"                            {key} = {format_value(value)};")
        if field['notes']:
            lines.append(f"                            HelpText = {format_value(field['notes'])};")
        lines.append("                        }")
    lines.append("                    }")
    lines.append("                }")
    lines.append("            }")
    lines.append("        }")
    lines.append("")
    return lines


def render_application(forms, name_map):
    lines = []
    lines.append(f"application {APP_SLUG}")
    lines.append("{")
    lines.append(f"    DisplayName = {format_value(APP_DISPLAY_NAME)};")
    lines.append("    Forms")
    lines.append("    {")
    for form in forms:
        form_lines = render_form_lines(form, name_map)
        lines.extend(form_lines)
    if lines[-1] != "":
        lines.append("")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main():
    forms = parse_forms()
    ensure_unique_slugs(forms)
    name_map = build_name_maps(forms)
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    app_content = render_application(forms, name_map)
    target_path = OUTPUT_ROOT / f"{APP_SLUG}.ds"
    target_path.write_text(app_content)
    print(f"Generated application script with {len(forms)} forms at {target_path}")
    if UNMAPPED_LOOKUPS:
        print("Unmapped lookup targets detected:")
        for key in sorted(UNMAPPED_LOOKUPS):
            unique = sorted(set(UNMAPPED_LOOKUPS[key]))
            print(f"  - {key}: {', '.join(unique)}")


if __name__ == '__main__':
    main()
