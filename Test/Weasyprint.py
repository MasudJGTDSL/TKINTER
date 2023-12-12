import pandas as pd
import numpy as np
from weasyprint import HTML, CSS
import subprocess


def weasy_print_pdf():
    data_read = pd.read_csv("JGTDSL_Employee.csv")
    selected_column = [
        "JGID",
        "PersonName",
        "FathersName",
        "DateOfBirth",
        "CurrentBasicPay",
        "Email",
        "Mobile",
    ]

    selected_column_df = data_read[selected_column]
    data_dict_df = selected_column_df.T.to_dict()
    data = [[x for x in val.values()] for val in data_dict_df.values()]
    # For Data -------------
    html_string = """<html>
    <head>
    <style>
    table, td, th {
    border: 1px solid;
    }
    .align_enter {
    text-align: center;
    }
    table {
    width: 100%;
    border-collapse: collapse;
    }
    </style>
    </head>
    <body><table><tr><th class='align_enter'>জেজি আই</th><th>নাম</th><th>পিতার নাম</th></tr>"""

    for dt in data:
        html_string += (
            f"<tr><td class='align_enter'>{dt[0]}</td><td>{dt[1]}</td><td>{dt[2]}</td></tr>"
        )

    html_string += "</table></body></html>"
    # For Data End -------------
    html_doc = HTML(string=html_string)

    html_doc.write_pdf(f"your_report.pdf", stylesheets=None)


weasy_print_pdf()

subprocess.Popen("your_report.pdf",shell=True)
