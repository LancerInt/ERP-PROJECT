local stringify = (require "pandoc.utils").stringify

local current_heading = { level = 0, text = "" }

local function make_cell(text, align)
  align = align or pandoc.AlignCenter
  local contents = {pandoc.Plain({pandoc.Str(text)})}
  return pandoc.Cell(pandoc.Attr(), align, 1, 1, contents)
end

local function ensure_header_format(row)
  for _, cell in ipairs(row.cells) do
    local inlines = {
      pandoc.RawInline("latex", "\\headercell{"),
      pandoc.Str(stringify(cell.contents)),
      pandoc.RawInline("latex", "}")
    }
    cell.contents = {pandoc.Plain(inlines)}
    cell.attr = cell.attr or pandoc.Attr()
  end
  -- prepend row color to the first cell only once
  local first_cell = row.cells[1]
  local first_inline_block = first_cell.contents[1]
  local inlines = first_inline_block.content
  table.insert(inlines, 1, pandoc.RawInline("latex", "\\rowcolor{tableHeader}"))
  first_cell.contents[1] = pandoc.Plain(inlines)
end

local function with_serial_numbers(tbl)
  local original_cols = #tbl.colspecs
  local new_colspecs = {}
  local serial_width = 0.08
  new_colspecs[1] = {pandoc.AlignCenter, serial_width}
  local remaining_width = 1.0 - serial_width

  local widths = {}
  if original_cols == 5 then
    local base = {0.24, 0.22, 0.18, 0.10, 0.26}
    for i = 1, original_cols do
      widths[i] = base[i] * remaining_width
    end
  else
    local per = remaining_width / original_cols
    for i = 1, original_cols do
      widths[i] = per
    end
  end

  for i = 1, original_cols do
    local align = tbl.colspecs[i][1] or pandoc.AlignLeft
    new_colspecs[i + 1] = {align, widths[i]}
  end
  tbl.colspecs = new_colspecs

  for _, row in ipairs(tbl.head.rows) do
    table.insert(row.cells, 1, make_cell("S.No."))
    ensure_header_format(row)
  end

  local counter = 1
  for _, body in ipairs(tbl.bodies) do
    for _, head_row in ipairs(body.head) do
      table.insert(head_row.cells, 1, make_cell("S.No."))
      ensure_header_format(head_row)
    end
    for _, row in ipairs(body.body) do
      table.insert(row.cells, 1, make_cell(tostring(counter)))
      counter = counter + 1
    end
  end

  for _, row in ipairs(tbl.foot.rows) do
    table.insert(row.cells, 1, make_cell(""))
  end

  return tbl
end

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
      if (not tbl.caption) or (#tbl.caption.long == 0 and #tbl.caption.short == 0) then
        if current_heading.text ~= "" then
          tbl.caption.long = { pandoc.Plain({ pandoc.Str(current_heading.text) }) }
        end
      end
      return with_serial_numbers(tbl)
    end
  }
}
