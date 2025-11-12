#!/usr/bin/env python3
"""Generate sample CSV data for all Creator forms."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

FORMS_DIR = Path('forms/ds/forms')
OUTPUT_PATH = Path('data/sample_form_data.csv')
NUM_RECORDS = 5

SKIP_NAMES = {'Section'}


def collect_block(lines: List[str], start_idx: int) -> Tuple[List[str], int]:
    """Collect lines inside a parenthesised block starting just after "("."""
    block: List[str] = []
    depth = 1
    i = start_idx
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == '(':
            depth += 1
            block.append(line)
        elif stripped == ')':
            depth -= 1
            if depth == 0:
                return block, i - start_idx + 1
            block.append(line)
        else:
            block.append(line)
        i += 1
    raise ValueError('Unbalanced parentheses in DS file')


def clean_field_name(raw: str) -> str:
    return re.sub(r'^(must have )?(unique )?', '', raw).strip()


def parse_field(raw_name: str, block_lines: List[str]) -> Dict[str, object] | None:
    info: Dict[str, object] = {
        'raw_name': raw_name.strip(),
        'name': clean_field_name(raw_name),
        'type': None,
        'displayname': None,
        'values': [],
        'subfields': [],
    }
    for line in block_lines:
        stripped = line.strip()
        if stripped.startswith('type ='):
            info['type'] = stripped.split('=', 1)[1].strip()
        elif stripped.startswith('displayname ='):
            info['displayname'] = stripped.split('=', 1)[1].strip().strip('"')
        elif 'values =' in stripped:
            info['values'] = re.findall(r'"([^\"]+)"', stripped)
    if info['type'] in (None, 'section'):
        return None
    if info['type'] == 'grid':
        info['subfields'] = parse_subfields(block_lines)
    return info


def parse_subfields(block_lines: List[str]) -> List[Dict[str, object]]:
    fields: List[Dict[str, object]] = []
    last_nonempty = ''
    i = 0
    while i < len(block_lines):
        line = block_lines[i]
        stripped = line.strip()
        if stripped == '(':
            indent = len(line) - len(line.lstrip())
            if indent == 2:
                raw_name = last_nonempty.strip()
                if raw_name and raw_name not in SKIP_NAMES:
                    sub_block, consumed = collect_block(block_lines, i + 1)
                    field_info = parse_field(raw_name, sub_block)
                    if field_info:
                        fields.append(field_info)
                    i += consumed
                    last_nonempty = ''
                    continue
        if stripped:
            last_nonempty = line
        i += 1
    return fields


def parse_form(path: Path) -> Tuple[str | None, str | None, List[Dict[str, object]]]:
    lines = path.read_text().splitlines()
    fields: List[Dict[str, object]] = []
    displayname: str | None = None
    last_nonempty = ''
    i = 0
    form_name: str | None = None
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('form '):
            form_name = stripped.split()[1]
        elif stripped.startswith('displayname =') and displayname is None and form_name:
            displayname = stripped.split('=', 1)[1].strip().strip('"')
        if stripped == '(':
            indent = len(line) - len(line.lstrip())
            if indent == 1:
                raw_name = last_nonempty.strip()
                if raw_name and raw_name not in SKIP_NAMES:
                    block, consumed = collect_block(lines, i + 1)
                    field_info = parse_field(raw_name, block)
                    if field_info:
                        fields.append(field_info)
                    i += consumed
                    last_nonempty = ''
                    continue
        if stripped:
            last_nonempty = line
        i += 1
    return form_name, displayname, fields


def generate_field_value(field: Dict[str, object], index: int) -> str:
    ftype = field['type']  # type: ignore[index]
    name = field['name']  # type: ignore[index]
    display = field.get('displayname') or str(name).replace('_', ' ').title()
    if ftype == 'text':
        return f"{display} Sample {index + 1}"
    if ftype == 'textarea':
        return f"Sample notes for {display} entry {index + 1}."
    if ftype == 'picklist':
        choices = field.get('values') or [f"Option {i}" for i in range(1, 5)]
        return choices[index % len(choices)]  # type: ignore[index]
    if ftype == 'list':
        choices = field.get('values') or [f"Choice {i}" for i in range(1, 5)]
        choices = list(choices)  # type: ignore[assignment]
        start = index % len(choices)
        picked = [choices[start]]
        if len(choices) > 1:
            picked.append(choices[(start + 1) % len(choices)])
        seen = set()
        ordered = []
        for val in picked:
            if val not in seen:
                seen.add(val)
                ordered.append(val)
        return '; '.join(ordered)
    if ftype == 'checkbox':
        return 'true' if index % 2 == 0 else 'false'
    if ftype == 'number':
        return str(100 + index * 5)
    if ftype == 'INR':
        return f"{1000 + index * 150:.2f}"
    if ftype == 'date':
        return f"2024-02-{index + 1:02d}"
    if ftype == 'datetime':
        return f"2024-02-{index + 1:02d} 10:{index * 10:02d}:00"
    if ftype == 'time':
        return f"10:{index * 10:02d}:00"
    if ftype == 'email':
        return f"contact{index + 1}@example.com"
    if ftype == 'phonenumber':
        return f"+91-9000000{index:02d}"
    if ftype == 'autonumber':
        return str(1000 + index)
    if ftype == 'address':
        return f"{index + 1} Sample Street, City {index + 1}, State, Country, 5600{index}"
    if ftype == 'upload file':
        return f"sample_{name}_{index + 1}.pdf"
    if ftype == 'url':
        return f"https://example.com/{name}/{index + 1}"
    if ftype == 'grid':
        subfields = field.get('subfields') or []
        records = []
        for sub_index in range(2):
            record = {
                subfield['name']: generate_field_value(subfield, index * 2 + sub_index)  # type: ignore[index]
                for subfield in subfields
            }
            records.append(record)
        return json.dumps(records, ensure_ascii=False)
    return f"Sample {display} {index + 1}"


def main() -> None:
    forms: Dict[str, Dict[str, object]] = {}
    for path in sorted(FORMS_DIR.glob('*.ds')):
        form_name, displayname, fields = parse_form(path)
        if not form_name:
            continue
        forms[form_name] = {
            'displayname': displayname or form_name.replace('_', ' ').title(),
            'fields': fields,
        }

    records: List[Dict[str, object]] = []
    ordered_fields: List[str] = []
    for form_name, info in forms.items():
        fields = info['fields']  # type: ignore[index]
        for field in fields:
            if field['name'] not in ordered_fields:
                ordered_fields.append(field['name'])
        for index in range(NUM_RECORDS):
            row: Dict[str, object] = {
                'form_name': form_name,
                'form_displayname': info['displayname'],
                'record_index': index + 1,
            }
            for field in fields:
                row[field['name']] = generate_field_value(field, index)  # type: ignore[index]
            records.append(row)

    columns = ['form_name', 'form_displayname', 'record_index', *ordered_fields]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for record in records:
            writer.writerow({column: record.get(column, '') for column in columns})

    print(f"Generated {len(records)} records across {len(forms)} forms -> {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
