from fpdf import FPDF 
pdf = FPDF() 
   
pdf.add_page()

pdf.add_font('Bang', '', 'Shonar.ttf', uni=True)
pdf.set_font("Bang", size = 14) 
  
# create a cell 
file = open("jg_employee_selected_column.csv", "r") 
    
# insert the texts in pdf 
for g in file: 
    # pdf.write(8, g)
    pdf.cell(0, 10, txt = g, ln = 1, align = 'L') 
     
  
pdf.output("op.pdf", 'F')