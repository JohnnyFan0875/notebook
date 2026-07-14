# Excel to PDF Conversion

This script converts a given sheet (and optional cell range) from an Excel file (`.xlsx`) into a formatted PDF table using **`openpyxl`** and **`reportlab`**.

## Features

- Works with `.xlsx` files
- Allows selection of:

  - Specific sheet by name
  - Specific cell range (e.g., `B1:I85`) or entire sheet

- Outputs a nicely formatted PDF with:

  - Header styling
  - Grid lines
  - Center-aligned text

## Code

```python
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def excel_range_to_pdf(excel_path, pdf_path, sheet_name=None, cell_range=None):
    """
    Convert a specified sheet and cell range of an Excel file to a PDF table.

    Parameters
    ----------
    excel_path : str
        Path to the input Excel file (.xlsx).
    pdf_path : str
        Path to the output PDF file.
    sheet_name : str, optional
        Name of the sheet to convert. If None, the active sheet is used.
    cell_range : str, optional
        Excel range string like 'B1:I85'. If None, the entire sheet is exported.
    """

    # Load workbook and select sheet
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active

    # Define range boundaries
    if cell_range:
        min_col, min_row, max_col, max_row = openpyxl.utils.range_boundaries(cell_range)
    else:
        min_col, min_row = 1, 1
        max_col, max_row = ws.max_column, ws.max_row

    # Extract data from sheet
    data = [
        [cell if cell is not None else '' for cell in row]
        for row in ws.iter_rows(
            min_row=min_row, max_row=max_row,
            min_col=min_col, max_col=max_col,
            values_only=True
        )
    ]

    # Create PDF document
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

    # Create and style table
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),        # Header background
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),   # Header text color
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),               # Center align
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),     # Bold header
        ('BOTTOMPADDING', (0,0), (-1,0), 12),              # Header padding
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),       # Grid lines
    ])
    table.setStyle(style)

    # Build PDF
    pdf.build([table])
    print(f"PDF saved to {pdf_path}")

if __name__ == "__main__":
    excel_file = "input.xlsx"
    output_pdf = "output.pdf"
    sheet = "Sheet1"        # or None for active sheet
    excel_range = "B1:I85"  # or None for entire sheet

    excel_range_to_pdf(excel_file, output_pdf, sheet_name=sheet, cell_range=excel_range)
```

## Usage

1. Install dependencies:

   ```bash
   pip install openpyxl reportlab
   ```

2. Modify the `excel_file`, `output_pdf`, `sheet`, and `excel_range` variables in the `__main__` block.

3. Run the script:

   ```bash
   python excel2pdf.py
   ```
