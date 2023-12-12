import pandas as pd
import numpy as np
from weasyprint import HTML, CSS
data = [{"a": 1, "b": 2, "c":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,],
                "d": [4,4,4,4,4,4,4,4,4,]},
        {"a": 5, "b": [6,6,6,6,6,6,6,6,6,6], "c":
          [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7], "d": 8}]

def pdf_gen_weasyprint():

        # extract headers from input data
        table_headers = [headers.title() for headers in data[0]]

        # extract table data from input data
        table_values = [str(v) for d in data for k, v in d.items()]

        # convert input data to HTML
        a = np.array(table_values)
        df = pd.DataFrame(a.reshape(-1, len(table_headers)), columns=table_headers)
        html_string = df.to_html(index=False)

        # write html to pdf
        html_doc = HTML(string=html_string)

        html_doc.write_pdf(f"your_report.pdf", stylesheets=None)

pdf_gen_weasyprint()