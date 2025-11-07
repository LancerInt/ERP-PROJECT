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
        data_type = 'Checkboxes'
    elif text == 'Multi-select Dropdown':
        data_type = 'Checkboxes'
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
    elif text == 'Percentage':
        data_type = 'Percentage'
    elif 'lookup' in text.lower():
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
    if data_type == 'UploadFile':
        props.setdefault('MaxFileCount', 10)
        props.setdefault('AllowMultiple', True)
        props.setdefault('FileSource', 'LocalDrive')
    return data_type, props


def extract_choice_values(field):
    notes = (field.get('notes') or '').strip()
    if not notes:
        return None
    notes = re.split(r'[.;]', notes)[0].strip()
    if not notes:
        return None
    if '/' in notes:
        parts = re.split(r'\s*/\s*', notes)
    elif ',' in notes and 'http' not in notes.lower():
        parts = [p.strip() for p in notes.split(',')]
    else:
        return None
    cleaned = []
    for part in parts:
        piece = re.sub(r"\s*\(.*?\)\s*", "", part).strip()
        piece = piece.strip('"')
        piece = piece.strip()
        if piece:
            cleaned.append(piece)
    if len(cleaned) < 2:
        return None
    if any(len(piece) > 40 for piece in cleaned):
        return None
    return cleaned


def prepare_field_meta(form, name_map):
    prepared = []
    for field in form['fields']:
        link_name = field['link_name'] or slugify(field['field_name'])
        data_type, props = map_field_type(field, form, name_map)
        if data_type == 'Lookup':
            continue
        prepared.append({
            'field': field,
            'link_name': link_name,
            'data_type': data_type,
            'props': props,
            'required': field['required'].strip().upper(),
            'choices': extract_choice_values(field) if data_type in {'Dropdown', 'Checkboxes'} else None,
        })
    return prepared


def ds_attr_name(key: str) -> str:
    key = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', key)
    key = key.replace('_', ' ')
    return key.strip().lower()


def ds_value(value, key=None):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    if isinstance(value, list):
        return '{' + ','.join(f'"{v}"' for v in value) + '}'
    if value is None:
        return 'null'
    value = str(value)
    lower_key = (key or '').lower()
    if lower_key in {'type', 'row', 'column', 'width', 'height', 'file count', 'start index', 'browse', 'format'}:
        return value
    if lower_key in {'related form', 'related forms'} and value:
        return value
    if lower_key == 'timedisplayoptions':
        return f'"{value}"'
    if value.endswith('px') and lower_key == 'height':
        return value
    return f'"{value}"'


def render_address_components(indent):
    components = [
        ('address_line_1', 'Address Line 1'),
        ('address_line_2', 'Address Line 2'),
        ('district_city', 'City / District'),
        ('state_province', 'State / Province'),
        ('postal_Code', 'Postal Code'),
        ('country', 'Country'),
        ('latitude', 'Latitude'),
        ('longitude', 'Longitude'),
    ]
    lines = []
    for name, label in components:
        lines.append(f"{indent}{name}")
        lines.append(f"{indent}(")
        lines.append(f"{indent}\ttype = {ds_value(name, 'type')}")
        lines.append(f"{indent}\tdisplayname = \"{label}\"")
        if name in {'latitude', 'longitude'}:
            lines.append(f"{indent}\tvisibility = false")
        lines.append(f"{indent})")
        lines.append("")
    if lines:
        lines.pop()
    return lines


def map_to_ds_type(meta):
    data_type = meta['data_type']
    extras = []
    if data_type == 'SingleLine':
        ds_type = 'text'
    elif data_type == 'MultiLine':
        ds_type = 'textarea'
        extras.append(('height', '100px'))
    elif data_type == 'Email':
        ds_type = 'email'
        extras.append(('personal data', True))
    elif data_type == 'Phone':
        ds_type = 'phonenumber'
        extras.append(('personal data', True))
    elif data_type == 'Dropdown':
        ds_type = 'picklist'
    elif data_type == 'Checkboxes':
        ds_type = 'list'
    elif data_type == 'Checkbox':
        ds_type = 'checkbox'
    elif data_type == 'Date':
        ds_type = 'date'
    elif data_type == 'DateTime':
        ds_type = 'datetime'
    elif data_type == 'Time':
        ds_type = 'time'
        extras.append(('timedisplayoptions', 'hh:mm:ss'))
    elif data_type == 'AutoNumber':
        ds_type = 'autonumber'
        extras.append(('start index', 1))
    elif data_type == 'Percentage':
        ds_type = 'percentage'
    elif data_type == 'Decimal':
        ds_type = 'number'
    elif data_type == 'Number':
        ds_type = 'number'
    elif data_type == 'INR':
        ds_type = 'INR'
    elif data_type == 'Address':
        ds_type = 'address'
        extras.append(('capture_coordinates', True))
        extras.append(('adjust_using_map', False))
        extras.append(('personal data', True))
    elif data_type == 'Lookup':
        ds_type = 'lookup'
        if 'AllowMultiple' in meta['props'] and meta['props']['AllowMultiple']:
            extras.append(('allow multiple', True))
        related_single = meta['props'].get('RelatedFormLinkName')
        related_multi = meta['props'].get('RelatedFormLinkNames')
        if related_multi:
            extras.append(('related forms', related_multi))
        elif related_single:
            extras.append(('related form', related_single))
    elif data_type == 'SubForm':
        ds_type = 'grid'
    elif data_type == 'UploadFile':
        ds_type = 'upload file'
        source = meta['props'].get('FileSource', 'local_drive')
        source = re.sub(r'(?<!^)(?=[A-Z])', '_', str(source)).lower()
        extras.append(('file count', meta['props'].get('MaxFileCount', 10)))
        extras.append(('browse', source))
    elif data_type == 'UploadImage':
        ds_type = 'upload file'
        source = meta['props'].get('FileSource', 'local_drive')
        source = re.sub(r'(?<!^)(?=[A-Z])', '_', str(source)).lower()
        extras.append(('file count', meta['props'].get('MaxFileCount', 10)))
        extras.append(('browse', source))
    elif data_type == 'URL':
        ds_type = 'url'
    else:
        ds_type = 'text'
    return ds_type, extras


def render_field(meta, forms_meta, indent='\t', include_layout=True, visited=None):
    if visited is None:
        visited = set()
    required = meta['required']
    is_unique = bool(meta['props'].get('IsUnique'))
    if is_unique:
        prefix = 'must have unique '
    elif required in {'Y', 'C'}:
        prefix = 'must have '
    else:
        prefix = ''
    lines = []
    lines.append(f"{indent}{prefix}{meta['link_name']}")
    lines.append(f"{indent}(")
    ds_type, extras = map_to_ds_type(meta)
    lines.append(f"{indent}\ttype = {ds_value(ds_type, 'type')}")
    lines.append(f"{indent}\tdisplayname = \"{meta['field']['field_name']}\"")
    pre_layout = []
    post_layout = []
    for key, value in extras:
        attr_name = ds_attr_name(key)
        target = post_layout if attr_name == 'personal data' else pre_layout
        target.append(f"{indent}\t{attr_name} = {ds_value(value, attr_name)}")
    for key, value in meta['props'].items():
        if key in {'MaxFileCount', 'FileSource', 'AllowMultiple', 'RelatedFormLinkName', 'RelatedFormLinkNames', 'SubFormLinkName', 'IsUnique'}:
            continue
        attr_name = ds_attr_name(key)
        target = post_layout if attr_name == 'personal data' else pre_layout
        target.append(f"{indent}\t{attr_name} = {ds_value(value, attr_name)}")
    if ds_type == 'picklist':
        choices = meta['choices'] or ["Option 1", "Option 2", "Option 3"]
        pre_layout.append(f"{indent}\tmaxchar = 100")
        pre_layout.append(f"{indent}\tvalues = {ds_value(choices, 'values')}")
    if ds_type == 'list':
        choices = meta['choices'] or ["Choice 1", "Choice 2", "Choice 3"]
        pre_layout.append(f"{indent}\tvalues = {ds_value(choices, 'values')}")
        pre_layout.append(f"{indent}\theight = 60px")
    lines.extend(pre_layout)
    if meta['data_type'] == 'Address':
        sub_lines = render_address_components(f"{indent}\t")
        lines.extend(sub_lines)
    layout_lines = []
    if include_layout:
        layout_lines.extend([f"{indent}\trow = 1", f"{indent}\tcolumn = 1"])
    width_line = f"{indent}\twidth = medium"
    if meta['data_type'] != 'SubForm':
        lines.extend(layout_lines)
        lines.append(width_line)
        lines.extend(post_layout)
    if meta['data_type'] == 'SubForm':
        sub_slug = meta['props'].get('SubFormLinkName')
        if sub_slug and sub_slug not in visited and sub_slug in forms_meta:
            visited.add(sub_slug)
            for sub_meta in forms_meta[sub_slug]:
                lines.extend(render_field(sub_meta, forms_meta, indent + '\t', include_layout=False, visited=visited))
            visited.remove(sub_slug)
        lines.extend(layout_lines)
        lines.append(width_line)
        lines.extend(post_layout)
    lines.append(f"{indent})")
    lines.append("")
    return lines


def render_form_ds(form, field_meta, forms_meta):
    display_name = re.sub(r"\s*\(subform\)", "", form['display_name'], flags=re.IGNORECASE)
    lines = []
    lines.append(f"form {form['slug']}")
    lines.append("{")
    lines.append(f"\tdisplayname = \"{display_name}\"")
    lines.append(f"\tsuccess message = \"{display_name} added successfully\"")
    lines.append("")
    lines.append("\tSection")
    lines.append("\t(")
    lines.append("\t\ttype = section")
    lines.append("\t\trow = 1")
    lines.append("\t\tcolumn = 0")
    lines.append("\t\twidth = medium")
    lines.append("\t)")
    lines.append("")
    for meta in field_meta:
        lines.extend(render_field(meta, forms_meta))
    lines.append("\tactions")
    lines.append("\t{")
    lines.append("\t\ton add")
    lines.append("\t\t{")
    lines.append("\t\t\tsubmit")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\ttype = submit")
    lines.append("\t\t\t\tdisplayname = \"Submit\"")
    lines.append("\t\t\t)")
    lines.append("\t\t\treset")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\ttype = reset")
    lines.append("\t\t\t\tdisplayname = \"Reset\"")
    lines.append("\t\t\t)")
    lines.append("\t\t}")
    lines.append("\t\ton edit")
    lines.append("\t\t{")
    lines.append("\t\t\tupdate")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\ttype = submit")
    lines.append("\t\t\t\tdisplayname = \"Update\"")
    lines.append("\t\t\t)")
    lines.append("\t\t\tcancel")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\ttype = cancel")
    lines.append("\t\t\t\tdisplayname = \"Cancel\"")
    lines.append("\t\t\t)")
    lines.append("\t\t}")
    lines.append("\t}")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def render_report_ds(form, field_meta):
    display_name = re.sub(r"\s*\(subform\)", "", form['display_name'], flags=re.IGNORECASE)
    slug = form['slug']
    lines = []
    lines.append(f"list {slug}_report")
    lines.append("{")
    lines.append(f"\tdisplayName = \"{display_name} Report\"")
    lines.append(f"\tshow all rows from {slug}")
    lines.append("\t(")
    for meta in field_meta:
        lines.append(f"\t\t{meta['link_name']} as \"{meta['field']['field_name']}\"")
    lines.append("\t)")
    lines.append("\tquickview")
    lines.append("\t(")
    lines.append("\t\tlayout")
    lines.append("\t\t(")
    lines.append("\t\t\tdatablock1")
    lines.append("\t\t\t(")
    lines.append(f"\t\t\t\ttitle = \"{display_name} Overview\"")
    lines.append("\t\t\t\tfields")
    lines.append("\t\t\t\t(")
    for meta in field_meta:
        lines.append(f"\t\t\t\t\t{meta['link_name']} as \"{meta['field']['field_name']}\"")
    lines.append("\t\t\t\t)")
    lines.append("\t\t\t)")
    lines.append("\t\t)")
    lines.append("\t\tmenu")
    lines.append("\t\t(")
    lines.append("\t\t\theader")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\tEdit")
    lines.append("\t\t\t\tDuplicate")
    lines.append("\t\t\t\tDelete")
    lines.append("\t\t\t)")
    lines.append("\t\t\trecord")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\tEdit")
    lines.append("\t\t\t\tDuplicate")
    lines.append("\t\t\t\tDelete")
    lines.append("\t\t\t)")
    lines.append("\t\t)")
    lines.append("\t\taction")
    lines.append("\t\t(")
    lines.append("\t\t\ton click")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\tView Record")
    lines.append("\t\t\t)")
    lines.append("\t\t\ton right click")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\tEdit")
    lines.append("\t\t\t\tDelete")
    lines.append("\t\t\t\tDuplicate")
    lines.append("\t\t\t\tView Record")
    lines.append("\t\t\t)")
    lines.append("\t\t)")
    lines.append("\t)")
    lines.append("\tdetailview")
    lines.append("\t(")
    lines.append("\t\tlayout")
    lines.append("\t\t(")
    lines.append("\t\t\tdatablock1")
    lines.append("\t\t\t(")
    lines.append(f"\t\t\t\ttitle = \"{display_name} Overview\"")
    lines.append("\t\t\t\tfields")
    lines.append("\t\t\t\t(")
    for meta in field_meta:
        lines.append(f"\t\t\t\t\t{meta['link_name']} as \"{meta['field']['field_name']}\"")
    lines.append("\t\t\t\t)")
    lines.append("\t\t\t)")
    lines.append("\t\t)")
    lines.append("\t\tmenu")
    lines.append("\t\t(")
    lines.append("\t\t\theader")
    lines.append("\t\t\t(")
    lines.append("\t\t\t\tEdit")
    lines.append("\t\t\t\tDuplicate")
    lines.append("\t\t\t\tDelete")
    lines.append("\t\t\t)")
    lines.append("\t\t)")
    lines.append("\t)")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main():
    forms = parse_forms()
    ensure_unique_slugs(forms)
    name_map = build_name_maps(forms)
    forms_meta = {}
    for form in forms:
        forms_meta[form['slug']] = prepare_field_meta(form, name_map)
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    FORMS_OUTPUT.mkdir(parents=True, exist_ok=True)
    REPORTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    for form in forms:
        field_meta = forms_meta[form['slug']]
        form_content = render_form_ds(form, field_meta, forms_meta)
        form_path = FORMS_OUTPUT / f"{form['slug']}_form.ds"
        form_path.write_text(form_content)
        report_content = render_report_ds(form, field_meta)
        report_path = REPORTS_OUTPUT / f"{form['slug']}_report.ds"
        report_path.write_text(report_content)
    print(f"Generated {len(forms)} forms and reports in {OUTPUT_ROOT}")
    if UNMAPPED_LOOKUPS:
        print("Unmapped lookup targets detected:")
        for key in sorted(UNMAPPED_LOOKUPS):
            unique = sorted(set(UNMAPPED_LOOKUPS[key]))
            print(f"  - {key}: {', '.join(unique)}")


if __name__ == '__main__':
    main()
