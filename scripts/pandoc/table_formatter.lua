-- table_formatter.lua
-- ✅ Final portrait-mode version for Pandoc 3.8.2.1 (Lua 5.4)
-- Adds serial numbers, alternating gray rows, thin gray borders,
-- and one-line captions like “1.1.2.1 Godown (subform) (Table 3)”.

local stringify = (require "pandoc.utils").stringify
local current_heading = { level = 0, text = "" }

---------------------------------------------------------------------
-- Pandoc 3.8 record-style Cell constructor
---------------------------------------------------------------------
local function make_cell(text, align)
  align = align or "AlignCenter"
  return pandoc.Cell{
    attr      = pandoc.Attr(),
    alignment = align,
    contents  = { pandoc.Plain({ pandoc.Str(text or "") }) },
    rowspan   = 1,
    colspan   = 1
  }
end

---------------------------------------------------------------------
-- Header formatting
---------------------------------------------------------------------
local function ensure_header_format(row)
  for _, cell in ipairs(row.cells) do
    local txt = stringify(cell.contents or "")
    local inlines = {
      pandoc.RawInline("latex", "\\headercell{"),
      pandoc.Str(txt),
      pandoc.RawInline("latex", "}")
    }
    cell.contents = { pandoc.Plain(inlines) }
  end
end

---------------------------------------------------------------------
-- Serial-number injection + alternating colors
---------------------------------------------------------------------
local function with_serial_numbers(tbl)
  local original_cols = #tbl.colspecs
  local new_colspecs = {}
  local serial_width = 0.08
  new_colspecs[1] = { "AlignCenter", serial_width }
  local remaining_width = 1.0 - serial_width

  local widths = {}
  if original_cols == 5 then
    local base = {0.24, 0.22, 0.18, 0.10, 0.26}
    for i = 1, original_cols do widths[i] = base[i] * remaining_width end
  else
    local per = remaining_width / math.max(original_cols, 1)
    for i = 1, original_cols do widths[i] = per end
  end
  for i = 1, original_cols do
    local align = tbl.colspecs[i][1] or "AlignLeft"
    new_colspecs[i + 1] = { align, widths[i] }
  end
  tbl.colspecs = new_colspecs

  -- Header
  for _, row in ipairs(tbl.head.rows or {}) do
    table.insert(row.cells, 1, make_cell("S.No."))
    ensure_header_format(row)
  end

  -- Body
  local counter = 1
  for _, body in ipairs(tbl.bodies or {}) do
    for _, row in ipairs(body.body or {}) do
      table.insert(row.cells, 1, make_cell(tostring(counter)))
      counter = counter + 1
    end
  end

  -- Foot
  for _, row in ipairs(tbl.foot.rows or {}) do
    table.insert(row.cells, 1, make_cell(""))
  end

  return tbl
end

---------------------------------------------------------------------
-- Custom caption builder: “Title (Table N)” merged in one line
---------------------------------------------------------------------
local function reorder_caption(tbl)
  local heading_text = current_heading.text or ""
  local num = ""
  if tbl.identifier and #tbl.identifier > 0 then
    num = tbl.identifier:gsub("[^%d]+", "")
  elseif tbl.attr and tbl.attr.identifier and #tbl.attr.identifier > 0 then
    num = tbl.attr.identifier:gsub("[^%d]+", "")
  end
  local final_caption = heading_text
  if num ~= "" then
    final_caption = final_caption .. " (Table " .. num .. ")"
  end
  tbl.caption = pandoc.Caption{
    long = { pandoc.Plain({ pandoc.Str(final_caption) }) }
  }
  return tbl
end

---------------------------------------------------------------------
-- Main Pandoc filter
---------------------------------------------------------------------
return {
  {
    Header = function(el)
      if el.level >= 3 then
        current_heading = { level = el.level, text = stringify(el.content) }
      else
        current_heading = { level = el.level, text = "" }
      end
      return el
    end,

    Table = function(tbl)
      tbl = with_serial_numbers(tbl)
      tbl = reorder_caption(tbl)

      return {
        pandoc.RawBlock("latex",
          "\\rowcolors{2}{gray!5}{white}\n" ..
          "\\arrayrulecolor{gray!50}\\setlength{\\arrayrulewidth}{0.3pt}"
        ),
        tbl
      }
    end
  }
}
