from fpdf import FPDF
import uharfbuzz as hb

pdf = FPDF()
pdf.add_page()
pdf.set_text_shaping(True)
# Set the font
pdf.add_font('BanglaFont', '', 'ARIALUNI.ttf', uni=True)
pdf.set_font('BanglaFont', '', 12)  # Set the font size to 12

# Add text to the PDF
pdf.cell(0, 10, 'বাংলা ফন্টে লেখা', ln=True)

# Output the PDF
pdf.output('output.pdf','F')
