import re
import shutil
from pathlib import Path
from collections import defaultdict
import copy

DATA_MODEL_PATH = Path('docs/data-models/zoho_creator_data_models.md')
OUTPUT_ROOT = Path('forms/ds')
FORMS_OUTPUT = OUTPUT_ROOT / 'forms'
REPORTS_OUTPUT = OUTPUT_ROOT / 'reports'
UNMAPPED_LOOKUPS = defaultdict(list)

LOOKUP_ALIAS_MAP = {
    'approval workflow': ['approval_workflow'],
    'bank details': ['vendor_bank_details'],
    'customer shipping address': ['shipping_address'],
    'shipping addresses': ['shipping_address'],
    'invoice': ['sales_invoice_check'],
    'ledger': ['vendor_ledger', 'customer_ledger', 'freight_ledger', 'wage_ledger'],
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
    'role': ['role_definition'],
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
            {
                'field_name': 'Stage',
                'link_name': 'stage',
                'type': 'Dropdown',
                'required': 'Y',
                'notes': 'Draft Review / Finance Manager Review / Office Manager Authorization',
            },
            {
                'field_name': 'Approver',
                'link_name': 'approver',
                'type': 'Lookup (Stakeholder User)',
                'required': 'Y',
                'notes': 'Approving stakeholder',
            },
            {
                'field_name': 'Decision',
                'link_name': 'decision',
                'type': 'Dropdown',
                'required': 'Y',
                'notes': 'Pending / Approved / Rejected',
            },
            {
                'field_name': 'Decision Date',
                'link_name': 'decision_date',
                'type': 'Date-Time',
                'required': 'C',
                'notes': 'Required when decision is approved/rejected',
            },
            {
                'field_name': 'Remarks',
                'link_name': 'remarks',
                'type': 'Multi-line',
                'required': '',
                'notes': 'Approval comments',
            },
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
                'fields': [],
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
                'fields': [],
            }
        elif line.startswith('| Field Name |') or line.startswith('| Field |'):
            collecting = True
            rows = []
        elif collecting and line.startswith('| ---'):
            continue
        elif collecting and line.startswith('|'):
            cols = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cols) >= 5 and cols[0]:
                rows.append(
                    {
                        'field_name': cols[0],
                        'link_name': cols[1],
                        'type': cols[2],
                        'required': cols[3],
                        'notes': cols[4],
                    }
                )
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
    if norm == 'lines' and form is not None:
        form_name = (form.get('name') or '').lower()
        if 'purchase request' in form_name:
            return 'pr_lines'
        if 'purchase order' in form_name:
            return 'po_lines'
        if 'quote' in form_name:
            return 'quote_lines'
        if 'sales order' in form_name:
            return 'so_lines'
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
        props['AllowMultiple'] = True
    elif text == 'Multi-select Dropdown':
        data_type = 'MultiSelectDropdown'
        props['AllowMultiple'] = True
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
        data_type = 'INR'
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
        data_type = 'UploadImage'
    elif text == 'File Upload':
        data_type = 'UploadFile'
    elif text == 'Auto Number':
        data_type = 'AutoNumber'
    elif text.startswith('Lookup') or text.startswith('Multi-select Lookup') or text.startswith('Multi-Select Lookup') or 'Lookup' in text:
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
        if not subform_slug:
            link_name = (field.get('link_name') or '').strip().lower()
            candidates = [link_name]
            field_slug = slugify(field['field_name'])
            if field_slug:
                candidates.append(field_slug)
            form_slug = form.get('slug') or ''
            if form_slug and link_name:
                candidates.append(f"{form_slug}_{link_name}")
            for candidate in candidates:
                if not candidate:
                    continue
                mapped = map_lookup_target(candidate, name_map, form, field)
                if mapped:
                    subform_slug = mapped if not isinstance(mapped, list) else mapped[0]
                    break
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
    if data_type == 'UploadFile':
        props.setdefault('MaxFileCount', 10)
        props.setdefault('AllowMultiple', True)
        props.setdefault('FileSource', 'LocalDrive')
    return data_type, props


def ds_type_for(meta_type: str) -> str:
    mapping = {
        'SingleLine': 'text',
        'MultiLine': 'textarea',
        'Email': 'email',
        'Phone': 'phonenumber',
        'Dropdown': 'picklist',
        'MultiSelect': 'checkboxes',
        'MultiSelectDropdown': 'list',
        'Checkbox': 'checkbox',
        'Date': 'date',
        'DateTime': 'datetime',
        'DateRange': 'daterange',
        'Time': 'time',
        'INR': 'INR',
        'Decimal': 'number',
        'Number': 'number',
        'Address': 'address',
        'URL': 'url',
        'UploadFile': 'upload file',
        'UploadImage': 'upload file',
        'AutoNumber': 'autonumber',
        'Lookup': 'lookup',
        'SubForm': 'grid',
    }
    return mapping.get(meta_type, 'text')


def normalize_choice_text(value: str) -> str:
    value = re.sub(r"\s*\([^)]*\)", "", value)
    return value.strip()


def extract_choice_values(field) -> list[str]:
    notes = field.get('notes', '') or ''
    if not notes:
        return []
    if 'http' in notes.lower():
        return []
    if 'etc' in notes.lower():
        return []
    separators = []
    if ' / ' in notes:
        separators.append(r"\s*/\s*")
    if ',' in notes:
        separators.append(r",")
    if not separators:
        return []
    tokens = [normalize_choice_text(token) for token in re.split('|'.join(separators), notes)]
    tokens = [token for token in tokens if token]
    if not tokens:
        return []
    if any(len(token.split()) > 5 for token in tokens):
        return []
    return tokens


def escape(value: str) -> str:
    return value.replace('"', '\"')


def prepare_field_meta(form, name_map):
    prepared = []
    for field in form['fields']:
        link_name = field['link_name'] or slugify(field['field_name'])
        data_type, props = map_field_type(field, form, name_map)
        prepared.append(
            {
                'field': field,
                'link_name': link_name,
                'data_type': data_type,
                'props': props,
            }
        )
    return prepared


def render_subform_fields(sub_form, name_map, subform_map, indent):
    lines = []
    sub_meta = prepare_field_meta(sub_form, name_map)
    row_index = 1
    for child in sub_meta:
        lines.extend(render_field_block(child, row_index, name_map, subform_map, indent=indent, include_position=False))
        lines.append("")
        row_index += 1
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def render_field_block(meta, row_index, name_map, subform_map, indent="    ", include_position=True):
    field = meta['field']
    ds_type = ds_type_for(meta['data_type'])
    required = (field['required'] or '').strip().upper()
    prefix = "must have " if required in {"Y", "C"} else ""
    header = f"{indent}{prefix}{meta['link_name']}"
    lines = [header, f"{indent}("]
    lines.append(f"{indent}    type = {ds_type}")
    lines.append(f"{indent}    displayname = \"{escape(field['field_name'])}\"")
    if include_position:
        lines.append(f"{indent}    row = {row_index}")
        lines.append(f"{indent}    column = 1")
    lines.append(f"{indent}    width = medium")

    if required == 'Y':
        lines.append(f"{indent}    mandatory = true")
    elif required == 'C':
        lines.append(f"{indent}    conditional mandatory = true")

    if meta['props'].get('IsUnique'):
        lines.append(f"{indent}    unique = true")

    if meta['data_type'] == 'AutoNumber':
        lines.append(f"{indent}    start index = 1")

    if meta['data_type'] == 'Time':
        lines.append(f"{indent}    timedisplayoptions = \"hh:mm:ss\"")

    if meta['data_type'] == 'INR':
        lines.append(f"{indent}    format = commadotindian")

    if meta['data_type'] == 'Address':
        lines.append(f"{indent}    capture_coordinates = true")
        lines.append(f"{indent}    adjust_using_map = false")
        address_parts = [
            ('address_line_1', 'Address Line 1', True),
            ('address_line_2', 'Address Line 2', True),
            ('district_city', 'City / District', True),
            ('state_province', 'State / Province', True),
            ('postal_code', 'Postal Code', True),
            ('country', 'Country', True),
            ('latitude', 'Latitude', False),
            ('longitude', 'Longitude', False),
        ]
        for key, label, visible in address_parts:
            lines.append(f"{indent}    {key}")
            lines.append(f"{indent}    (")
            lines.append(f"{indent}        type = {key}")
            lines.append(f"{indent}        displayname = \"{label}\"")
            if not visible:
                lines.append(f"{indent}        visibility = false")
            lines.append(f"{indent}    )")

    choices = []
    if meta['data_type'] in {'Dropdown', 'MultiSelect', 'MultiSelectDropdown', 'Checkbox'}:
        choices = extract_choice_values(field)
    if choices:
        joined = ','.join(f'"{escape(choice)}"' for choice in choices)
        lines.append(f"{indent}    values = {{{joined}}}")

    if meta['props'].get('AllowMultiple'):
        lines.append(f"{indent}    allow multiple = true")

    related = meta['props'].get('RelatedFormLinkName')
    related_list = meta['props'].get('RelatedFormLinkNames')
    if not related and related_list:
        related = related_list[0]
    if meta['data_type'] == 'Lookup' and related:
        lines.append(f"{indent}    formlinkname = {related}")

    if meta['props'].get('IsFormula'):
        lines.append(f"{indent}    formula = true")

    if meta['data_type'] == 'UploadFile':
        max_files = meta['props'].get('MaxFileCount', 10)
        lines.append(f"{indent}    file count = {max_files}")
        lines.append(f"{indent}    browse = local_drive")

    if meta['data_type'] == 'UploadImage':
        max_files = meta['props'].get('MaxFileCount', 10)
        lines.append(f"{indent}    file count = {max_files}")
        lines.append(f"{indent}    browse = local_drive")

    if meta['data_type'] == 'Lookup' and field['notes']:
        lines.append(f"{indent}    notes = \"{escape(field['notes'])}\"")
    elif field['notes'] and meta['data_type'] != 'SubForm':
        lines.append(f"{indent}    notes = \"{escape(field['notes'])}\"")

    if meta['data_type'] == 'Email' or 'email' in field['field_name'].lower():
        lines.append(f"{indent}    personal data = true")
    if meta['data_type'] == 'Phone' or 'phone' in field['field_name'].lower():
        lines.append(f"{indent}    personal data = true")
    if meta['data_type'] == 'Address':
        lines.append(f"{indent}    personal data = true")

    if meta['data_type'] == 'SubForm':
        sub_slug = meta['props'].get('SubFormLinkName')
        sub_form = subform_map.get(sub_slug)
        if sub_form:
            lines.append("")
            lines.extend(render_subform_fields(sub_form, name_map, subform_map, indent=indent + "    "))

    lines.append(f"{indent})")
    return lines


def render_form_ds(form, name_map, subform_map):
    display_name = re.sub(r"\s*\(subform\)", "", form['display_name'], flags=re.IGNORECASE)
    field_meta = prepare_field_meta(form, name_map)
    lines = []
    lines.append(f"// Module: {form['module'] or 'General'}")
    lines.append(f"form {form['slug']}")
    lines.append("{")
    lines.append("")
    lines.append(f"    displayname = \"{escape(display_name)}\"")
    lines.append(f"    success message = \"{escape(display_name)} added successfully\"")
    lines.append("")
    lines.append("    Section")
    lines.append("    (")
    lines.append("        type = section")
    lines.append("        row = 1")
    lines.append("        column = 0")
    lines.append("        width = medium")
    lines.append("    )")
    lines.append("")

    row_index = 1
    for meta in field_meta:
        lines.extend(render_field_block(meta, row_index, name_map, subform_map))
        lines.append("")
        row_index += 1
    if lines and lines[-1] == "":
        lines.pop()

    lines.append("")
    lines.append("    actions")
    lines.append("    {")
    lines.append("        on add")
    lines.append("        {")
    lines.append("            submit")
    lines.append("            (")
    lines.append("                type = submit")
    lines.append("                displayname = \"Submit\"")
    lines.append("            )")
    lines.append("            reset")
    lines.append("            (")
    lines.append("                type = reset")
    lines.append("                displayname = \"Reset\"")
    lines.append("            )")
    lines.append("        }")
    lines.append("        on edit")
    lines.append("        {")
    lines.append("            update")
    lines.append("            (")
    lines.append("                type = submit")
    lines.append("                displayname = \"Update\"")
    lines.append("            )")
    lines.append("            cancel")
    lines.append("            (")
    lines.append("                type = cancel")
    lines.append("                displayname = \"Cancel\"")
    lines.append("            )")
    lines.append("        }")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines), field_meta


def render_report_ds(form, field_meta):
    display_name = re.sub(r"\s*\(subform\)", "", form['display_name'], flags=re.IGNORECASE)
    report_slug = f"{form['slug']}_report"
    column_links = [meta['link_name'] for meta in field_meta]
    columns_joined = ', '.join(column_links)
    lines = []
    lines.append(f"report {report_slug}")
    lines.append("{")
    lines.append("")
    lines.append(f"    displayname = \"{escape(display_name)} Report\"")
    lines.append(f"    sourceform = {form['slug']}")
    lines.append("    type = list")
    lines.append("")
    for view_name in ('listview', 'quickview', 'detailview'):
        lines.append(f"    {view_name}")
        lines.append("    (")
        lines.append(f"        type = {view_name}")
        lines.append(f"        columns = {{{columns_joined}}}")
        lines.append("    )")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main():
    forms = parse_forms()
    ensure_unique_slugs(forms)
    name_map = build_name_maps(forms)
    subform_map = {form['slug']: form for form in forms if form.get('is_subform')}
    top_level_forms = [form for form in forms if not form.get('is_subform')]

    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    FORMS_OUTPUT.mkdir(parents=True, exist_ok=True)
    REPORTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    for form in top_level_forms:
        form_content, field_meta = render_form_ds(form, name_map, subform_map)
        form_path = FORMS_OUTPUT / f"{form['slug']}_form.ds"
        form_path.write_text(form_content)
        report_content = render_report_ds(form, field_meta)
        report_path = REPORTS_OUTPUT / f"{form['slug']}_report.ds"
        report_path.write_text(report_content)

    print(f"Generated {len(top_level_forms)} forms and reports in {OUTPUT_ROOT}")
    if UNMAPPED_LOOKUPS:
        print("Unmapped lookup targets detected:")
        for key in sorted(UNMAPPED_LOOKUPS):
            unique = sorted(set(UNMAPPED_LOOKUPS[key]))
            print(f"  - {key}: {', '.join(unique)}")


if __name__ == '__main__':
    main()
