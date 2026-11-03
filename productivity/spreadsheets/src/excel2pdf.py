# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl", "reportlab"]
# ///
"""Export one sheet (or a cell range) of an .xlsx file to a PDF table.

Usage:
    uv run excel2pdf.py input.xlsx output.pdf [--sheet Sheet1] [--range B1:I85]
"""
import argparse

import openpyxl
from openpyxl.utils import range_boundaries
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def excel_range_to_pdf(excel_path, pdf_path, sheet_name=None, cell_range=None):
    # data_only=True reads cached formula results instead of formula strings
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active

    if cell_range:
        min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    else:
        min_col, min_row, max_col, max_row = 1, 1, ws.max_column, ws.max_row

    data = [
        ["" if v is None else v for v in row]
        for row in ws.iter_rows(min_row=min_row, max_row=max_row,
                                min_col=min_col, max_col=max_col, values_only=True)
    ]

    table = Table(data, repeatRows=1)  # repeat header row on every page
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    SimpleDocTemplate(pdf_path, pagesize=landscape(A4)).build([table])
    print(f"PDF saved to {pdf_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("excel_path")
    p.add_argument("pdf_path")
    p.add_argument("--sheet", default=None, help="sheet name (default: active sheet)")
    p.add_argument("--range", dest="cell_range", default=None, help="e.g. B1:I85 (default: whole sheet)")
    args = p.parse_args()
    excel_range_to_pdf(args.excel_path, args.pdf_path, args.sheet, args.cell_range)
