#!/usr/bin/env python3
import os
import re
import tempfile
from fpdf import FPDF

input_file = "../docs/data-models/zoho_creator_data_model_field_map.md"
output_pdf = "../docs/data-models/zoho_creator_data_model_field_map_mermaid.pdf"

# Read Markdown
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Extract Mermaid blocks and section titles
blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
titles = re.findall(r"## (.*?)\n```mermaid", content)

if not blocks:
    raise ValueError("❌ No mermaid diagrams found in markdown.")

tmpdir = tempfile.mkdtemp()
png_paths = []

# Render each diagram directly to PNG using Mermaid CLI
for i, code in enumerate(blocks, start=1):
    mmd_path = os.path.join(tmpdir, f"diagram_{i}.mmd")
    png_path = os.path.join(tmpdir, f"diagram_{i}.png")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(code.strip())

    title = titles[i-1] if i-1 < len(titles) else f"Diagram {i}"
    print(f"🧩 Rendering {title} → {png_path}")
    os.system(f"mmdc -i {mmd_path} -o {png_path} --backgroundColor white --width 2400")

    png_paths.append((title, png_path))

# Assemble landscape PDF
pdf = FPDF(orientation="L", unit="mm", format="A4")
for title, png_path in png_paths:
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.image(png_path, x=10, y=20, w=270)

pdf.output(output_pdf)
print(f"\n✅ PDF created successfully: {output_pdf}")

