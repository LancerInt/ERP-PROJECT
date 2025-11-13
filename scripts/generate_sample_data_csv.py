#!/usr/bin/env python3
"""Generate sample CSV data for Zoho Creator forms.

This script can ingest either the compiled ``ERP_PRO.ds`` application export or
the already-split ``forms/ds/forms`` directory.  For every form discovered we
emit a standalone CSV populated with ``NUM_RECORDS`` illustrative rows so that
imports can be trialled without touching production data.
"""

from __future__ import annotations

import csv
import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

FORMS_DIR = Path('forms/ds/forms')
DS_EXPORT = Path('ERP_PRO.ds')
OUTPUT_DIR = Path('data/sample_form_data')
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


def parse_field(raw_name: str, block_lines: List[str], *, max_indent: int = 2) -> Dict[str, object] | None:
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
        indent = len(line) - len(line.lstrip())
        if stripped.startswith('type =') and indent <= max_indent:
            info['type'] = stripped.split('=', 1)[1].strip()
        elif stripped.startswith('displayname =') and indent <= max_indent:
            info['displayname'] = stripped.split('=', 1)[1].strip().strip('"')
        elif 'values =' in stripped and indent <= max_indent:
            info['values'] = re.findall(r'"([^\"]+)"', stripped)
    if info['type'] in (None, 'section', 'submit', 'reset', 'cancel'):
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
                    field_info = parse_field(raw_name, sub_block, max_indent=3)
                    if field_info:
                        fields.append(field_info)
                    i += consumed
                    last_nonempty = ''
                    continue
        if stripped:
            last_nonempty = line
        i += 1
    return fields


def parse_form_lines(lines: List[str]) -> Tuple[str | None, str | None, List[Dict[str, object]]]:
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


def parse_form(path: Path) -> Tuple[str | None, str | None, List[Dict[str, object]]]:
    return parse_form_lines(path.read_text().splitlines())


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


def split_forms_from_ds(lines: List[str]) -> Iterable[List[str]]:
    """Yield each form definition block from an application DS export."""

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('form '):
            block: List[str] = [lines[i]]
            i += 1
            depth = 0
            started = False
            while i < len(lines):
                line = lines[i]
                block.append(line)
                open_count = line.count('{')
                close_count = line.count('}')
                if open_count:
                    depth += open_count
                    started = True
                if close_count and started:
                    depth -= close_count
                    if depth <= 0:
                        i += 1
                        break
                i += 1
            yield block
            continue
        i += 1


def load_forms_from_directory(directory: Path) -> Dict[str, Dict[str, object]]:
    forms: Dict[str, Dict[str, object]] = {}
    for path in sorted(directory.glob('*.ds')):
        form_name, displayname, fields = parse_form(path)
        if not form_name:
            continue
        forms[form_name] = {
            'displayname': displayname or form_name.replace('_', ' ').title(),
            'fields': fields,
        }
    return forms


def load_forms_from_ds(path: Path) -> Dict[str, Dict[str, object]]:
    lines = path.read_text().splitlines()
    forms: Dict[str, Dict[str, object]] = {}
    for block in split_forms_from_ds(lines):
        form_name, displayname, fields = parse_form_lines(block)
        if not form_name:
            continue
        forms[form_name] = {
            'displayname': displayname or form_name.replace('_', ' ').title(),
            'fields': fields,
        }
    return forms


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-i',
        '--input',
        type=Path,
        help='Path to ERP_PRO.ds or a directory of form DS files (defaults to auto-detection)',
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        type=Path,
        default=OUTPUT_DIR,
        help=f'Directory to write CSV files (default: {OUTPUT_DIR})',
    )
    parser.add_argument(
        '-n',
        '--num-records',
        type=int,
        default=NUM_RECORDS,
        help=f'Number of sample records per form (default: {NUM_RECORDS})',
    )
    parser.add_argument(
        '-f',
        '--form',
        dest='forms',
        action='append',
        help='Limit generation to the provided form link names (case-insensitive)',
    )
    parser.add_argument(
        '--include-metadata',
        action='store_true',
        help='Include helper columns (form name, display name, record index) in each CSV',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source_path = args.input
    forms: Dict[str, Dict[str, object]]
    if source_path:
        if source_path.is_file():
            forms = load_forms_from_ds(source_path)
        elif source_path.is_dir():
            forms = load_forms_from_directory(source_path)
        else:
            raise FileNotFoundError(f'Input path {source_path} does not exist')
    else:
        if DS_EXPORT.exists():
            forms = load_forms_from_ds(DS_EXPORT)
        else:
            forms = load_forms_from_directory(FORMS_DIR)

    requested_forms = {name.lower() for name in args.forms} if args.forms else None

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files: List[Path] = []
    for form_name in sorted(forms):
        info = forms[form_name]
        if requested_forms and form_name.lower() not in requested_forms:
            continue

        fields = info['fields']  # type: ignore[index]
        if not fields:
            continue

        rows: List[Dict[str, object]] = []
        for index in range(args.num_records):
            row: Dict[str, object] = {}
            if args.include_metadata:
                row.update(
                    {
                        'form_name': form_name,
                        'form_displayname': info['displayname'],
                        'record_index': index + 1,
                    }
                )
            for field in fields:
                row[field['name']] = generate_field_value(field, index)  # type: ignore[index]
            rows.append(row)

        columns: List[str] = []
        if args.include_metadata:
            columns.extend(['form_name', 'form_displayname', 'record_index'])
        columns.extend(field['name'] for field in fields)
        output_path = output_dir / f'{form_name}_sample_data.csv'
        with output_path.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        generated_files.append(output_path)

    if not generated_files:
        if requested_forms:
            missing = ', '.join(sorted(requested_forms))
            raise SystemExit(f'No forms matched the requested filters: {missing}')
        raise SystemExit('No forms discovered in the provided input')

    if requested_forms:
        filtered_count = len(generated_files)
        print(f'Generated {filtered_count} CSV file(s) in {output_dir} for requested forms')
    else:
        print(f'Generated {len(generated_files)} CSV files in {output_dir}')


if __name__ == '__main__':
    main()
