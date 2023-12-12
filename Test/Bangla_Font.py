from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.add_font('Bang', '', 'Shonar.ttf', uni=True)
        self.set_font("Bang", size = 20) 
        # Set up the font and size
        # self.set_font('Arial', 'B', 12)
        # Add a cell with Bengali text
        self.cell(0, 10, u'বাংলা পিডিএফ', ln=True, align='C')

    def footer(self):
        # Set up the font and size
        self.add_font('Bang', '', 'Shonar.ttf', uni=True)
        self.set_font("Bang", size = 14) 
        # self.set_font('Arial', 'I', 8)
        # Add a page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        # Set up the font and size
        self.add_font('Bang', '', 'Shonar.ttf', uni=True)
        self.set_font("Bang", size = 14) 
        # self.set_font('Arial', 'B', 16)
        # Add a chapter title with Bengali text
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        # Set up the font and size
        self.add_font('Bang', '', 'Shonar.ttf', uni=True)
        self.set_font("Bang", size = 14) 
        # self.set_font('Arial', '', 12)
        # Add the chapter body with Bengali text
        self.multi_cell(0, 10, body)

# Create a new PDF object
pdf = PDF()
pdf.add_page()

# Add content with Bengali text
pdf.chapter_title(u'প্রথম অধ্যায়')
pdf.chapter_body(u'মোঃ মাসুদ জামান')

pdf.output("output.pdf","F")
